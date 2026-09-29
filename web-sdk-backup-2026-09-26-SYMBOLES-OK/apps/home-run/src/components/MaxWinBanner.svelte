<script lang="ts">
	/**
	 * Gold MAX WIN window title + ×25 000 multiplier badge.
	 * Shown on top of the big-win spine when winLevel alias is "max".
	 */
	import { Container, Text } from 'pixi-svelte';

	type Props = {
		y?: number;
		/** Book-event amount (100 = 1x bet). Defaults to cap branding ×25 000. */
		amount?: number;
	};

	const props: Props = $props();

	const MAX_WIN_CAP = 25_000;

	const multiplierLabel = $derived.by(() => {
		const fromAmount =
			props.amount != null && props.amount > 0
				? Math.round(props.amount / 100)
				: MAX_WIN_CAP;
		const n = fromAmount > 0 ? fromAmount : MAX_WIN_CAP;
		return `×${n.toLocaleString('fr-FR')}`;
	});
</script>

<Container y={props.y ?? -360}>
	<Text
		text="MAX WIN"
		anchor={0.5}
		y={0}
		style={{
			fill: '#FFD700',
			fontSize: 64,
			fontWeight: '900',
			fontFamily: 'Arial Black, Arial, sans-serif',
			letterSpacing: 4,
			align: 'center',
			stroke: { color: '#8a5a00', width: 4 },
		}}
	/>
	<Text
		text={multiplierLabel}
		anchor={0.5}
		y={100}
		style={{
			fill: '#FFE566',
			fontSize: 120,
			fontWeight: '900',
			fontFamily: 'Arial Black, Arial, sans-serif',
			letterSpacing: 4,
			align: 'center',
			stroke: { color: '#8a5a00', width: 6 },
		}}
	/>
</Container>
