<script lang="ts" module>
	export type EmitterEventFreeSpinIntro =
		| { type: 'freeSpinIntroShow' }
		| { type: 'freeSpinIntroHide' }
		| { type: 'freeSpinIntroUpdate'; totalFreeSpins: number };
</script>

<script lang="ts">
	import { CanvasSizeRectangle } from 'components-layout';
	import { FadeContainer } from 'components-pixi';
	import { waitForResolve } from 'utils-shared/wait';
	import { BitmapText } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import PressToContinue from './PressToContinue.svelte';
	import BonusScoreboard from './BonusScoreboard.svelte';

	const context = getContext();

	let show = $state(false);
	let freeSpinsFromEvent = $state(0);
	let oncomplete = $state(() => {});
	let completed = $state(false);
	/** True only while awaiting player continue — ignores premature taps. */
	let canContinue = $state(false);

	const finish = () => {
		if (completed || !canContinue) return;
		completed = true;
		canContinue = false;
		oncomplete();
	};

	context.eventEmitter.subscribeOnMount({
		freeSpinIntroShow: () => {
			completed = false;
			canContinue = false;
			show = true;
		},
		freeSpinIntroHide: () => {
			show = false;
			canContinue = false;
		},
		freeSpinIntroUpdate: async (emitterEvent) => {
			completed = false;
			freeSpinsFromEvent = emitterEvent.totalFreeSpins;
			await waitForResolve((resolve) => {
				oncomplete = resolve;
				canContinue = true;
			});
		},
	});
</script>

<FadeContainer persistent {show} duration={100}>
	{#if show}
		<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.55} eventMode="none" />

		<!-- Centered on the slot (same axis X/Y as the board) -->
		<BonusScoreboard y={0} title="HOME RUN!" footer="INNINGS">
			{#snippet center()}
				<BitmapText
					anchor={{ x: 0.5, y: 0.5 }}
					text={String(freeSpinsFromEvent)}
					style={{
						fontFamily: 'gold',
						fontSize: 110,
						fontWeight: 'bold',
					}}
				/>
			{/snippet}
		</BonusScoreboard>

		{#if canContinue}
			<PressToContinue onpress={() => finish()} />
		{/if}
	{/if}
</FadeContainer>
