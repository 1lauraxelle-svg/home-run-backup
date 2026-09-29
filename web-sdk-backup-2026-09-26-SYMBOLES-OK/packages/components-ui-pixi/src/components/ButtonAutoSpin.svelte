<script lang="ts">
	import type * as PIXI from 'pixi.js';
	import { Container, Graphics } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';
	import { stateBet, stateBetDerived, stateModal } from 'state-shared';

	import UiSprite from './UiSprite.svelte';
	import { getContext } from '../context';
	import { UI_BASE_SIZE } from '../constants';
	import ButtonBetAutoSpinsCounter from './ButtonBetAutoSpinsCounter.svelte';

	const props: Partial<Omit<ButtonProps, 'children'>> = $props();
	const context = getContext();
	const sizes = { width: UI_BASE_SIZE, height: UI_BASE_SIZE };
	const active = $derived(stateBetDerived.hasAutoBetCounter());
	const disabled = $derived.by(() => {
		if (stateBet.isSpaceHold) return true;
		if (!context.stateXstateDerived.isIdle() && !stateBetDerived.hasAutoBetCounter()) return true;
		if (!stateBetDerived.isBetCostAvailable()) return true;
		return false;
	});

	const stopAutoSpin = () => (stateBet.autoSpinsCounter = 0);
	const openModal = () => (stateModal.modal = { name: 'autoSpin' });
	const onpress = () => {
		context.eventEmitter.broadcast({ type: 'soundPressGeneral' });
		stateBetDerived.hasAutoBetCounter() ? stopAutoSpin() : openModal();
	};

	/** Play icon: white circle + right-pointing triangle (reference). */
	const drawPlayIcon = (g: PIXI.Graphics) => {
		const r = sizes.height * 0.28;
		const stroke = Math.max(4, sizes.height * 0.045);
		g.circle(0, 0, r);
		g.stroke({ width: stroke, color: 0xffffff });

		const triH = r * 1.05;
		const triW = r * 0.9;
		const ox = -triW * 0.15;
		g.moveTo(ox - triW * 0.35, -triH * 0.45);
		g.lineTo(ox + triW * 0.55, 0);
		g.lineTo(ox - triW * 0.35, triH * 0.45);
		g.closePath();
		g.fill({ color: 0xffffff });
	};
</script>

<Button {...props} {sizes} {active} {onpress} {disabled}>
	{#snippet children({ center })}
		<Container {...center}>
			<UiSprite
				width={sizes.width}
				height={sizes.height}
				anchor={0.5}
				backgroundColor={0x0d0d0d}
				borderWidth={active ? 8 : 4}
				borderColor={0xffffff}
				borderAlpha={active ? 1 : 0.85}
				{...disabled
					? {
							backgroundColor: 0x666666,
						}
					: {}}
			/>
			{#if !active}
				<Graphics draw={drawPlayIcon} />
			{/if}
			<ButtonBetAutoSpinsCounter />
		</Container>
	{/snippet}
</Button>
