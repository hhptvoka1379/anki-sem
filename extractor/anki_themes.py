from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import tempfile
import time
import zipfile
from pathlib import Path
from typing import Dict, Tuple

import genanki

GOOGLE_FONTS_IMPORT = """@import url('https://fonts.googleapis.com/css2?family=Archivo+Black&family=Cormorant+Garamond:ital,wght@0,500;0,700;1,500;1,700&family=IBM+Plex+Mono:wght@400;600;700&family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Space+Grotesk:wght@500;700&family=Space+Mono:wght@400;700&family=Syne:wght@700;800&display=swap');"""

GOOGLE_FONTS_LINK_HTML = """<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Cormorant+Garamond:ital,wght@0,500;0,700;1,500;1,700&family=IBM+Plex+Mono:wght@400;600;700&family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Space+Grotesk:wght@500;700&family=Space+Mono:wght@400;700&family=Syne:wght@700;800&display=swap" rel="stylesheet">"""

HOST_VIEWPORT_RESET_CSS = """
html, body, #qa {
  margin: 0 !important;
  padding: 0 !important;
  width: 100% !important;
  min-height: 100vh !important;
}
"""

BASE_RESET_CSS = """
.card {
  min-height: 100vh;
  width: 100%;
  margin: 0;
  padding: 20px 14px 32px;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
  text-align: left;
}
.card *, .card *::before, .card *::after {
  box-sizing: border-box;
}
.fig-box {
  margin: 14px 0;
  text-align: center;
}
.fig-box img, details.orig-scan img {
  max-width: 100%;
  height: auto;
  background: #ffffff;
}
.opt {
  cursor: pointer;
  user-select: none;
}
details.orig-scan {
  margin-top: 14px;
  font-size: 12px;
}
details.orig-scan summary {
  cursor: pointer;
  font-weight: 600;
  padding: 4px 0;
}
"""


def _stable_id(seed: str) -> int:
    digest = hashlib.sha256(seed.encode("utf-8")).digest()
    return 1_000_000_000 + (int.from_bytes(digest[:8], "big") % 999_000_000)


def _convert_card_selectors_to_sf_canvas(css_text: str) -> str:
    """Map `.card` / `.card.nightMode` rules onto our isolated `#qa` child `.sf-canvas` / `.sf-canvas.sf-dark`
    so Anki Desktop's automatic `<body class="card card1 isMac nightMode">` NEVER overrides any theme's
    intended surface palette or splits the viewport background!"""
    s = css_text
    s = s.replace(".card:not(.nightMode)", ".sf-canvas:not(.sf-dark)")
    s = s.replace(".card.nightMode", ".sf-canvas.sf-dark")
    s = s.replace(".nightMode.card", ".sf-canvas.sf-dark")
    s = s.replace(".night_mode .card", ".sf-canvas.sf-dark")
    s = re.sub(r"\.nightMode\s+", ".sf-canvas.sf-dark ", s)
    s = re.sub(r"\.night_mode\s+", ".sf-canvas.sf-dark ", s)
    s = re.sub(r"\.card(?![A-Za-z0-9_-])", ".sf-canvas", s)
    return s


# ==============================================================================
# EXACT 10 ART-DIRECTED ANKI DESIGN SYSTEMS FROM theme_showcase.html
# ==============================================================================

