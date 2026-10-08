import { readdir, readFile } from 'node:fs/promises';
import { Failure } from './shared.ts';

export type Result = { code: number; status: string };

function milliseconds(value: string | undefined): number | undefined {
  if (value === undefined || !/^[0-9]+$/.test(value)) return undefined;
  const number = Number(value);
  return Number.isSafeInteger(number) && number >= 1 && number <= 60000
    ? number
    : undefined;
}

export async function execute(args: string[]): Promise<Result> {
  if (
    args.length < 7 ||
    args[0] !== 'supervise' ||
    args[1] !== '--timeout-ms' ||
    args[3] !== '--grace-ms' ||
    args[5] !== '--' ||
    args[6] === ''
  )
    throw new Failure(2, 'error: invalid arguments');
  const timeout = milliseconds(args[2]);
  const grace = milliseconds(args[4]);
  if (timeout === undefined || grace === undefined)
    throw new Failure(2, 'error: invalid arguments');
  const started = performance.now();
  let child: ReturnType<typeof Bun.spawn>;
  try {
    child = Bun.spawn(args.slice(6), {
      stdin: 'ignore',
      stdout: 'inherit',
      stderr: 'inherit',
      detached: true,
    });
  } catch {
    throw new Failure(127, 'error: cannot start command');
  }
  const pgid = child.pid;
  const completion = child.exited;
  const deadline = started + timeout;
  while (true) {
    if (!(await groupLive(pgid))) {
      const code = await completion;
      return {
        code,
        status: `status=exited exit_code=${code} term_sent=false kill_sent=false reaped=1\n`,
      };
    }
    if (performance.now() >= deadline) break;
    await delay(5);
  }
  signalGroup(pgid, 'SIGTERM');
  const graceDeadline = performance.now() + grace;
  while (performance.now() < graceDeadline) await delay(5);
  const killSent = await groupLive(pgid);
  if (killSent) {
    signalGroup(pgid, 'SIGKILL');
    while (await groupLive(pgid)) await delay(5);
  }
  await completion;
  return {
    code: 124,
    status: `status=timeout exit_code=124 term_sent=true kill_sent=${killSent} reaped=1\n`,
  };
}

function delay(milliseconds: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}
function signalGroup(pgid: number, signal: 'SIGTERM' | 'SIGKILL'): void {
  try {
    process.kill(-pgid, signal);
  } catch {
    /* exited at signal boundary */
  }
}
async function groupLive(pgid: number): Promise<boolean> {
  let entries: string[];
  try {
    entries = await readdir('/proc');
  } catch {
    return false;
  }
  for (const entry of entries) {
    if (!/^[0-9]+$/.test(entry)) continue;
    let stat: string;
    try {
      stat = await readFile(`/proc/${entry}/stat`, 'utf8');
    } catch {
      continue;
    }
    const close = stat.lastIndexOf(')');
    if (close < 0) continue;
    const fields = stat
      .slice(close + 2)
      .trim()
      .split(/\s+/);
    if (
      fields.length >= 3 &&
      fields[0] !== 'Z' &&
      fields[0] !== 'X' &&
      Number(fields[2]) === pgid
    )
      return true;
  }
  return false;
}
