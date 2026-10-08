import { Failure } from './shared.ts';

type Job = {
  id: string;
  argv: string[];
  attempts: number;
  done: boolean;
  exit_code: number;
  stdout: string;
  stderr: string;
};
type State = { jobs: Job[] };
type Result = {
  id: string;
  attempt: number;
  exit_code: number;
  stdout: string;
  stderr: string;
  status: string;
};
type SpawnResult = {
  exitCode: number;
  signalCode?: string | null;
  stdout: Uint8Array;
  stderr: Uint8Array;
  success: boolean;
};
const idPattern = /^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$/;

export async function execute(args: string[]): Promise<string> {
  const parsed = parse(args);
  if (!parsed) throw new Failure(2, 'error: invalid arguments');
  const store = parsed.values['--store'];
  const mkdir = Bun.spawnSync(['mkdir', '-p', store]);
  if (!mkdir.success) throw new Failure(4, 'error: store failure');
  const lockPath = `${store}/.lock`;
  await acquireLock(store, lockPath);
  try {
    return await executeLocked(args);
  } finally {
    await releaseLock(lockPath);
  }
}

async function executeLocked(args: string[]): Promise<string> {
  const parsed = parse(args);
  if (!parsed) throw new Failure(2, 'error: invalid arguments');
  const dir = parsed.values['--store'];
  let state: State;
  try {
    state = await readState(dir);
  } catch {
    throw new Failure(4, 'error: store failure');
  }
  if (parsed.command === 'add') {
    const id = parsed.values['--id'];
    if (state.jobs.some((job) => job.id === id))
      throw new Failure(3, 'error: duplicate job id');
    let argv: unknown;
    try {
      argv = JSON.parse(parsed.values['--argv']);
    } catch {
      throw new Failure(2, 'error: invalid arguments');
    }
    if (
      !Array.isArray(argv) ||
      argv.length === 0 ||
      argv.some(
        (part) =>
          typeof part !== 'string' || part.length === 0 || part.includes('\0'),
      )
    )
      throw new Failure(2, 'error: invalid arguments');
    state.jobs.push({
      id,
      argv: argv as string[],
      attempts: 0,
      done: false,
      exit_code: 0,
      stdout: '',
      stderr: '',
    });
    try {
      await writeState(dir, state);
    } catch {
      throw new Failure(4, 'error: store failure');
    }
    return `queued ${id}\n`;
  }
  if (parsed.command === 'status')
    return state.jobs
      .map((job) =>
        !job.done
          ? `${job.id} pending\n`
          : job.exit_code === 0
            ? `${job.id} succeeded\n`
            : `${job.id} failed ${job.exit_code}\n`,
      )
      .join('');
  const results: Result[] = [];
  for (const job of state.jobs) {
    if (job.done) continue;
    job.attempts += 1;
    try {
      await writeState(dir, state);
    } catch {
      throw new Failure(4, 'error: store failure');
    }
    let child: SpawnResult;
    try {
      child = Bun.spawnSync(job.argv, { stdout: 'pipe', stderr: 'pipe' });
    } catch {
      child = {
        exitCode: 127,
        signalCode: null,
        stdout: new Uint8Array(),
        stderr: new TextEncoder().encode('exec failed\n'),
        success: false,
      };
    }
    let code = child.exitCode;
    if (child.signalCode) code = 128 + signalNumber(child.signalCode);
    job.done = true;
    job.exit_code = code;
    job.stdout = new TextDecoder('utf-8', { fatal: false }).decode(
      child.stdout,
    );
    job.stderr = new TextDecoder('utf-8', { fatal: false }).decode(
      child.stderr,
    );
    try {
      await writeState(dir, state);
    } catch {
      throw new Failure(4, 'error: store failure');
    }
    results.push({
      id: job.id,
      attempt: job.attempts,
      exit_code: code,
      stdout: job.stdout,
      stderr: job.stderr,
      status: code === 0 ? 'succeeded' : 'failed',
    });
  }
  return results.map((row) => `${JSON.stringify(row)}\n`).join('');
}

function signalNumber(signal: string): number {
  const values: Record<string, number> = {
    SIGHUP: 1,
    SIGINT: 2,
    SIGQUIT: 3,
    SIGILL: 4,
    SIGTRAP: 5,
    SIGABRT: 6,
    SIGBUS: 7,
    SIGFPE: 8,
    SIGKILL: 9,
    SIGUSR1: 10,
    SIGSEGV: 11,
    SIGUSR2: 12,
    SIGPIPE: 13,
    SIGALRM: 14,
    SIGTERM: 15,
  };
  return values[signal] ?? 0;
}

