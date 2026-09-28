import _ from 'lodash';

import type { RawSymbol, SymbolState } from './types';

export const SYMBOL_SIZE = 120;

export const REEL_PADDING = 0.53;

// Showcase board: every symbol visible (rows 1–3), pads top/bottom.
// Layout (visible): H1 H4 L2 L5 H1 / H2 H5 L3 W L1 / H3 L1 L4 S W
export const INITIAL_BOARD: RawSymbol[][] = [
	[{ name: 'H1' }, { name: 'W', multiplier: 2 }, { name: 'L2' }, { name: 'H3' }, { name: 'H1' }],
	[{ name: 'H4' }, { name: 'W', multiplier: 4 }, { name: 'L1' }, { name: 'H5' }, { name: 'H4' }],
	[{ name: 'L3' }, { name: 'W', multiplier: 5 }, { name: 'L4' }, { name: 'L2' }, { name: 'L3' }],
	[{ name: 'L5' }, { name: 'W', multiplier: 7 }, { name: 'S' }, { name: 'H2' }, { name: 'L5' }],
	[{ name: 'S' }, { name: 'W', multiplier: 10 }, { name: 'H1' }, { name: 'L4' }, { name: 'S' }],
];

export const BOARD_DIMENSIONS = { x: INITIAL_BOARD.length, y: INITIAL_BOARD[0].length - 2 };

export const BOARD_SIZES = {
	width: SYMBOL_SIZE * BOARD_DIMENSIONS.x,
	height: SYMBOL_SIZE * BOARD_DIMENSIONS.y,
};

export const BACKGROUND_RATIO = 2039 / 1000;
export const PORTRAIT_BACKGROUND_RATIO = 1242 / 2208;
const PORTRAIT_RATIO = 800 / 1422;
const LANDSCAPE_RATIO = 1600 / 900;
const DESKTOP_RATIO = 1422 / 800;

const DESKTOP_HEIGHT = 800;
const LANDSCAPE_HEIGHT = 900;
const PORTRAIT_HEIGHT = 1422;
export const DESKTOP_MAIN_SIZES = { width: DESKTOP_HEIGHT * DESKTOP_RATIO, height: DESKTOP_HEIGHT };
export const LANDSCAPE_MAIN_SIZES = {
	width: LANDSCAPE_HEIGHT * LANDSCAPE_RATIO,
	height: LANDSCAPE_HEIGHT,
};
export const PORTRAIT_MAIN_SIZES = {
	width: PORTRAIT_HEIGHT * PORTRAIT_RATIO,
	height: PORTRAIT_HEIGHT,
};

export const HIGH_SYMBOLS = ['H1', 'H2', 'H3', 'H4', 'H5'];

export const INITIAL_SYMBOL_STATE: SymbolState = 'static';

const SPIN_OPTIONS_SHARED = {
	reelBounceBackSpeed: 0.15,
	reelSpinSpeedBeforeBounce: 4,
	reelPaddingMultiplierNormal: 1.2,
	reelPaddingMultiplierAnticipated: 10,
	reelSpinDelay: 145,
};

export const SPIN_OPTIONS_DEFAULT = {
	...SPIN_OPTIONS_SHARED,
	reelPreSpinSpeed: 2,
	reelSpinSpeed: 3,
	reelBounceSizeMulti: 0.3,
};

export const SPIN_OPTIONS_FAST = {
	...SPIN_OPTIONS_SHARED,
	reelPreSpinSpeed: 5,
	reelSpinSpeed: 5,
	reelBounceSizeMulti: 0.05,
};

export const MOTION_BLUR_VELOCITY = 31;

export const zIndexes = {
	background: {
		backdrop: -3,
		normal: -2,
		feature: -1,
	},
};

const explosion = {
	type: 'spine',
	assetKey: 'explosion',
	animationName: 'explosion',
	sizeRatios: { width: 1, height: 1 },
};

const h1Static = { type: 'sprite', assetKey: 'h1.webp', sizeRatios: { width: 1, height: 1 } };
const h2Static = { type: 'sprite', assetKey: 'h2.webp', sizeRatios: { width: 1, height: 1 } };
const h3Static = { type: 'sprite', assetKey: 'h3.webp', sizeRatios: { width: 1, height: 1 } };
const h4Static = { type: 'sprite', assetKey: 'h4.webp', sizeRatios: { width: 1, height: 1 } };
const h5Static = { type: 'sprite', assetKey: 'h5.webp', sizeRatios: { width: 1, height: 1 } };

