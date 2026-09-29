// @ts-ignore
import config from 'config-svelte';
import adapter from '@sveltejs/adapter-static';

const base = config();

/** @type {import('@sveltejs/kit').Config} */
export default {
	...base,
	kit: {
		...base.kit,
		paths: {
			...(base.kit?.paths ?? {}),
			relative: true,
		},
		output: {
			...(base.kit?.output ?? {}),
			// CRITICAL: 'inline' makes import.meta.url = page URL (/home-run/vN/),
			// so ../../assets resolves to /assets/... (404). 'single' keeps
			// import.meta.url on /_app/immutable/bundle.js → ../../assets = /home-run/vN/assets.
			bundleStrategy: 'single',
		},
		adapter: adapter({
			strict: false,
			fallback: 'index.html',
		}),
	},
};
