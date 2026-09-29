<script lang="ts">
	import { Container, Sprite } from 'pixi-svelte';
	import { onDestroy } from 'svelte';

	import { getSymbolInfo } from '../game/utils';
	import { SYMBOL_SIZE } from '../game/constants';
	import type { SymbolState } from '../game/types';

	type Props = {
		x?: number;
		y?: number;
		state?: SymbolState;
		symbolInfo: ReturnType<typeof getSymbolInfo>;
		oncomplete?: () => void;
	};

	const props: Props = $props();

	let scale = $state(1);
	let rotation = $state(0);
	let alpha = $state(1);

	let cancelled = false;
	let raf = 0;
	let completed = false;

	const easeOutBack = (t: number) => {
		const c1 = 1.9;
		const c3 = c1 + 1;
		return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);
	};

	const easeInOutSine = (t: number) => -(Math.cos(Math.PI * t) - 1) / 2;

	const finish = () => {
		if (completed || cancelled) return;
		completed = true;
		scale = 1;
		rotation = 0;
		alpha = 1;
		props.oncomplete?.();
	};

	/** Continuous wobble while reels are spinning — same for every symbol */
	const runSpin = () => {
		const start = performance.now();
		const tick = (now: number) => {
			if (cancelled) return;
			const t = (now - start) / 1000;
			scale = 1 + 0.07 * Math.sin(t * 22);
			rotation = 0.09 * Math.sin(t * 17);
			alpha = 0.9 + 0.1 * Math.sin(t * 12);
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);
	};

	/** Bounce + settle when a reel stops — same punch on every row */
	const runLand = () => {
		const duration = 520;
		const start = performance.now();
		const tick = (now: number) => {
			if (cancelled) return;
			const t = Math.min(1, (now - start) / duration);
			const bounce = easeOutBack(t);
			scale = 0.55 + 0.45 * bounce;
			rotation = (1 - t) * 0.28 * Math.sin(t * Math.PI * 3.2);
			alpha = 0.8 + 0.2 * t;
			if (t < 1) {
				raf = requestAnimationFrame(tick);
			} else {
				scale = 1;
				rotation = 0;
				alpha = 1;
				finish();
			}
		};
		raf = requestAnimationFrame(tick);
	};

	const runWin = () => {
		const duration = 1200;
		const start = performance.now();
		const tick = (now: number) => {
			if (cancelled) return;
			const t = Math.min(1, (now - start) / duration);
			const pulse = 1 + 0.28 * Math.sin(t * Math.PI * 5);
			scale = pulse;
			rotation = 0.1 * Math.sin(t * Math.PI * 4);
			alpha = 0.82 + 0.18 * easeInOutSine((Math.sin(t * Math.PI * 5) + 1) / 2);
			if (t < 1) {
				raf = requestAnimationFrame(tick);
			} else {
				scale = 1;
				rotation = 0;
				alpha = 1;
				finish();
			}
		};
		raf = requestAnimationFrame(tick);
	};

	$effect(() => {
		// Only react to animation state — do NOT track symbolInfo (new object refs
		// + oncomplete re-renders caused effect_update_depth_exceeded loops).
		const state = props.state ?? 'static';
		cancelled = false;
		cancelAnimationFrame(raf);
		scale = 1;
		rotation = 0;
		alpha = 1;

		if (state === 'spin') {
			completed = false;
			runSpin();
		} else if (state === 'land') {
			completed = false;
			runLand();
		} else if (state === 'win') {
			completed = false;
			runWin();
		} else {
			// static: settle once; finish() is idempotent via `completed`
			queueMicrotask(() => finish());
		}

		return () => {
			cancelled = true;
			cancelAnimationFrame(raf);
		};
	});

	onDestroy(() => {
		cancelled = true;
		cancelAnimationFrame(raf);
	});
</script>

<Container x={props.x} y={props.y} scale={scale} rotation={rotation} {alpha}>
	<Sprite
		anchor={0.5}
		key={props.symbolInfo.assetKey}
		width={SYMBOL_SIZE * props.symbolInfo.sizeRatios.width}
		height={SYMBOL_SIZE * props.symbolInfo.sizeRatios.height}
	/>
</Container>
