export class Failure extends Error {
  constructor(
    public code: number,
    message: string,
  ) {
    super(message);
  }
}

export function physicalLines(text: string): string[] {
  return text
    .split('\n')
    .map((line) => (line.endsWith('\r') ? line.slice(0, -1) : line));
}

export async function load(
  path: string | undefined,
  prefix: string,
): Promise<Uint8Array> {
  try {
    const file =
      path === undefined || path === '-' ? Bun.stdin : Bun.file(path);
    return new Uint8Array(await file.arrayBuffer());
  } catch {
    throw new Failure(1, `${prefix}: cannot read input`);
  }
}
