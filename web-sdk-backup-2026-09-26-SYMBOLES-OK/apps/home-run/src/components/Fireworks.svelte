<script lang="ts">
	import { onDestroy } from 'svelte';
	import { Container, Graphics } from 'pixi-svelte';
	import type * as PIXI from 'pixi.js';

	import { getContext } from '../game/context';

	type Particle = {
		x: number;
		y: number;
		vx: number;
		vy: number;
		life: number;
		maxLife: number;
		size: number;
		color: number;
		trail: boolean;
	};

	type Rocket = {
		x: number;
		y: number;
		vy: number;
		targetY: number;
		color: number;
		alive: boolean;
	};

	const COLORS = [0xff4d6d, 0xffd166, 0x06d6a0, 0x4cc9f0, 0xf72585, 0xfff3b0, 0xb5179e, 0xffffff];

	const context = getContext();
	const canvas = $derived(context.stateLayoutDerived.canvasSizes());
	const active = $derived(context.stateGame.gameType === 'freegame');

	let particles = $state<Particle[]>([]);
	let rockets = $state<Rocket[]>([]);
	let drawRev = $state(0);
	let raf = 0;
	let last = 0;
	let nextSpawnAt = 0;
	let cancelled = false;

	const spawnRocket = () => {
		const w = canvas.width;
		const h = canvas.height;
		const color = COLORS[(Math.random() * COLORS.length) | 0];
		rockets = [
			...rockets,
			{
				x: w * (0.08 + Math.random() * 0.84),
				y: h * 0.72,
				vy: -(280 + Math.random() * 220),
				targetY: h * (0.06 + Math.random() * 0.28),
				color,
				alive: true,
			},
		].slice(-8);
	};

	const draw = (g: PIXI.Graphics) => {
		drawRev; // dependency
		for (const r of rockets) {
			if (!r.alive) continue;
			g.circle(r.x, r.y, 2.4);
			g.fill({ color: 0xfff6c8, alpha: 0.95 });
			g.circle(r.x, r.y + 8, 1.6);
			g.fill({ color: r.color, alpha: 0.55 });
		}
		for (const p of particles) {
			const t = Math.min(1, p.life / p.maxLife);
			const alpha = (1 - t) * (1 - t);
			const size = p.size * (1 - t * 0.35);
			if (p.trail) {
				g.moveTo(p.x, p.y);
				g.lineTo(p.x - p.vx * 0.035, p.y - p.vy * 0.035);
				g.stroke({ width: size * 0.7, color: p.color, alpha: alpha * 0.45 });
			}
			g.circle(p.x, p.y, size);
			g.fill({ color: p.color, alpha });
		}
	};

	$effect(() => {
		cancelled = true;
		if (raf) cancelAnimationFrame(raf);
		particles = [];
		rockets = [];
		drawRev++;

		if (!active) return;

		cancelled = false;
		last = performance.now();
		nextSpawnAt = last + 200;

		const tick = (now: number) => {
			if (cancelled) return;
			const dt = Math.min(0.05, (now - last) / 1000);
			last = now;

			if (now >= nextSpawnAt) {
				spawnRocket();
				nextSpawnAt = now + 550 + Math.random() * 900;
			}

			const gravity = 160;
			const drag = 0.985;
			const newBursts: Particle[] = [];

			const nextRockets: Rocket[] = [];
			for (const r of rockets) {
				if (!r.alive) continue;
				const y = r.y + r.vy * dt;
				const vy = r.vy + 40 * dt;
				if (y <= r.targetY || vy >= -20) {
					const color = r.color;
					const bx = r.x;
					const by = Math.min(y, r.targetY);
					for (let i = 0; i < 42; i++) {
						const angle = (Math.PI * 2 * i) / 42 + Math.random() * 0.2;
						const speed = 80 + Math.random() * 220;
						newBursts.push({
							x: bx,
							y: by,
							vx: Math.cos(angle) * speed,
							vy: Math.sin(angle) * speed,
							life: 0,
							maxLife: 0.7 + Math.random() * 0.9,
							size: 1.5 + Math.random() * 2.8,
							color: Math.random() > 0.25 ? color : COLORS[(Math.random() * COLORS.length) | 0],
							trail: Math.random() > 0.55,
						});
					}
					for (let i = 0; i < 18; i++) {
						const angle = Math.random() * Math.PI * 2;
						const speed = 40 + Math.random() * 90;
						newBursts.push({
							x: bx,
							y: by,
							vx: Math.cos(angle) * speed,
							vy: Math.sin(angle) * speed,
							life: 0,
							maxLife: 0.4 + Math.random() * 0.5,
							size: 1 + Math.random() * 1.6,
							color: 0xffffff,
							trail: false,
						});
					}
					continue;
				}
				nextRockets.push({ ...r, y, vy });
			}
			rockets = nextRockets;

			particles = [...particles, ...newBursts]
				.map((p) => ({
					...p,
					life: p.life + dt,
					x: p.x + p.vx * dt,
					y: p.y + p.vy * dt,
					vx: p.vx * drag,
					vy: p.vy * drag + gravity * dt,
				}))
				.filter((p) => p.life < p.maxLife)
				.slice(-280);

			drawRev++;
			raf = requestAnimationFrame(tick);
		};
		raf = requestAnimationFrame(tick);

		return () => {
			cancelled = true;
			if (raf) cancelAnimationFrame(raf);
		};
	});

	onDestroy(() => {
		cancelled = true;
		if (raf) cancelAnimationFrame(raf);
	});
</script>

{#if active}
	<Container zIndex={0}>
		<Graphics {draw} />
	</Container>
{/if}
