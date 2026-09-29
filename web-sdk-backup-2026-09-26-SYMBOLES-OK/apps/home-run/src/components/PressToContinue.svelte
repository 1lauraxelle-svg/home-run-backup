<script lang="ts">
	import { MainContainer, OnPressFullScreen } from 'components-layout';
	import { OnHotkey } from 'components-shared';
	import { stateUrlDerived } from 'state-shared';
	import { Sprite } from 'pixi-svelte';

	import { getContext } from '../game/context';

	type Props = {
		onpress: () => void;
	};

	const props: Props = $props();
	const context = getContext();

	// Sprite source is 711×351 — keep native aspect; sized to clear feature cards above.
	const PRESS_W = 340;
	const PRESS_H = Math.round((PRESS_W * 351) / 711);
	const BOTTOM_MARGIN = 28;
</script>

<MainContainer alignVertical="bottom">
	<Sprite
		key="pressToContinueText_{stateUrlDerived.lang()}.png"
		width={PRESS_W}
		height={PRESS_H}
		anchor={{ x: 0.5, y: 1 }}
		x={context.stateLayoutDerived.mainLayout().width * 0.5}
		y={context.stateLayoutDerived.mainLayout().height - BOTTOM_MARGIN}
	/>
</MainContainer>
<OnHotkey hotkey="Space" onpress={() => props.onpress()} />
<OnPressFullScreen onpress={() => props.onpress()} />
