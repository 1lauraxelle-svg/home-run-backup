<script lang="ts" module>
	import type { WinLevelData } from '../game/winLevelMap';

	export type EmitterEventFreeSpinOutro =
		| { type: 'freeSpinOutroShow' }
		| { type: 'freeSpinOutroHide' }
		| { type: 'freeSpinOutroCountUp'; amount: number; winLevelData: WinLevelData };
</script>

<script lang="ts">
	import { Container } from 'pixi-svelte';
	import { FadeContainer, WinCountUpProvider, ResponsiveBitmapText } from 'components-pixi';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';
	import { waitForResolve, waitForTimeout } from 'utils-shared/wait';
	import { CanvasSizeRectangle, MainContainer } from 'components-layout';
	import { OnMount } from 'components-shared';

	import { getContext } from '../game/context';
	import PressToContinue from './PressToContinue.svelte';
	import BonusScoreboard from './BonusScoreboard.svelte';
	import MaxWinBanner from './MaxWinBanner.svelte';

	const context = getContext();

	let show = $state(false);
	let amount = $state(0);
	let winLevelData = $state<WinLevelData>();
	let oncomplete = $state(() => {});
	let completed = $state(false);
	/** After 1st press freezes the amount — wait for 2nd press (no auto-continue). */
	let amountFrozenByPress = $state(false);

	const finish = () => {
		if (completed) return;
		completed = true;
		oncomplete();
	};

	context.eventEmitter.subscribeOnMount({
		freeSpinOutroShow: () => {
			completed = false;
			amountFrozenByPress = false;
			show = true;
		},
		freeSpinOutroHide: async () => (show = false),
		freeSpinOutroCountUp: async (emitterEvent) => {
			if (!emitterEvent.winLevelData) {
				amount = emitterEvent.amount;
				return;
			}
			completed = false;
			amountFrozenByPress = false;
			amount = emitterEvent.amount;
			winLevelData = emitterEvent.winLevelData;
			await waitForResolve((resolve) => (oncomplete = resolve));
		},
	});
</script>

<FadeContainer persistent {show} duration={100}>
	{#if winLevelData && show}
		{@const duration = winLevelData.presentDuration}
		{@const isMaxWin = winLevelData.alias === 'max'}
		{@const isBigWin = winLevelData.type === 'big'}
		<WinCountUpProvider {amount} {duration} oncomplete={() => {}}>
			{#snippet children({ countUpAmount, startCountUp, finishCountUp, countUpCompleted })}
				<OnMount
					onmount={async () => {
						const t0 = performance.now();
						await startCountUp();
						if (completed) return;
						if (amountFrozenByPress) return;
						const elapsed = performance.now() - t0;
						const waitMore = Math.max(200, 1000 - elapsed);
						await waitForTimeout(waitMore);
						if (completed || amountFrozenByPress) return;
						finish();
					}}
				/>

				<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.55} eventMode="none" />

				{#if isMaxWin}
					<MainContainer>
						<Container
							x={context.stateGameDerived.boardLayout().x}
							y={context.stateGameDerived.boardLayout().y - 320}
						>
							<MaxWinBanner {amount} y={0} />
						</Container>
					</MainContainer>
				{/if}

				<!-- Stadium scoreboard — centered on the slot -->
				<BonusScoreboard
					y={0}
					eyebrow="★ STRIKE ZONE ★"
					title="FINAL SCORE"
					subtitle="BONUS COMPLETE"
					footer="SCORE"
				>
					{#snippet center()}
						<ResponsiveBitmapText
							anchor={0.5}
							maxWidth={250}
							text={bookEventAmountToCurrencyString(countUpAmount)}
							style={{
								fontFamily: 'gold',
								fontSize: isBigWin ? 72 : 64,
								fontWeight: 'bold',
								align: 'center',
							}}
						/>
					{/snippet}
				</BonusScoreboard>

				<!-- 1st press: freeze amount · 2nd press: continue -->
				<PressToContinue
					onpress={() => {
						if (!countUpCompleted) {
							amountFrozenByPress = true;
							finishCountUp();
						} else {
							finish();
						}
					}}
				/>
			{/snippet}
		</WinCountUpProvider>
	{/if}
</FadeContainer>