RAW_THEMES: Dict[str, dict] = {
    "01_swiss_poster": {
        "num": "01",
        "slug": "01_swiss_poster",
        "name": "Zürich 1962 — Swiss Poster Grid",
        "tagline": "Josef Müller-Brockmann asymmetric typographic grid • Giant vermilion index numeral, registration crosshairs & stark invert bars",
        "accent": "#e11d18",
        "default_dark": False,
        "layout": "swiss",
        "css": BASE_RESET_CSS + """
.card {
  background: #e6e3dc;
  color: #0d0d0d;
  font-family: "Inter", "Helvetica Neue", Helvetica, Arial, sans-serif;
}
.card.nightMode { background: #0c0c0c; color: #f2f0eb; }
.swiss-sheet {
  max-width: 780px;
  margin: 0 auto;
  background: #f4f1ea;
  border: 2px solid #0d0d0d;
  position: relative;
}
.card.nightMode .swiss-sheet { background: #141414; border-color: #f2f0eb; }
.swiss-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 16px;
  border-bottom: 2px solid #0d0d0d;
  font-family: "IBM Plex Mono", monospace;
  font-size: 10.5px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.card.nightMode .swiss-topbar { border-bottom-color: #f2f0eb; }
.swiss-red-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  background: #e11d18;
  margin-right: 8px;
}
.swiss-grid {
  display: grid;
  grid-template-columns: 128px 1fr;
}
@media (max-width: 600px) { .swiss-grid { grid-template-columns: 1fr; } }
.swiss-rail {
  border-right: 2px solid #0d0d0d;
  padding: 18px 14px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: #ece8df;
}
.card.nightMode .swiss-rail { background: #1b1b1b; border-right-color: #f2f0eb; }
@media (max-width: 600px) {
  .swiss-rail { border-right: none; border-bottom: 2px solid #0d0d0d; flex-direction: row; align-items: baseline; }
}
.swiss-big-num {
  font-family: "Archivo Black", "Inter", sans-serif;
  font-size: 46px;
  line-height: 0.92;
  color: #e11d18;
  letter-spacing: -0.04em;
}
.swiss-meta-stack {
  font-family: "IBM Plex Mono", monospace;
  font-size: 10px;
  line-height: 1.5;
  text-transform: uppercase;
  margin-top: 18px;
  opacity: 0.85;
}
.swiss-main { padding: 22px 24px 24px; }
.stem {
  font-size: 18px;
  font-weight: 700;
  line-height: 1.38;
  letter-spacing: -0.02em;
  margin-bottom: 18px;
}
.blank-slot { display: inline-block; min-width: 90px; border-bottom: 3px solid #e11d18; color: transparent; }
.blank-filled { background: #e11d18; color: #ffffff; padding: 1px 8px; font-weight: 800; }
.options { display: flex; flex-direction: column; border-top: 1.5px solid #0d0d0d; margin-top: 14px; }
.card.nightMode .options { border-top-color: #f2f0eb; }
.opt {
  display: flex;
  align-items: baseline;
  gap: 14px;
  padding: 11px 10px;
  border-bottom: 1px solid #0d0d0d;
  transition: background 0.1s ease, color 0.1s ease;
}
.card.nightMode .opt { border-bottom-color: #383838; }
.opt:hover { background: #0d0d0d; color: #f4f1ea; }
.card.nightMode .opt:hover { background: #f2f0eb; color: #0d0d0d; }
.opt-letter {
  font-family: "Archivo Black", sans-serif;
  font-size: 14px;
  color: #e11d18;
  min-width: 24px;
}
.opt:hover .opt-letter { color: #ff5a52; }
.opt.user-picked { background: #0d0d0d; color: #f4f1ea; }
.opt.user-picked .opt-letter { color: #facc15; }
.opt.user-wrong { background: #fee2e2; color: #7f1d1d; text-decoration: line-through; }
.opt.correct { background: #e11d18; color: #ffffff; font-weight: 700; }
.opt.correct .opt-letter { color: #ffffff; }
.ans-banner {
  margin-top: 18px;
  padding: 12px 14px;
  background: #0d0d0d;
  color: #f4f1ea;
  font-family: "IBM Plex Mono", monospace;
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
}
.card.nightMode .ans-banner { background: #e11d18; color: #ffffff; }
.expl-box {
  margin-top: 14px;
  padding: 14px 16px;
  border-left: 4px solid #e11d18;
  background: #ebe7de;
  font-size: 14px;
  line-height: 1.58;
}
.card.nightMode .expl-box { background: #1e1e1e; color: #e5e5e5; }
.fig-box img, details.orig-scan img { border: 1.5px solid #0d0d0d; padding: 6px; }
""",
    },

    "02_teenage_engineering": {
        "num": "02",
        "slug": "02_teenage_engineering",
        "name": "Teenage Engineering OP-1 Field",
        "tagline": "Anodized machined aluminum chassis • Recessed dark OLED stem display, screw-head corners & tactile orange keycaps",
        "accent": "#ff4f00",
        "default_dark": False,
        "layout": "te_hardware",
        "css": BASE_RESET_CSS + """
.card {
  background: #bfc3c9;
  color: #181a1d;
  font-family: "Space Grotesk", sans-serif;
}
.card.nightMode { background: #111315; color: #e5e7eb; }
.te-chassis {
  max-width: 720px;
  margin: 0 auto;
  background: linear-gradient(180deg, #e4e6ea 0%, #cfd3d9 100%);
  border: 1.5px solid #8c929c;
  border-radius: 22px;
  padding: 18px 20px 22px;
  box-shadow: inset 0 2px 0 rgba(255,255,255,0.85), 0 18px 36px rgba(0,0,0,0.22);
}
.card.nightMode .te-chassis {
  background: linear-gradient(180deg, #24272c 0%, #191b1f 100%);
  border-color: #3b4048;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.08), 0 18px 40px rgba(0,0,0,0.65);
}
.te-screw-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-family: "Space Mono", monospace;
  font-size: 10.5px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #4b525c;
  margin-bottom: 12px;
}
.card.nightMode .te-screw-row { color: #9ca3af; }
.te-screw {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: #b0b5bd;
  border: 1px solid #6b7280;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  color: #374151;
}
.te-orange-led {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ff4f00;
  box-shadow: 0 0 8px #ff4f00;
  margin-right: 6px;
}
.te-screen {
  background: #101316;
  color: #f3f4f6;
  border-radius: 12px;
  border: 3px solid #2b3036;
  padding: 18px 20px;
  box-shadow: inset 0 4px 14px rgba(0,0,0,0.75);
}
.te-screen-hud {
  display: flex;
  justify-content: space-between;
  font-family: "Space Mono", monospace;
  font-size: 11px;
  color: #ff6b2b;
  border-bottom: 1px dashed #2d3540;
  padding-bottom: 8px;
  margin-bottom: 12px;
}
.stem { font-size: 16.5px; font-weight: 500; line-height: 1.52; color: #f8fafc; }
.blank-slot { display: inline-block; min-width: 84px; border-bottom: 2px solid #ff4f00; color: transparent; }
.blank-filled { background: #ff4f00; color: #ffffff; padding: 1px 8px; border-radius: 4px; font-family: "Space Mono", monospace; }
.options { display: flex; flex-direction: column; gap: 9px; margin-top: 16px; }
.opt {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 12px;
  background: #f5f6f8;
  border: 1px solid #9fa6b2;
  box-shadow: 0 4px 0 #9fa6b2, 0 6px 10px rgba(0,0,0,0.08);
  color: #111827;
  transition: transform 0.08s ease, box-shadow 0.08s ease;
}
.card.nightMode .opt {
  background: #2d3138;
  border-color: #111315;
  box-shadow: 0 4px 0 #0d0f12;
  color: #f3f4f6;
}
.opt:hover { transform: translateY(-1px); border-color: #ff4f00; }
.opt:active, .opt.user-picked {
  transform: translateY(3px);
  box-shadow: 0 1px 0 #7b2600;
  background: #ff4f00;
  border-color: #c23b00;
  color: #ffffff;
}
.opt-letter {
  width: 28px;
  height: 28px;
  border-radius: 7px;
  background: #e5e7eb;
  border: 1px solid #cbd5e1;
  font-family: "Space Mono", monospace;
  font-weight: 700;
  font-size: 13px;
  color: #111827;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.opt.user-picked .opt-letter { background: #111316; color: #ff4f00; border-color: #111316; }
.opt.user-wrong { background: #ef4444; color: #ffffff; box-shadow: 0 2px 0 #991b1b; }
.opt.correct { background: #10b981; border-color: #059669; color: #052e16; font-weight: 700; box-shadow: 0 4px 0 #047857; }
.opt.correct .opt-letter { background: #052e16; color: #6ee7b7; border-color: #052e16; }
.ans-banner {
  margin-top: 16px;
  padding: 11px 15px;
  border-radius: 10px;
  background: #101316;
  color: #10b981;
  font-family: "Space Mono", monospace;
  font-size: 13px;
  font-weight: 700;
  border: 1.5px solid #2b3036;
}
.expl-box {
  margin-top: 12px;
  padding: 13px 16px;
  border-radius: 10px;
  background: rgba(255,255,255,0.72);
  border: 1px solid #b0b6c0;
  font-size: 14px;
  line-height: 1.56;
  color: #1f2937;
}
.card.nightMode .expl-box { background: #16181c; border-color: #374151; color: #d1d5db; }
.fig-box img, details.orig-scan img { border-radius: 8px; padding: 6px; border: 2px solid #374151; }
""",
    },

    "03_nerv_magi_crt": {
        "num": "03",
        "slug": "03_nerv_magi_crt",
        "name": "NERV // MAGI Tactical CRT",
        "tagline": "Tokyo-3 cybernetic command console • Angled hazard stripes, CRT phosphor scanlines & chamfered polygon options",
        "accent": "#ff6a00",
        "default_dark": True,
        "layout": "nerv",
        "css": BASE_RESET_CSS + """
.card, .card.nightMode {
  background: #050507;
  color: #ffb000;
  font-family: "JetBrains Mono", monospace;
}
.nerv-frame {
  max-width: 750px;
  margin: 0 auto;
  background:
    repeating-linear-gradient(0deg, rgba(255,136,0,0.03) 0px, rgba(255,136,0,0.03) 1px, transparent 1px, transparent 3px),
    #090a0d;
  border: 1.5px solid #ff6a00;
  padding: 0 0 20px;
  box-shadow: 0 0 28px rgba(255,106,0,0.16), inset 0 0 40px rgba(255,106,0,0.05);
}
.nerv-hazard {
  height: 14px;
  background: repeating-linear-gradient(-45deg, #ff6a00, #ff6a00 10px, #090a0d 10px, #090a0d 20px);
  border-bottom: 1.5px solid #ff6a00;
}
.nerv-head {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  padding: 10px 18px;
  border-bottom: 1px solid rgba(255,106,0,0.4);
  font-size: 11px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.nerv-tag {
  background: #ff1e38;
  color: #050507;
  font-weight: 800;
  padding: 2px 8px;
}
.nerv-body { padding: 18px 20px 0; }
.stem {
  font-size: 15.5px;
  line-height: 1.6;
  color: #ffdca8;
  text-shadow: 0 0 8px rgba(255,176,0,0.28);
  margin-bottom: 16px;
}
.blank-slot { display: inline-block; min-width: 84px; border-bottom: 2px solid #00ff9d; color: transparent; }
.blank-filled { background: rgba(0,255,157,0.18); color: #00ff9d; border: 1px solid #00ff9d; padding: 1px 8px; }
.options { display: flex; flex-direction: column; gap: 8px; }
.opt {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  background: rgba(255,106,0,0.06);
  border: 1px solid rgba(255,106,0,0.45);
  clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 12px 100%, 0 calc(100% - 12px));
  color: #ffb84d;
  font-size: 14px;
  transition: all 0.12s ease;
}
.opt:hover {
  background: rgba(255,106,0,0.2);
  border-color: #ffb000;
  color: #ffffff;
  transform: translateX(4px);
}
.opt-letter {
  font-weight: 800;
  color: #050507;
  background: #ff6a00;
  padding: 2px 7px;
  font-size: 12px;
}
.opt.user-picked { background: rgba(0,229,255,0.18); border-color: #00e5ff; color: #e0faff; }
.opt.user-picked .opt-letter { background: #00e5ff; color: #050507; }
.opt.user-wrong { background: rgba(255,30,56,0.25); border-color: #ff1e38; color: #ffc2c9; }
.opt.user-wrong .opt-letter { background: #ff1e38; color: #ffffff; }
.opt.correct { background: rgba(0,255,157,0.18); border-color: #00ff9d; color: #b8ffe3; font-weight: 700; box-shadow: 0 0 16px rgba(0,255,157,0.2); }
.opt.correct .opt-letter { background: #00ff9d; color: #050507; }
.ans-banner {
  margin-top: 16px;
  padding: 10px 14px;
  border: 1px solid #00ff9d;
  background: rgba(0,255,157,0.1);
  color: #00ff9d;
  font-size: 13px;
  font-weight: 700;
}
.expl-box {
  margin-top: 12px;
  padding: 13px 15px;
  border-left: 3px solid #ff6a00;
  background: rgba(255,106,0,0.05);
  color: #fed7aa;
  font-family: "Inter", sans-serif;
  font-size: 14px;
  line-height: 1.58;
}
details.orig-scan summary { color: #ff8800; }
.fig-box img, details.orig-scan img { border: 1.5px solid #ff6a00; padding: 6px; }
""",
    },

    "04_neobrutalist_bauhaus": {
        "num": "04",
        "slug": "04_neobrutalist_bauhaus",
        "name": "Neo-Brutalist Risoprint Zine",
        "tagline": "Halftone dot-grid paper, tilted ink stamp badge, Syne display & hard offset press",
        "accent": "#facc15",
        "default_dark": False,
        "layout": "brutalist",
        "css": BASE_RESET_CSS + """
.card {
  font-family: "Space Grotesk", sans-serif;
  background-color: #fef08a;
  background-image: radial-gradient(#111111 1.15px, transparent 1.15px);
  background-size: 16px 16px;
  color: #111111;
  line-height: 1.5;
}
.card.nightMode {
  background-color: #18181b;
  background-image: radial-gradient(#3f3f46 1.15px, transparent 1.15px);
  color: #fafafa;
}
.wrap {
  max-width: 720px;
  margin: 0 auto;
  background: #fffef9;
  border: 3px solid #111111;
  border-radius: 2px;
  padding: 22px 24px 24px;
  box-shadow: -3px -3px 0px #ff2e93, 8px 8px 0px #111111;
  position: relative;
}
.wrap::before {
  content: "+ RISO.ZINE // REG.04 +";
  position: absolute;
  top: 6px;
  right: 12px;
  font-family: "Space Mono", monospace;
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: #111111;
  opacity: 0.48;
}
.card.nightMode .wrap { background: #232329; border-color: #fafafa; box-shadow: -3px -3px 0px #ec4899, 8px 8px 0px #facc15; }
.card.nightMode .wrap::before { color: #facc15; opacity: 0.7; }
.meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  padding-bottom: 14px;
  margin-bottom: 16px;
  border-bottom: 2.5px solid #111111;
}
.card.nightMode .meta { border-bottom-color: #fafafa; }
.badge {
  display: inline-block;
  transform: rotate(-1.8deg);
  padding: 4px 11px;
  border: 2.5px solid #111111;
  font-family: "Syne", sans-serif;
  font-weight: 800;
  font-size: 11.5px;
  text-transform: uppercase;
  box-shadow: 3px 3px 0px #111111;
}
.subj-CHIM { background: #c4b5fd; color: #111111; }
.subj-BIO  { background: #86efac; color: #111111; }
.subj-FIS  { background: #7dd3fc; color: #111111; }
.meta-dim { font-family: "Space Mono", monospace; font-weight: 700; font-size: 11.5px; }
.stem { font-size: 18px; font-weight: 700; margin: 14px 0 18px; letter-spacing: -0.015em; }
.blank-slot { display: inline-block; min-width: 88px; background: #fde047; border: 2px solid #111111; padding: 0 6px; color: transparent; }
.blank-filled { background: #86efac; color: #111111; border: 2px solid #111111; padding: 1px 8px; font-weight: 800; }
.options { display: flex; flex-direction: column; gap: 10px; }
.opt {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 14px;
  border: 2.5px solid #111111;
  background: #ffffff;
  box-shadow: 4px 4px 0px #111111;
  font-weight: 600;
  transition: transform 0.08s ease, box-shadow 0.08s ease, background 0.08s ease;
}
.card.nightMode .opt { background: #18181b; border-color: #fafafa; box-shadow: 4px 4px 0px #fafafa; }
.opt:hover { background: #fde047; color: #111111; transform: translate(-2px, -2px); box-shadow: 6px 6px 0px #111111; }
.opt:active, .opt.user-picked { transform: translate(3px, 3px); box-shadow: 1px 1px 0px #111111; background: #7dd3fc; color: #111111; }
.opt-letter {
  width: 28px;
  height: 28px;
  border: 2px solid #111111;
  background: #facc15;
  color: #111111;
  font-family: "Syne", sans-serif;
  font-weight: 800;
  font-size: 13px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.opt.user-wrong { background: #fca5a5; color: #111111; }
.opt.correct { background: #86efac; color: #111111; font-weight: 800; }
.opt.correct .opt-letter { background: #111111; color: #86efac; }
.ans-banner {
  margin-top: 18px;
  padding: 12px 15px;
  border: 2.5px solid #111111;
  background: #fde047;
  color: #111111;
  font-family: "Space Mono", monospace;
  font-size: 13px;
  font-weight: 700;
  box-shadow: 4px 4px 0px #111111;
}
.expl-box {
  margin-top: 14px;
  padding: 14px 16px;
  border: 2.5px solid #111111;
  background: #f4f4f5;
  color: #111111;
  font-size: 14.5px;
  line-height: 1.56;
}
.fig-box img, details.orig-scan img { border: 2.5px solid #111111; box-shadow: 4px 4px 0px #111111; padding: 6px; }
""",
    },

    "05_milano_editorial": {
        "num": "05",
        "slug": "05_milano_editorial",
        "name": "Milano Editorial — Print & Didone",
        "tagline": "Luxury Italian print journal • High-contrast Cormorant & Instrument Serif display, double masthead & burgundy ink",
        "accent": "#7f1d1d",
        "default_dark": False,
        "layout": "editorial",
        "css": BASE_RESET_CSS + """
.card {
  background: #e9e2d4;
  color: #191614;
  font-family: "Cormorant Garamond", Georgia, serif;
}
.card.nightMode { background: #141210; color: #f3ede2; }
.ed-page {
  max-width: 720px;
  margin: 0 auto;
  background: #faf6ee;
  border: 1px solid #cfc4b0;
  padding: 28px 34px 30px;
  box-shadow: 0 12px 32px rgba(40,30,15,0.08);
}
.card.nightMode .ed-page { background: #1c1916; border-color: #3a332b; }
.ed-masthead {
  text-align: center;
  border-top: 2px solid #191614;
  border-bottom: 4px double #191614;
  padding: 8px 0 9px;
  margin-bottom: 22px;
  font-family: "Inter", sans-serif;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.2em;
  text-transform: uppercase;
}
.card.nightMode .ed-masthead { border-color: #e6dfd3; }
.ed-kicker {
  color: #881337;
  font-weight: 800;
}
.card.nightMode .ed-kicker { color: #fda4af; }
.stem {
  font-family: "Cormorant Garamond", Georgia, serif;
  font-size: 24px;
  font-weight: 600;
  line-height: 1.36;
  letter-spacing: -0.01em;
  margin-bottom: 20px;
}
.blank-slot { display: inline-block; min-width: 92px; border-bottom: 1.5px solid #881337; color: transparent; }
.blank-filled { font-style: italic; color: #881337; border-bottom: 2px solid #881337; padding: 0 6px; font-weight: 700; }
.card.nightMode .blank-filled { color: #fda4af; border-bottom-color: #fda4af; }
.options { display: flex; flex-direction: column; gap: 4px; margin-top: 12px; }
.opt {
  display: flex;
  align-items: baseline;
  gap: 14px;
  padding: 9px 12px;
  border-bottom: 1px solid #e5dccb;
  font-size: 19px;
  line-height: 1.42;
  transition: all 0.14s ease;
}
.card.nightMode .opt { border-bottom-color: #2f2a24; }
.opt:hover { background: #f1eadb; padding-left: 18px; }
.card.nightMode .opt:hover { background: #26221e; }
.opt-letter {
  font-family: "Instrument Serif", Georgia, serif;
  font-style: italic;
  font-size: 22px;
  color: #881337;
  min-width: 22px;
}
.card.nightMode .opt-letter { color: #fda4af; }
.opt.user-picked { background: #ede3d1; border-left: 3px solid #881337; }
.card.nightMode .opt.user-picked { background: #2e2622; border-left-color: #fda4af; }
.opt.user-wrong { color: #991b1b; text-decoration: line-through; opacity: 0.72; }
.opt.correct { background: #eef5ee; border-left: 3px solid #166534; color: #14532d; font-weight: 700; }
.card.nightMode .opt.correct { background: #14291d; color: #bbf7d0; border-left-color: #4ade80; }
.ans-banner {
  margin-top: 20px;
  padding: 10px 0;
  border-top: 1.5px solid #191614;
  border-bottom: 1.5px solid #191614;
  font-family: "Inter", sans-serif;
  font-size: 12.5px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: #881337;
}
.card.nightMode .ans-banner { border-color: #d6d3d1; color: #fda4af; }
.expl-box {
  margin-top: 16px;
  padding: 14px 18px;
  background: #f3ede0;
  font-size: 17.5px;
  line-height: 1.55;
  font-style: italic;
}
.card.nightMode .expl-box { background: #24201c; }
details.orig-scan { font-family: "Inter", sans-serif; }
.fig-box img, details.orig-scan img { border: 1px solid #bfb39c; padding: 8px; }
""",
    },

    "06_linear_mono": {
        "num": "06",
        "slug": "06_linear_mono",
        "name": "Linear / Vercel Mono-Tech",
        "tagline": "Subtle radial dot-matrix canvas, specular top border gleam & machined zinc keycaps",
        "accent": "#52525b",
        "default_dark": True,
        "layout": "standard",
        "css": BASE_RESET_CSS + """
.card {
  font-family: "Inter", sans-serif;
  background-color: #fafafa;
  background-image: radial-gradient(#d4d4d8 1px, transparent 1px);
  background-size: 20px 20px;
  color: #09090b;
  line-height: 1.55;
}
.card.nightMode {
  background-color: #09090b;
  background-image: radial-gradient(#27272a 1px, transparent 1px);
  color: #fafafa;
}
.wrap {
  max-width: 700px;
  margin: 0 auto;
  background: #ffffff;
  border: 1px solid #e4e4e7;
  border-radius: 14px;
  padding: 24px 26px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.04);
}
.card.nightMode .wrap {
  background: linear-gradient(180deg, #141418 0%, #0e0e11 100%);
  border-color: #27272a;
  box-shadow: inset 0 1px 0 rgba(255,255,255,0.09), 0 18px 40px rgba(0,0,0,0.65);
}
.meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  font-family: "JetBrains Mono", monospace;
  font-size: 11px;
  color: #71717a;
  padding-bottom: 13px;
  margin-bottom: 16px;
  border-bottom: 1px solid #f4f4f5;
}
.card.nightMode .meta { border-bottom-color: #1f1f24; }
.badge {
  padding: 2px 8px;
  border-radius: 5px;
  background: #18181b;
  color: #fafafa;
  font-weight: 700;
}
.card.nightMode .badge { background: #fafafa; color: #09090b; }
.stem { font-size: 16.5px; font-weight: 500; letter-spacing: -0.015em; margin: 14px 0 18px; }
.blank-slot { display: inline-block; min-width: 82px; border-bottom: 1.5px solid currentColor; color: transparent; }
.blank-filled { font-family: "JetBrains Mono", monospace; background: #10b981; color: #052e16; font-weight: 700; padding: 2px 8px; border-radius: 5px; font-size: 14px; }
.options { display: flex; flex-direction: column; gap: 7px; }
.opt {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 13px;
  border-radius: 9px;
  border: 1px solid #e4e4e7;
  background: #ffffff;
  transition: all 0.12s ease;
}
.card.nightMode .opt { background: rgba(255,255,255,0.025); border-color: #27272a; }
.opt:hover { border-color: #a1a1aa; background: #f4f4f5; }
.card.nightMode .opt:hover { border-color: #52525b; background: rgba(255,255,255,0.06); }
.opt-letter {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  border: 1px solid #d4d4d8;
  box-shadow: 0 1.5px 0 #d4d4d8;
  font-family: "JetBrains Mono", monospace;
  font-size: 11.5px;
  font-weight: 700;
  color: #52525b;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.card.nightMode .opt-letter { border-color: #3f3f46; box-shadow: 0 1.5px 0 #3f3f46; color: #a1a1aa; background: #18181b; }
.opt.user-picked { border-color: #3b82f6; background: rgba(59,130,246,0.12); }
.opt.user-picked .opt-letter { background: #3b82f6; border-color: #3b82f6; color: #ffffff; box-shadow: none; }
.opt.user-wrong { border-color: #ef4444; background: rgba(239,68,68,0.12); }
.opt.user-wrong .opt-letter { background: #ef4444; border-color: #ef4444; color: #ffffff; box-shadow: none; }
.opt.correct { border-color: #10b981; background: rgba(16,185,129,0.13); font-weight: 600; }
.opt.correct .opt-letter { background: #10b981; border-color: #10b981; color: #052e16; box-shadow: none; }
.ans-banner {
  margin-top: 16px;
  padding: 11px 14px;
  border-radius: 9px;
  border: 1px solid #27272a;
  background: rgba(16,185,129,0.1);
  color: #34d399;
  font-family: "JetBrains Mono", monospace;
  font-size: 12.5px;
  font-weight: 700;
}
.card:not(.nightMode) .ans-banner { background: #f0fdf4; border-color: #bbf7d0; color: #166534; }
.expl-box {
  margin-top: 12px;
  padding: 13px 15px;
  border-radius: 9px;
  border: 1px solid #e4e4e7;
  background: #fafafa;
  font-size: 14px;
  line-height: 1.58;
}
.card.nightMode .expl-box { background: #141418; border-color: #27272a; color: #d4d4d8; }
.fig-box img, details.orig-scan img { border-radius: 8px; border: 1px solid #3f3f46; padding: 6px; }
""",
    },

    "07_cyanotype_blueprint": {
        "num": "07",
        "slug": "07_cyanotype_blueprint",
        "name": "Prussian Cyanotype Blueprint",
        "tagline": "Engineering drafting table • Deep #082f49 cyanotype paper, 20px architectural grid rules & technical title block",
        "accent": "#0284c7",
        "default_dark": True,
        "layout": "blueprint",
        "css": BASE_RESET_CSS + """
.card, .card.nightMode {
  background-color: #082f49;
  background-image:
    linear-gradient(rgba(255,255,255,0.09) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.09) 1px, transparent 1px),
    linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
  background-size: 100px 100px, 100px 100px, 20px 20px, 20px 20px;
  color: #f0f9ff;
  font-family: "IBM Plex Mono", monospace;
}
.bp-sheet {
  max-width: 750px;
  margin: 0 auto;
  border: 2px solid rgba(255,255,255,0.85);
  background: rgba(11, 56, 86, 0.86);
  backdrop-filter: blur(2px);
}
.bp-titleblock {
  display: grid;
  grid-template-columns: auto 1fr auto;
  border-bottom: 2px solid rgba(255,255,255,0.85);
  font-size: 11px;
  text-transform: uppercase;
}
.bp-cell {
  padding: 8px 14px;
  border-right: 1px solid rgba(255,255,255,0.55);
}
.bp-cell:last-child { border-right: none; }
.bp-body { padding: 20px 24px 24px; }
.stem {
  font-family: "Space Grotesk", sans-serif;
  font-size: 17.5px;
  font-weight: 600;
  line-height: 1.5;
  color: #ffffff;
  margin-bottom: 18px;
}
.blank-slot { display: inline-block; min-width: 88px; border-bottom: 2px dashed #7dd3fc; color: transparent; }
.blank-filled { background: #ffffff; color: #082f49; font-weight: 700; padding: 1px 8px; }
.options { display: flex; flex-direction: column; gap: 8px; }
.opt {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border: 1px solid rgba(255,255,255,0.5);
  background: rgba(8, 47, 73, 0.55);
  font-size: 14px;
  transition: all 0.12s ease;
}
.opt:hover { background: rgba(255,255,255,0.16); border-color: #ffffff; }
.opt-letter {
  width: 25px;
  height: 25px;
  border: 1.5px solid #ffffff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 12px;
  flex-shrink: 0;
}
.opt.user-picked { background: #ffffff; color: #082f49; font-weight: 700; }
.opt.user-picked .opt-letter { border-color: #082f49; }
.opt.user-wrong { background: rgba(239,68,68,0.35); border-color: #fca5a5; }
.opt.correct { background: #38bdf8; color: #082f49; border-color: #ffffff; font-weight: 700; }
.opt.correct .opt-letter { background: #082f49; color: #ffffff; border-color: #082f49; }
.ans-banner {
  margin-top: 18px;
  padding: 11px 14px;
  border: 2px solid #ffffff;
  background: rgba(56,189,248,0.22);
  color: #ffffff;
  font-size: 13px;
  font-weight: 700;
}
.expl-box {
  margin-top: 12px;
  padding: 13px 16px;
  border: 1px dashed rgba(255,255,255,0.65);
  font-family: "Inter", sans-serif;
  font-size: 14px;
  line-height: 1.58;
  color: #e0f2fe;
}
.fig-box img, details.orig-scan img { border: 2px solid #ffffff; padding: 6px; }
""",
    },

    "08_split_ipad_pro": {
        "num": "08",
        "slug": "08_split_ipad_pro",
        "name": "Studio Split-Deck (2-Column Gallery)",
        "tagline": "Tinted left question canvas well + elevated right answer stack — zero vertical scroll!",
        "accent": "#4f46e5",
        "default_dark": False,
        "layout": "split",
        "css": BASE_RESET_CSS + """
.card {
  font-family: "Plus Jakarta Sans", "Inter", sans-serif;
  background: #e8ecf4;
  color: #0f172a;
}
.card.nightMode { background: #0b101b; color: #f1f5f9; }
.split-shell {
  max-width: 960px;
  margin: 0 auto;
  background: #ffffff;
  border: 1px solid #d5dfec;
  border-radius: 22px;
  overflow: hidden;
  box-shadow: 0 16px 40px rgba(15,23,42,0.08);
  display: grid;
  grid-template-columns: 1.08fr 1fr;
}
.card.nightMode .split-shell { background: #131b2c; border-color: #24324b; }
@media (max-width: 680px) { .split-shell { grid-template-columns: 1fr; } }
.split-left-well {
  background: #f4f7fc;
  border-right: 1px solid #e2e8f0;
  padding: 24px 26px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.card.nightMode .split-left-well { background: #0f1624; border-right-color: #24324b; }
.split-right-well { padding: 24px 26px; }
.meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
  font-size: 11.5px;
}
.badge {
  padding: 4px 10px;
  border-radius: 8px;
  font-weight: 800;
  font-size: 11px;
  background: #4f46e5;
  color: #ffffff;
}
.subj-BIO { background: #059669; }
.subj-FIS { background: #0284c7; }
.meta-dim { color: #64748b; font-weight: 600; }
.card.nightMode .meta-dim { color: #94a3b8; }
.stem { font-size: 17px; font-weight: 600; line-height: 1.5; margin: 6px 0 14px; }
.blank-slot { display: inline-block; min-width: 82px; border-bottom: 2.5px solid #4f46e5; color: transparent; }
.blank-filled { background: #4f46e5; color: #ffffff; font-weight: 700; padding: 1px 9px; border-radius: 6px; }
.options { display: flex; flex-direction: column; gap: 9px; }
.opt {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 14px;
  border-radius: 12px;
  border: 1.5px solid #e2e8f0;
  background: #ffffff;
  font-size: 14.5px;
  font-weight: 500;
  transition: all 0.14s ease;
}
.card.nightMode .opt { background: #19243a; border-color: #293856; }
.opt:hover { border-color: #6366f1; background: #eef2ff; transform: translateX(2px); }
.card.nightMode .opt:hover { border-color: #818cf8; background: #21304d; }
.opt-letter {
  width: 27px;
  height: 27px;
  border-radius: 8px;
  background: #eef2ff;
  color: #4338ca;
  font-weight: 800;
  font-size: 12.5px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.card.nightMode .opt-letter { background: #283655; color: #c7d2fe; }
.opt.user-picked { border-color: #4f46e5; background: #e0e7ff; color: #1e1b4b; }
.opt.user-picked .opt-letter { background: #4f46e5; color: #ffffff; }
.opt.user-wrong { border-color: #ef4444; background: #fef2f2; color: #991b1b; }
.opt.correct { border-color: #10b981; background: #ecfdf5; color: #064e3b; font-weight: 700; }
.card.nightMode .opt.correct { background: rgba(16,185,129,0.18); color: #ecfdf5; }
.opt.correct .opt-letter { background: #10b981; color: #ffffff; }
.ans-banner {
  margin-top: 14px;
  padding: 11px 14px;
  border-radius: 11px;
  background: #eef2ff;
  border-left: 4px solid #4f46e5;
  color: #312e81;
  font-size: 13.5px;
  font-weight: 800;
}
.card.nightMode .ans-banner { background: #1e1b4b; color: #e0e7ff; border-left-color: #818cf8; }
.expl-box {
  margin-top: 12px;
  padding: 13px 15px;
  border-radius: 11px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  font-size: 13.5px;
  line-height: 1.56;
}
.card.nightMode .expl-box { background: #0f1624; border-color: #24324b; }
.fig-box img, details.orig-scan img { border-radius: 10px; border: 1px solid #cbd5e1; padding: 6px; }
""",
    },

    "09_kyoto_washi": {
        "num": "09",
        "slug": "09_kyoto_washi",
        "name": "Kyoto Washi & Hanko Seal",
        "tagline": "Japanese handmade kozo paper • Vermilion red carved hanko stamp, vertical rail & ai-zome indigo dye",
        "accent": "#c53030",
        "default_dark": False,
        "layout": "washi",
        "css": BASE_RESET_CSS + """
.card {
  background: #e5dfd3;
  color: #1f1d1a;
  font-family: "Cormorant Garamond", "Hiragino Mincho ProN", Georgia, serif;
}
.card.nightMode { background: #161513; color: #ede8dd; }
.washi-card {
  max-width: 720px;
  margin: 0 auto;
  background: #f7f3ea;
  border: 1px solid #d4cbb8;
  padding: 26px 28px;
  position: relative;
  box-shadow: 0 10px 28px rgba(31,29,26,0.07);
}
.card.nightMode .washi-card { background: #201e1b; border-color: #3b3730; }
.washi-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid #d4cbb8;
  padding-bottom: 14px;
  margin-bottom: 18px;
}
.card.nightMode .washi-top { border-bottom-color: #3b3730; }
.hanko-seal {
  width: 44px;
  height: 44px;
  border: 2.5px solid #c53030;
  border-radius: 4px;
  color: #c53030;
  font-family: "IBM Plex Mono", monospace;
  font-weight: 800;
  font-size: 11px;
  line-height: 1.05;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  transform: rotate(3deg);
  flex-shrink: 0;
}
.washi-meta {
  font-family: "Inter", sans-serif;
  font-size: 11.5px;
  color: #6b6459;
  letter-spacing: 0.04em;
}
.card.nightMode .washi-meta { color: #a8a29e; }
.stem { font-size: 21px; font-weight: 600; line-height: 1.46; margin-bottom: 18px; }
.blank-slot { display: inline-block; min-width: 86px; border-bottom: 1.5px solid #c53030; color: transparent; }
.blank-filled { background: #1e3a5f; color: #f7f3ea; padding: 1px 9px; font-weight: 700; }
.options { display: flex; flex-direction: column; gap: 7px; font-family: "Inter", sans-serif; font-size: 14.5px; }
.opt {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  background: #fcfaf5;
  border: 1px solid #ded6c6;
  border-left: 3px solid transparent;
  transition: all 0.14s ease;
}
.card.nightMode .opt { background: #292622; border-color: #3d3831; }
.opt:hover { border-left-color: #c53030; background: #f1ece0; }
.card.nightMode .opt:hover { background: #332f2a; }
.opt-letter {
  font-family: "IBM Plex Mono", monospace;
  font-size: 12px;
  font-weight: 700;
  color: #c53030;
  min-width: 20px;
}
.opt.user-picked { background: #e6eef6; border-left-color: #1e3a5f; color: #1e3a5f; font-weight: 600; }
.opt.user-wrong { background: #fae8e6; border-left-color: #c53030; color: #9b2c2c; }
.opt.correct { background: #1e3a5f; color: #f7f3ea; border-color: #1e3a5f; font-weight: 600; }
.opt.correct .opt-letter { color: #fbd38d; }
.ans-banner {
  margin-top: 18px;
  padding: 11px 15px;
  background: #1e3a5f;
  color: #f7f3ea;
  font-family: "Inter", sans-serif;
  font-size: 13.5px;
  font-weight: 700;
}
.expl-box {
  margin-top: 12px;
  padding: 14px 16px;
  border-left: 2px solid #c53030;
  background: #f0ebe0;
  font-family: "Inter", sans-serif;
  font-size: 14px;
  line-height: 1.6;
}
.card.nightMode .expl-box { background: #292622; }
.fig-box img, details.orig-scan img { border: 1px solid #c8beaa; padding: 6px; }
""",
    },

    "10_macintosh_1984": {
        "num": "10",
        "slug": "10_macintosh_1984",
        "name": "Macintosh System 1.0 (1984 1-Bit)",
        "tagline": "Susan Kare 1-bit pixel desktop • Authentic dithered checkerboard wallpaper, 6-stripe title bar & inverse-video highlight",
        "accent": "#000000",
        "default_dark": False,
        "layout": "mac1984",
        "css": BASE_RESET_CSS + """
.card, .card.nightMode {
  background-color: #ffffff;
  background-image:
    linear-gradient(45deg, #000 25%, transparent 25%),
    linear-gradient(-45deg, #000 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, #000 75%),
    linear-gradient(-45deg, transparent 75%, #000 75%);
  background-size: 4px 4px;
  background-position: 0 0, 0 2px, 2px -2px, -2px 0;
  color: #000000;
  font-family: "Space Mono", monospace;
}
.mac-win {
  max-width: 710px;
  margin: 0 auto;
  background: #ffffff;
  border: 2px solid #000000;
  box-shadow: 4px 4px 0px #000000;
  color: #000000;
}
.mac-titlebar {
  height: 28px;
  border-bottom: 2px solid #000000;
  background: repeating-linear-gradient(
    0deg,
    #ffffff 0px,
    #ffffff 2px,
    #000000 2px,
    #000000 4px
  );
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 10px;
}
.mac-close {
  width: 14px;
  height: 14px;
  background: #ffffff;
  border: 2px solid #000000;
  box-shadow: 0 0 0 2px #ffffff;
}
.mac-title-plaque {
  background: #ffffff;
  padding: 1px 12px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: -0.02em;
}
.mac-subbar {
  display: flex;
  justify-content: space-between;
  padding: 5px 14px;
  border-bottom: 2px solid #000000;
  font-size: 11px;
  background: #ffffff;
}
.mac-content { padding: 18px 20px 22px; background: #ffffff; }
.stem { font-size: 15px; font-weight: 700; line-height: 1.55; margin-bottom: 16px; }
.blank-slot { display: inline-block; min-width: 84px; border-bottom: 2px solid #000000; color: transparent; }
.blank-filled { background: #000000; color: #ffffff; padding: 1px 7px; font-weight: 700; }
.options { display: flex; flex-direction: column; gap: 6px; }
.opt {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 11px;
  border: 2px solid #000000;
  background: #ffffff;
  color: #000000;
  font-size: 13.5px;
}
.opt:hover, .opt.user-picked {
  background: #000000;
  color: #ffffff;
}
.opt-letter {
  font-weight: 700;
  min-width: 28px;
}
.opt-letter::before { content: "("; }
.opt-letter::after { content: ")"; }
.opt.user-wrong {
  background: #ffffff;
  color: #000000;
  text-decoration: line-through;
  border-style: dashed;
}
.opt.correct {
  background: #000000;
  color: #ffffff;
  font-weight: 700;
  box-shadow: 3px 3px 0px #000000;
  outline: 2px solid #ffffff;
  outline-offset: -5px;
}
.ans-banner {
  margin-top: 16px;
  padding: 10px 12px;
  border: 2px solid #000000;
  background: #000000;
  color: #ffffff;
  font-size: 12.5px;
  font-weight: 700;
}
.expl-box {
  margin-top: 12px;
  padding: 12px 14px;
  border: 2px solid #000000;
  background: #ffffff;
  font-size: 13px;
  line-height: 1.55;
}
.fig-box img, details.orig-scan img { border: 2px solid #000000; padding: 6px; }
""",
    },
}

