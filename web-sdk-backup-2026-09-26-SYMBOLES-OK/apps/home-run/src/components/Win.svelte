<script lang="ts" module>
	import type { WinLevelData } from '../game/winLevelMap';

	export type EmitterEventWin =
		| { type: 'winShow' }
		| { type: 'winHide' }
		| { type: 'winUpdate'; amount: number; winLevelData: WinLevelData };
</script>

<script lang="ts">
	import { Container } from 'pixi-svelte';
	import { FadeContainer, WinCountUpProvider, ResponsiveBitmapText } from 'components-pixi';
	import { waitForResolve, waitForTimeout } from 'utils-shared/wait';
	import { bookEventAmountToCurrencyString } from 'utils-shared/amount';
	import { CanvasSizeRectangle, MainContainer } from 'components-layout';
	import { OnMount } from 'components-shared';

	import WinCoins from './WinCoins.svelte';
	import WinAnimation from './WinAnimation.svelte';
	import MaxWinBanner from './MaxWinBanner.svelte';
	import PressToContinue from './PressToContinue.svelte';
	import { SYMBOL_SIZE } from '../game/constants';
	import { getContext } from '../game/context';

	const context = getContext();

	/** Auto-dismiss only if player never froze the amount (~1s for small wins). */
	const AUTO_CONTINUE_MS = 1000;
	const HOLD_AFTER_COUNT_MS = 200;

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
		winShow: () => {
			completed = false;
			amountFrozenByPress = false;
			show = true;
		},
		winHide: () => (show = false),
		winUpdate: async (emitterEvent) => {
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

<!-- persistent: keep children mounted so completion can always run -->
<FadeContainer persistent {show} duration={120}>
	{#if winLevelData}
		{@const isBigWin = winLevelData.type === 'big'}
		{@const duration = winLevelData.presentDuration}
		<WinCountUpProvider {amount} {duration} oncomplete={() => {}}>
			{#snippet children({ countUpAmount, startCountUp, finishCountUp, countUpCompleted })}
				{#if isBigWin}
					<CanvasSizeRectangle backgroundColor={0x000000} backgroundAlpha={0.5} eventMode="none" />
				{/if}

				{#if show}
					<OnMount
						onmount={async () => {
							const t0 = performance.now();
							await startCountUp();
							if (completed) return;
							// Player froze the amount — wait for 2nd click
							if (amountFrozenByPress) return;
							const elapsed = performance.now() - t0;
							const waitMore = isBigWin
								? HOLD_AFTER_COUNT_MS
								: Math.max(HOLD_AFTER_COUNT_MS, AUTO_CONTINUE_MS - elapsed);
							await waitForTimeout(waitMore);
							if (completed || amountFrozenByPress) return;
							finish();
						}}
					/>

					<MainContainer>
						<Container
							x={context.stateGameDerived.boardLayout().x}
							y={context.stateGameDerived.boardLayout().y}
						>
							{#if winLevelData?.alias === 'max'}
								<MaxWinBanner {amount} y={-360} />
							{/if}
							{#if winLevelData?.animation}
								<WinAnimation animationMap={winLevelData.animation}>
									<ResponsiveBitmapText
										anchor={0.5}
										maxWidth={2130}
										text={bookEventAmountToCurrencyString(countUpAmount)}
										style={{
											fontFamily: 'gold',
											fontSize: SYMBOL_SIZE * 3.6,
											align: 'center',
											fontWeight: 'bold',
											letterSpacing: 0,
										}}
									/>
								</WinAnimation>
							{:else}
								<ResponsiveBitmapText
									anchor={0.5}
									maxWidth={context.stateLayoutDerived.canvasSizes().width /
										context.stateLayoutDerived.mainLayout().scale}
									text={bookEventAmountToCurrencyString(countUpAmount)}
									style={{
										fontFamily: 'gold',
										fontSize: SYMBOL_SIZE,
										align: 'center',
										fontWeight: 'bold',
										letterSpacing: 0,
									}}
								/>
							{/if}
						</Container>
					</MainContainer>

					<WinCoins emit={!countUpCompleted} levelAlias={winLevelData?.alias} />

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
				{/if}
			{/snippet}
		</WinCountUpProvider>
	{/if}
</FadeContainer>
