<script lang="ts">
	import { Text } from 'pixi-svelte';
	import { Button, type ButtonProps } from 'components-pixi';

	import UiSprite from './UiSprite.svelte';
	import type { ButtonIcon } from '../types';
	import type { Snippet } from 'svelte';
	import { i18nDerived } from '../i18n/i18nDerived';

	/** Icon glyphs for compact HUD (match reference bar). */
	const ICON_GLYPH: Partial<Record<ButtonIcon, string>> = {
		turbo: '⚡',
		menu: '☰',
		autoSpin: '⟳',
		increase: '▲',
		decrease: '▼',
		menuExit: '✕',
	};

	type Props = Omit<ButtonProps, 'children'> & {
		icon: ButtonIcon;
		sizes: { width: number; height: number };
		active?: boolean;
		children?: Snippet;
		variant?: 'dark' | 'light';
		/** Prefer symbol over text label (compact bar). */
		glyph?: boolean;
	};

	const {
		icon,
		active,
		variant = 'dark',
		glyph = true,
		children: childrenFromParent,
		...buttonProps
	}: Props = $props();

	const label = $derived(
		glyph && ICON_GLYPH[icon] ? ICON_GLYPH[icon]! : i18nDerived[icon](),
	);
	const fontSize = $derived(
		glyph && ICON_GLYPH[icon]
			? Math.round(buttonProps.sizes.height * 0.42)
			: Math.round(Math.min(buttonProps.sizes.height * 0.2, 28)),
	);
	const wrapWidth = $derived(Math.round(buttonProps.sizes.width * 0.82));
</script>

<Button {...buttonProps}>
	{#snippet children({ center, hovered, pressed })}
		<UiSprite
			{...center}
			anchor={0.5}
			width={buttonProps.sizes.width}
			height={buttonProps.sizes.height}
			backgroundColor={variant === 'dark' ? 0x0d0d0d : 0xffffff}
			borderWidth={glyph && ICON_GLYPH[icon] ? 4 : 0}
			borderColor={0xffffff}
			borderAlpha={glyph && ICON_GLYPH[icon] ? 0.85 : 0}
			{...buttonProps.disabled
				? {
						backgroundColor: 0x666666,
					}
				: {}}
			{...active
				? {
						borderWidth: 8,
						borderColor: variant === 'dark' ? 0xffffff : 0x000000,
						borderAlpha: 1,
					}
				: {}}
		/>

		<Text
			{...center}
			anchor={0.5}
			text={label}
			style={{
				align: 'center',
				wordWrap: true,
				wordWrapWidth: wrapWidth,
				fontFamily: 'Arial Black, Arial, sans-serif',
				fontWeight: '700',
				fontSize,
				lineHeight: fontSize * 1.15,
				fill: variant === 'dark' ? 0xffffff : 0x111111,
			}}
		/>

		{@render childrenFromParent?.()}
	{/snippet}
</Button>
