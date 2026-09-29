<script lang="ts">
	import { Text } from 'pixi-svelte';
	import { WHITE } from 'constants-shared/colors';

	import { UI_BASE_FONT_SIZE } from '../constants';

	type Props = {
		label: string;
		value: string;
		tiled?: boolean;
		stacked?: boolean;
	};

	const props: Props = $props();

	const labelStyle = {
		fontFamily: 'Arial, sans-serif',
		fontSize: UI_BASE_FONT_SIZE * 0.5,
		fontWeight: '600',
		letterSpacing: 1.5,
		fill: 0xcccccc,
	} as const;

	const valueStyle = {
		fontFamily: 'Arial Black, Arial, sans-serif',
		fontSize: UI_BASE_FONT_SIZE * 0.9,
		fontWeight: '700',
		fill: WHITE,
	} as const;

	/** Vertical gap between label and value when stacked (centered as a block). */
	const STACK_GAP = UI_BASE_FONT_SIZE * 0.55;
</script>

{#if props.stacked}
	<!-- Both lines centered as a block around y=0 so they sit inside the panel -->
	<Text
		anchor={0.5}
		y={-STACK_GAP * 0.55}
		text={props.label}
		style={labelStyle}
	/>
	<Text
		anchor={0.5}
		y={STACK_GAP * 0.7}
		text={props.value}
		style={valueStyle}
	/>
{:else}
	<Text anchor={{ x: 0, y: 0.5 }} text={props.label} style={labelStyle} />
	<Text
		anchor={{ x: 1, y: 0.5 }}
		text={props.value}
		style={valueStyle}
		x={UI_BASE_FONT_SIZE * 10}
	/>
{/if}
