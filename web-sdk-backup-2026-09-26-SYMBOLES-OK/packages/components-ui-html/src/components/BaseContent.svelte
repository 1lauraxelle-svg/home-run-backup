<script lang="ts">
	import type { Snippet } from 'svelte';

	type Props = {
		maxWidth: '100%' | '500px';
		children: Snippet;
	};

	const props: Props = $props();
</script>

<div class="ui-popup-standard-content-wrap" style="--maxWidth: {props.maxWidth}; --zIndex: {100}">
	{@render props.children()}
</div>

<style lang="scss">
	.ui-popup-standard-content-wrap {
		display: flex;
		flex-direction: column;
		justify-content: flex-start;
		align-items: stretch;
		z-index: var(--zIndex);
		position: relative;
		width: min(960px, 94vw);
		max-width: var(--maxWidth);
		max-height: min(88vh, 920px);
		min-height: 0;
		gap: 0.75rem;
		padding: 0.75rem 0.25rem 1rem;
		box-sizing: border-box;
		overflow: hidden;
	}

	.ui-popup-standard-content-wrap :global(.ui-modal-title-wrap) {
		flex: 0 0 auto;
		text-align: center;
		padding: 0 2.5rem;
	}
</style>
