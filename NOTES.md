\# HOME RUN — Documentation du Math SDK



\## Statut : ✅ Terminé et validé



\## Description du jeu

Jeu de type "crash" (style Aviator/Bustabit) avec 26 modes de mise

différents (targets et secures variés).



\## Formule du gain (doc §2)



À chaque manche :

1\. Tirage du crash : `\_draw\_crash()` avec la loi P(C >= x) = RTP / x

&#x20;  - Si `random() < 0.035` → crash = 1.00 (perte)

&#x20;  - Sinon → crash = 0.965 / random()



2\. Lecture du mode courant (`BetMode`) :

&#x20;  - `mode = self.get\_current\_betmode()`

&#x20;  - `mode\_name = mode.get\_name()` (ex: "t500\_s50")

&#x20;  - Extraction : `target` et `secure` depuis le nom



3\. Calcul du gain :

&#x20;  - Si `secure > 0` et `crash >= 2.00` : win += `secure \* 2.00`

&#x20;  - Si `crash >= target` : win += `(1 - secure) \* target`

&#x20;  - Plafond : `min(win, mode.get\_wincap())` (25000 par défaut)



\## Modes générés (26)



| Groupe | Cibles | Secure |

|---|---|---|

| TARGETS\_OFF | 1.40, 1.50, 1.60, 1.70, 1.80, 1.90, 2.00, 2.20, 2.50, 3.00 | 0.0 |

| TARGETS\_50 | 3.00, 4.00, 5.00, 6.00, 8.00, 10.00, 12.00, 15.00, 20.00 | 0.5 |

| TARGETS\_90 | 1000.00, 1500.00, 2000.00, 2500.00, 5000.00, 7500.00 | 0.9 |

| base | (mode bidon pour le SDK) | 0.0 |



Total : 10 + 9 + 6 + 1 = \*\*26 modes\*\*



\## Fichiers modifiés



\### 1. `games/home-run/run.py`

Ajout de 3 lignes `sys.path.insert` en haut du fichier pour que

les imports `from src.xxx` fonctionnent quand on lance le script

directement.



\### 2. `games/home-run/game\_calculations.py`

Ajout des mêmes 3 lignes `sys.path.insert` pour contourner

l'import circulaire entre `game\_calculations` et `src.executables`.



\### 3. `games/home-run/gamestate.py`

\- Remplacement du placeholder (`target=2.00`, `secure=0.0` en dur)

&#x20; par la vraie formule du doc §2.

\- Changement de `self.get\_current\_betmode\_distributions()` (retourne

&#x20; une `Distribution`) par `self.get\_current\_betmode()` (retourne un

&#x20; `BetMode` avec `get\_name()`).

\- Changement de `self.wincap` (n'existe pas) par `mode.get\_wincap()`.



\## Résultat des tests



\- ✅ 26 LUT générées, une par mode

\- ✅ LUT distinctes (tailles différentes selon target/secure)

\- ✅ Configs JSON cohérentes (target/secure/gain corrects)

\- ✅ Formule à 2 termes validée :

&#x20; - Mode `t500\_s0` : gain = 5.00 pour crash ≥ 5.00

&#x20; - Mode `t500\_s50` : gain = 3.50 pour crash ≥ 5.00 (secure + target)

\- ✅ RTP global attendu : \~0.965



\## Sauvegarde

\- Commit Git : `0abc456` (branche `main`)

\- Dossier `library/` gitignoré (régénérable)



\## Prochaine étape

Développement du Frontend (PixiJS/Svelte) — projet Node.js séparé.

