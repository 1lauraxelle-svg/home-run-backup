"""Simulate natural weighted spins from Studio LUTs until MAX WIN (25000x)."""
from __future__ import annotations

import csv
import random
import time
from pathlib import Path

BASE = Path(r"C:\Users\francis1\Desktop\home-run-MATHS-POUR-STUDIO")
MODES = {
    "base": 1.0,
    "ante": 1.25,
    "bonus_3": 100.0,
    "bonus_4": 160.0,
    "bonus": 200.0,
}
MAX_PAYOUT = 2_500_000  # 25000.00x in LUT hundredths
SEED = int(time.time())
rng = random.Random(SEED)


def load_lut(mode: str):
    path = BASE / f"lookUpTable_{mode}_0.csv"
    idx, weights, pays = [], [], []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) < 3:
                continue
            try:
                i = int(float(row[0]))
                w = float(row[1])
                p = float(row[2])
            except ValueError:
                continue
            if w <= 0:
                continue
            idx.append(i)
            weights.append(w)
            pays.append(p)
    return idx, weights, pays


def main() -> None:
    print(f"seed={SEED}")
    print("Natural LUT sim until MAX WIN x25000 (no forced book)")
    print()

    luts = {}
    probs = {}
    for mode in MODES:
        idx, w, pay = load_lut(mode)
        total_w = sum(w)
        max_w = sum(ww for ww, pp in zip(w, pay) if pp >= MAX_PAYOUT)
        p = max_w / total_w
        max_ids = [i for i, pp in zip(idx, pay) if pp >= MAX_PAYOUT]
        max_weights = [ww for ww, pp in zip(w, pay) if pp >= MAX_PAYOUT]
        max_pays = [pp for pp in pay if pp >= MAX_PAYOUT]
        luts[mode] = (idx, w, pay, max_ids, max_weights, max_pays)
        probs[mode] = p
        print(
            f"{mode:8s}  P(max)={p:.6e}  E[spins]={1 / p:,.0f}  maxwin_books={len(max_ids)}"
        )

    print()
    print("--- Draws ---")

    def sample_loop(mode: str):
        import bisect

        idx, w, pay, *_ = luts[mode]
        cum = []
        s = 0.0
        for ww in w:
            s += ww
            cum.append(s)
        total = cum[-1]
        t0 = time.time()
        for n in range(1, 50_000_001):
            r = rng.random() * total
            i = bisect.bisect_left(cum, r)
            if i >= len(idx):
                i = len(idx) - 1
            if pay[i] >= MAX_PAYOUT:
                return n, idx[i], pay[i] / 100.0, time.time() - t0, "loop"
        raise RuntimeError(f"no maxwin in {mode}")

    def sample_geometric(mode: str):
        """Waiting time ~ Geometric(p); same distribution as spin-by-spin."""
        import math

        _, _, _, max_ids, max_weights, max_pays = luts[mode]
        p = probs[mode]
        t0 = time.time()
        # trials until first success (support starts at 1)
        n = max(1, math.ceil(math.log(1.0 - rng.random()) / math.log(1.0 - p)))
        j = rng.choices(range(len(max_ids)), weights=max_weights, k=1)[0]
        return n, max_ids[j], max_pays[j] / 100.0, time.time() - t0, "geometric"

    # Buy bonus: real weighted loop (P ~ 1e-5..1e-6)
    for mode in ("bonus", "bonus_4", "bonus_3"):
        n, book_id, mult, dt, how = sample_loop(mode)
        print(
            f"{mode:8s} [BUY BONUS ]  MAX WIN after {n:>12,} spins  "
            f"| book {book_id} | {mult:.0f}x | {dt:.1f}s ({how})"
        )

    # Base / ante: geometric (P ~ 4e-8 — loop would take hours)
    for mode, label in (("base", "BASE GAME"), ("ante", "ANTE")):
        n, book_id, mult, dt, how = sample_geometric(mode)
        print(
            f"{mode:8s} [{label:10s}]  MAX WIN after {n:>12,} spins  "
            f"| book {book_id} | {mult:.0f}x | equiv {how}"
        )

    print()
    print("Note: base/ante use Geometric(P) = same odds as spin-by-spin.")
    print("Buy bonus = real LUT draw loop.")


if __name__ == "__main__":
    main()
