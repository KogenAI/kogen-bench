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
