"""Clean stadium ads: remove inscriptions, keep panel colors.

Key idea: detect vivid ad panels, dilate to swallow white/dark lettering,
then solid-fill each blob with the panel's background color.
"""
from __future__ import annotations

import cv2
import numpy as np
from pathlib import Path


def bg_from_pixels(pix: np.ndarray) -> np.ndarray:
    """Median BGR of Nx3 pixels, preferring saturated mid-value colors."""
    pix = pix.reshape(-1, 3).astype(np.float32)
    if len(pix) == 0:
        return np.zeros(3, dtype=np.uint8)
    u8 = pix.reshape(-1, 1, 3).astype(np.uint8)
    hsv = cv2.cvtColor(u8, cv2.COLOR_BGR2HSV).reshape(-1, 3)
    S, V = hsv[:, 1], hsv[:, 2]
    good = (S > 50) & (V > 50) & (V < 230)
    if int(good.sum()) < 20:
        good = (V > 40) & (V < 240)
    sample = pix[good] if int(good.sum()) >= 10 else pix
    return np.median(sample, axis=0).astype(np.uint8)


def solid_fill_horizontal_panels(
    img: np.ndarray,
    y0: int,
    y1: int,
    x0: int,
    x1: int,
    jump_thr: float = 22.0,
    min_w: int = 16,
    max_w_ratio: float = 0.35,
) -> int:
    h, w = img.shape[:2]
    y0, y1 = max(0, y0), min(h, y1)
    x0, x1 = max(0, x0), min(w, x1)
    strip = img[y0:y1, x0:x1]
    if strip.size == 0:
        return 0
    cols = np.median(strip.astype(np.float32), axis=0)
    d = np.linalg.norm(np.diff(cols, axis=0), axis=1)
    cuts = [0] + [i + 1 for i, v in enumerate(d) if v > jump_thr] + [strip.shape[1]]
    merged = [cuts[0]]
    for c in cuts[1:]:
        if c - merged[-1] >= min_w:
            merged.append(c)
    if merged[-1] != strip.shape[1]:
        merged.append(strip.shape[1])

    max_w = int(strip.shape[1] * max_w_ratio)
    n = 0
    for a, b in zip(merged[:-1], merged[1:]):
        if (b - a) > max_w:
            continue
        panel = strip[:, a:b]
        med = bg_from_pixels(panel)
        strip[:, a:b] = med
        n += 1
    img[y0:y1, x0:x1] = strip
    return n


