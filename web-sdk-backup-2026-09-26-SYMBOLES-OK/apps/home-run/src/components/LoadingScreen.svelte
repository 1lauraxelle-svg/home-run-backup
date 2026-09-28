<script lang="ts">
	import { SpineProvider, SpineTrack, Container, Sprite } from 'pixi-svelte';
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

	let loadingType = $state<'start' | 'transition'>('start');
	const layout = $derived(context.stateLayoutDerived.mainLayout());
</script>

<!-- logo and loading progress -->
<FadeContainer show={loadingType === 'start'}>
	<MainContainer>
		<Container x={layout.width * 0.5} y={layout.height * 0.5}>
			<!-- Logo studio au-dessus de HOME RUN -->
			<StudioLogo y={-295} width={150} height={114} alpha={1} zIndex={20} />

			<!-- HOME RUN -->
			<SpineProvider key="loader" width={240} y={-175}>
				<SpineTrack trackIndex={0} animationName={'title_screen'} loop timeScale={3} />
			</SpineProvider>

			<!-- Panneaux agrandis -->
			<LoadingFeatureCards y={-35} scale={1.05} />

			{#if !context.stateApp.loaded}
				<LoadingProgress y={255} width={1967 * 0.18} height={346 * 0.18}>
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

<!-- press to continue -->
<FadeContainer show={loadingType === 'start' && context.stateApp.loaded}>
	<PressToContinue onpress={() => (loadingType = 'transition')} />
</FadeContainer>

<!-- transition between the loading screen and the game -->
<FadeContainer show={loadingType === 'transition'}>
	<TransitionAnimation oncomplete={props.onloaded} />
</FadeContainer>
