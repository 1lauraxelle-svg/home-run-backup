/** In-memory wallet for local offline play (shared by wallet API routes). */

const START_BALANCE = 1_000_000_000_000; // 1_000_000 dollars in API units (x1e6)

type Session = {
	balance: number;
	currency: string;
	roundId: number;
};

const sessions = new Map<string, Session>();

export const getSession = (sessionID = 'offline') => {
	let session = sessions.get(sessionID);
	if (!session) {
		session = { balance: START_BALANCE, currency: 'USD', roundId: 1 };
		sessions.set(sessionID, session);
	}
	return session;
};
