declare const Bun: {
  stdin: { arrayBuffer(): Promise<ArrayBuffer> };
  file(path: string): { arrayBuffer(): Promise<ArrayBuffer> };
  stdout: unknown;
  stderr: unknown;
  write(target: unknown, text: string): Promise<number>;
};
declare const process: { argv: string[]; exit(code: number): never };
declare module 'node:fs/promises' {
  export function readFile(path: string, encoding: 'utf8'): Promise<string>;
  export function readFile(path: string): Promise<Uint8Array>;
  export function appendFile(
    path: string,
    data: string,
    options: { encoding: 'utf8'; flag: 'a' },
  ): Promise<void>;
}
declare module 'bun:test' {
  export function test(name: string, fn: () => void): void;
  export function expect(value: unknown): { toEqual(expected: unknown): void };
}
