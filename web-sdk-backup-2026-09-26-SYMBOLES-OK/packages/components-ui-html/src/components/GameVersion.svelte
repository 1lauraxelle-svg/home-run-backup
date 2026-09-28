<script lang="ts">
	import { PUBLIC_SITE_MODE } from 'envs';

	type Props = {
		version: string; // "major.feature.patch"
		studio?: string;
	};

	const props: Props = $props();
</script>

{#if props.studio}
	<span class="studio">{props.studio}</span>
{/if}
{PUBLIC_SITE_MODE}
{props.version}

<style>
	.studio {
		display: block;
		opacity: 0.85;
		font-weight: 600;
		letter-spacing: 0.02em;
	}
</style>