function parse(
  args: string[],
): { command: string; values: Record<string, string> } | null {
  if (
    args.length < 2 ||
    args[0] !== 'queue' ||
    !['add', 'run', 'status'].includes(args[1] ?? '')
  )
    return null;
  const command = args[1] as string;
  const allowed =
    command === 'add' ? ['--store', '--id', '--argv'] : ['--store'];
  const values: Record<string, string> = {};
  for (let i = 2; i < args.length; i += 1) {
    const key = args[i];
    if (
      !key ||
      !allowed.includes(key) ||
      Object.hasOwn(values, key) ||
      i + 1 >= args.length
    )
      return null;
    values[key] = args[i + 1] ?? '';
    i += 1;
  }
  if (!values['--store']) return null;
  if (
    command === 'add' &&
    (!values['--id'] || !idPattern.test(values['--id']) || !values['--argv'])
  )
    return null;
  return { command, values };
}

async function readState(dir: string): Promise<State> {
  const file = Bun.file(`${dir}/state.json`);
  if (!(await file.exists())) return { jobs: [] };
  const value: unknown = JSON.parse(await file.text());
  if (
    typeof value !== 'object' ||
    value === null ||
    !('jobs' in value) ||
    !Array.isArray(value.jobs)
  )
    throw new Error('bad state');
  return value as State;
}

async function acquireLock(store: string, lockPath: string): Promise<void> {
  const bootId = (
    await Bun.file('/proc/sys/kernel/random/boot_id').text()
  ).trim();
  const ownStart = await processStartTime(process.pid);
  if (!ownStart) throw new Failure(4, 'error: store failure');
  const ownerText = `${process.pid}\n${bootId}\n${ownStart}`;
  let ownerlessWait = 0;
  for (;;) {
    const created = Bun.spawnSync(['mkdir', lockPath], {
      stdout: 'pipe',
      stderr: 'pipe',
    });
    if (created.success) {
      try {
        await Bun.write(`${lockPath}/owner`, ownerText);
        return;
      } catch {
        Bun.spawnSync(['rmdir', lockPath]);
        throw new Failure(4, 'error: store failure');
      }
    }
    let existing: string | undefined;
    try {
      existing = await Bun.file(`${lockPath}/owner`).text();
    } catch {
      existing = undefined;
    }
    if (existing) {
      ownerlessWait = 0;
      const [pidText, oldBoot, oldStart] = existing.trim().split('\n');
      const pid = Number(pidText);
      const live =
        Number.isSafeInteger(pid) &&
        pid > 0 &&
        oldBoot === bootId &&
        (await processStartTime(pid)) === oldStart;
      if (!live) await reapLock(store, lockPath);
    } else {
      ownerlessWait += 1;
      if (ownerlessWait >= 100) await reapLock(store, lockPath);
    }
    await new Promise<void>((resolve) => setTimeout(resolve, 10));
  }
}

async function processStartTime(pid: number): Promise<string | undefined> {
  try {
    const stat = await Bun.file(`/proc/${pid}/stat`).text();
    const fields = stat
      .slice(stat.lastIndexOf(')') + 2)
      .trim()
      .split(/\s+/);
    return fields[19];
  } catch {
    return undefined;
  }
}

async function reapLock(store: string, lockPath: string): Promise<void> {
  const gate = `${lockPath}/.reaper`;
  const acquired = Bun.spawnSync(['mkdir', gate], {
    stdout: 'pipe',
    stderr: 'pipe',
  });
  if (!acquired.success) return;
  const quarantine = `${store}/.lock-stale-${process.pid}-${Date.now()}`;
  const moved = Bun.spawnSync(['mv', lockPath, quarantine], {
    stdout: 'pipe',
    stderr: 'pipe',
  });
  if (moved.success) {
    Bun.spawnSync(['rm', '-f', `${quarantine}/owner`], {
      stdout: 'pipe',
      stderr: 'pipe',
    });
    Bun.spawnSync(['rmdir', `${quarantine}/.reaper`], {
      stdout: 'pipe',
      stderr: 'pipe',
    });
    Bun.spawnSync(['rmdir', quarantine], { stdout: 'pipe', stderr: 'pipe' });
  } else Bun.spawnSync(['rmdir', gate], { stdout: 'pipe', stderr: 'pipe' });
}

async function releaseLock(lockPath: string): Promise<void> {
  const removed = Bun.spawnSync(['rm', '-f', `${lockPath}/owner`], {
    stdout: 'pipe',
    stderr: 'pipe',
  });
  const released = Bun.spawnSync(['rmdir', lockPath], {
    stdout: 'pipe',
    stderr: 'pipe',
  });
  if (!removed.success || !released.success)
    throw new Failure(4, 'error: store failure');
}
async function writeState(dir: string, state: State): Promise<void> {
  const temp = `${dir}/.state-${process.pid}.tmp`;
  await Bun.write(temp, JSON.stringify(state));
  const syncFile = Bun.spawnSync(['sync', '-f', temp]);
  const moved = Bun.spawnSync(['mv', '-f', temp, `${dir}/state.json`]);
  const syncDir = Bun.spawnSync(['sync', '-f', dir]);
  if (!syncFile.success || !moved.success || !syncDir.success)
    throw new Error('write failed');
}
