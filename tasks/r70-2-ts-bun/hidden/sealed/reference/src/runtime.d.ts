declare const Bun: {
  stdin: { arrayBuffer(): Promise<ArrayBuffer> };
  file(path: string): { arrayBuffer(): Promise<ArrayBuffer> };
  stdout: unknown;
  stderr: unknown;
  write(target: unknown, text: string): Promise<number>;
  spawn(
    command: string[],
    options: {
      stdin: string;
      stdout: string;
      stderr: string;
      detached: boolean;
    },
  ): { pid: number; exited: Promise<number> };
};
declare const process: {
  argv: string[];
  exit(code: number): never;
  kill(pid: number, signal: 'SIGTERM' | 'SIGKILL'): void;
};
declare module 'node:fs/promises' {
  export function readdir(path: string): Promise<string[]>;
  export function readFile(path: string, encoding: 'utf8'): Promise<string>;
}
declare module 'bun:test' {
  export function test(name: string, fn: () => void): void;
  export function expect(value: unknown): { toEqual(expected: unknown): void };
}