def fill_ad_blobs(
    img: np.ndarray,
    zone: np.ndarray,
    *,
    min_area: int = 250,
    max_area_frac: float = 0.04,
    max_h: int = 110,
    max_w: int = 550,
    dilate: int = 4,
) -> int:
    """Fill vivid ad blobs including lettering swallowed by dilation."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(hsv)
    grass = (H >= 35) & (H <= 95) & (S > 45) & (V > 70)

    vivid = zone & (S > 65) & (V > 65) & (V < 250) & (~grass)
    ad_hue = (
        (H < 22)
        | (H > 155)
        | ((H >= 5) & (H <= 42) & (S > 80))
        | ((H >= 85) & (H <= 145) & (S > 65))
        | ((H >= 42) & (H <= 85) & (S > 85) & (V < 210))
    )
    core = (vivid & ad_hue).astype(np.uint8) * 255
    core = cv2.morphologyEx(core, cv2.MORPH_CLOSE, np.ones((3, 13), np.uint8))
    core = cv2.morphologyEx(core, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))

    num, labels, stats, _ = cv2.connectedComponentsWithStats(core, 8)
    h, w = img.shape[:2]
    max_area = int(h * w * max_area_frac)
    filled = 0
    k = np.ones((dilate, dilate), np.uint8)

    for i in range(1, num):
        area = stats[i, cv2.CC_STAT_AREA]
        ww = stats[i, cv2.CC_STAT_WIDTH]
        hh = stats[i, cv2.CC_STAT_HEIGHT]
        if area < min_area or area > max_area:
            continue
        if ww < 30 or hh > max_h or ww > max_w:
            continue

        m = (labels == i).astype(np.uint8)
        # Swallow white/dark lettering attached to the panel
        m_big = cv2.dilate(m, k, iterations=1)
        # Only expand into zone + near-white or near-dark (likely text)
        white = ((S < 70) & (V > 175)).astype(np.uint8)
        dark = ((V < 60) & (S < 100)).astype(np.uint8)
        textish = cv2.bitwise_or(white, dark)
        expand = cv2.bitwise_and(m_big, cv2.bitwise_or(m, textish))
        expand = cv2.bitwise_or(m, expand)
        expand = cv2.bitwise_and(expand, zone.astype(np.uint8) * 255)
        expand = cv2.dilate(expand, np.ones((2, 2), np.uint8), iterations=1)

        sel = expand.astype(bool)
        if sel.sum() < 50:
            continue
        med = bg_from_pixels(img[sel])
        img[sel] = med
        filled += 1
    return filled


def solid_fill_color_bands(
    img: np.ndarray,
    zone: np.ndarray,
    hue_lo: int,
    hue_hi: int,
    *,
    wrap: bool = False,
    s_min: int = 90,
    v_min: int = 80,
    dilate: int = 3,
    min_area: int = 180,
    min_aspect: float = 0.0,
) -> int:
    """Solid-fill connected hue bands; only expand into lettering, not crowd."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(hsv)
    if wrap:
        hue = (H <= hue_lo) | (H >= hue_hi)
    else:
        hue = (H >= hue_lo) & (H <= hue_hi)
    core = (zone & hue & (S > s_min) & (V > v_min) & (V < 250)).astype(np.uint8) * 255
    core = cv2.morphologyEx(core, cv2.MORPH_CLOSE, np.ones((3, 11), np.uint8))
    num, labels, stats, _ = cv2.connectedComponentsWithStats(core, 8)
    filled = 0
    white = ((S < 70) & (V > 175)).astype(np.uint8) * 255
    dark = ((V < 55) & (S < 100)).astype(np.uint8) * 255
    textish = cv2.bitwise_or(white, dark)
    for i in range(1, num):
        area = stats[i, cv2.CC_STAT_AREA]
        hh = max(1, stats[i, cv2.CC_STAT_HEIGHT])
        ww = stats[i, cv2.CC_STAT_WIDTH]
        if area < min_area or hh > 90 or ww > 550:
            continue
        if min_aspect > 0 and (ww / hh) < min_aspect and hh > 35:
            continue
        m = (labels == i).astype(np.uint8) * 255
        # expand only a few px, and only onto text-like pixels inside zone
        ring = cv2.dilate(m, np.ones((dilate, dilate), np.uint8), iterations=1)
        expand = cv2.bitwise_and(ring, textish)
        sel = cv2.bitwise_or(m, expand)
        sel = cv2.bitwise_and(sel, zone.astype(np.uint8) * 255)
        sel_b = sel.astype(bool)
        core_sel = labels == i
        med = bg_from_pixels(img[core_sel])
        img[sel_b] = med
        filled += 1
    return filled


def wipe_letters_solid(img: np.ndarray, y0: int, y1: int, x0: int, x1: int) -> None:
    """Replace white/dark letters on saturated panels with local panel median."""
    roi = img[y0:y1, x0:x1]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    S, V = hsv[:, :, 1], hsv[:, :, 2]
    panel = S > 70
    white = (S < 70) & (V > 175)
    dark = (V < 55) & (S < 90)
    near = cv2.dilate(panel.astype(np.uint8), np.ones((11, 11), np.uint8)).astype(bool)
    letters = (white | dark) & near
    if not letters.any():
        return
    u8 = letters.astype(np.uint8) * 255
    u8 = cv2.dilate(u8, np.ones((3, 3), np.uint8), iterations=1)
    num, labels, stats, _ = cv2.connectedComponentsWithStats(u8, 8)
    for i in range(1, num):
        if stats[i, cv2.CC_STAT_AREA] < 8:
            continue
        m = labels == i
        ring = cv2.dilate(m.astype(np.uint8), np.ones((15, 15), np.uint8)).astype(bool)
        ring = ring & panel & (~m)
        if ring.sum() < 10:
            continue
        med = bg_from_pixels(roi[ring])
        roi[m] = med
    img[y0:y1, x0:x1] = roi


