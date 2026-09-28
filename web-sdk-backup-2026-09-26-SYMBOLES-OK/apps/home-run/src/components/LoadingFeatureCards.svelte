<script lang="ts">
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

	const CARD_W = 220;
	const CARD_H = 270;
	const GAP = 20;
	const RADIUS = 22;
	const ICON_BOX = 128;

	const cards: Card[] = [
		{
			title: 'BONUS',
			titleColor: 0xffffff,
			body: '3 symboles SCATTER\ndéclenchent les tours gratuits.',
			iconKey: 's.png',
		},
		{
			title: 'MULTIPLIERS',
			titleColor: 0xffffff,
			body: 'Les WILD portent des\nmultiplicateurs x2 à x10.',
			iconKey: 'm3_10x.png',
		},
		{
			title: '20 LIGNES',
			titleColor: 0xffffff,
			body: 'Les gains paient de gauche\nà droite sur 20 lignes.',
			iconKey: 'w.png',
		},
		{
			title: 'MAX WIN',
			titleColor: 0xb8ff2e,
			body: 'Plafond x25 000 votre mise\n— le home run ultime.',
			iconKey: 'h1.webp',
			highlight: true,
		},
	];

	const totalW = cards.length * CARD_W + (cards.length - 1) * GAP;
	const scale = $derived(props.scale ?? 1);
</script>

<!-- x compensates scale so the row stays centered on parent (0,0) -->
<Container y={props.y ?? 0} scale={scale} x={-totalW * scale * 0.5}>
	{#each cards as card, i}
		{@const x = i * (CARD_W + GAP)}
		<Container {x}>
			<!-- Card body -->
			<Rectangle
				width={CARD_W}
				height={CARD_H}
				borderRadius={RADIUS}
				backgroundColor={0x1a1512}
				backgroundAlpha={0.92}
				borderColor={card.highlight ? 0xe8902a : 0x3a3028}
				borderWidth={card.highlight ? 3 : 1.5}
				borderAlpha={card.highlight ? 0.95 : 0.7}
			/>
			<!-- Soft top rim -->
			<Rectangle
				x={10}
				y={8}
				width={CARD_W - 20}
				height={4}
				borderRadius={2}
				backgroundColor={card.highlight ? 0xe8902a : 0x5a4a3a}
				backgroundAlpha={0.55}
			/>
			<!-- Icon inset -->
			<Rectangle
				x={(CARD_W - ICON_BOX) * 0.5}
				y={28}
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
				y={28 + ICON_BOX * 0.5}
				anchor={0.5}
				width={100}
				height={100}
			/>
			<!-- Title -->
			<Text
				text={card.title}
				x={CARD_W * 0.5}
				y={175}
				anchor={0.5}
				style={{
					fill: card.titleColor,
					fontSize: 22,
					fontWeight: '800',
					fontFamily: 'Arial Black, Arial, sans-serif',
					letterSpacing: 1,
				}}
			/>
			<!-- Body -->
			<Text
				text={card.body}
				x={CARD_W * 0.5}
				y={218}
				anchor={0.5}
				style={{
					fill: 0xe8e0d8,
					fontSize: 13,
					fontWeight: '400',
					fontFamily: 'Arial, sans-serif',
					align: 'center',
					wordWrap: true,
					wordWrapWidth: CARD_W - 28,
					lineHeight: 17,
				}}
			/>
		</Container>
	{/each}
</Container>
