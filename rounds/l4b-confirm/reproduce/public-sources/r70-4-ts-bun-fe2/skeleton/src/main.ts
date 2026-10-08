import { execute } from './core.ts';
import { Failure } from './shared.ts';

try {
  const output = await execute(process.argv.slice(2));
  const exitCode = output.startsWith('rebased ') ? 10 : 0;
  await Bun.write(Bun.stdout, output);
  if (exitCode !== 0) process.exit(exitCode);
} catch (error) {
  if (error instanceof Failure) {
    await Bun.write(Bun.stderr, `${error.message}\n`);
    process.exit(error.code);
  }
  throw error;
}