def clean_1376(bgr: np.ndarray) -> np.ndarray:
    out = bgr.copy()
    h, w = out.shape[:2]

    # --- 1) Outfield fence ads ---
    print(
        "outfield panels",
        solid_fill_horizontal_panels(
            out, 478, 512, 300, 1100, jump_thr=22, min_w=16, max_w_ratio=0.28
        ),
    )

    # --- 2) Foreground dugout wall ads ---
    print(
        "foreground panels",
        solid_fill_horizontal_panels(
            out, 608, 642, 300, 980, jump_thr=18, min_w=18, max_w_ratio=0.22
        ),
    )

    # --- 3) Side ribbons — horizontal solid fill (clean, no crowd spill) ---
    print(
        "left ribbon",
        solid_fill_horizontal_panels(
            out, 208, 238, 55, 270, jump_thr=14, min_w=24, max_w_ratio=0.7
        ),
    )
    print(
        "right ribbon",
        solid_fill_horizontal_panels(
            out, 212, 238, 1100, 1315, jump_thr=14, min_w=24, max_w_ratio=0.7
        ),
    )

    # Left scoreboard ad stack — explicit solid panels
    for y0, y1, x0, x1 in [
        (150, 195, 250, 325),  # blue SPORTS GLOBAL
        (195, 245, 250, 325),  # red BEST SODA
    ]:
        roi = out[y0:y1, x0:x1]
        out[y0:y1, x0:x1] = bg_from_pixels(roi)
    print("red stack", 1)

    # --- 3b) Mid-tier side ribbons (between seating levels) ---
    for y0, y1, x0, x1 in [
        (255, 285, 40, 330),
        (300, 335, 50, 360),
        (255, 290, 1040, 1340),
        (310, 345, 1040, 1340),
    ]:
        solid_fill_horizontal_panels(out, y0, y1, x0, x1, jump_thr=14, min_w=22, max_w_ratio=0.65)
    print("mid ribbons ok")

    # Center scoreboard branded panels (not live game video)
    for y0, y1, x0, x1 in [
        (175, 230, 700, 780),  # white / logo panel
        (230, 255, 700, 780),  # red strip under it
        (100, 130, 520, 700),  # top red vodacone-like
    ]:
        out[y0:y1, x0:x1] = bg_from_pixels(out[y0:y1, x0:x1])
    print("sb brand panels", 3)
    print(
        "lower ribbon",
        solid_fill_horizontal_panels(
            out, 415, 445, 160, 1180, jump_thr=16, min_w=30, max_w_ratio=0.4
        ),
    )

    # --- 5) Scoreboard top ad strips (conservative) ---
    zone = np.zeros((h, w), dtype=bool)
    zone[95:140, 340:520] = True
    zone[95:140, 980:1080] = True
    zone[160:250, 980:1070] = True
    print("sb blobs", fill_ad_blobs(out, zone, dilate=3, max_h=70))

    # --- 6) Solid wipe leftover letters ---
    for box in [
        (95, 255, 230, 1100),
        (208, 238, 55, 270),
        (212, 238, 1100, 1315),
        (255, 345, 40, 360),
        (255, 345, 1040, 1340),
        (415, 445, 160, 1180),
        (608, 642, 300, 980),
        (478, 512, 300, 1100),
        (150, 245, 250, 325),
    ]:
        wipe_letters_solid(out, *box)

    return out


def clean_any(bgr: np.ndarray) -> np.ndarray:
    h, w = bgr.shape[:2]
    if (w, h) == (1376, 768):
        return clean_1376(bgr)
    small = cv2.resize(bgr, (1376, 768), interpolation=cv2.INTER_AREA)
    cleaned = clean_1376(small)
    diff = cv2.cvtColor(cv2.absdiff(small, cleaned), cv2.COLOR_BGR2GRAY) > 4
    big = cv2.resize(cleaned, (w, h), interpolation=cv2.INTER_LINEAR)
    mask = cv2.resize(diff.astype(np.uint8) * 255, (w, h), interpolation=cv2.INTER_NEAREST) > 0
    out = bgr.copy()
    out[mask] = big[mask]
    return out


def process(path: Path) -> None:
    bak = path.with_suffix(path.suffix + ".bak_ads")
    img = cv2.imread(str(bak), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise SystemExit(f"missing bak: {bak}")
    has_alpha = img.ndim == 3 and img.shape[2] == 4
    bgr = img[:, :, :3] if has_alpha else img
    alpha = img[:, :, 3] if has_alpha else None
    cleaned = clean_any(bgr)
    out = np.dstack([cleaned, alpha]) if has_alpha else cleaned
    if path.suffix.lower() == ".webp":
        cv2.imwrite(str(path), out, [cv2.IMWRITE_WEBP_QUALITY, 93])
    else:
        cv2.imwrite(str(path), out)
    print("ok", path.name, out.shape)


def main() -> None:
    base = Path(
        r"C:\Users\francis1\Desktop\math-sdk-backup-2026-09-25"
        r"\web-sdk-backup-2026-09-26-SYMBOLES-OK\apps\home-run"
        r"\static\assets\spines\foregroundAnimation"
    )
    process(base / "mm_bg.webp")
    process(base / "mm_bg.png")
    print("done")


if __name__ == "__main__":
    main()
