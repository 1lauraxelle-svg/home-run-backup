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
	let offlineReady = $state(false);

	const loaderUrlStakeEngine = new URL('../../stake-engine-loader.gif', import.meta.url).href;
	const loaderUrl = new URL('../../loader.gif', import.meta.url).href;

	// Mode offline local : sessionID + rgs_url pointent vers ce serveur Vite.
	if (browser) {
		const params = new URLSearchParams(window.location.search);
		const needsSession = !params.get('sessionID');
		const needsRgs = !params.get('rgs_url');
		if (needsSession || needsRgs) {
			if (needsSession) params.set('sessionID', 'offline');
			if (needsRgs) params.set('rgs_url', window.location.host);
			window.location.replace(`${window.location.pathname}?${params.toString()}`);
		} else {
			offlineReady = true;
		}
	}

	setContext();
</script>

{#if offlineReady}
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