const l1Static = { type: 'sprite', assetKey: 'l1.webp', sizeRatios: { width: 1, height: 1 } };
const l2Static = { type: 'sprite', assetKey: 'l2.webp', sizeRatios: { width: 1, height: 1 } };
const l3Static = { type: 'sprite', assetKey: 'l3.webp', sizeRatios: { width: 1, height: 1 } };
const l4Static = { type: 'sprite', assetKey: 'l4.webp', sizeRatios: { width: 1, height: 1 } };
const l5Static = {
	type: 'sprite',
	assetKey: 'm1_2x.png',
	sizeRatios: { width: 1, height: 1 },
};

const sStatic = { type: 'sprite', assetKey: 's.png', sizeRatios: { width: 1.243, height: 1.243 } };
const wStatic = { type: 'sprite', assetKey: 'w.png', sizeRatios: { width: 1.12, height: 1.12 } };

/** Dedicated baseball multiplier art (atlas frames). */
export const MULTIPLIER_ASSET_KEYS: Record<number, string> = {
	2: 'm1_2x.png',
	4: 'm1_4x.png',
	5: 'm2_5x.png',
	7: 'm2_7x.png',
	10: 'm3_10x.png',
};

export const hasMultiplierArt = (multiplier?: number) =>
	typeof multiplier === 'number' && multiplier in MULTIPLIER_ASSET_KEYS;

export const getWildSpriteInfo = (multiplier?: number) => {
	const key = typeof multiplier === 'number' ? MULTIPLIER_ASSET_KEYS[multiplier] : undefined;
	if (key) {
		return { type: 'sprite' as const, assetKey: key, sizeRatios: { width: 1.12, height: 1.12 } };
	}
	return wStatic;
};

// Sprite land/win: pixi bounce + pulse (same punch for every symbol)
const animOf = <T extends { type: string; assetKey: string; sizeRatios: { width: number; height: number } }>(
	base: T,
	bump = 1.18,
) => ({
	...base,
	sizeRatios: {
		width: base.sizeRatios.width * bump,
		height: base.sizeRatios.height * bump,
	},
});

const h1Land = animOf(h1Static);
const h2Land = animOf(h2Static);
const h3Land = animOf(h3Static);
const h4Land = animOf(h4Static);
const h5Land = animOf(h5Static);
const l1Land = animOf(l1Static);
const l2Land = animOf(l2Static);
const l3Land = animOf(l3Static);
const l4Land = animOf(l4Static);
const l5Land = animOf(l5Static);
const wAnim = animOf(wStatic, 1.2);
const sAnim = animOf(sStatic, 1.15);

export const SYMBOL_INFO_MAP = {
	H1: {
		explosion,
		win: h1Land,
		postWinStatic: h1Static,
		static: h1Static,
		spin: h1Static,
		land: h1Land,
	},
	H2: {
		explosion,
		win: h2Land,
		postWinStatic: h2Static,
		static: h2Static,
		spin: h2Static,
		land: h2Land,
	},
	H3: {
		explosion,
		win: h3Land,
		postWinStatic: h3Static,
		static: h3Static,
		spin: h3Static,
		land: h3Land,
	},
	H4: {
		explosion,
		win: h4Land,
		postWinStatic: h4Static,
		static: h4Static,
		spin: h4Static,
		land: h4Land,
	},
	H5: {
		explosion,
		win: h5Land,
		postWinStatic: h5Static,
		static: h5Static,
		spin: h5Static,
		land: h5Land,
	},
	L1: {
		explosion,
		win: l1Land,
		postWinStatic: l1Static,
		static: l1Static,
		spin: l1Static,
		land: l1Land,
	},
	L2: {
		explosion,
		win: l2Land,
		postWinStatic: l2Static,
		static: l2Static,
		spin: l2Static,
		land: l2Land,
	},
	L3: {
		explosion,
		win: l3Land,
		postWinStatic: l3Static,
		static: l3Static,
		spin: l3Static,
		land: l3Land,
	},
	L4: {
		explosion,
		win: l4Land,
		postWinStatic: l4Static,
		static: l4Static,
		spin: l4Static,
		land: l4Land,
	},
	L5: {
		explosion,
		win: l5Land,
		postWinStatic: l5Static,
		static: l5Static,
		spin: l5Static,
		land: l5Land,
	},
	W: {
		explosion,
		postWinStatic: {
			type: 'sprite',
			assetKey: 'explodedW.png',
			sizeRatios: { width: 0.85, height: 0.85 },
		},
		static: wStatic,
		spin: wStatic,
		win: wAnim,
		land: wAnim,
	},
	S: {
		explosion,
		postWinStatic: sStatic,
		static: sStatic,
		spin: sStatic,
		win: sAnim,
		land: sAnim,
	},
} as const;

export const SCATTER_LAND_SOUND_MAP = {
	1: 'sfx_scatter_stop_1',
	2: 'sfx_scatter_stop_2',
	3: 'sfx_scatter_stop_3',
	4: 'sfx_scatter_stop_4',
	5: 'sfx_scatter_stop_5',
} as const;
