// fakeprov: a local fake Responses-API provider for fault fixtures (family D, no model calls).
// POST /<scenario>/v1/responses; the Nth request to a scenario runs step N-1 (the last step repeats).
// Every request is logged as one JSON line (accept / first-byte / end times, client-gone, tool output seen).
package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"
)

var (
	start = time.Now()
	logmu sync.Mutex
	logf  *os.File
	cnt   = map[string]int{}
	cntmu sync.Mutex
	current string
)

func el() float64 { return float64(time.Since(start).Milliseconds()) / 1000 }

func logj(m map[string]any) {
	logmu.Lock()
	defer logmu.Unlock()
	b, _ := json.Marshal(m)
	logf.Write(append(b, '\n'))
}

// scenarios: name -> steps. step grammar in run().
var scenarios = map[string][]string{}

func main() {
	listen := flag.String("listen", "localhost:0", "")
	logp := flag.String("log", "fake.jsonl", "")
	portp := flag.String("port", "port", "")
	scen := flag.String("scenarios", "scenarios.json", "")
	flag.Parse()
	data, err := os.ReadFile(*scen)
	if err != nil {
		panic(err)
	}
	if err := json.Unmarshal(data, &scenarios); err != nil {
		panic(err)
	}
	logf, _ = os.OpenFile(*logp, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0o600)
	ln, err := net.Listen("tcp4", *listen)
	if err != nil {
		panic(err)
	}
	os.WriteFile(*portp, []byte(strconv.Itoa(ln.Addr().(*net.TCPAddr).Port)), 0o600)
	srv := &http.Server{Handler: http.HandlerFunc(handle)}
	srv.Serve(ln)
}

func sse(w http.ResponseWriter, typ string, v map[string]any) {
	v["type"] = typ
	b, _ := json.Marshal(v)
	fmt.Fprintf(w, "event: %s\ndata: %s\n\n", typ, b)
	w.(http.Flusher).Flush()
}

func msgItem(text string) map[string]any {
	return map[string]any{"type": "message", "id": "msg_1", "role": "assistant", "status": "completed",
		"content": []any{map[string]any{"type": "output_text", "text": text}}}
}
func callItem(id, cmd string) map[string]any {
	args, _ := json.Marshal(map[string]any{"command": cmd})
	return map[string]any{"type": "function_call", "id": "fc_" + id, "call_id": id, "name": "shell", "arguments": string(args), "status": "completed"}
}

// full writes a complete valid stream for item.
func full(w http.ResponseWriter, item map[string]any, gap time.Duration, done <-chan struct{}) bool {
	sse(w, "response.created", map[string]any{"response": map[string]any{"id": "resp_f", "status": "in_progress"}})
	sse(w, "response.output_item.added", map[string]any{"output_index": 0, "item": map[string]any{"type": item["type"], "id": item["id"]}})
	if gap > 0 {
		select {
		case <-time.After(gap):
		case <-done:
			return false
		}
	}
	sse(w, "response.output_text.delta", map[string]any{"output_index": 0, "delta": "x"})
	sse(w, "response.output_item.done", map[string]any{"output_index": 0, "item": item})
	sse(w, "response.completed", map[string]any{"response": map[string]any{"id": "resp_f", "model": "fake", "status": "completed",
		"output": []any{item}, "usage": map[string]any{"input_tokens": 10, "output_tokens": 5}}})
	return true
}

func sleep(d time.Duration, done <-chan struct{}) bool {
	select {
	case <-time.After(d):
		return true
	case <-done:
		return false
	}
}