THEMES: Dict[str, dict] = {}
for _k, _v in RAW_THEMES.items():
    _entry = dict(_v)
    _entry["raw_showcase_css"] = _v["css"]
    _entry["css"] = GOOGLE_FONTS_IMPORT + HOST_VIEWPORT_RESET_CSS + _convert_card_selectors_to_sf_canvas(_v["css"])
    THEMES[_k] = _entry


def _build_layout_shell(layout: str, front_inner: str, back_inner: str, scan_open_attr: str) -> Tuple[str, str]:
    """Exact 1-to-1 structural DOM shells matching theme_showcase.html across all 10 themes."""
    if layout == "swiss":
        qfmt = f"""
<div class="swiss-sheet">
  <div class="swiss-topbar">
    <span><i class="swiss-red-dot"></i>SEMESTRE FILTRO // ARCHIVIO DIDATTICO</span>
    <span>+ PAG. {{{{BookPage}}}} +</span>
  </div>
  <div class="swiss-grid">
    <div class="swiss-rail">
      <div class="swiss-big-num">{{{{QuestionNum}}}}</div>
      <div class="swiss-meta-stack">
        <strong>{{{{SubjectCode}}}}</strong><br>
        CAP. {{{{ChapterNum}}}}<br>
        {{{{QuizTypeLabel}}}}
      </div>
    </div>
    <div class="swiss-main">
      {front_inner}
    </div>
  </div>
</div>"""
        afmt = f"""
<div class="swiss-sheet">
  <div class="swiss-topbar">
    <span><i class="swiss-red-dot"></i>SEMESTRE FILTRO // SOLUZIONE VERIFICATA</span>
    <span>+ PAG. {{{{BookPage}}}} +</span>
  </div>
  <div class="swiss-grid">
    <div class="swiss-rail">
      <div class="swiss-big-num">{{{{QuestionNum}}}}</div>
      <div class="swiss-meta-stack">
        <strong>{{{{SubjectCode}}}}</strong><br>
        CAP. {{{{ChapterNum}}}}<br>
        {{{{QuizTypeLabel}}}}
      </div>
    </div>
    <div class="swiss-main">
      {back_inner}
    </div>
  </div>
</div>"""
        return qfmt, afmt

    if layout == "te_hardware":
        qfmt = f"""
<div class="te-chassis">
  <div class="te-screw-row">
    <span class="te-screw">⊕</span>
    <span><i class="te-orange-led"></i>OP-DECK // {{{{SubjectCode}}}}-C{{{{ChapterNum}}}} • {{{{QuizTypeLabel}}}}</span>
    <span class="te-screw">⊕</span>
  </div>
  <div class="te-screen">
    <div class="te-screen-hud">
      <span>CH.{{{{ChapterNum}}}} // {{{{ChapterTitle}}}}</span>
      <span>Q#{{{{QuestionNum}}}} [P.{{{{BookPage}}}}]</span>
    </div>
    <div class="stem">{{{{FrontStemHTML}}}}</div>
    {{{{#FigureHTML}}}}<div class="fig-box">{{{{FigureHTML}}}}</div>{{{{/FigureHTML}}}}
  </div>
  {{{{FrontOptionsHTML}}}}
  {{{{#QuestionScanHTML}}}}<details class="orig-scan"{scan_open_attr}><summary>Scansione originale della domanda (p. {{{{BookPage}}}})</summary>{{{{QuestionScanHTML}}}}</details>{{{{/QuestionScanHTML}}}}
</div>"""
        afmt = f"""
<div class="te-chassis">
  <div class="te-screw-row">
    <span class="te-screw">⊕</span>
    <span><i class="te-orange-led"></i>OP-DECK // VERIFIED OUTPUT • Q#{{{{QuestionNum}}}}</span>
    <span class="te-screw">⊕</span>
  </div>
  <div class="te-screen">
    <div class="te-screen-hud">
      <span>CH.{{{{ChapterNum}}}} // {{{{ChapterTitle}}}}</span>
      <span>Q#{{{{QuestionNum}}}} [P.{{{{BookPage}}}}]</span>
    </div>
    <div class="stem">{{{{BackStemHTML}}}}</div>
    {{{{#FigureHTML}}}}<div class="fig-box">{{{{FigureHTML}}}}</div>{{{{/FigureHTML}}}}
  </div>
  {{{{BackOptionsHTML}}}}
  <div class="ans-banner">{{{{AnswerBannerHTML}}}}</div>
  {{{{#ExplanationHTML}}}}<div class="expl-box"><strong>Spiegazione:</strong> {{{{ExplanationHTML}}}}</div>{{{{/ExplanationHTML}}}}
  {{{{#QuestionScanHTML}}}}<details class="orig-scan"{scan_open_attr}><summary>Scansione originale della domanda (p. {{{{BookPage}}}})</summary>{{{{QuestionScanHTML}}}}</details>{{{{/QuestionScanHTML}}}}
  {{{{#SolutionScanHTML}}}}<details class="orig-scan"><summary>Risoluzione grafica originale del libro</summary>{{{{SolutionScanHTML}}}}</details>{{{{/SolutionScanHTML}}}}
</div>"""
        return qfmt, afmt

    if layout == "nerv":
        qfmt = f"""
<div class="nerv-frame">
  <div class="nerv-hazard"></div>
  <div class="nerv-head">
    <span><span class="nerv-tag">MAGI.SYS</span> // {{{{SubjectCode}}}} • CAP.{{{{ChapterNum}}}}</span>
    <span>[{{{{QuizTypeLabel}}}} #{{{{QuestionNum}}}} // P.{{{{BookPage}}}}]</span>
  </div>
  <div class="nerv-body">{front_inner}</div>
</div>"""
        afmt = f"""
<div class="nerv-frame">
  <div class="nerv-hazard"></div>
  <div class="nerv-head">
    <span><span class="nerv-tag">MAGI.OK</span> // PATTERN CONFIRMED</span>
    <span>[{{{{QuizTypeLabel}}}} #{{{{QuestionNum}}}} // P.{{{{BookPage}}}}]</span>
  </div>
  <div class="nerv-body">{back_inner}</div>
</div>"""
        return qfmt, afmt

    if layout == "editorial":
        qfmt = f"""
<div class="ed-page">
  <div class="ed-masthead">
    <span class="ed-kicker">{{{{Subject}}}}</span> &nbsp;•&nbsp; CAPITOLO {{{{ChapterNum}}}} ({{{{ChapterTitle}}}}) &nbsp;•&nbsp; N° {{{{QuestionNum}}}}
  </div>
  {front_inner}
</div>"""
        afmt = f"""
<div class="ed-page">
  <div class="ed-masthead">
    <span class="ed-kicker">{{{{Subject}}}}</span> &nbsp;•&nbsp; CAPITOLO {{{{ChapterNum}}}} ({{{{ChapterTitle}}}}) &nbsp;•&nbsp; SOLUZIONE N° {{{{QuestionNum}}}}
  </div>
  {back_inner}
</div>"""
        return qfmt, afmt

    if layout == "blueprint":
        qfmt = f"""
<div class="bp-sheet">
  <div class="bp-titleblock">
    <div class="bp-cell"><strong>TAV. {{{{SubjectCode}}}}-{{{{ChapterNum}}}}</strong></div>
    <div class="bp-cell">{{{{ChapterTitle}}}} — {{{{QuizTypeLabel}}}}</div>
    <div class="bp-cell">N° {{{{QuestionNum}}}} (P.{{{{BookPage}}}})</div>
  </div>
  <div class="bp-body">{front_inner}</div>
</div>"""
        afmt = f"""
<div class="bp-sheet">
  <div class="bp-titleblock">
    <div class="bp-cell"><strong>TAV. {{{{SubjectCode}}}}-{{{{ChapterNum}}}}</strong></div>
    <div class="bp-cell">{{{{ChapterTitle}}}} — VERIFICA</div>
    <div class="bp-cell">N° {{{{QuestionNum}}}} (P.{{{{BookPage}}}})</div>
  </div>
  <div class="bp-body">{back_inner}</div>
</div>"""
        return qfmt, afmt

    if layout == "split":
        qfmt = f"""
<div class="split-shell">
  <div class="split-left-well">
    <div>
      <div class="meta">
        <span class="badge subj-{{{{SubjectCode}}}}">{{{{Subject}}}}</span>
        <span class="meta-dim">Cap. {{{{ChapterNum}}}} — {{{{ChapterTitle}}}}</span>
        <span class="meta-dim">• #{{{{QuestionNum}}}} (p. {{{{BookPage}}}})</span>
      </div>
      <div class="stem">{{{{FrontStemHTML}}}}</div>
      {{{{#FigureHTML}}}}<div class="fig-box">{{{{FigureHTML}}}}</div>{{{{/FigureHTML}}}}
    </div>
    {{{{#QuestionScanHTML}}}}<details class="orig-scan"{scan_open_attr}><summary>Scansione originale della domanda (p. {{{{BookPage}}}})</summary>{{{{QuestionScanHTML}}}}</details>{{{{/QuestionScanHTML}}}}
  </div>
  <div class="split-right-well">
    {{{{FrontOptionsHTML}}}}
  </div>
</div>"""
        afmt = f"""
<div class="split-shell">
  <div class="split-left-well">
    <div>
      <div class="meta">
        <span class="badge subj-{{{{SubjectCode}}}}">{{{{Subject}}}}</span>
        <span class="meta-dim">Cap. {{{{ChapterNum}}}} — {{{{ChapterTitle}}}}</span>
        <span class="meta-dim">• #{{{{QuestionNum}}}} (p. {{{{BookPage}}}})</span>
      </div>
      <div class="stem">{{{{BackStemHTML}}}}</div>
      {{{{#FigureHTML}}}}<div class="fig-box">{{{{FigureHTML}}}}</div>{{{{/FigureHTML}}}}
    </div>
    {{{{#QuestionScanHTML}}}}<details class="orig-scan"{scan_open_attr}><summary>Scansione originale della domanda (p. {{{{BookPage}}}})</summary>{{{{QuestionScanHTML}}}}</details>{{{{/QuestionScanHTML}}}}
  </div>
  <div class="split-right-well">
    {{{{BackOptionsHTML}}}}
    <div class="ans-banner">{{{{AnswerBannerHTML}}}}</div>
    {{{{#ExplanationHTML}}}}<div class="expl-box"><strong>Spiegazione:</strong> {{{{ExplanationHTML}}}}</div>{{{{/ExplanationHTML}}}}
    {{{{#SolutionScanHTML}}}}<details class="orig-scan"><summary>Risoluzione grafica originale del libro</summary>{{{{SolutionScanHTML}}}}</details>{{{{/SolutionScanHTML}}}}
  </div>
</div>"""
        return qfmt, afmt

    if layout == "washi":
        qfmt = f"""
<div class="washi-card">
  <div class="washi-top">
    <div class="washi-meta">
      <div style="font-weight:700;color:inherit;font-size:13px;">{{{{Subject}}}} — Cap. {{{{ChapterNum}}}}: {{{{ChapterTitle}}}}</div>
      <div>{{{{QuizTypeLabel}}}} • Quesito #{{{{QuestionNum}}}} ( Pag. {{{{BookPage}}}} )</div>
    </div>
    <div class="hanko-seal"><span>{{{{SubjectCode}}}}</span><span>印</span></div>
  </div>
  {front_inner}
</div>"""
        afmt = f"""
<div class="washi-card">
  <div class="washi-top">
    <div class="washi-meta">
      <div style="font-weight:700;color:inherit;font-size:13px;">{{{{Subject}}}} — Cap. {{{{ChapterNum}}}}: {{{{ChapterTitle}}}}</div>
      <div>{{{{QuizTypeLabel}}}} • Soluzione #{{{{QuestionNum}}}} ( Pag. {{{{BookPage}}}} )</div>
    </div>
    <div class="hanko-seal"><span>{{{{SubjectCode}}}}</span><span>正解</span></div>
  </div>
  {back_inner}
</div>"""
        return qfmt, afmt

    if layout == "mac1984":
        qfmt = f"""
<div class="mac-win">
  <div class="mac-titlebar">
    <div class="mac-close"></div>
    <div class="mac-title-plaque">{{{{SubjectCode}}}} — Quesito #{{{{QuestionNum}}}}.doc</div>
    <div style="width:14px;"></div>
  </div>
  <div class="mac-subbar">
    <span>Cap. {{{{ChapterNum}}}}: {{{{ChapterTitle}}}}</span>
    <span>Pag. {{{{BookPage}}}}</span>
  </div>
  <div class="mac-content">{front_inner}</div>
</div>"""
        afmt = f"""
<div class="mac-win">
  <div class="mac-titlebar">
    <div class="mac-close"></div>
    <div class="mac-title-plaque">{{{{SubjectCode}}}} — Soluzione #{{{{QuestionNum}}}}.doc</div>
    <div style="width:14px;"></div>
  </div>
  <div class="mac-subbar">
    <span>Cap. {{{{ChapterNum}}}}: {{{{ChapterTitle}}}}</span>
    <span>Pag. {{{{BookPage}}}}</span>
  </div>
  <div class="mac-content">{back_inner}</div>
</div>"""
        return qfmt, afmt

    # Exact "brutalist" (#04 Neo-Brutalist Risoprint Zine) and "standard" (#06 / #00) layout from theme_showcase.html!
    qfmt = f"""
<div class="wrap">
  <div class="meta">
    <span class="badge subj-{{{{SubjectCode}}}}">{{{{Subject}}}}</span>
    <span class="meta-dim">Cap. {{{{ChapterNum}}}} — {{{{ChapterTitle}}}}</span>
    <span class="meta-dim">• {{{{QuizTypeLabel}}}} #{{{{QuestionNum}}}} (p. {{{{BookPage}}}})</span>
  </div>
  {front_inner}
</div>"""
    afmt = f"""
<div class="wrap">
  <div class="meta">
    <span class="badge subj-{{{{SubjectCode}}}}">{{{{Subject}}}}</span>
    <span class="meta-dim">Cap. {{{{ChapterNum}}}} — {{{{ChapterTitle}}}}</span>
    <span class="meta-dim">• {{{{QuizTypeLabel}}}} #{{{{QuestionNum}}}} (p. {{{{BookPage}}}})</span>
  </div>
  {back_inner}
</div>"""
    return qfmt, afmt


