package main

import (
	"bytes"
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"math"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"
	"unicode/utf8"
)

type options struct {
	url, prompt, usage string
	timeout            time.Duration
}
type usageRecord struct {
	Input  int64 `json:"input_tokens"`
	Output int64 `json:"output_tokens"`
}

func parseArgs(args []string) (options, bool) {
	if len(args) < 2 || args[0] != "model" {
		return options{}, false
	}
	values := map[string]string{}
	for i := 1; i < len(args); {
		key := args[i]
		if key != "--url" && key != "--prompt" && key != "--idle-timeout-ms" && key != "--usage-file" {
			return options{}, false
		}
		if _, ok := values[key]; ok || i+1 >= len(args) {
			return options{}, false
		}
		values[key] = args[i+1]
		i += 2
	}
	u, ok1 := values["--url"]
	p, ok2 := values["--prompt"]
	t, ok3 := values["--idle-timeout-ms"]
	f, ok4 := values["--usage-file"]
	if !ok1 || !ok2 || !ok3 || !ok4 || f == "" {
		return options{}, false
	}
	for _, ch := range t {
		if ch < '0' || ch > '9' {
			return options{}, false
		}
	}
	n, err := strconv.Atoi(t)
	if err != nil || n < 1 || n > 60000 {
		return options{}, false
	}
	parsed, err := url.Parse(u)
	if err != nil || parsed.Scheme != "http" || parsed.Host == "" {
		return options{}, false
	}
	return options{url: u, prompt: p, usage: f, timeout: time.Duration(n) * time.Millisecond}, true
}

func execute(args []string) (string, int, error) {
	opts, ok := parseArgs(args)
	if !ok {
		return "", 2, errors.New("error: invalid arguments")
	}
	text, record, err := request(opts)
	if err != nil {
		return "", 5, errors.New("error: request failed")
	}
	if err := atomicUsage(opts.usage, record); err != nil {
		return "", 5, errors.New("error: request failed")
	}
	return text + "\n", 0, nil
}

func request(opts options) (string, usageRecord, error) {
	body, _ := json.Marshal(struct {
		Prompt string `json:"prompt"`
	}{opts.prompt})
	for attempt := 0; attempt < 2; attempt++ {
		text, usage, retry, err := requestOnce(opts, body)
		if err == nil {
			return text, usage, nil
		}
		if !retry || attempt == 1 {
			return "", usageRecord{}, err
		}
	}
	return "", usageRecord{}, errors.New("failed")
}

func requestOnce(opts options, body []byte) (string, usageRecord, bool, error) {
	client := &http.Client{CheckRedirect: func(_ *http.Request, _ []*http.Request) error {
		return http.ErrUseLastResponse
	}}
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	timer := time.AfterFunc(opts.timeout, cancel)
	defer timer.Stop()
	req, err := http.NewRequestWithContext(ctx, http.MethodPost, opts.url, bytes.NewReader(body))
	if err != nil {
		return "", usageRecord{}, false, err
	}
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Accept", "text/event-stream")
	resp, err := client.Do(req)
	if err != nil {
		return "", usageRecord{}, true, err
	}
	timer.Reset(opts.timeout)
	defer func() { _ = resp.Body.Close() }()
	if resp.StatusCode >= 500 && resp.StatusCode <= 599 {
		return "", usageRecord{}, true, errors.New("server status")
	}
	if resp.StatusCode < 200 || resp.StatusCode > 299 {
		return "", usageRecord{}, false, errors.New("http status")
	}
	var data []byte
	buf := make([]byte, 4096)
	for {
		n, readErr := resp.Body.Read(buf)
		if n > 0 {
			timer.Reset(opts.timeout)
			data = append(data, buf[:n]...)
		}
		if readErr == io.EOF {
			break
		}
		if readErr != nil {
			return "", usageRecord{}, true, readErr
		}
	}
	if !utf8.Valid(data) {
		return "", usageRecord{}, false, errors.New("invalid utf-8")
	}
	text, usage, err := parseSSE(string(data))
	if err != nil {
		return "", usageRecord{}, false, err
	}
	return text, usage, false, nil
}

func parseSSE(input string) (string, usageRecord, error) {
	var output strings.Builder
	var usage usageRecord
	hasUsage, finished := false, false
	var values []string
	lines := strings.Split(input, "\n")
	for _, raw := range lines {
		line := strings.TrimSuffix(raw, "\r")
		if line == "" {
			if len(values) > 0 {
				joined := strings.Join(values, "\n")
				if joined == "[DONE]" {
					finished = true
					break
				}
				var obj map[string]json.RawMessage
				dec := json.NewDecoder(strings.NewReader(joined))
				dec.UseNumber()
				if err := dec.Decode(&obj); err != nil || obj == nil {
					return "", usageRecord{}, errors.New("bad event")
				}
				var trailing any
				if err := dec.Decode(&trailing); err != io.EOF {
					return "", usageRecord{}, errors.New("trailing event data")
				}
				var kind string
				if rawType, ok := obj["type"]; ok {
					_ = json.Unmarshal(rawType, &kind)
				}
				switch kind {
				case "text":
					var value string
					if err := json.Unmarshal(obj["text"], &value); err != nil {
						return "", usageRecord{}, errors.New("bad text")
					}
					output.WriteString(value)
				case "usage":
					in, err1 := integer(obj["input_tokens"])
					out, err2 := integer(obj["output_tokens"])
					if err1 != nil || err2 != nil {
						return "", usageRecord{}, errors.New("bad usage")
					}
					usage = usageRecord{Input: in, Output: out}
					hasUsage = true
				}
				values = nil
			}
			continue
		}
		if strings.HasPrefix(line, ":") {
			continue
		}
		if strings.HasPrefix(line, "data:") {
			value := strings.TrimPrefix(line, "data:")
			values = append(values, strings.TrimPrefix(value, " "))
		}
	}
	if !finished || !hasUsage {
		return "", usageRecord{}, errors.New("incomplete stream")
	}
	return output.String(), usage, nil
}

func integer(raw json.RawMessage) (int64, error) {
	var value any
	dec := json.NewDecoder(bytes.NewReader(raw))
	dec.UseNumber()
	if err := dec.Decode(&value); err != nil {
		return 0, err
	}
	n, ok := value.(json.Number)
	if !ok {
		return 0, errors.New("invalid integer")
	}
	if v, err := strconv.ParseInt(string(n), 10, 64); err == nil && v >= 0 && v <= 9007199254740991 {
		return v, nil
	}
	v, err := strconv.ParseFloat(string(n), 64)
	if err != nil || math.IsNaN(v) || math.IsInf(v, 0) || v < 0 || v > 9007199254740991 || math.Trunc(v) != v {
		return 0, errors.New("invalid integer")
	}
	return int64(v), nil
}

func atomicUsage(path string, record usageRecord) error {
	parent := filepath.Dir(path)
	if err := os.MkdirAll(parent, 0o755); err != nil {
		return err
	}
	file, err := os.CreateTemp(parent, ".kogen-usage-*")
	if err != nil {
		return err
	}
	name := file.Name()
	defer func() { _ = os.Remove(name) }()
	if _, err = fmt.Fprintf(file, `{"input_tokens":%d,"output_tokens":%d}`+"\n", record.Input, record.Output); err != nil {
		_ = file.Close()
		return err
	}
	if err = file.Sync(); err != nil {
		_ = file.Close()
		return err
	}
	if err = file.Close(); err != nil {
		return err
	}
	return os.Rename(name, path)
}
