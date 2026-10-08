import { expect, test } from 'bun:test';
import { physicalLines } from '../src/shared.ts';

test('physical CRLF and final CR', () => {
  expect(physicalLines('a\r\n\nb\r')).toEqual(['a', '', 'b']);
});
