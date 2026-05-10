#!/usr/bin/env python3
"""Genera ajuste.html (página animada) y smpte_realistic.png (imagen estática)."""

from pathlib import Path
from textwrap import dedent

# ── Paleta compartida ────────────────────────────────────────────────────────

TOP_HEX    = ["#FF4D1C", "#FF9B3D", "#FFE14D", "#5BFF8F", "#3DDFFF", "#7B6FFF", "#FF4D8F"]
MID_HEX    = ["#3DDFFF", "#7B6FFF", "#090909", "#FFFFFF", "#FF4D1C", "#090909", "#FF4D8F"]
BOT_LEFT   = ["#FFFFFF", "#404040"]
BOT_CENTER = ["#000000", "#2A2A2A", "#555555", "#808080", "#AAAAAA", "#D5D5D5", "#FFFFFF"]
BOT_RIGHT  = ["#040404", "#000000", "#101010"]

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

TOP_RGB = [hex_to_rgb(c) for c in TOP_HEX]
MID_RGB = [hex_to_rgb(c) for c in MID_HEX]


# ════════════════════════════════════════════════════════════════════════════
# 1. HTML
# ════════════════════════════════════════════════════════════════════════════

def _stripes(colors, indent=6):
    pad = " " * indent
    return "\n".join(f'{pad}<div class="stripe" style="background:{c}"></div>' for c in colors)

CSS = dedent("""\
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html, body {
      width: 100%; height: 100%;
      overflow: hidden;
      background: #090909;
    }

    #screen {
      position: relative;
      width: 100vw; height: 100vh;
      display: flex; flex-direction: column;
    }

    /* Zonas: flex-grow como porcentaje (67 + 8 + 25 = 100) */
    #zone-top { flex: 67 0 0; display: flex; }
    #zone-mid { flex: 8  0 0; display: flex; }
    #zone-bot { flex: 25 0 0; display: flex; }

    .stripe { flex: 1 0 0; }

    #bot-left   { flex: 2 0 0; display: flex; }
    #bot-center { flex: 7 0 0; display: flex; }
    #bot-right  { flex: 3 0 0; display: flex; }

    #overlay { position: fixed; inset: 0; pointer-events: none; z-index: 10; }

    .label {
      position: absolute;
      font-family: 'Courier New', Courier, monospace;
      font-size: 13px; line-height: 1.65; letter-spacing: 0.04em;
      color: rgba(255, 255, 255, 0.5);
      white-space: nowrap;
    }
    #lbl-tl { top: 14px; left: 16px; }
    #lbl-tr { top: 14px; right: 16px; text-align: right; }
    #lbl-br { bottom: 14px; right: 16px; text-align: right; }

    #btn-start {
      position: fixed; top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      z-index: 20;
      background: transparent;
      border: 1px solid rgba(255, 255, 255, 0.3);
      color: #ffffff;
      font-family: 'Courier New', Courier, monospace;
      font-size: 13px; letter-spacing: 0.15em;
      padding: 18px 44px;
      cursor: pointer;
      transition: border-color 200ms ease;
      outline: none;
    }
    #btn-start:hover { border-color: rgba(255, 255, 255, 0.6); }
""")

JS = dedent("""\
    const btn     = document.getElementById('btn-start');
    const overlay = document.getElementById('overlay');

    btn.addEventListener('click', () => {
      btn.style.pointerEvents = 'none';

      const fadeOpts = { duration: 400, fill: 'forwards' };
      btn.animate([{ opacity: 1 }, { opacity: 0 }], fadeOpts);
      overlay.animate([{ opacity: 1 }, { opacity: 0 }], fadeOpts);

      setTimeout(expandStripes, 100);
    });

    function expandStripes() {
      const stripes = Array.from(document.querySelectorAll('#zone-top .stripe'));
      const zoneMid = document.getElementById('zone-mid');
      const zoneBot = document.getElementById('zone-bot');

      const rects = stripes.map(s => s.getBoundingClientRect());

      zoneMid.style.visibility = 'hidden';
      zoneBot.style.visibility = 'hidden';

      stripes.forEach((stripe, i) => {
        const rect  = rects[i];
        const scale = window.innerHeight / rect.height;
        const delay = Math.abs(i - 3) * 60;

        Object.assign(stripe.style, {
          position:   'fixed',
          top:        '0px',
          left:       rect.left + 'px',
          width:      rect.width + 'px',
          height:     rect.height + 'px',
          zIndex:     '5',
          willChange: 'transform',
        });

        stripe.animate(
          [
            { transform: 'scaleY(1)',           transformOrigin: '50% 0%' },
            { transform: `scaleY(${scale})`,    transformOrigin: '50% 0%' },
          ],
          {
            delay,
            duration: 800,
            easing:   'cubic-bezier(0.34, 1.56, 0.64, 1)',
            fill:     'forwards',
          }
        );
      });
    }
""")

