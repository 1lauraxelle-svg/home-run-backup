<script lang="ts">
	import { Sprite } from 'pixi-svelte';

	type Props = {
		x?: number;
		y?: number;
		anchor?: number | { x: number; y: number };
		width?: number;
		height?: number;
		alpha?: number;
		zIndex?: number;
	};

	const props: Props = $props();
</script>

<Sprite
	key="studioLogo"
	x={props.x ?? 0}
	y={props.y ?? 0}
	anchor={props.anchor ?? 0.5}
	width={props.width ?? 158}
	height={props.height ?? 120}
	alpha={props.alpha ?? 1}
	zIndex={props.zIndex}
/>
