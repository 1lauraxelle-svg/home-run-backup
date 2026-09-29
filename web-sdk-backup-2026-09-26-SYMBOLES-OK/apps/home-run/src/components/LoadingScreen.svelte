<script lang="ts">
	import { onMount } from 'svelte';
	import { SpineProvider, SpineTrack, Container, Sprite, Rectangle, Text } from 'pixi-svelte';
	import { FadeContainer, LoadingProgress } from 'components-pixi';
	import { MainContainer } from 'components-layout';

	import { getContext } from '../game/context';
	import TransitionAnimation from './TransitionAnimation.svelte';
	import PressToContinue from './PressToContinue.svelte';
	import StudioLogo from './StudioLogo.svelte';
	import LoadingFeatureCards from './LoadingFeatureCards.svelte';

	type Props = {
		onloaded: () => void;
	};

	const props: Props = $props();
	const context = getContext();

	const SPLASH_MS = 5000;
	const LOGO_W = 480;
	const LOGO_H = Math.round((LOGO_W * 300) / 341);

	let splashMinElapsed = $state(false);
	let loadingType = $state<'loading' | 'transition'>('loading');

	const layout = $derived(context.stateLayoutDerived.mainLayout());
	const canvas = $derived(context.stateLayoutDerived.canvasSizes());

	const showSplash = $derived(
		loadingType === 'loading' && !(splashMinElapsed && context.stateApp.loaded),
	);
	const showWelcome = $derived(
		loadingType === 'loading' && splashMinElapsed && context.stateApp.loaded,
	);

	onMount(() => {
		const t = setTimeout(() => {
			splashMinElapsed = true;
		}, SPLASH_MS);
		return () => clearTimeout(t);
	});
</script>

<!-- Phase 1: logo studio sur fond noir (min. 5 s) -->
<FadeContainer show={showSplash}>
	<Rectangle {...canvas} backgroundColor={0x000000} zIndex={0} />
	<MainContainer>
		<Container x={layout.width * 0.5} y={layout.height * 0.5}>
			<StudioLogo width={LOGO_W} height={LOGO_H} alpha={1} zIndex={20} />

			{#if !context.stateApp.loaded}
				<LoadingProgress y={LOGO_H * 0.5 + 56} width={1967 * 0.18} height={346 * 0.18}>
					{#snippet background(sizes)}
						<Sprite key="progressBarBackground.png" {...sizes} />
					{/snippet}
					{#snippet progress(sizes)}
						<Sprite key="progressBar.png" {...sizes} />
					{/snippet}
					{#snippet frame(sizes)}
						<Sprite key="progressBarFrame.png" {...sizes} />
					{/snippet}
				</LoadingProgress>
			{/if}
		</Container>
	</MainContainer>
</FadeContainer>

<!-- Phase 2: écran d'accueil — tout centré -->
<FadeContainer show={showWelcome}>
	<MainContainer>
		<Container x={layout.width * 0.5} y={layout.height * 0.36}>
			<StudioLogo y={-235} width={120} height={91} alpha={1} zIndex={20} anchor={0.5} />

			<SpineProvider key="loader" width={210} y={-145} anchor={0.5}>
				<SpineTrack trackIndex={0} animationName={'title_screen'} loop timeScale={3} />
			</SpineProvider>

			<!-- Midway between HOME RUN title and feature cards -->
			<Text
				text="MAX WIN ×25 000"
				anchor={0.5}
				x={0}
				y={-48}
				style={{
					fill: '#FFE566',
					fontSize: 40,
					fontWeight: '900',
					fontFamily: 'Arial Black, Arial, sans-serif',
					letterSpacing: 2,
					align: 'center',
					stroke: { color: '#8a5a00', width: 4 },
				}}
			/>

			<LoadingFeatureCards y={8} scale={1.05} />
		</Container>
	</MainContainer>
	<PressToContinue onpress={() => (loadingType = 'transition')} />
</FadeContainer>

<!-- Transition vers le jeu -->
<FadeContainer show={loadingType === 'transition'}>
	<TransitionAnimation oncomplete={props.onloaded} />
</FadeContainer>
