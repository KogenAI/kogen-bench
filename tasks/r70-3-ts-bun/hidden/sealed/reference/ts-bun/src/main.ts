import { execute } from './core.ts';
import { Failure } from './shared.ts';

try {
  await Bun.write(Bun.stdout, await execute(process.argv.slice(2)));
} catch (error) {
  if (error instanceof Failure) {
    await Bun.write(Bun.stderr, `${error.message}\n`);
    process.exit(error.code);
  }
  throw error;
}
