<script lang="ts">
	import type { Snippet } from 'svelte';

	import BaseContent from './BaseContent.svelte';
	import BaseScrollable from './BaseScrollable.svelte';

	type Props = {
		maxListLength: number;
		betAmount: Snippet;
		bonusCardsActivate: Snippet;
		bonusCardsBuy: Snippet;
	};

	// maxListLength kept for ModalBuyBonus API compatibility
	const props: Props = $props();
</script>

<!-- Portrait: stack cards vertically + scroll — avoid crushing 3 columns with scale() -->
<BaseContent maxWidth="100%">
	<div class="amount">
		{@render props.betAmount()}
	</div>

	<BaseScrollable type="column">
		<div class="bonuses-wrap">
			{@render props.bonusCardsActivate()}
			{@render props.bonusCardsBuy()}
		</div>
	</BaseScrollable>
</BaseContent>

<style lang="scss">
	.amount {
		display: flex;
		justify-content: center;
		padding: 0.5rem 0 0.25rem;
		flex-shrink: 0;
	}

	.bonuses-wrap {
		display: flex;
		flex-direction: column;
		align-items: stretch;
		gap: 0.75rem;
		width: min(100%, 340px);
		margin: 0 auto;
		padding: 0.25rem 0.75rem 1.5rem;
		box-sizing: border-box;
	}

	.bonuses-wrap :global(.bonus-card-wrap) {
		min-width: 0;
		max-width: none;
		width: 100%;
		padding: 0.85rem 1rem;
		background: rgba(0, 0, 0, 0.72);
		border: 1px solid rgba(255, 255, 255, 0.2);
	}

	.bonuses-wrap :global(.title) {
		font-size: 1.1rem;
		line-height: 1.2;
		font-weight: 700;
	}

	.bonuses-wrap :global(.description) {
		font-size: 0.85rem;
		min-height: 0;
		line-height: 1.25;
	}

	.bonuses-wrap :global(.price) {
		font-size: 1.15rem;
		font-weight: 700;
		margin-top: 0.25rem;
	}
</style>
