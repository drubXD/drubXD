import { readFileSync } from 'node:fs';
export const html = readFileSync(new URL('./pulse.html', import.meta.url), 'utf8');