# ==============================================================================
# SCOPED MULTI-THEME CSS & LIVE NUMBER SWITCHER FOR Semestre_Filtro_Complete.apkg
# ==============================================================================


def _scope_css_block(css_body: str, num: str) -> str:
    """Scope every selector of a theme cleanly under html[data-sf-theme="XX"]."""
    cleaned = re.sub(r"/\*.*?\*/", "", _convert_card_selectors_to_sf_canvas(css_body), flags=re.S)
    cleaned = re.sub(r"@import\s+url\([^\)]*\)\s*;", "", cleaned)
    prefix = f'html[data-sf-theme="{num}"]'
    out = []
    pos = 0
    n = len(cleaned)
    while pos < n:
        while pos < n and cleaned[pos].isspace():
            pos += 1
        if pos >= n:
            break
        brace = cleaned.find("{", pos)
        if brace == -1:
            break
        prelude = cleaned[pos:brace].strip()
        depth = 1
        end = brace + 1
        while end < n and depth > 0:
            if cleaned[end] == "{":
                depth += 1
            elif cleaned[end] == "}":
                depth -= 1
            end += 1
        inner = cleaned[brace + 1 : end - 1]
        if prelude.startswith("@media"):
            out.append(f"{prelude} {{\n{_scope_css_block(inner, num)}\n}}")
        else:
            raw_sels = [p.strip() for p in prelude.split(",") if p.strip()]
            scoped_sels = ", ".join(f"{prefix} {s}" for s in raw_sels)
            out.append(f"{scoped_sels} {{ {inner.strip()} }}")
        pos = end
    return "\n".join(out)


