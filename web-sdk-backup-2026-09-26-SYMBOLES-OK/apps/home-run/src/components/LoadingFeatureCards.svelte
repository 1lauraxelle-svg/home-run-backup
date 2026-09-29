<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { Container, Rectangle, Sprite, Text } from 'pixi-svelte';

	type Card = {
		title: string;
		titleColor: number;
		body: string;
		iconKey: string;
		highlight?: boolean;
	};

	type Props = {
		y?: number;
		scale?: number;
	};

	const props: Props = $props();

	const CARD_W = 232;
	const CARD_H = 278;
	const GAP = 20;
	const RADIUS = 20;
	const ICON_BOX = 112;

	const cards: Card[] = [
		{
			title: 'BONUS',
			titleColor: 0xffffff,
			body: '3 SCATTER = 10 FS\n4 = 12 · 5 = 15 FS',
			iconKey: 's.png',
		},
		{
			title: 'MULTIPLIERS',
			titleColor: 0xffffff,
			body: 'WILD × se multiplient\nsur la ligne (×2 × ×3 = ×6)',
			iconKey: 'm3_10x.png',
		},
		{
			title: '20 LIGNES',
			titleColor: 0xffffff,
			body: 'Gains de gauche\nà droite · 20 lignes',
			iconKey: 'w.png',
		},
		{
			title: 'MAX WIN',
			titleColor: 0xb8ff2e,
			body: 'Plafond ×25 000\nle home run ultime',
			iconKey: 'h1.webp',
			highlight: true,
		},
	];

	const totalW = cards.length * CARD_W + (cards.length - 1) * GAP;
	const scale = $derived(props.scale ?? 1);

	/** Per-card wind phase (radians). */
	const phases = cards.map((_, i) => i * 1.15 + 0.4);
	let windT = $state(0);
	let raf = 0;

	const sway = (i: number) => {
		const t = windT;
		const p = phases[i];
		return {
			rot: Math.sin(t * 1.35 + p) * 0.045 + Math.sin(t * 2.1 + p * 1.3) * 0.015,
			dx: Math.sin(t * 1.1 + p) * 4.5,
			dy: Math.cos(t * 0.9 + p * 0.8) * 3.2,
		};
	};

	onMount(() => {
		let last = performance.now();
		const tick = (now: number) => {
			const dt = Math.min(0.05, (now - last) / 1000);
			last = now;
			windT += dt;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
	});

	onDestroy(() => {
		if (raf) cancelAnimationFrame(raf);
	});
</script>

<!-- Outer: position. Middle: scale from center. Inner: cards L→R, centered. -->
<Container y={props.y ?? 0} x={0}>
	<Container scale={scale}>
		<Container x={-totalW * 0.5}>
			{#each cards as card, i}
				{@const x = i * (CARD_W + GAP)}
				{@const w = sway(i)}
				<!-- Pivot near bottom so cards sway like hanging in the wind -->
				<Container
					x={x + CARD_W * 0.5 + w.dx}
					y={CARD_H + w.dy}
					rotation={w.rot}
					pivot={{ x: CARD_W * 0.5, y: CARD_H }}
				>
					<Rectangle
						width={CARD_W}
						height={CARD_H}
						borderRadius={RADIUS}
						backgroundColor={0x1a1512}
						backgroundAlpha={0.94}
						borderColor={card.highlight ? 0xe8902a : 0x3a3028}
						borderWidth={card.highlight ? 3 : 1.5}
						borderAlpha={card.highlight ? 0.95 : 0.7}
					/>
					<Rectangle
						x={12}
						y={10}
						width={CARD_W - 24}
						height={3}
						borderRadius={2}
						backgroundColor={card.highlight ? 0xe8902a : 0x5a4a3a}
						backgroundAlpha={0.55}
					/>
					<Rectangle
						x={(CARD_W - ICON_BOX) * 0.5}
						y={26}
						width={ICON_BOX}
						height={ICON_BOX}
						borderRadius={14}
						backgroundColor={0x0c0a09}
						backgroundAlpha={0.95}
						borderColor={0x2a221c}
						borderWidth={1}
					/>
					<Sprite
						key={card.iconKey}
						x={CARD_W * 0.5}
						y={26 + ICON_BOX * 0.5}
						anchor={0.5}
						width={92}
						height={92}
					/>
					<Text
						text={card.title}
						x={CARD_W * 0.5}
						y={162}
						anchor={0.5}
						style={{
							fill: card.titleColor,
							fontSize: 22,
							fontWeight: '800',
							fontFamily: 'Arial Black, Arial, sans-serif',
							letterSpacing: 0.5,
						}}
					/>
					<Text
						text={card.body}
						x={CARD_W * 0.5}
						y={212}
						anchor={0.5}
						style={{
							fill: 0xe8e0d8,
							fontSize: 14,
							fontWeight: '400',
							fontFamily: 'Arial, sans-serif',
							align: 'center',
							wordWrap: true,
							wordWrapWidth: CARD_W - 28,
							lineHeight: 18,
						}}
					/>
				</Container>
			{/each}
		</Container>
	</Container>
</Container>
