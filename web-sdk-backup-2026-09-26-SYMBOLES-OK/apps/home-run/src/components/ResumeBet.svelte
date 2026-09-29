<script lang="ts">
	import { tick, onMount } from 'svelte';
	import { stateBet } from 'state-shared';

	import { getContext } from '../game/context';

	const context = getContext();

	onMount(async () => {
		// Wait until Board / Win / UI listeners are subscribed.
		await tick();
		await tick();

		const betToResume = stateBet.betToResume;
		if (!betToResume) return;

		if (betToResume.active && betToResume.mode) {
			stateBet.activeBetModeKey = betToResume.mode;
		}

		context.eventEmitter.broadcast({ type: 'resumeBet' });
	});
</script>