func handle(w http.ResponseWriter, r *http.Request) {
	if strings.HasPrefix(r.URL.Path, "/_set/") {
		cntmu.Lock()
		current = strings.TrimPrefix(r.URL.Path, "/_set/")
		cnt[current] = 0
		cntmu.Unlock()
		fmt.Fprint(w, "ok")
		return
	}
	cntmu.Lock()
	name := current
	steps, ok := scenarios[name]
	if !ok || r.URL.Path != "/v1/responses" {
		cntmu.Unlock()
		http.NotFound(w, r)
		return
	}
	cnt[name]++
	n := cnt[name]
	cntmu.Unlock()
	step := steps[min(n, len(steps))-1]
	body, _ := io.ReadAll(r.Body)
	rec := map[string]any{"scenario": name, "req": n, "step": step, "t_accept": el(), "body_bytes": len(body)}
	var req struct {
		Input []map[string]any `json:"input"`
	}
	json.Unmarshal(body, &req)
	var outs []string
	for _, it := range req.Input {
		if it["type"] == "function_call_output" {
			if s, ok := it["output"].(string); ok {
				outs = append(outs, s)
			}
		}
	}
	rec["n_input"] = len(req.Input)
	if len(outs) > 0 {
		last := outs[len(outs)-1]
		rec["tool_out_bytes"] = len(last)
		rec["tool_out_head"] = last[:min(len(last), 160)]
		rec["tool_out_tail"] = last[max(0, len(last)-120):]
	}
	done := r.Context().Done()
	first := -1.0
	mark := func() {
		if first < 0 {
			first = el()
		}
	}
	end := "handler_done"
	completed := false
	func() {
		kind, arg, _ := strings.Cut(step, ":")
		switch kind {
		case "ok": // arg: text
			w.Header().Set("Content-Type", "text/event-stream")
			mark()
			completed = full(w, msgItem("done "+arg), 0, done)
		case "call": // arg: shell command
			w.Header().Set("Content-Type", "text/event-stream")
			mark()
			completed = full(w, callItem("call_1", arg), 0, done)
		case "fb": // arg: seconds before any byte, then ok
			secs, _ := strconv.ParseFloat(arg, 64)
			if !sleep(time.Duration(secs*float64(time.Second)), done) {
				end = "client_gone"
				return
			}
			w.Header().Set("Content-Type", "text/event-stream")
			mark()
			completed = full(w, msgItem("done"), 0, done)
		case "hang": // no headers, no bytes
			sleep(600*time.Second, done)
			end = "client_gone"
		case "hdr_hang": // 200 headers flushed, then silence
			w.Header().Set("Content-Type", "text/event-stream")
			w.WriteHeader(200)
			w.(http.Flusher).Flush()
			mark()
			sleep(600*time.Second, done)
			end = "client_gone"
		case "gap": // arg: secs; progress event, silence, then complete
			secs, _ := strconv.ParseFloat(arg, 64)
			w.Header().Set("Content-Type", "text/event-stream")
			mark()
			if !full(w, msgItem("done"), time.Duration(secs*float64(time.Second)), done) {
				end = "client_gone"
				return
			}
			completed = true
		case "slow": // arg: N:secs  N progress events secs apart, then complete
			ns, ss, _ := strings.Cut(arg, ":")
			cntN, _ := strconv.Atoi(ns)
			secs, _ := strconv.ParseFloat(ss, 64)
			w.Header().Set("Content-Type", "text/event-stream")
			mark()
			sse(w, "response.created", map[string]any{"response": map[string]any{"id": "resp_f"}})
			sse(w, "response.output_item.added", map[string]any{"output_index": 0, "item": map[string]any{"type": "message", "id": "msg_1"}})
			for i := 0; i < cntN; i++ {
				if !sleep(time.Duration(secs*float64(time.Second)), done) {
					end = "client_gone"
					return
				}
				sse(w, "response.output_text.delta", map[string]any{"output_index": 0, "delta": "x"})
			}
			sse(w, "response.output_item.done", map[string]any{"output_index": 0, "item": msgItem("done")})
			sse(w, "response.completed", map[string]any{"response": map[string]any{"id": "resp_f", "status": "completed",
				"output": []any{msgItem("done")}, "usage": map[string]any{"input_tokens": 1, "output_tokens": 1}}})
			completed = true
		case "keepalive": // one progress event then SSE comments every 5 s forever
			w.Header().Set("Content-Type", "text/event-stream")
			mark()
			sse(w, "response.output_text.delta", map[string]any{"delta": "x"})
			for {
				if !sleep(5*time.Second, done) {
					end = "client_gone"
					return
				}
				fmt.Fprint(w, ": ping\n\n")
				w.(http.Flusher).Flush()
			}
		case "trickle": // one progress event then an unfinished event, 1 byte per 5 s
			w.Header().Set("Content-Type", "text/event-stream")
			mark()
			sse(w, "response.output_text.delta", map[string]any{"delta": "x"})
			fmt.Fprint(w, "event: response.output_text.delta\ndata: {\"type\":\"response.output_text.delta\",\"delta\":\"")
			w.(http.Flusher).Flush()
			for {
				if !sleep(5*time.Second, done) {
					end = "client_gone"
					return
				}
				fmt.Fprint(w, "y")
				w.(http.Flusher).Flush()
			}
		case "trunc_mid": // valid events, then clean close, no completed
			w.Header().Set("Content-Type", "text/event-stream")
			mark()
			sse(w, "response.created", map[string]any{"response": map[string]any{"id": "resp_f"}})
			sse(w, "response.output_item.added", map[string]any{"output_index": 0, "item": map[string]any{"type": "message", "id": "msg_1"}})
			sse(w, "response.output_text.delta", map[string]any{"delta": "x"})
		case "trunc_json": // cut inside an event, clean close
			w.Header().Set("Content-Type", "text/event-stream")
			mark()
			sse(w, "response.created", map[string]any{"response": map[string]any{"id": "resp_f"}})
			fmt.Fprint(w, "event: response.completed\ndata: {\"type\":\"response.completed\",\"response\":{\"id\":\"resp")
			w.(http.Flusher).Flush()
		case "reset": // RST mid-stream
			w.Header().Set("Content-Type", "text/event-stream")
			mark()
			sse(w, "response.created", map[string]any{"response": map[string]any{"id": "resp_f"}})
			hj, _ := w.(http.Hijacker)
			c, _, _ := hj.Hijack()
			c.(*net.TCPConn).SetLinger(0)
			c.Close()
			end = "rst"
		case "empty200":
			w.Header().Set("Content-Type", "text/event-stream")
			w.WriteHeader(200)
			mark()
		case "badjson":
			w.Header().Set("Content-Type", "text/event-stream")
			mark()
			fmt.Fprint(w, "event: response.created\ndata: {not json\n\n")
			w.(http.Flusher).Flush()
		case "http": // arg: code[:retry-after]
			cs, ra, _ := strings.Cut(arg, ":")
			code, _ := strconv.Atoi(cs)
			if ra != "" {
				w.Header().Set("Retry-After", ra)
			}
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(code)
			mark()
			fmt.Fprintf(w, `{"error":{"message":"fake %d","type":"fake","code":"fake_%d"}}`, code, code)
		case "sse_err": // arg: code  -> response.failed with that error code
			w.Header().Set("Content-Type", "text/event-stream")
			mark()
			sse(w, "response.failed", map[string]any{"response": map[string]any{"id": "resp_f", "status": "failed",
				"error": map[string]any{"code": arg, "message": "fake " + arg}}})
		case "incomplete":
			w.Header().Set("Content-Type", "text/event-stream")
			mark()
			sse(w, "response.incomplete", map[string]any{"response": map[string]any{"id": "resp_f", "status": "incomplete",
				"incomplete_details": map[string]any{"reason": "max_output_tokens"}}})
		case "overflow": // > 64 MiB of progress events
			w.Header().Set("Content-Type", "text/event-stream")
			mark()
			bw := bufio.NewWriterSize(w, 1<<20)
			line := "event: response.output_text.delta\ndata: {\"type\":\"response.output_text.delta\",\"delta\":\"" + strings.Repeat("a", 60000) + "\"}\n\n"
			for i := 0; i < 1200; i++ {
				if _, err := bw.WriteString(line); err != nil {
					end = "write_err_client_gone"
					return
				}
			}
			bw.Flush()
		default:
			http.Error(w, "unknown step "+step, 500)
		}
	}()
	if completed {
		end = "completed_sent"
	} else if end == "handler_done" {
		select {
		case <-done:
			end = "client_gone"
		default:
		}
	}
	rec["t_first_byte"] = first
	rec["t_end"] = el()
	rec["end"] = end
	logj(rec)
}
