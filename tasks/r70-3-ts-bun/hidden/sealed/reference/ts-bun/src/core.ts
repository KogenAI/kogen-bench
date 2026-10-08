import { mkdir, rename, unlink, writeFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { Failure } from './shared.ts';

type Options = { url: string; prompt: string; timeout: number; usage: string };
type Usage = { input_tokens: number; output_tokens: number };
class Retryable extends Error {}
class InvalidResponse extends Error {}

function parse(args: string[]): Options {
  if (args[0] !== 'model' || args.length !== 9 || args.length % 2 !== 1)
    throw new Error();
  const values = new Map<string, string>();
  for (let i = 1; i < args.length; i += 2) {
    const key = args[i];
    const value = args[i + 1];
    if (key === undefined || value === undefined) throw new Error();
    if (
      !['--url', '--prompt', '--idle-timeout-ms', '--usage-file'].includes(
        key,
      ) ||
      values.has(key)
    )
      throw new Error();
    values.set(key, value);
  }
  const url = values.get('--url');
  const prompt = values.get('--prompt');
  const rawTimeout = values.get('--idle-timeout-ms');
  const usage = values.get('--usage-file');
  if (
    url === undefined ||
    prompt === undefined ||
    rawTimeout === undefined ||
    usage === undefined ||
    usage === ''
  )
    throw new Error();
  if (!/^[0-9]+$/.test(rawTimeout)) throw new Error();
  const timeout = Number(rawTimeout);
  if (!Number.isInteger(timeout) || timeout < 1 || timeout > 60000)
    throw new Error();
  const parsed = new URL(url);
  if (parsed.protocol !== 'http:' || parsed.hostname === '') throw new Error();
  return { url, prompt, timeout, usage };
}

export async function execute(args: string[]): Promise<string> {
  let opts: Options;
  try {
    opts = parse(args);
  } catch {
    throw new Failure(2, 'error: invalid arguments');
  }
  try {
    const [text, usage] = await request(opts);
    await atomicUsage(opts.usage, usage);
    return `${text}\n`;
  } catch {
    throw new Failure(5, 'error: request failed');
  }
}

async function request(opts: Options): Promise<[string, Usage]> {
  const body = JSON.stringify({ prompt: opts.prompt });
  for (let attempt = 0; attempt < 2; attempt++) {
    try {
      return await once(opts, body);
    } catch (error) {
      if (error instanceof Retryable && attempt === 0) continue;
      throw error;
    }
  }
  throw new Retryable();
}

async function withinIdle<T>(
  promise: Promise<T>,
  controller: AbortController,
  ms: number,
): Promise<T> {
  let timer: ReturnType<typeof setTimeout> | undefined;
  const timeout = new Promise<never>((_, reject) => {
    timer = setTimeout(() => {
      controller.abort();
      reject(new Retryable('idle timeout'));
    }, ms);
  });
  try {
    return await Promise.race([promise, timeout]);
  } finally {
    if (timer !== undefined) clearTimeout(timer);
  }
}

async function once(opts: Options, body: string): Promise<[string, Usage]> {
  const controller = new AbortController();
  let response: Response;
  try {
    response = await withinIdle(
      fetch(opts.url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Accept: 'text/event-stream',
        },
        body,
        signal: controller.signal,
        redirect: 'manual',
      }),
      controller,
      opts.timeout,
    );
  } catch (error) {
    throw error instanceof InvalidResponse
      ? error
      : new Retryable('connection');
  }
  if (response.status >= 500 && response.status <= 599)
    throw new Retryable('server status');
  if (!response.ok) throw new InvalidResponse('http status');
  if (!response.body) throw new InvalidResponse('missing body');
  const reader = response.body.getReader();
  const chunks: Uint8Array[] = [];
  for (;;) {
    let item: Awaited<ReturnType<typeof reader.read>>;
    try {
      item = await withinIdle(reader.read(), controller, opts.timeout);
    } catch (error) {
      void reader.cancel().catch(() => undefined);
      throw error instanceof InvalidResponse
        ? error
        : new Retryable('connection');
    }
    if (item.done) break;
    chunks.push(item.value);
  }
  const size = chunks.reduce((sum, chunk) => sum + chunk.length, 0);
  const bytes = new Uint8Array(size);
  let offset = 0;
  for (const chunk of chunks) {
    bytes.set(chunk, offset);
    offset += chunk.length;
  }
  let content: string;
  try {
    content = new TextDecoder('utf-8', { fatal: true }).decode(bytes);
  } catch {
    throw new InvalidResponse('invalid utf-8');
  }
  return parseSse(content);
}

function parseSse(content: string): [string, Usage] {
  let output = '';
  let usage: Usage | undefined;
  let done = false;
  let data: string[] = [];
  for (const raw of content.split('\n')) {
    const line = raw.endsWith('\r') ? raw.slice(0, -1) : raw;
    if (line === '') {
      if (data.length > 0) {
        const joined = data.join('\n');
        data = [];
        if (joined === '[DONE]') {
          done = true;
          break;
        }
        let value: unknown;
        try {
          value = JSON.parse(joined);
        } catch {
          throw new InvalidResponse('bad JSON');
        }
        if (value === null || typeof value !== 'object' || Array.isArray(value))
          throw new InvalidResponse('bad event');
        const object = value as Record<string, unknown>;
        if (object.type === 'text') {
          if (typeof object.text !== 'string')
            throw new InvalidResponse('bad text');
          output += object.text;
        } else if (object.type === 'usage') {
          const input = object.input_tokens;
          const out = object.output_tokens;
          if (
            !Number.isSafeInteger(input) ||
            (input as number) < 0 ||
            !Number.isSafeInteger(out) ||
            (out as number) < 0
          )
            throw new InvalidResponse('bad usage');
          usage = {
            input_tokens: input as number,
            output_tokens: out as number,
          };
        }
      }
    } else if (!line.startsWith(':') && line.startsWith('data:')) {
      const value = line.slice(5);
      data.push(value.startsWith(' ') ? value.slice(1) : value);
    }
  }
  if (!done || usage === undefined)
    throw new InvalidResponse('incomplete stream');
  return [output, usage];
}

async function atomicUsage(path: string, usage: Usage): Promise<void> {
  const parent = dirname(path);
  await mkdir(parent, { recursive: true });
  const temp = join(
    parent,
    `.kogen-usage-${Date.now()}-${Math.random().toString(36).slice(2)}`,
  );
  try {
    await writeFile(
      temp,
      `{"input_tokens":${usage.input_tokens},"output_tokens":${usage.output_tokens}}\n`,
      { encoding: 'utf8', flag: 'wx' },
    );
    await rename(temp, path);
  } finally {
    await unlink(temp).catch(() => undefined);
  }
}
