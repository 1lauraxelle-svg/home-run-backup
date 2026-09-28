import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const prerender = false;

export const POST: RequestHandler = async ({ request }) => {
	const body = await request.json().catch(() => ({}));
	return json({
		event: body.event ?? '0',
		status: { statusCode: 'SUCCESS', statusMessage: 'offline event' },
	});
};
