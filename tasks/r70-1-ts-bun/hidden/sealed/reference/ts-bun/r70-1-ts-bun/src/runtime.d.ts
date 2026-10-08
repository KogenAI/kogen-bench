declare const Bun: {
  stdin: { arrayBuffer(): Promise<ArrayBuffer> };
  file(path: string): {
    arrayBuffer(): Promise<ArrayBuffer>;
    text(): Promise<string>;
    exists(): Promise<boolean>;
  };
  stdout: unknown;
  stderr: unknown;
  write(target: unknown, text: string): Promise<number>;
  spawnSync(
    argv: string[],
    options?: {
      stdout?: 'pipe';
      stderr?: 'pipe';
      env?: Record<string, string | undefined>;
    },
  ): {
    exitCode: number;
    signalCode: string | null;
    stdout: Uint8Array;
    stderr: Uint8Array;
    success: boolean;
  };
};
declare const process: {
  argv: string[];
  execPath: string;
  pid: number;
  env: Record<string, string | undefined>;
  exit(code: number): never;
};
declare module 'bun:test' {
  export function test(name: string, fn: () => void): void;
  export function expect(value: unknown): { toEqual(expected: unknown): void };
}
