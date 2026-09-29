<script lang="ts">
	import type { Snippet } from 'svelte';

	type Element = null | HTMLDivElement;

	type Props = {
		type: 'column' | 'row';
		noScroll?: boolean;
		children: Snippet<[{ element: Element }]>;
	};

	let element = $state(null as Element);

	const props: Props = $props();
</script>

<div
	bind:this={element}
	class="content {props.type}"
	class:scrollX={!props.noScroll && props.type === 'row'}
	class:scrollY={!props.noScroll && props.type === 'column'}
>
	{@render props.children({ element })}
</div>

<style lang="scss">
	.content {
		position: relative;
		text-align: center;
		display: flex;
		gap: 1rem;
		width: 100%;
		min-height: 0;
		min-width: 0;
		box-sizing: border-box;

		&.column {
			flex-direction: column;
			align-items: center;
			flex: 1 1 auto;
			/* Parent BaseContent caps height → this fills remaining space and scrolls */
			max-height: 100%;
			overflow-y: auto;
			overflow-x: hidden;
			padding: 0 0.5rem 0.5rem;
			overscroll-behavior: contain;
		}

		&.row {
			flex-direction: row;
			justify-content: center;
			max-width: 100%;
			overflow-x: auto;
			overflow-y: hidden;
			padding-bottom: 0.5rem;
		}
	}
</style>
