# Home Run — mode offline (dev)

## Lancer

```bash
cd web-sdk-backup-2026-09-26-SYMBOLES-OK
pnpm run dev --filter=home-run
```

Ouvre : **http://localhost:3001/**

(sans params : le jeu injecte automatiquement `sessionID=offline` + mock RGS local)

## Jouer

1. **PRESS TO CONTINUE** sur l’écran de chargement
2. Clique le bouton spin (home plate) ou appuie sur **Espace**
3. Free spins / wins se jouent avec les books locaux

## Technique

- Mock wallet : `/wallet/authenticate`, `/wallet/play`, `/wallet/end-round`
- Books offline : `src/lib/offline/books.json` (échantillon base + bonus)
- Max win config front : **25000x**
