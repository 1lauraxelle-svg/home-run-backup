import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { getSession } from '../../../lib/offline/session';

export const prerender = false;

export const POST: RequestHandler = async ({ request }) => {
	const body = await request.json().catch(() => ({}));
	const session = getSession(body.sessionID || 'offline') as any;

	if (typeof session._pendingPayout === 'number') {
		session.balance += session._pendingPayout;
		session._pendingPayout = 0;
	}

	return json({
		balance: {
			amount: session.balance,
			currency: session.currency,
		},
		status: { statusCode: 'SUCCESS', statusMessage: 'offline end-round' },
	});
};