SWITCHER_UI_CSS = """
/* Compact Theme Switcher Widget (ONLY present in Semestre_Filtro_Complete.apkg) */
.sf-theme-ui {
  position: fixed;
  top: 8px;
  right: 10px;
  z-index: 99999;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 5px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  user-select: none;
}
.sf-theme-bar {
  display: flex;
  align-items: center;
  gap: 3px;
  background: rgba(15, 23, 42, 0.86);
  color: #f8fafc;
  border: 1px solid rgba(255, 255, 255, 0.24);
  border-radius: 999px;
  padding: 3px;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.24);
}
.sf-num-btn {
  appearance: none;
  border: none;
  background: transparent;
  color: #cbd5e1;
  font-family: inherit;
  font-size: 11px;
  font-weight: 700;
  line-height: 1;
  padding: 4px 6px;
  border-radius: 999px;
  cursor: pointer;
  transition: background 0.12s ease, color 0.12s ease;
}
.sf-num-btn:hover {
  background: rgba(255, 255, 255, 0.16);
  color: #ffffff;
}
.sf-num-btn.is-active {
  background: #facc15;
  color: #111111;
}
.sf-theme-bar:not(.is-open) .sf-num-btn:not(.is-current-toggle) {
  display: none;
}
.sf-theme-bar:not(.is-open) {
  opacity: 0.78;
}
.sf-theme-bar:not(.is-open):hover,
.sf-theme-bar.is-open {
  opacity: 1;
}
.sf-theme-bar.is-open .is-current-toggle {
  display: none;
}
.sf-theme-toast {
  display: none;
  font-size: 10.5px;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: 6px;
  background: rgba(15, 23, 42, 0.9);
  color: #f8fafc;
  border: 1px solid rgba(255, 255, 255, 0.18);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  white-space: nowrap;
}
.sf-theme-ui.show-label .sf-theme-toast {
  display: block;
}
"""


