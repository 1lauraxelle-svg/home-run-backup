<script lang="ts">
	import { type Snippet } from 'svelte';
	import { browser } from '$app/environment';
	import { GlobalStyle } from 'components-ui-html';
	import { Authenticate, LoaderStakeEngine, LoaderExample, LoadI18n } from 'components-shared';
	import Game from '../components/Game.svelte';
	import { setContext } from '../game/context';

	import messagesMap from '../i18n/messagesMap';

	type Props = { children: Snippet };

	const props: Props = $props();

	let showYourLoader = $state(false);
	// Prod/Studio: always mount. Dev offline: wait until sessionID+rgs_url are present.
	let appReady = $state(!browser || !import.meta.env.DEV);

	const loaderUrlStakeEngine = new URL('../../stake-engine-loader.gif', import.meta.url).href;
	const loaderUrl = new URL('../../loader.gif', import.meta.url).href;

	// DEV only: inject mock session so local `vite dev` works without Studio params.
	// Never do this in production — Studio provides sessionID/rgs_url; injecting
	// offline + CDN host causes a blank screen / auth failure.
	if (browser && import.meta.env.DEV) {
		const params = new URLSearchParams(window.location.search);
		const needsSession = !params.get('sessionID');
		const needsRgs = !params.get('rgs_url');
		if (needsSession || needsRgs) {
			if (needsSession) params.set('sessionID', 'offline');
			if (needsRgs) params.set('rgs_url', window.location.host);
			window.location.replace(`${window.location.pathname}?${params.toString()}`);
		} else {
			appReady = true;
		}
	}

	setContext();
</script>

{#if appReady}
	<GlobalStyle>
		<Authenticate>
			<LoadI18n {messagesMap}>
				<Game />
			</LoadI18n>
		</Authenticate>
	</GlobalStyle>

	<LoaderStakeEngine src={loaderUrlStakeEngine} oncomplete={() => (showYourLoader = true)} />

	{#if showYourLoader}
		<LoaderExample src={loaderUrl} />
	{/if}
{/if}

{@render props.children()}
