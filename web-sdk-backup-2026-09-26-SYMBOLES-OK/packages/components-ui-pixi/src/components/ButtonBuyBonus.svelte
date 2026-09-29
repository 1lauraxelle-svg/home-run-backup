<script lang="ts">
	import { Text } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';
	import { stateModal, stateBet, stateBetDerived } from 'state-shared';

	import UiSprite from './UiSprite.svelte';
	import { UI_BASE_SIZE } from '../constants';
	import { getContext } from '../context';
	import { i18nDerived } from '../i18n/i18nDerived';

	const props: Partial<Omit<ButtonProps, 'children'>> = $props();
	const { stateXstateDerived, eventEmitter } = getContext();

	/** Wider / taller gold buy button */
	const sizes = { width: UI_BASE_SIZE * 1.55, height: UI_BASE_SIZE * 1.2 };
	const disabled = $derived(!stateXstateDerived.isIdle());
	const active = $derived(stateBetDerived.activeBetMode()?.type === 'activate');

	const GOLD = 0xe8b84a;
	const GOLD_DEEP = 0xb8860b;
	const GOLD_LIGHT = 0xffe566;
	const BROWN = 0x3a2808;

	const openModal = () => (stateModal.modal = { name: 'buyBonus' });
	const disableActiveBetMode = () => (stateBet.activeBetModeKey = 'BASE');
	const onpress = () => {
		eventEmitter.broadcast({ type: 'soundPressGeneral' });

		if (active) {
			disableActiveBetMode();
		} else {
			openModal();
		}
	};

	const label = $derived(active ? i18nDerived.disable() : i18nDerived.buyBonus());
	const fontSize = $derived(Math.round(sizes.height * 0.28));
</script>

<Button {...props} {sizes} {disabled} {onpress}>
	{#snippet children({ center, hovered, pressed })}
		<UiSprite
			key="buyBonus"
			{...center}
			anchor={0.5}
			width={sizes.width}
			height={sizes.height}
			borderRadius={28}
			backgroundColor={disabled ? 0x888888 : pressed ? GOLD_DEEP : hovered ? GOLD_LIGHT : GOLD}
			borderWidth={active || hovered ? 5 : 3}
			borderColor={disabled ? 0x555555 : 0xfff3c4}
			borderAlpha={0.95}
		/>

		<Text
			{...center}
			anchor={0.5}
			text={label}
			style={{
				align: 'center',
				wordWrap: true,
				wordWrapWidth: sizes.width * 0.88,
				fontFamily: 'Arial Black, Impact, Arial, sans-serif',
				fontWeight: '900',
				fontSize,
				lineHeight: fontSize * 1.1,
				letterSpacing: 1,
				fill: BROWN,
				stroke: { color: '#fff6d0', width: 3 },
			}}
		/>
	{/snippet}
</Button>
