<script lang="ts" module>
	export type EmitterEventCatcher =
		| { type: 'catcherCatch' }
		| { type: 'catcherIdle' };
</script>

<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { SYMBOL_SIZE } from '../game/constants';

	const context = getContext();

	type Pose = 'idle' | 'catch';

	let pose = $state<Pose>('idle');
	let catcherScale = $state(1);
	let catcherRot = $state(0);

	let raf = 0;
	let cancelled = false;
	let catching = false;

	const board = $derived(context.stateGameDerived.boardLayout());
	const catcherH = $derived(board.height * 1.05);
	const catcherW = $derived(catcherH * 0.72);
	// Left of frame (mirror of batter)
	const baseX = $derived(board.x - board.width * 0.5 - catcherW * 0.35 - SYMBOL_SIZE * 0.15);
	// Feet on the white chalk marks near home plate
	const baseY = $derived(board.y + board.height * 0.55);

	const spriteKey = $derived(pose === 'catch' ? 'catcherCatch' : 'catcherIdle');

	const easeOutCubic = (t: number) => 1 - Math.pow(1 - t, 3);

	/** Timed to batter: contact ~110ms after swing, ball arrives ~650–750ms later */
	const runCatch = () => {
		if (cancelled || catching) return;
		catching = true;

		const start = performance.now();
		// Anticipate → snag → settle (synced to batter's 900ms swing)
		const anticipateMs = 420;
		const catchHoldMs = 280;
		const settleMs = 320;
		const total = anticipateMs + catchHoldMs + settleMs;

		const tick = (now: number) => {
			if (cancelled) return;
			const elapsed = now - start;

			if (elapsed < anticipateMs) {
				const u = elapsed / anticipateMs;
				pose = 'idle';
				catcherScale = 1 + 0.04 * u;
				catcherRot = 0.04 * u;
			} else if (elapsed < anticipateMs + catchHoldMs) {
				const u = (elapsed - anticipateMs) / catchHoldMs;
				pose = 'catch';
				catcherScale = 1.04 + 0.1 * Math.sin(Math.min(1, u * 1.2) * Math.PI);
				catcherRot = -0.08 * easeOutCubic(Math.min(1, u * 1.5));
			} else {
				const u = Math.min(1, (elapsed - anticipateMs - catchHoldMs) / settleMs);
				pose = u < 0.55 ? 'catch' : 'idle';
				catcherScale = 1.08 - 0.08 * easeOutCubic(u);
				catcherRot = -0.06 * (1 - easeOutCubic(u));
			}

			if (elapsed < total) {
				raf = requestAnimationFrame(tick);
			} else {
				pose = 'idle';
				catcherScale = 1;
				catcherRot = 0;
				catching = false;
				runIdleBreath();
			}
		};
		raf = requestAnimationFrame(tick);
	};

	const runIdleBreath = () => {
		const start = performance.now();
		const loop = (now: number) => {
			if (cancelled || catching) return;
			const t = ((now - start) % 2600) / 2600;
			catcherScale = 1 + 0.02 * Math.sin(t * Math.PI * 2);
			catcherRot = -0.012 * Math.sin(t * Math.PI * 2);
			raf = requestAnimationFrame(loop);
		};
		raf = requestAnimationFrame(loop);
	};

	context.eventEmitter.subscribeOnMount({
		catcherCatch: () => {
			runCatch();
		},
		catcherIdle: () => {
			pose = 'idle';
			catching = false;
		},
	});

	onMount(() => {
		runIdleBreath();
	});

	onDestroy(() => {
		cancelled = true;
		if (raf) cancelAnimationFrame(raf);
	});
</script>

<Container x={baseX} y={baseY} zIndex={2} scale={catcherScale} rotation={catcherRot}>
	<Sprite
		key={spriteKey}
		anchor={{ x: 0.5, y: 0.92 }}
		width={catcherW}
		height={catcherH}
	/>
</Container>
