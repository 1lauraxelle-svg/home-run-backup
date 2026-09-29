import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

/**
 * Studio serves the SPA under /{game}/v{N}/.
 * 1) SPA fallback keeps base:"" → client 404.
 * 2) SPA fallback keeps absolute /_app/... imports → assets 404 off-subdir.
 */
const indexPath = join('build', 'index.html');
let html = readFileSync(indexPath, 'utf8');

const before = html;

html = html.replace(
	/(__sveltekit_[a-z0-9]+)\s*=\s*\{\s*base:\s*""\s*\}/,
	`$1 = { base: (() => { let p = location.pathname.replace(/\\/index\\.html$/i, ''); if (p.length > 1 && p.endsWith('/')) p = p.slice(0, -1); return p === '/' ? '' : p; })() }`,
);

// Make kit/vite absolute asset URLs document-relative for subdirectory hosting
html = html.replaceAll('"/_app/', '"./_app/');
html = html.replaceAll('"/favicon', '"./favicon');
html = html.replaceAll("'/ _app/", "'./_app/"); // safety

if (html === before) {
	console.error('postbuild: no changes applied — check index.html format');
	process.exit(1);
}

if (!html.includes('location.pathname')) {
	console.error('postbuild: base patch missing');
	process.exit(1);
}
if (html.includes('"/_app/')) {
	console.error('postbuild: absolute /_app/ references remain');
	process.exit(1);
}

writeFileSync(indexPath, html);
console.log('postbuild: patched sveltekit base + relative _app URLs');
