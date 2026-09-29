<script lang="ts">
	import type { GameRuleData } from 'state-shared';

	type Props = {
		sections: GameRuleData[];
	};

	const props: Props = $props();
</script>

{#each props.sections as section}
	<section class="rule-section">
		<h2 class="rule-section-title">{section.title}</h2>
		<div
			class="rule-grid"
			style="--cols: {section.columns}; --rows: {section.rows};"
		>
			{#each section.containers as cell}
				<article
					class="rule-card"
					style="grid-row: {cell.row + 1}; grid-column: {cell.column + 1};"
				>
					{#if cell.title}
						<h3 class="rule-card-title">{cell.title}</h3>
					{/if}
					<p class="rule-card-text">{cell.text}</p>
				</article>
			{/each}
		</div>
	</section>
{/each}

<style lang="scss">
	.rule-section {
		width: min(920px, 92vw);
		display: flex;
		flex-direction: column;
		gap: 0.75rem;
		margin-bottom: 1.25rem;
		text-align: left;
	}

	.rule-section-title {
		margin: 0;
		font-family: 'Arial Black', Arial, sans-serif;
		font-size: 1.15rem;
		letter-spacing: 0.04em;
		color: #ffe566;
		text-align: center;
	}

	.rule-grid {
		display: grid;
		grid-template-columns: repeat(var(--cols), minmax(0, 1fr));
		gap: 0.65rem;
	}

	.rule-card {
		background: rgba(18, 14, 12, 0.92);
		border: 1.5px solid #3a3028;
		border-radius: 12px;
		padding: 0.85rem 0.95rem;
		color: #f2ebe3;
	}

	.rule-card-title {
		margin: 0 0 0.4rem;
		font-family: Arial, sans-serif;
		font-size: 0.95rem;
		font-weight: 800;
		letter-spacing: 0.03em;
		color: #ffd700;
	}

	.rule-card-text {
		margin: 0;
		font-family: Arial, sans-serif;
		font-size: 0.88rem;
		line-height: 1.45;
		white-space: pre-line;
		color: #e8e0d8;
	}

	@media (max-width: 640px) {
		.rule-grid {
			grid-template-columns: 1fr;
		}

		.rule-card {
			grid-column: 1 !important;
			grid-row: auto !important;
		}
	}
</style>
