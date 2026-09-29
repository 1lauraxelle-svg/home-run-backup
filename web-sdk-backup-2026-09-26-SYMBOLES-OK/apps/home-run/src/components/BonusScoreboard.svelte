<script lang="ts">
	/**
	 * Stadium scoreboard panel for free-spin intro / bonus announce.
	 * Baseball spirit: night-game LED board, gold frame, red accents.
	 */
	import type { Snippet } from 'svelte';
	import { Container, Rectangle, Text } from 'pixi-svelte';
	import { MainContainer } from 'components-layout';

	import { getContext } from '../game/context';

	type Props = {
		/** Vertical offset from board center (negative = higher). */
		y?: number;
		/** Big number / amount slot rendered in the center plaque. */
		center?: Snippet;
		eyebrow?: string;
		title?: string;
		subtitle?: string;
		footer?: string;
	};

	const props: Props = $props();
	const context = getContext();

	const W = 520;
	const H = 340;
	const GOLD = 0xe8b84a;
	const GOLD_DIM = 0xa67c2a;
	const NAVY = 0x0a1628;
	const NAVY_MID = 0x122038;
	const RED = 0xc41e3a;
	const CREAM = 0xf5ecd7;
</script>

<MainContainer>
	<Container
		x={context.stateGameDerived.boardLayout().x}
		y={context.stateGameDerived.boardLayout().y + (props.y ?? 0)}
	>
		<!-- Outer metal frame -->
		<Rectangle
			x={-W * 0.5}
			y={-H * 0.5}
			width={W}
			height={H}
			borderRadius={10}
			backgroundColor={GOLD_DIM}
			backgroundAlpha={1}
		/>
		<!-- Inner night-board -->
		<Rectangle
			x={-W * 0.5 + 8}
			y={-H * 0.5 + 8}
			width={W - 16}
			height={H - 16}
			borderRadius={6}
			backgroundColor={NAVY}
			backgroundAlpha={0.98}
			borderColor={GOLD}
			borderWidth={2}
			borderAlpha={0.9}
		/>
		<!-- Scoreboard top LED strip -->
		<Rectangle
			x={-W * 0.5 + 18}
			y={-H * 0.5 + 16}
			width={W - 36}
			height={6}
			borderRadius={2}
			backgroundColor={GOLD}
			backgroundAlpha={0.85}
		/>
		<!-- Foul-line red accents -->
		<Rectangle
			x={-W * 0.5 + 18}
			y={-H * 0.5 + 28}
			width={48}
			height={3}
			backgroundColor={RED}
			backgroundAlpha={0.95}
		/>
		<Rectangle
			x={W * 0.5 - 66}
			y={-H * 0.5 + 28}
			width={48}
			height={3}
			backgroundColor={RED}
			backgroundAlpha={0.95}
		/>
		<!-- Mid panel shade behind number -->
		<Rectangle
			x={-140}
			y={-28}
			width={280}
			height={130}
			borderRadius={8}
			backgroundColor={NAVY_MID}
			backgroundAlpha={0.95}
			borderColor={GOLD}
			borderWidth={2}
			borderAlpha={0.75}
		/>

		<Text
			text={props.eyebrow ?? '★ STRIKE ZONE ★'}
			anchor={0.5}
			y={-H * 0.5 + 52}
			style={{
				fill: GOLD,
				fontSize: 16,
				fontWeight: '700',
				fontFamily: 'Arial Black, Arial, sans-serif',
				letterSpacing: 4,
				align: 'center',
			}}
		/>
		<Text
			text={props.title ?? 'HOME RUN!'}
			anchor={0.5}
			y={-H * 0.5 + 92}
			style={{
				fill: GOLD,
				fontSize: 48,
				fontWeight: '900',
				fontFamily: 'Arial Black, Arial, sans-serif',
				letterSpacing: 3,
				align: 'center',
				stroke: { color: '#5a3a00', width: 4 },
			}}
		/>
		<Text
			text={props.subtitle ?? 'MANCHES BONUS'}
			anchor={0.5}
			y={-H * 0.5 + 128}
			style={{
				fill: CREAM,
				fontSize: 18,
				fontWeight: '600',
				fontFamily: 'Arial, sans-serif',
				letterSpacing: 3,
				align: 'center',
			}}
		/>

		{#if props.center}
			<Container y={38}>
				{@render props.center()}
			</Container>
		{/if}

		<Text
			text={props.footer ?? 'INNINGS'}
			anchor={0.5}
			y={H * 0.5 - 36}
			style={{
				fill: RED,
				fontSize: 22,
				fontWeight: '800',
				fontFamily: 'Arial Black, Arial, sans-serif',
				letterSpacing: 6,
				align: 'center',
			}}
		/>
		<!-- Bottom LED strip -->
		<Rectangle
			x={-W * 0.5 + 18}
			y={H * 0.5 - 18}
			width={W - 36}
			height={4}
			borderRadius={2}
			backgroundColor={GOLD}
			backgroundAlpha={0.55}
		/>
	</Container>
</MainContainer>
