<script lang="ts">
	import { stateUi } from 'state-shared';
	import { BLACK } from 'constants-shared/colors';
	import { MainContainer } from 'components-layout';
	import { Container, Rectangle, anchorToPivot } from 'pixi-svelte';

	import { DESKTOP_BASE_SIZE } from '../constants';
	import { getContext } from '../context';
	import type { LayoutUiProps } from '../types';

	const props: LayoutUiProps = $props();
	const context = getContext();

	/** Wider bar so BUY BONUS has clear gaps left & right */
	const BAR_W = 1420;
	const ROW_Y = DESKTOP_BASE_SIZE * 0.55;
	const BAR_BOTTOM_PAD = 28;

	const PANEL = 0x1a1a1a;
	const PANEL_SOFT = 0x2a2a2a;
	const PANEL_H = 88;
	const PANEL_TOP = ROW_Y - PANEL_H * 0.5;
</script>

<Container x={20}>
	{@render props.gameName()}
</Container>

<Container x={context.stateLayoutDerived.canvasSizes().width - 20}>
	{@render props.logo()}
</Container>

<MainContainer standard alignVertical="bottom">
	<Container
		x={context.stateLayoutDerived.mainLayoutStandard().width * 0.5}
		y={context.stateLayoutDerived.mainLayoutStandard().height - DESKTOP_BASE_SIZE - BAR_BOTTOM_PAD}
		pivot={anchorToPivot({
			anchor: { x: 0.5, y: 0 },
			sizes: { height: DESKTOP_BASE_SIZE, width: BAR_W },
		})}
	>
		<!-- Turbo -->
		<Container y={ROW_Y} x={48} scale={0.58}>
			{@render props.buttonTurbo({ anchor: 0.5 })}
		</Container>

		<!-- Info panel: menu + balance + win -->
		<Rectangle
			x={105}
			y={PANEL_TOP}
			width={430}
			height={PANEL_H}
			borderRadius={22}
			backgroundColor={PANEL_SOFT}
			backgroundAlpha={0.92}
		/>
		<Container y={ROW_Y} x={148} scale={0.44}>
			{@render props.buttonMenu({ anchor: 0.5 })}
		</Container>
		<Container y={ROW_Y} x={270} scale={0.74}>
			{@render props.amountBalance({ stacked: true })}
		</Container>
		<Container y={ROW_Y} x={430} scale={0.74}>
			{@render props.amountWin({ stacked: true })}
		</Container>

		<!-- Buy bonus — clear space between info & bet panels -->
		<Container y={ROW_Y} x={650} scale={0.68}>
			{@render props.buttonBuyBonus({ anchor: 0.5 })}
		</Container>

		<!-- Bet panel + chevrons (starts after buy bonus) -->
		<Rectangle
			x={780}
			y={PANEL_TOP}
			width={250}
			height={PANEL_H}
			borderRadius={20}
			backgroundColor={PANEL}
			backgroundAlpha={0.95}
		/>
		<Container y={ROW_Y} x={870} scale={0.74}>
			{@render props.amountBet({ stacked: true })}
		</Container>
		<Container y={ROW_Y - 18} x={985} scale={0.3}>
			{@render props.buttonIncrease({ anchor: 0.5 })}
		</Container>
		<Container y={ROW_Y + 18} x={985} scale={0.3}>
			{@render props.buttonDecrease({ anchor: 0.5 })}
		</Container>

		<!-- Auto -->
		<Container y={ROW_Y} x={1105} scale={0.58}>
			{@render props.buttonAutoSpin({ anchor: 0.5 })}
		</Container>

		<!-- Spin -->
		<Container y={ROW_Y} x={1265} scale={0.9}>
			{@render props.buttonBet({ anchor: 0.5 })}
		</Container>
	</Container>
</MainContainer>

{#if stateUi.menuOpen}
	<Rectangle
		eventMode="static"
		cursor="pointer"
		alpha={0.5}
		anchor={0.5}
		backgroundColor={BLACK}
		width={context.stateLayoutDerived.canvasSizes().width}
		height={context.stateLayoutDerived.canvasSizes().height}
		x={context.stateLayoutDerived.canvasSizes().width * 0.5}
		y={context.stateLayoutDerived.canvasSizes().height * 0.5}
		onpointerup={() => (stateUi.menuOpen = false)}
	/>

	<MainContainer standard alignVertical="bottom">
		<Container
			x={175}
			y={context.stateLayoutDerived.mainLayoutStandard().height - DESKTOP_BASE_SIZE - BAR_BOTTOM_PAD}
		>
			<Container scale={0.7} y={DESKTOP_BASE_SIZE * 0.5 - 150 - 150 * 3}>
				{@render props.buttonPayTable({ anchor: 0.5 })}
			</Container>

			<Container scale={0.7} y={DESKTOP_BASE_SIZE * 0.5 - 150 - 150 * 2}>
				{@render props.buttonGameRules({ anchor: 0.5 })}
			</Container>

			<Container scale={0.7} y={DESKTOP_BASE_SIZE * 0.5 - 150 - 150 * 1}>
				{@render props.buttonSettings({ anchor: 0.5 })}
			</Container>

			<Container scale={0.7} y={DESKTOP_BASE_SIZE * 0.5 - 150}>
				{@render props.buttonSoundSwitch({ anchor: 0.5 })}
			</Container>

			<Container scale={0.7} y={DESKTOP_BASE_SIZE * 0.5}>
				{@render props.buttonMenuClose({ anchor: 0.5 })}
			</Container>
		</Container>
	</MainContainer>
{/if}
