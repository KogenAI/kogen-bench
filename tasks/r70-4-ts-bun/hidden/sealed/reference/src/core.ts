import { Failure } from './shared.ts';

declare const Bun: typeof globalThis.Bun & { readonly pid?: undefined };

const usage =
  'cas-land: usage: cas-land --repo DIR --target REF --base OID --candidate OID';
const invalid = 'cas-land: invalid repository or commit';

type GitResult = { code: number; out: string };

function git(repo: string, args: string[]): GitResult {
  try {
    const result = Bun.spawnSync({
      cmd: ['git', '-C', repo, ...args],
      stdout: 'pipe',
      stderr: 'pipe',
    });
    return {
      code: result.exitCode,
      out: new TextDecoder().decode(result.stdout).trim(),
    };
  } catch {
    return { code: 127, out: '' };
  }
}

function requireOk(result: GitResult): string {
  if (result.code !== 0) throw new Failure(1, invalid);
  return result.out;
}

function cleanup(repo: string, work: string): void {
  git(repo, ['worktree', 'remove', '--force', work]);
  try {
    Bun.spawnSync({
      cmd: ['rm', '-rf', work],
      stdout: 'ignore',
      stderr: 'ignore',
    });
  } catch {
    // The worktree command normally removes this directory; this is best-effort cleanup.
  }
}

export async function execute(
  args: string[],
): Promise<{ output: string; code: number }> {
  const values: Record<string, string> = {};
  const allowed = new Set(['--repo', '--target', '--base', '--candidate']);
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i];
    const value = args[i + 1];
    if (
      !allowed.has(key) ||
      Object.hasOwn(values, key) ||
      value === undefined ||
      value === ''
    ) {
      throw new Failure(2, usage);
    }
    values[key] = value;
  }
  if (Object.keys(values).length !== allowed.size) throw new Failure(2, usage);
  const repo = values['--repo'];
  const target = values['--target'];
  const base = values['--base'];
  const candidate = values['--candidate'];
  if (!repo || !target || !base || !candidate) throw new Failure(2, usage);
  if (
    !target.startsWith('refs/') ||
    git(repo, ['check-ref-format', target]).code !== 0
  ) {
    throw new Failure(1, invalid);
  }
  const parents = requireOk(
    git(repo, ['rev-list', '--parents', '-n', '1', candidate]),
  ).split(/\s+/);
  if (parents.length !== 2 || parents[1] !== base)
    throw new Failure(1, invalid);
  const current = requireOk(git(repo, ['rev-parse', '--verify', target]));
  const rebased = current !== base;
  let landing = candidate;
  if (rebased) {
    const work = `/tmp/cas-land-${Bun.pid}-${Date.now()}-${Math.random().toString(16).slice(2)}`;
    const add = git(repo, ['worktree', 'add', '--detach', work, candidate]);
    if (add.code !== 0) throw new Failure(1, invalid);
    const rebase = git(work, ['rebase', '--onto', current, base]);
    if (rebase.code !== 0) {
      const unmerged = git(work, ['diff', '--name-only', '--diff-filter=U']);
      git(work, ['rebase', '--abort']);
      cleanup(repo, work);
      if (unmerged.code === 0 && unmerged.out !== '')
        throw new Failure(20, 'cas-land: conflict');
      throw new Failure(1, invalid);
    }
    try {
      landing = requireOk(git(work, ['rev-parse', 'HEAD']));
    } finally {
      cleanup(repo, work);
    }
  }
  if (git(repo, ['update-ref', target, landing, current]).code !== 0) {
    throw new Failure(30, 'cas-land: lost race');
  }
  return {
    output: `${rebased ? 'rebased' : 'landed'} ${landing}\n`,
    code: rebased ? 10 : 0,
  };
}
