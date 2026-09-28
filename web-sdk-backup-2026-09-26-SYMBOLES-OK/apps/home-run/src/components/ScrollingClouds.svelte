<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	const context = getContext();

	const SPEED = 28; // px / second
	const CLOUD_ALPHA = 0.55;

	let offset = $state(0);
	let raf = 0;
	let last = 0;

	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const cloudWidth = $derived(Math.max(canvas.width * 1.35, 900));
	const cloudHeight = $derived(Math.max(canvas.height * 0.28, 120));
	const cloudY = $derived(canvas.height * 0.02);

	onMount(() => {
		last = performance.now();
		const tick = (now: number) => {
			const dt = Math.min(0.05, (now - last) / 1000);
			last = now;
			const w = cloudWidth;
			offset = (offset + SPEED * dt) % w;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
	});

	onDestroy(() => {
		if (raf) cancelAnimationFrame(raf);
	});
</script>

<Container zIndex={-1} alpha={CLOUD_ALPHA}>
	<Sprite
		key="cloudsScroll"
		x={-offset}
		y={cloudY}
		width={cloudWidth}
		height={cloudHeight}
	/>
	<Sprite
		key="cloudsScroll"
		x={-offset + cloudWidth}
		y={cloudY}
		width={cloudWidth}
		height={cloudHeight}
	/>
</Container>
