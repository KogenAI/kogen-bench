import { execute } from './core.ts';
import { Failure } from './shared.ts';

try {
  const result = await execute(process.argv.slice(2));
  await Bun.write(Bun.stdout, result.output);
  process.exit(result.code);
} catch (error) {
  if (error instanceof Failure) {
    await Bun.write(Bun.stderr, `${error.message}\n`);
    process.exit(error.code);
  }
  throw error;
}
