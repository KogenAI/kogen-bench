declare const Bun: {
  stdin: { arrayBuffer(): Promise<ArrayBuffer> };
  file(path: string): { arrayBuffer(): Promise<ArrayBuffer> };
  stdout: unknown;
  stderr: unknown;
  write(target: unknown, text: string): Promise<number>;
};
declare const process: { argv: string[]; exit(code: number): never };
declare module 'bun:test' {
  export function test(name: string, fn: () => void): void;
  export function expect(value: unknown): { toEqual(expected: unknown): void };
}

declare module 'node:fs/promises' {
  export function rename(oldPath: string, newPath: string): Promise<void>;
  export function mkdir(
    path: string,
    options: { recursive: true },
  ): Promise<string | undefined>;
  export function writeFile(
    path: string,
    data: string,
    options: { encoding: string; flag: string },
  ): Promise<void>;
  export function unlink(path: string): Promise<void>;
}
declare module 'node:path' {
  export function dirname(path: string): string;
  export function join(...paths: string[]): string;
}
