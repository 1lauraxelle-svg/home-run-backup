import books from './books.json';
import maxWinBookRaw from './maxwin_book.json';

type OfflineBook = {
	id: number;
	payoutMultiplier: number;
	events: unknown[];
	criteria?: string;
};

const pools = books as { base: OfflineBook[]; bonus: OfflineBook[] };

/**
 * Real math max-win book (id 121): base → free spins → wincap 25000x.
 * Math stores payoutMultiplier in hundredths (2500000 = 25000x).
 */
const MAX_WIN_BOOK: OfflineBook = {
	...(maxWinBookRaw as OfflineBook),
	payoutMultiplier: (maxWinBookRaw as OfflineBook).payoutMultiplier / 100,
};

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

/** Force next base spin(s) to the real max-win book (for QA). */
const FORCE_MAX_WIN = false;
/** Set false to restore random offline books. */
const FORCE_SHOWCASE = false;

export const pickBook = (mode: string) => {
	const isBonus = mode?.toLowerCase().includes('bonus');
	if (FORCE_MAX_WIN && !isBonus) {
		return MAX_WIN_BOOK;
	}
	if (FORCE_SHOWCASE && !isBonus) {
		return SHOWCASE_BOOK;
	}
	const key = isBonus ? 'bonus' : 'base';
	const pool = pools[key];
	const book = pool[Math.floor(Math.random() * pool.length)];
	return book;
};
