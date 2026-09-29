<script lang="ts">
	import type { Snippet } from 'svelte';

	import { Popup } from 'components-shared';
	import { zIndex } from 'constants-shared/zIndex';
	import { stateModal, stateMeta } from 'state-shared';

	import BaseContent from './BaseContent.svelte';
	import BaseScrollable from './BaseScrollable.svelte';
	import BaseTitle from './BaseTitle.svelte';
	import GameRuleSections from './GameRuleSections.svelte';

	type Props = {
		children: Snippet;
	};

	const props: Props = $props();
</script>

{#if stateModal.modal?.name === 'payTable'}
	<Popup zIndex={zIndex.modal} onclose={() => (stateModal.modal = null)}>
		<BaseContent maxWidth="100%">
			<BaseTitle>PAYTABLE</BaseTitle>
			<BaseScrollable type="column">
				<GameRuleSections sections={stateMeta.gameRuleMeta.payTable} />
				{@render props.children()}
			</BaseScrollable>
		</BaseContent>
	</Popup>
{/if}