def build_master_multitheme_bundle(default_css: str) -> Tuple[str, str, str]:
    """Build the complete all-in-one CSS + Front/Back templates WITH the compact `00`..`10`
    number switcher exclusively for `output/Semestre_Filtro_Complete.apkg`."""
    front_inner = """<div class="stem">{{FrontStemHTML}}</div>
  {{#FigureHTML}}<div class="fig-box">{{FigureHTML}}</div>{{/FigureHTML}}
  {{FrontOptionsHTML}}
  {{#QuestionScanHTML}}<details class="orig-scan"><summary>Scansione originale della domanda (p. {{BookPage}})</summary>{{QuestionScanHTML}}</details>{{/QuestionScanHTML}}"""

    back_inner = """<div class="stem">{{BackStemHTML}}</div>
  {{#FigureHTML}}<div class="fig-box">{{FigureHTML}}</div>{{/FigureHTML}}
  {{BackOptionsHTML}}
  <div class="ans-banner">{{AnswerBannerHTML}}</div>
  {{#ExplanationHTML}}<div class="expl-box"><strong>Spiegazione:</strong> {{ExplanationHTML}}</div>{{/ExplanationHTML}}
  {{#QuestionScanHTML}}<details class="orig-scan"><summary>Scansione originale della domanda (p. {{BookPage}})</summary>{{QuestionScanHTML}}</details>{{/QuestionScanHTML}}
  {{#SolutionScanHTML}}<details class="orig-scan"><summary>Risoluzione grafica originale del libro</summary>{{{{SolutionScanHTML}}}}</details>{{{{/SolutionScanHTML}}}}""".replace(
        "{{{{SolutionScanHTML}}}}", "{{SolutionScanHTML}}"
    ).replace(
        "{{{{/SolutionScanHTML}}}}", "{{/SolutionScanHTML}}"
    )

    css_sections = [GOOGLE_FONTS_IMPORT, HOST_VIEWPORT_RESET_CSS, _scope_css_block(default_css, "00")]
    q_tpls = []
    a_tpls = []

    q0, a0 = _build_layout_shell("standard", front_inner, back_inner, "")
    q_tpls.append(f'<template id="sf-t00">{q0}</template>')
    a_tpls.append(f'<template id="sf-t00">{a0}</template>')

    theme_meta_js = [("00", "00 · Classico Pulito (Default)")]
    default_dark_map = {"00": "auto"}
    for _, tmeta in THEMES.items():
        num = tmeta["num"]
        css_sections.append(_scope_css_block(tmeta["raw_showcase_css"], num))
        qt, at = _build_layout_shell(tmeta["layout"], front_inner, back_inner, "")
        q_tpls.append(f'<template id="sf-t{num}">{qt}</template>')
        a_tpls.append(f'<template id="sf-t{num}">{at}</template>')
        theme_meta_js.append((num, f"{num} · {tmeta['name']}"))
        default_dark_map[num] = bool(tmeta["default_dark"])

    css_sections.append(SWITCHER_UI_CSS)
    full_css = "\n\n".join(css_sections)

    labels_json = json.dumps(dict(theme_meta_js), ensure_ascii=False)
    nums_json = json.dumps([n for n, _ in theme_meta_js])
    dark_json = json.dumps(default_dark_map)

    shared_runtime_js = f"""
(function() {{
  var NUMS = {nums_json};
  var LABELS = {labels_json};
  var DEFAULT_DARK = {dark_json};
  var canvas = document.getElementById('sf-canvas');
  var side = canvas.getAttribute('data-side');
  var itemId = "{{{{ItemID}}}}";

  function readTheme() {{
    try {{ if (window._sfTheme && LABELS[window._sfTheme]) return window._sfTheme; }} catch(e) {{}}
    try {{ if (window.parent && window.parent._sfTheme && LABELS[window.parent._sfTheme]) return window.parent._sfTheme; }} catch(e) {{}}
    try {{ var ls = localStorage.getItem('sf_theme'); if (ls && LABELS[ls]) return ls; }} catch(e) {{}}
    try {{ var ss = sessionStorage.getItem('sf_theme'); if (ss && LABELS[ss]) return ss; }} catch(e) {{}}
    var m = (document.cookie || '').match(/(?:^|;\\s*)sf_theme=([0-9]{{2}})/);
    return (m && LABELS[m[1]]) ? m[1] : '00';
  }}

  function saveTheme(n) {{
    try {{ window._sfTheme = n; }} catch(e) {{}}
    try {{ if (window.parent) window.parent._sfTheme = n; }} catch(e) {{}}
    try {{ localStorage.setItem('sf_theme', n); }} catch(e) {{}}
    try {{ sessionStorage.setItem('sf_theme', n); }} catch(e) {{}}
    try {{ document.cookie = 'sf_theme=' + n + ';path=/;max-age=31536000;SameSite=Lax'; }} catch(e) {{}}
  }}

  function bindCardInteractions() {{
    var opts = canvas.querySelectorAll('.opt');
    var picked = null;
    try {{ picked = sessionStorage.getItem('pick_' + itemId); }} catch(e) {{}}
    opts.forEach(function(el, idx) {{
      var lEl = el.querySelector('.opt-letter');
      var letter = lEl ? lEl.textContent.replace(/[().✓\\s]/g, '') : String.fromCharCode(65 + idx);
      if (side === 'front') {{
        if (picked === letter) el.classList.add('user-picked');
        el.addEventListener('click', function() {{
          picked = letter;
          try {{ sessionStorage.setItem('pick_' + itemId, letter); }} catch(e) {{}}
          opts.forEach(function(o) {{ o.classList.remove('user-picked'); }});
          el.classList.add('user-picked');
        }});
      }} else if (picked && letter === picked && !el.classList.contains('correct')) {{
        el.classList.add('user-wrong');
      }}
    }});
  }}

  var cur = readTheme();

  function syncCanvasSurface() {{
    var d = DEFAULT_DARK[cur];
    var useDark = (d === 'auto')
      ? !!(document.body && (document.body.classList.contains('nightMode') || document.body.classList.contains('night_mode')))
      : !!d;
    canvas.className = useDark ? 'sf-canvas sf-dark' : 'sf-canvas';
  }}

  function applyTheme(n, showToast) {{
    if (!LABELS[n]) n = '00';
    cur = n;
    saveTheme(n);
    document.documentElement.setAttribute('data-sf-theme', n);
    syncCanvasSurface();
    var tpl = document.getElementById('sf-t' + n);
    if (tpl && canvas) {{
      canvas.innerHTML = '';
      canvas.appendChild(tpl.content.cloneNode(true));
      bindCardInteractions();
    }}
    var ui = document.getElementById('sf-theme-ui');
    if (ui) {{
      var tog = ui.querySelector('.is-current-toggle');
      if (tog) tog.textContent = n;
      ui.querySelectorAll('.sf-choice').forEach(function(b) {{
        b.classList.toggle('is-active', b.getAttribute('data-num') === n);
      }});
      var toast = ui.querySelector('.sf-theme-toast');
      if (toast) toast.textContent = LABELS[n];
      if (showToast) {{
        ui.classList.add('show-label');
        clearTimeout(ui._toastTimer);
        ui._toastTimer = setTimeout(function() {{
          if (!ui.querySelector('.sf-theme-bar').classList.contains('is-open')) {{
            ui.classList.remove('show-label');
          }}
        }}, 1400);
      }}
    }}
  }}

  var ui = document.getElementById('sf-theme-ui');
  if (ui) {{
    var bar = ui.querySelector('.sf-theme-bar');
    var tog = ui.querySelector('.is-current-toggle');
    tog.addEventListener('click', function(ev) {{
      ev.stopPropagation();
      bar.classList.add('is-open');
      ui.classList.add('show-label');
    }});
    tog.addEventListener('contextmenu', function(ev) {{
      ev.preventDefault();
      var nextIdx = (NUMS.indexOf(cur) + 1) % NUMS.length;
      applyTheme(NUMS[nextIdx], true);
    }});
    ui.querySelectorAll('.sf-choice').forEach(function(btn) {{
      btn.addEventListener('click', function(ev) {{
        ev.stopPropagation();
        applyTheme(btn.getAttribute('data-num'), true);
      }});
    }});
    document.addEventListener('click', function(ev) {{
      if (bar.classList.contains('is-open') && !ui.contains(ev.target)) {{
        bar.classList.remove('is-open');
        ui.classList.remove('show-label');
      }}
    }});
  }}

  if (window.MutationObserver && document.body) {{
    new MutationObserver(syncCanvasSurface).observe(document.body, {{ attributes: true, attributeFilter: ['class'] }});
  }}
  if (side === 'front' && window._sfLastItem !== itemId) {{
    window._sfLastItem = itemId;
    try {{ sessionStorage.removeItem('pick_' + itemId); }} catch(e) {{}}
  }}
  applyTheme(cur, false);
}})();"""

    switcher_html = (
        '<div id="sf-theme-ui" class="sf-theme-ui">'
        '<div class="sf-theme-bar">'
        '<button type="button" class="sf-num-btn is-current-toggle" title="Cambia tema grafico (00–10)">00</button>'
        + "".join(
            f'<button type="button" class="sf-num-btn sf-choice" data-num="{n}" title="{lbl}">{n}</button>'
            for n, lbl in theme_meta_js
        )
        + '</div><div class="sf-theme-toast"></div></div>'
    )

    master_qfmt = (
        GOOGLE_FONTS_LINK_HTML
        + switcher_html
        + f'<div id="sf-canvas" class="sf-canvas" data-side="front">{q0}</div>\n'
        + "\n".join(q_tpls)
        + f"\n<script>{shared_runtime_js}</script>"
    )
    master_afmt = (
        GOOGLE_FONTS_LINK_HTML
        + switcher_html
        + f'<div id="sf-canvas" class="sf-canvas" data-side="back">{a0}</div>\n'
        + "\n".join(a_tpls)
        + f"\n<script>{shared_runtime_js}</script>"
    )
    return full_css, master_qfmt, master_afmt


