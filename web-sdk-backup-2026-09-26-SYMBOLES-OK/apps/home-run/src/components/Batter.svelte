<script lang="ts" module>
	export type EmitterEventBatter =
		| { type: 'batterSwing' }
		| { type: 'batterIdle' };
</script>

<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { Container, Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';
	import { eventEmitter } from '../game/eventEmitter';
	import { SYMBOL_SIZE } from '../game/constants';

	const context = getContext();

	type Pose = 'idle' | 'swing';

	let pose = $state<Pose>('idle');
	let ballVisible = $state(false);
	let ballX = $state(0);
	let ballY = $state(0);
	let ballScale = $state(0.7);
	let batterScale = $state(1);
	let batterRot = $state(0);

	let raf = 0;
	let cancelled = false;
	let swinging = false;
	let nextAutoSwingAt = 0;
	let catcherNotified = false;

	const board = $derived(context.stateGameDerived.boardLayout());
	const batterH = $derived(board.height * 1.15);
	const batterW = $derived(batterH * 0.65);
	const baseX = $derived(board.x + board.width * 0.5 + batterW * 0.35 + SYMBOL_SIZE * 0.15);
	// Feet on the white chalk marks near home plate
	const baseY = $derived(board.y + board.height * 0.55);

	const spriteKey = $derived(pose === 'swing' ? 'batterSwing' : 'batterIdle');

	const easeOutCubic = (t: number) => 1 - Math.pow(1 - t, 3);

	const runSwing = () => {
		if (cancelled || swinging) return;
		swinging = true;
		catcherNotified = false;
		pose = 'swing';
		ballVisible = true;
		batterScale = 1.05;
		batterRot = -0.08;
		eventEmitter.broadcast({ type: 'soundOnce', name: 'sfx_bat_hit' });

		const start = performance.now();
		const duration = 900;
		// Ball leaves the bat toward the catcher (left side of the board)
		const startX = -batterW * 0.15;
		const startY = -batterH * 0.28;
		const endX = -board.width * 1.15 - batterW * 0.2;
		const endY = -board.height * 0.08;

		const tick = (now: number) => {
			if (cancelled) return;
			const t = Math.min(1, (now - start) / duration);

			if (t < 0.16) {
				const u = t / 0.16;
				batterScale = 1.05 + 0.1 * Math.sin(u * Math.PI);
				batterRot = -0.08 - 0.14 * u;
			} else {
				const u = (t - 0.16) / 0.84;
				batterScale = 1.05 - 0.05 * easeOutCubic(u);
				batterRot = -0.22 * (1 - easeOutCubic(Math.min(1, u * 1.4)));
			}

			// Contact ~12% in — notify catcher so he can time the mitt
			if (!catcherNotified && t >= 0.12) {
				catcherNotified = true;
				eventEmitter.broadcast({ type: 'catcherCatch' });
			}

			const fly = easeOutCubic(Math.min(1, Math.max(0, (t - 0.1) / 0.72)));
			ballX = startX + (endX - startX) * fly;
			ballY = startY + (endY - startY) * fly - Math.sin(fly * Math.PI) * board.height * 0.28;
			ballScale = 0.8 + 0.15 * fly;
			ballVisible = fly < 0.98;

			if (t < 1) {
				raf = requestAnimationFrame(tick);
			} else {
				ballVisible = false;
				pose = 'idle';
				batterScale = 1;
				batterRot = 0;
				swinging = false;
				nextAutoSwingAt = performance.now() + 6500;
				runIdleBreath();
			}
		};
		raf = requestAnimationFrame(tick);
	};

	const runIdleBreath = () => {
		const start = performance.now();
		nextAutoSwingAt = start + 6500;
		const loop = (now: number) => {
			if (cancelled || swinging) return;
			const t = ((now - start) % 2400) / 2400;
			batterScale = 1 + 0.018 * Math.sin(t * Math.PI * 2);
			batterRot = 0.015 * Math.sin(t * Math.PI * 2);
			if (now >= nextAutoSwingAt) {
				runSwing();
				return;
			}
			raf = requestAnimationFrame(loop);
		};
		raf = requestAnimationFrame(loop);
	};

	context.eventEmitter.subscribeOnMount({
		batterSwing: () => {
			runSwing();
		},
		batterIdle: () => {
			pose = 'idle';
			ballVisible = false;
			swinging = false;
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

<Container x={baseX} y={baseY} zIndex={2} scale={batterScale} rotation={batterRot}>
	<Sprite
		key={spriteKey}
		anchor={{ x: 0.5, y: 0.92 }}
		width={batterW}
		height={batterH}
	/>
	{#if ballVisible}
		<Sprite
			key="batterBall"
			anchor={0.5}
			x={ballX}
			y={ballY - batterH * 0.35}
			width={SYMBOL_SIZE * 0.45 * ballScale}
			height={SYMBOL_SIZE * 0.45 * ballScale}
		/>
	{/if}
</Container>