def build_html():
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Señal de Ajuste — SMPTE</title>
  <style>
{CSS}  </style>
</head>
<body>

  <div id="screen">
    <div id="zone-top">
{_stripes(TOP_HEX)}
    </div>
    <div id="zone-mid">
{_stripes(MID_HEX)}
    </div>
    <div id="zone-bot">
      <div id="bot-left">
{_stripes(BOT_LEFT, indent=8)}
      </div>
      <div id="bot-center">
{_stripes(BOT_CENTER, indent=8)}
      </div>
      <div id="bot-right">
{_stripes(BOT_RIGHT, indent=8)}
      </div>
    </div>
  </div>

  <div id="overlay">
    <div class="label" id="lbl-tl">
      SMPTE · COLOR REFERENCE · 1920×1080 · 29.97fps<br>
      DT/WEB/IDENT · SIGNAL GENERATOR v1.0
    </div>
    <div class="label" id="lbl-tr">
      IRE 100<br>
      FORMAT: HD · BARS+TONE
    </div>
    <div class="label" id="lbl-br">
      TC 00:00:00:00&nbsp;&nbsp;CH-A
    </div>
  </div>

  <button id="btn-start">[ INICIAR ]</button>

  <script>
{JS}  </script>

</body>
</html>
"""


# ════════════════════════════════════════════════════════════════════════════
# 2. PNG  (requiere Pillow — brew install pillow)
# ════════════════════════════════════════════════════════════════════════════

def build_png(dest: Path):
    from PIL import Image, ImageDraw, ImageFont

    W, H = 1920, 1080
    img  = Image.new("RGB", (W, H), (9, 9, 9))
    draw = ImageDraw.Draw(img)

    main_h   = int(H * 0.67)
    stripe_w = W // 7

    # Zona A — barras de color
    for i, c in enumerate(TOP_RGB):
        x0 = i * stripe_w
        x1 = x0 + stripe_w if i < 6 else W
        draw.rectangle([x0, 0, x1, main_h], fill=c)

    # Zona B — segmentos de referencia
    mid_y0 = main_h
    mid_y1 = mid_y0 + int(H * 0.08)
    for i, c in enumerate(MID_RGB):
        x0 = i * stripe_w
        x1 = x0 + stripe_w if i < 6 else W
        draw.rectangle([x0, mid_y0, x1, mid_y1], fill=c)

    # Zona C — rampa de grises + PLUGE
    py0      = mid_y1
    left_w   = stripe_w * 2
    center_w = stripe_w * 3
    right_w  = W - left_w - center_w

    draw.rectangle([0,          py0, left_w // 2, H], fill=hex_to_rgb("#FFFFFF"))
    draw.rectangle([left_w // 2, py0, left_w,     H], fill=hex_to_rgb("#404040"))

    sub_w  = center_w // 7
    grays  = [0x00, 0x20, 0x40, 0x80, 0xB0, 0xD0, 0xFF]
    for i, g in enumerate(grays):
        x0 = left_w + i * sub_w
        x1 = x0 + sub_w if i < 6 else left_w + center_w
        draw.rectangle([x0, py0, x1, H], fill=(g, g, g))

    px     = left_w + center_w
    pseg   = right_w // 3
    draw.rectangle([px,          py0, px + pseg,     H], fill=(0x04, 0x04, 0x04))
    draw.rectangle([px + pseg,   py0, px + pseg * 2, H], fill=(0x00, 0x00, 0x00))
    draw.rectangle([px + pseg*2, py0, W,             H], fill=(0x10, 0x10, 0x10))

    # Texto técnico
    font_paths = [
        "/opt/homebrew/share/fonts/dejavu-fonts/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    font = ImageFont.load_default()
    for p in font_paths:
        if Path(p).exists():
            font = ImageFont.truetype(p, 13)
            break

    draw.text((18, 14),       "SMPTE · COLOR REFERENCE · 1920x1080 · 29.97fps", fill=(255,255,255,180), font=font)
    draw.text((18, 34),       "DT/WEB/IDENT · SIGNAL GENERATOR v1.0",           fill=(255,255,255,100), font=font)
    draw.text((W-200, 14),    "IRE 100",                                         fill=(255,255,255,100), font=font)
    draw.text((W-220, 34),    "FORMAT: HD · BARS+TONE",                         fill=(255,255,255, 80), font=font)
    draw.text((W-200, H-28),  "TC 00:00:00:00  CH-A",                           fill=(255,255,255,120), font=font)
    draw.text((18,    py0+10), "REF WHITE",                                      fill=(  0,  0,  0),    font=font)
    draw.text((left_w//2+8, py0+10), "7.5 IRE",                                 fill=(180,180,180),    font=font)
    draw.text((px+8,  py0+10), "PLUGE",                                          fill=(100,100,100),    font=font)

    img.save(dest)


# ════════════════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    root = Path(__file__).parent

    html_out = root / "ajuste.html"
    html_out.write_text(build_html(), encoding="utf-8")
    print(f"✓  {html_out}")

    png_out = root / "smpte_realistic.png"
    try:
        build_png(png_out)
        print(f"✓  {png_out}")
    except ImportError:
        print("✗  smpte_realistic.png omitido (instalar Pillow: brew install pillow)")