def build_card_templates(
    theme_key: str,
    instant_grade_front: bool = False,
    show_timer: bool = False,
    type_in_completamento: bool = False,
    auto_open_scan: bool = False,
) -> Tuple[str, str]:
    """Generate exact theme_showcase.html HTML + full-viewport `.sf-canvas` wrapper (NO switcher UI)."""
    theme = THEMES[theme_key]
    scan_open_attr = " open" if auto_open_scan else ""
    canvas_cls = "sf-canvas sf-dark" if theme.get("default_dark") else "sf-canvas"

    front_inner = f"""<div class="stem">{{{{FrontStemHTML}}}}</div>
  {{{{#FigureHTML}}}}<div class="fig-box">{{{{FigureHTML}}}}</div>{{{{/FigureHTML}}}}
  {{{{FrontOptionsHTML}}}}
  {{{{#QuestionScanHTML}}}}<details class="orig-scan"{scan_open_attr}><summary>Scansione originale della domanda (p. {{{{BookPage}}}})</summary>{{{{QuestionScanHTML}}}}</details>{{{{/QuestionScanHTML}}}}"""

    back_inner = f"""<div class="stem">{{{{BackStemHTML}}}}</div>
  {{{{#FigureHTML}}}}<div class="fig-box">{{{{FigureHTML}}}}</div>{{{{/FigureHTML}}}}
  {{{{BackOptionsHTML}}}}
  <div class="ans-banner">{{{{AnswerBannerHTML}}}}</div>
  {{{{#ExplanationHTML}}}}<div class="expl-box"><strong>Spiegazione:</strong> {{{{ExplanationHTML}}}}</div>{{{{/ExplanationHTML}}}}
  {{{{#QuestionScanHTML}}}}<details class="orig-scan"{scan_open_attr}><summary>Scansione originale della domanda (p. {{{{BookPage}}}})</summary>{{{{QuestionScanHTML}}}}</details>{{{{/QuestionScanHTML}}}}
  {{{{#SolutionScanHTML}}}}<details class="orig-scan"><summary>Risoluzione grafica originale del libro</summary>{{{{SolutionScanHTML}}}}</details>{{{{/SolutionScanHTML}}}}"""

    q_shell, a_shell = _build_layout_shell(theme.get("layout", "standard"), front_inner, back_inner, scan_open_attr)
    instant_js = "true" if instant_grade_front else "false"

    front_script = f"""
<span id="ans-hidden-ref" style="display:none;">{{{{AnswerBannerHTML}}}}</span>
<script>
(function() {{
  document.documentElement.removeAttribute('data-sf-theme');
  var itemId = "{{{{ItemID}}}}";
  var instantGrade = {instant_js};
  var ansRef = document.getElementById('ans-hidden-ref');
  var ansBanner = ansRef ? ansRef.textContent : "";
  try {{ sessionStorage.removeItem("pick_" + itemId); }} catch(e) {{}}
  var opts = document.querySelectorAll('.opt');
  opts.forEach(function(el, idx) {{
    var lEl = el.querySelector('.opt-letter');
    var letter = lEl ? lEl.textContent.replace(/[()\\s]/g, '') : String.fromCharCode(65 + idx);
    el.addEventListener('click', function() {{
      try {{ sessionStorage.setItem("pick_" + itemId, letter); }} catch(e) {{}}
      opts.forEach(function(o) {{ o.classList.remove('user-picked', 'correct', 'user-wrong'); }});
      if (instantGrade && ansBanner) {{
        var m = ansBanner.match(/Risposta corretta:\\s*([A-E])/);
        var corr = m ? m[1] : "";
        opts.forEach(function(o) {{
          var olEl = o.querySelector('.opt-letter');
          var ol = olEl ? olEl.textContent.replace(/[()\\s]/g, '') : "";
          if (ol === corr) o.classList.add('correct');
        }});
        if (letter !== corr) el.classList.add('user-wrong');
      }} else {{
        el.classList.add('user-picked');
      }}
    }});
  }});
}})();
</script>"""

    back_script = """
<script>
(function() {
  document.documentElement.removeAttribute('data-sf-theme');
  var itemId = "{{ItemID}}";
  try {
    var picked = sessionStorage.getItem("pick_" + itemId);
    if (picked) {
      document.querySelectorAll('.opt').forEach(function(o) {
        var l = o.querySelector('.opt-letter');
        var txt = l ? l.textContent.replace(/[()\\s]/g, '') : '';
        if (txt === picked && !o.classList.contains('correct')) {
          o.classList.add('user-wrong');
        }
      });
    }
  } catch(e) {}
})();
</script>"""

    return (
        f'{GOOGLE_FONTS_LINK_HTML}<div id="sf-canvas" class="{canvas_cls}">{q_shell}</div>{front_script}',
        f'{GOOGLE_FONTS_LINK_HTML}<div id="sf-canvas" class="{canvas_cls}">{a_shell}</div>{back_script}',
    )


