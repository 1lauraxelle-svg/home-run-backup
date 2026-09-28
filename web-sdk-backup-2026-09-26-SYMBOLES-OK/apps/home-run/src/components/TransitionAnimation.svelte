<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { Container, Rectangle, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	type Props = {
		oncomplete: () => void;
	};

	type Ball = {
		id: number;
		x: number;
		y: number;
		vx: number;
		rot: number;
		vr: number;
		size: number;
		delay: number;
		startY: number;
	};

	const props: Props = $props();
	const context = getContext();

	const canvas = $derived(context.stateLayoutDerived.canvasSizes());

	let overlayAlpha = $state(0);
	let balls = $state<Ball[]>([]);
	let done = false;
	let raf = 0;
	let cancelled = false;

	const easeInCubic = (t: number) => t * t * t;
	const easeOutCubic = (t: number) => 1 - Math.pow(1 - t, 3);

	onMount(() => {
		const w = canvas.width;
		const h = canvas.height;

		const spawned: Ball[] = [];
		for (let i = 0; i < 28; i++) {
			const startY = -60 - Math.random() * h * 0.85;
			spawned.push({
				id: i,
				x: w * (0.03 + Math.random() * 0.94),
				y: startY,
				startY,
				vx: (Math.random() - 0.5) * w * 0.12,
				rot: Math.random() * Math.PI * 2,
				vr: (Math.random() - 0.5) * 14,
				size: 34 + Math.random() * 56,
				delay: Math.random() * 0.35,
			});
		}
		balls = spawned;

		const start = performance.now();
		const duration = 1400;

		const tick = (now: number) => {
			if (cancelled) return;
			const t = Math.min(1, (now - start) / duration);

			// Soft dark flash behind the balls
			if (t < 0.2) {
				overlayAlpha = easeOutCubic(t / 0.2) * 0.55;
			} else if (t < 0.65) {
				overlayAlpha = 0.55;
			} else {
				overlayAlpha = 0.55 * (1 - easeInCubic((t - 0.65) / 0.35));
			}

			balls = spawned.map((b) => {
				const local = Math.min(1, Math.max(0, (t - b.delay) / Math.max(0.001, 1 - b.delay)));
				const fall = easeInCubic(local);
				return {
					...b,
					x: b.x + b.vx * fall,
					y: b.startY + (h * 1.35 - b.startY) * fall,
					rot: b.rot + b.vr * fall,
				};
			});

			if (t < 1) {
				raf = requestAnimationFrame(tick);
			} else if (!done) {
				done = true;
				props.oncomplete();
			}
		};

		raf = requestAnimationFrame(tick);
	});

	onDestroy(() => {
		cancelled = true;
		if (raf) cancelAnimationFrame(raf);
	});
</script>

<Container zIndex={1000}>
	<Rectangle
		x={0}
		y={0}
		width={canvas.width}
		height={canvas.height}
		backgroundColor={0x061028}
		alpha={overlayAlpha}
	/>

	{#each balls as b (b.id)}
		<Sprite
			key="transitionWhiteBall"
			anchor={0.5}
			x={b.x}
			y={b.y}
			width={b.size}
			height={b.size}
			rotation={b.rot}
		/>
	{/each}
</Container>
