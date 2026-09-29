<script lang="ts">
	import type * as PIXI from 'pixi.js';
	import { Container, Text, Graphics } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';
	import { OnHotkey } from 'components-shared';
	import { stateBetDerived } from 'state-shared';

	import UiSprite from './UiSprite.svelte';
	import ButtonBetProvider from './ButtonBetProvider.svelte';
	import { UI_BASE_SIZE } from '../constants';
	import { i18nDerived } from '../i18n/i18nDerived';

	const props: Partial<Omit<ButtonProps, 'children'>> = $props();
	const disabled = $derived(!stateBetDerived.isBetCostAvailable());
	const sizes = { width: UI_BASE_SIZE * 1.15, height: UI_BASE_SIZE * 1.15 };

	/** Clockwise spin arrow (same sense as the reference icon). */
	const drawSpinArrow = (g: PIXI.Graphics) => {
		const r = sizes.height * 0.27;
		const stroke = Math.max(8, sizes.height * 0.075);
		// Canvas angles: 0 = east, increase = clockwise. Gap near bottom-left, tip lower-right.
		const start = (210 * Math.PI) / 180;
		const end = (150 * Math.PI) / 180;
		g.moveTo(Math.cos(start) * r, Math.sin(start) * r);
		g.arc(0, 0, r, start, end, false);
		g.stroke({ width: stroke, color: 0xffffff, cap: 'round', join: 'round' });

		const tx = Math.cos(end) * r;
		const ty = Math.sin(end) * r;
		// Clockwise tangent (canvas): (-sin, cos)
		const tdx = -Math.sin(end);
		const tdy = Math.cos(end);
		const headLen = stroke * 2.4;
		const headW = stroke * 1.6;
		const bx = tx - tdx * headLen * 0.15;
		const by = ty - tdy * headLen * 0.15;
		g.moveTo(tx + tdx * headLen * 0.35, ty + tdy * headLen * 0.35);
		g.lineTo(bx - tdy * headW, by + tdx * headW);
		g.lineTo(bx + tdy * headW, by - tdx * headW);
		g.closePath();
		g.fill({ color: 0xffffff });
	};
</script>

<ButtonBetProvider>
	{#snippet children({ key, onpress })}
		{@const isStop = ['stop_default', 'stop_disabled'].includes(key)}
		<OnHotkey hotkey="Space" {disabled} {onpress} />
		<Button {...props} {sizes} {onpress} {disabled}>
			{#snippet children({ center })}
				<Container {...center}>
					<UiSprite
						key="bet"
						width={sizes.width}
						height={sizes.height}
						anchor={0.5}
						backgroundColor={0x0d0d0d}
						borderWidth={6}
						borderColor={0xffffff}
						borderAlpha={0.95}
						{...disabled || ['spin_disabled', 'stop_disabled'].includes(key)
							? {
									backgroundColor: 0x666666,
								}
							: {}}
					/>
					{#if isStop}
						<Text
							anchor={0.5}
							text={i18nDerived.stop()}
							style={{
								align: 'center',
								fontFamily: 'Arial Black, Arial, sans-serif',
								fontWeight: '700',
								fontSize: sizes.height * 0.22,
								fill: 0xffffff,
							}}
						/>
					{:else}
						<!-- Tip at bottom pointing down -->
						<Container rotation={-Math.PI / 3}>
							<Graphics draw={drawSpinArrow} />
						</Container>
					{/if}
				</Container>
			{/snippet}
		</Button>
	{/snippet}
</ButtonBetProvider>
