import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { getSession } from '../../../lib/offline/session';

export const prerender = false;

export const POST: RequestHandler = async ({ request }) => {
	const body = await request.json().catch(() => ({}));
	const session = getSession(body.sessionID || 'offline');

	return json({
		balance: {
			amount: session.balance,
			currency: session.currency,
		},
		config: {
			gameID: 'home-run',
			minBet: 100000,
			maxBet: 1000000000,
			stepBet: 10000,
			defaultBetLevel: 1000000,
			betLevels: [
				100000, 200000, 500000, 1000000, 2000000, 5000000, 10000000, 20000000, 50000000,
				100000000, 200000000, 500000000, 1000000000,
			],
			betModes: {
				base: { cost: 1, feature: true, buyBonus: false, rtp: 0.96, max_win: 25000 },
				ante: { cost: 1.25, feature: true, buyBonus: false, rtp: 0.96, max_win: 25000 },
				bonus_3: { cost: 100, feature: false, buyBonus: true, rtp: 0.96, max_win: 25000 },
				bonus_4: { cost: 160, feature: false, buyBonus: true, rtp: 0.96, max_win: 25000 },
				bonus: { cost: 200, feature: false, buyBonus: true, rtp: 0.96, max_win: 25000 },
			},
			jurisdiction: {
				socialCasino: false,
				disabledFullscreen: false,
				disabledTurbo: false,
				disabledSuperTurbo: false,
				disabledAutoplay: false,
				disabledSlamstop: false,
				disabledSpacebar: false,
				disabledBuyFeature: false,
				displayNetPosition: false,
				displayRTP: false,
				displaySessionTimer: false,
				minimumRoundDuration: 0,
			},
		},
		status: { statusCode: 'SUCCESS', statusMessage: 'offline ok' },
	});
};
