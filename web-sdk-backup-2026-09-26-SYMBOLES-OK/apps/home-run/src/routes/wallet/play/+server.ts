import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { getSession } from '../../../lib/offline/session';
import { pickBook } from '../../../lib/offline/pickBook';

export const prerender = false;

export const POST: RequestHandler = async ({ request }) => {
	const body = await request.json().catch(() => ({}));
	const session = getSession(body.sessionID || 'offline');
	const amount = Number(body.amount) || 1_000_000;
	const mode = String(body.mode || 'base');

	if (session.balance < amount) {
		return json({
			error: { message: 'Insufficient balance' },
			status: { statusCode: 'ERR_IPB', statusMessage: 'Insufficient Player Balance' },
		});
	}

	session.balance -= amount;
	const book = pickBook(mode);
	const payout = Math.round(amount * book.payoutMultiplier);
	const active = book.events.some((e: any) => e?.type === 'freeSpinTrigger');

	// Credit wins immediately for offline play (end-round still returns balance).
	if (!active) {
		session.balance += payout;
	} else {
		// Hold payout until end-round for bonus-style rounds.
		(session as any)._pendingPayout = payout;
	}

	const roundId = session.roundId++;

	return json({
		balance: {
			amount: session.balance,
			currency: session.currency,
		},
		round: {
			betID: roundId,
			roundID: roundId,
			amount,
			payout,
			payoutMultiplier: book.payoutMultiplier,
			active,
			mode,
			event: null,
			state: book.events,
		},
		status: { statusCode: 'SUCCESS', statusMessage: 'offline play' },
	});
};
