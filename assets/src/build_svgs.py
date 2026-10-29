"""Builds the animated SVGs used by the profile README.

Run from the repo root:  python3 assets/src/build_svgs.py
Edit the CONTENT section, re-run, commit the regenerated files in assets/.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- CONTENT
NAME = "Aditya Maurya"
STATUS = "currently building Kestrel"
TAGLINES = [
    "AI engineer · building AI that runs on your machine",
    "on-device LLMs · RAG · knowledge graphs",
    "Rust · Python · Kotlin · TypeScript",
]
TERMINAL = [  # (command, output)
    ("whoami", "Adi Maurya. AI engineer. I build AI that runs on your own machine."),
    ("cat focus.txt", "on-device LLMs  ·  RAG + knowledge graphs  ·  measured, reproducible ML"),
    ('kestrel "kal ki meeting notes ka summary do"',
     "✓ summary ready  ·  ran fully on-device  ·  0 bytes sent to the cloud"),
]
FOOTER = "thanks for stopping by  ✦"

# ---------------------------------------------------------------- THEME
VIOLET, CYAN, GREEN = "#a78bfa", "#22d3ee", "#4ade80"
TEXT, MUTED, BG, BORDER = "#e6edf3", "#8b949e", "#0d1117", "#30363d"
SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'JetBrains Mono', 'Fira Code', 'Cascadia Code', Consolas, 'DejaVu Sans Mono', monospace"


def header():
    w, h = 1200, 340
    stars = [(90, 70), (210, 250), (330, 110), (470, 290), (560, 60), (690, 270), (780, 95),
             (900, 240), (1010, 80), (1110, 200), (150, 170), (1060, 300), (620, 180), (400, 40)]
    star_svg = "\n    ".join(
        f'<circle class="s" cx="{x}" cy="{y}" r="{1.2 + (i % 3) * 0.5}" style="animation-delay:{(i * 0.37) % 3:.2f}s"/>'
        for i, (x, y) in enumerate(stars))
    n = len(TAGLINES)
    cycle = 3 * n
    tag_svg = "\n    ".join(
        f'<text class="t" x="600" y="232" style="animation-delay:{i * 3}s">{escape(t)}</text>'
        for i, t in enumerate(TAGLINES))
    shown = 100 / n
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(NAME)}: {escape(TAGLINES[0])}">
  <style>
    .s {{ fill: #fff; opacity: .15; animation: tw 3s ease-in-out infinite; }}
    @keyframes tw {{ 50% {{ opacity: .9; }} }}
    .t {{ font: 500 24px {MONO}; fill: #c9d1d9; text-anchor: middle; opacity: 0;
          animation: cyc {cycle}s ease-in-out infinite; }}
    @keyframes cyc {{
      0% {{ opacity: 0; transform: translateY(10px); }}
      {shown * .12:.1f}%, {shown * .85:.1f}% {{ opacity: 1; transform: translateY(0); }}
      {shown:.1f}%, 100% {{ opacity: 0; transform: translateY(-10px); }}
    }}
    .dot {{ animation: pulse 2s ease-in-out infinite; }}
    @keyframes pulse {{ 50% {{ opacity: .25; }} }}
  </style>
  <defs>
    <clipPath id="card"><rect width="{w}" height="{h}" rx="22"/></clipPath>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0a0e1a"/><stop offset="1" stop-color="#111729"/>
    </linearGradient>
    <linearGradient id="shine" x1="0" y1="0" x2="600" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="repeat">
      <stop offset="0" stop-color="{VIOLET}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/>
      <animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="600 0" dur="6s" repeatCount="indefinite"/>
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="#fff" stroke-opacity=".05"/>
    </pattern>
    <radialGradient id="fade"><stop offset=".3" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
    <mask id="gridMask"><rect width="{w}" height="{h}" fill="url(#fade)"/></mask>
    <filter id="blur" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="70"/></filter>
  </defs>
  <g clip-path="url(#card)">
    <rect width="{w}" height="{h}" fill="url(#bg)"/>
    <g filter="url(#blur)">
      <circle cx="260" cy="90" r="170" fill="{VIOLET}" opacity=".45">
        <animateTransform attributeName="transform" type="translate" values="0 0;140 60;0 0" dur="16s" repeatCount="indefinite"/>
      </circle>
      <circle cx="950" cy="260" r="170" fill="{CYAN}" opacity=".35">
        <animateTransform attributeName="transform" type="translate" values="0 0;-160 -50;0 0" dur="18s" repeatCount="indefinite"/>
      </circle>
    </g>
    <rect width="{w}" height="{h}" fill="url(#grid)" mask="url(#gridMask)"/>
    {star_svg}
  </g>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="22" fill="none" stroke="#fff" stroke-opacity=".08"/>
  <circle class="dot" cx="48" cy="44" r="5" fill="{GREEN}"/>
  <text x="62" y="49" style="font: 15px {MONO}; fill: {MUTED};">{escape(STATUS)}</text>
  <text x="600" y="172" text-anchor="middle" fill="url(#shine)" style="font: 800 92px {SANS}; letter-spacing: -2px;">{escape(NAME)}</text>
  <g>
    {tag_svg}
  </g>
  <text x="600" y="300" text-anchor="middle" style="font: 14px {MONO}; fill: {MUTED}; letter-spacing: 4px;">LOCAL-FIRST · PRIVATE BY DEFAULT · MEASURED</text>
</svg>
'''


def terminal():
    w, cw, fs, step = 1200, 12, 20, 34       # cw = monospace advance at fs (0.6em)
    x0, y0, prompt = 40, 100, "adi@local:~$ "
    px = x0 + len(prompt) * cw
    type_s, start, gap_out, gap_next, hold = 0.07, 0.8, 0.35, 0.7, 4.5

    # timeline: when each command starts typing, finishes, and its output appears
    events, t = [], start
    for cmd, _ in TERMINAL:
        typed = t + len(cmd) * type_s
        out = typed + gap_out
        events.append((t, typed, out))
        t = out + gap_next
    last_prompt = t
    dur = last_prompt + hold

    def kt(s):
        return f"{s / dur:.4f}"

    def show_from(s):
        return (f'<animate attributeName="opacity" calcMode="discrete" values="0;1" '
                f'keyTimes="0;{kt(s)}" dur="{dur:.2f}s" repeatCount="indefinite"/>')

    def prompt_text(y, s):
        hidden = f' opacity="0"' if s else ""
        return (f'<text x="{x0}" y="{y}" textLength="{len(prompt) * cw}"{hidden}>'
                f'<tspan fill="{VIOLET}">adi@local</tspan><tspan fill="{TEXT}">:</tspan>'
                f'<tspan fill="{CYAN}">~</tspan><tspan fill="{TEXT}">$ </tspan>{show_from(s) if s else ""}</text>')

    rows, clips, cur_x, cur_y, cur_t = [], [], [], [], []
    for i, ((cmd, out), (ts, te, to)) in enumerate(zip(TERMINAL, events)):
        y = y0 + 2 * i * step
        p_show = 0 if i == 0 else events[i - 1][2] + gap_next * 0.5
        rows.append(prompt_text(y, p_show))
        widths = [k * cw for k in range(len(cmd) + 1)]
        times = [ts + k * type_s for k in range(len(cmd) + 1)]
        clips.append(
            f'<clipPath id="c{i}"><rect x="{px}" y="{y - fs}" height="{fs + 8}" width="0">'
            f'<animate attributeName="width" calcMode="discrete" dur="{dur:.2f}s" repeatCount="indefinite" '
            f'values="0;{";".join(map(str, widths))}" keyTimes="0;{";".join(kt(s) for s in times)}"/></rect></clipPath>')
        rows.append(f'<text x="{px}" y="{y}" textLength="{len(cmd) * cw}" fill="{TEXT}" '
                    f'clip-path="url(#c{i})">{escape(cmd)}</text>')
        color = GREEN if out.startswith("✓") else MUTED
        rows.append(f'<text x="{x0 + 2 * cw}" y="{y + step}" textLength="{len(out) * cw}" fill="{color}" '
                    f'opacity="0">{escape(out)}{show_from(to)}</text>')
        # cursor: on the prompt line when it appears, then following each typed character
        cur_t += [p_show] + times
        cur_x += [px] + [px + k * cw for k in range(len(cmd) + 1)]
        cur_y += [y] * (len(cmd) + 2)

    y_last = y0 + 2 * len(TERMINAL) * step
    rows.append(prompt_text(y_last, events[-1][2] + gap_next * 0.5))
    cur_t.append(events[-1][2] + gap_next * 0.5)
    cur_x.append(px)
    cur_y.append(y_last)
    cur_t[0] = 0  # SMIL discrete keyTimes must start at 0
    h = y_last + 40

    cursor = (f'<g class="blink"><rect x="{px}" y="{y0 - fs + 2}" width="{cw}" height="{fs + 4}" '
              f'fill="{VIOLET}" opacity=".85">'
              f'<animate attributeName="x" calcMode="discrete" dur="{dur:.2f}s" repeatCount="indefinite" '
              f'values="{";".join(map(str, cur_x))}" keyTimes="{";".join(kt(s) for s in cur_t)}"/>'
              f'<animate attributeName="y" calcMode="discrete" dur="{dur:.2f}s" repeatCount="indefinite" '
              f'values="{";".join(str(v - fs + 2) for v in cur_y)}" keyTimes="{";".join(kt(s) for s in cur_t)}"/>'
              f'</rect></g>')

    nl = "\n  "
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="Terminal: {escape(TERMINAL[0][1])}">
  <style>
    text {{ font: {fs}px {MONO}; white-space: pre; }}
    .blink {{ animation: b 1s step-end infinite; }}
    @keyframes b {{ 50% {{ opacity: 0; }} }}
  </style>
  <defs>
  {nl.join(clips)}
  </defs>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="{BG}" stroke="{BORDER}"/>
  <path d="M.5 44V14.5a14 14 0 0 1 14-14h{w - 29}a14 14 0 0 1 14 14V44z" fill="#161b22"/>
  <line x1="0" y1="44" x2="{w}" y2="44" stroke="{BORDER}"/>
  <circle cx="26" cy="22" r="7" fill="#ff5f57"/><circle cx="50" cy="22" r="7" fill="#febc2e"/><circle cx="74" cy="22" r="7" fill="#28c840"/>
  <text x="{w // 2}" y="27" text-anchor="middle" style="font-size: 14px; fill: {MUTED};">adi@local: ~</text>
  {nl.join(rows)}
  {cursor}
</svg>
'''


def footer():
    w, h, period = 1200, 170, 600

    def wave(base, amp, color, opacity, dur, reverse=False):
        d = f"M{-period} {base}"
        x = -period
        d += f" Q{x + period / 4} {base - amp} {x + period / 2} {base}"
        x += period // 2
        while x < w + period:
            x += period // 2
            d += f" T{x} {base}"
        d += f" V{h} H{-period}Z"
        frm, to = ("0", str(period)) if not reverse else (str(period), "0")
        return (f'<path d="{d}" fill="{color}" fill-opacity="{opacity}">'
                f'<animateTransform attributeName="transform" type="translate" from="{frm} 0" to="{to} 0" '
                f'dur="{dur}s" repeatCount="indefinite"/></path>')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{escape(FOOTER)}">
  <defs>
    <linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
  </defs>
  <text x="{w // 2}" y="48" text-anchor="middle" style="font: 16px {MONO}; fill: {MUTED}; letter-spacing: 3px;">{escape(FOOTER)}</text>
  {wave(110, 16, "url(#g)", .25, 9)}
  {wave(122, 12, "url(#g)", .35, 7, reverse=True)}
  {wave(136, 9, "url(#g)", .6, 5)}
</svg>
'''


if __name__ == "__main__":
    for name, build in [("header.svg", header), ("terminal.svg", terminal), ("footer.svg", footer)]:
        (OUT / name).write_text(build(), encoding="utf-8")
        print("wrote", OUT / name)
