import books from './books.json';

type OfflineBook = {
	id: number;
	payoutMultiplier: number;
	events: unknown[];
	criteria?: string;
};

const pools = books as { base: OfflineBook[]; bonus: OfflineBook[] };

/**
 * Showcase: baseball multiplier wilds x2 / x4 / x5 / x7 / x10 on the 5×3.
 * (Each reel: pad / visible×3 / pad)
 */
const SHOWCASE_BOOK: OfflineBook = {
	id: 0,
	payoutMultiplier: 0,
	criteria: 'showcase',
	events: [
		{
			index: 0,
			type: 'reveal',
			board: [
				[{ name: 'H1' }, { name: 'W', multiplier: 2 }, { name: 'L2' }, { name: 'H3' }, { name: 'H1' }],
				[{ name: 'H4' }, { name: 'W', multiplier: 4 }, { name: 'L1' }, { name: 'H5' }, { name: 'H4' }],
				[{ name: 'L3' }, { name: 'W', multiplier: 5 }, { name: 'L4' }, { name: 'L2' }, { name: 'L3' }],
				[{ name: 'L5' }, { name: 'W', multiplier: 7 }, { name: 'S' }, { name: 'H2' }, { name: 'L5' }],
				[{ name: 'S' }, { name: 'W', multiplier: 10 }, { name: 'H1' }, { name: 'L4' }, { name: 'S' }],
			],
			paddingPositions: [0, 0, 0, 0, 0],
			gameType: 'basegame',
			anticipation: [0, 0, 0, 0, 0],
		},
		{ index: 1, type: 'setTotalWin', amount: 0 },
		{ index: 2, type: 'finalWin', amount: 0 },
	],
};

/** Set false to restore random offline books. */
const FORCE_SHOWCASE = true;

export const pickBook = (mode: string) => {
	if (FORCE_SHOWCASE && !mode?.toLowerCase().includes('bonus')) {
		return SHOWCASE_BOOK;
	}
	const key = mode?.toLowerCase().includes('bonus') ? 'bonus' : 'base';
	const pool = pools[key];
	const book = pool[Math.floor(Math.random() * pool.length)];
	return book;
};