def repackage_apkg_with_theme(
    source_apkg: Path,
    dest_apkg: Path,
    theme_key: str,
    instant_grade_front: bool = False,
    show_timer: bool = False,
    type_in_completamento: bool = False,
    auto_open_scan: bool = False,
    custom_css_append: str = "",
) -> Path:
    """Build a standalone single-theme .apkg (NO theme switcher widget) matching theme_showcase.html
    pixel-for-pixel, with independent Anki `model_id`, subdeck IDs, and note GUIDs."""
    theme = THEMES[theme_key]
    qfmt, afmt = build_card_templates(
        theme_key=theme_key,
        instant_grade_front=instant_grade_front,
        show_timer=show_timer,
        type_in_completamento=type_in_completamento,
        auto_open_scan=auto_open_scan,
    )
    final_css = theme["css"] + ("\n" + custom_css_append if custom_css_append else "")
    new_mid = _stable_id(f"SemestreFiltro-ThemeModel-v2-{theme_key}")
    now_sec = int(time.time()) + 30
    root_label = f"Semestre Filtro [{theme['num']} {theme['name']}]"

    dest_apkg.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpd:
        tmp_db = Path(tmpd) / "collection.anki2"
        with zipfile.ZipFile(source_apkg, "r") as zin:
            tmp_db.write_bytes(zin.read("collection.anki2"))

            conn = sqlite3.connect(str(tmp_db))
            cur = conn.cursor()
            models_raw, decks_raw = cur.execute("SELECT models, decks FROM col").fetchone()
            models = json.loads(models_raw)
            decks = json.loads(decks_raw)

            new_models = {}
            for _, mobj in models.items():
                mobj["id"] = new_mid
                mobj["name"] = root_label
                mobj["mod"] = now_sec
                mobj["usn"] = -1
                mobj["css"] = final_css
                mobj["tmpls"][0]["qfmt"] = qfmt
                mobj["tmpls"][0]["afmt"] = afmt
                new_models[str(new_mid)] = mobj

            did_remap: Dict[int, int] = {}
            new_decks = {}
            for dk_str, dobj in decks.items():
                old_did = int(dk_str)
                if old_did == 1:
                    new_decks["1"] = dobj
                    continue
                old_name = dobj["name"]
                new_name = re.sub(r"^Semestre Filtro(?=::|$)", root_label, old_name)
                new_did = _stable_id(f"deck::{theme_key}::{new_name}")
                did_remap[old_did] = new_did
                dobj["id"] = new_did
                dobj["name"] = new_name
                dobj["mod"] = now_sec
                dobj["usn"] = -1
                new_decks[str(new_did)] = dobj

            cur.execute(
                "UPDATE col SET models = ?, decks = ?, mod = ?",
                (json.dumps(new_models, ensure_ascii=False), json.dumps(new_decks, ensure_ascii=False), now_sec * 1000),
            )
            cur.execute("UPDATE notes SET mid = ?, mod = ?, usn = -1", (new_mid, now_sec))
            note_rows = cur.execute("SELECT id, sfld FROM notes").fetchall()
            cur.executemany(
                "UPDATE notes SET guid = ? WHERE id = ?",
                [(genanki.guid_for(f"sf-v2-{theme_key}", sfld), nid) for nid, sfld in note_rows],
            )
            for old_did, new_did in did_remap.items():
                cur.execute("UPDATE cards SET did = ?, mod = ?, usn = -1 WHERE did = ?", (new_did, now_sec, old_did))

            conn.commit()
            conn.close()

            with zipfile.ZipFile(dest_apkg, "w") as zout:
                zout.writestr("collection.anki2", tmp_db.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
                for info in zin.infolist():
                    if info.filename == "collection.anki2":
                        continue
                    data = zin.read(info.filename)
                    ctype = zipfile.ZIP_STORED if info.filename.isdigit() else zipfile.ZIP_DEFLATED
                    zout.writestr(info.filename, data, compress_type=ctype, compresslevel=9 if ctype == zipfile.ZIP_DEFLATED else None)

    return dest_apkg


def build_lightweight_theme_switcher_apkg(
    source_apkg: Path,
    dest_apkg: Path,
    theme_key: str,
    instant_grade_front: bool = False,
    show_timer: bool = False,
    type_in_completamento: bool = False,
    auto_open_scan: bool = False,
    custom_css_append: str = "",
) -> Path:
    """Create a ~15 KB single-theme Note-Type updater .apkg matching theme_showcase.html."""
    theme = THEMES[theme_key]
    qfmt, afmt = build_card_templates(
        theme_key=theme_key,
        instant_grade_front=instant_grade_front,
        show_timer=show_timer,
        type_in_completamento=type_in_completamento,
        auto_open_scan=auto_open_scan,
    )
    final_css = theme["css"] + ("\n" + custom_css_append if custom_css_append else "")
    newer_mod = int(time.time()) + 3600

    dest_apkg.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpd:
        tmp_db = Path(tmpd) / "collection.anki2"
        with zipfile.ZipFile(source_apkg, "r") as zin:
            tmp_db.write_bytes(zin.read("collection.anki2"))

        conn = sqlite3.connect(str(tmp_db))
        cur = conn.cursor()
        models = json.loads(cur.execute("SELECT models FROM col").fetchone()[0])
        for _, mobj in models.items():
            mobj["mod"] = newer_mod
            mobj["usn"] = -1
            mobj["css"] = final_css
            mobj["tmpls"][0]["qfmt"] = qfmt
            mobj["tmpls"][0]["afmt"] = afmt
        cur.execute("UPDATE col SET models = ?, mod = ?", (json.dumps(models, ensure_ascii=False), newer_mod * 1000))
        first_nid = cur.execute("SELECT id FROM notes LIMIT 1").fetchone()[0]
        cur.execute("DELETE FROM notes WHERE id != ?", (first_nid,))
        cur.execute("DELETE FROM cards WHERE nid != ?", (first_nid,))
        conn.commit()
        cur.execute("VACUUM")
        conn.close()

        with zipfile.ZipFile(dest_apkg, "w") as zout:
            zout.writestr("collection.anki2", tmp_db.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
            zout.writestr("media", "{}", compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    return dest_apkg
