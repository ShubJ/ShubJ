import base64
import json
import math
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
ICONS = ROOT / "icons"
FONTS = ROOT / "fonts"

INK = "#2b1a0e"
PARCH = "#f1dfb0"
GOLD = "#e7b54a"
RED = "#e0533f"
TEAL = "#2fc4b2"
SKY = "#8fd0ff"
TEXT = "#dfe7f3"
MUTED = "#8b9bb4"
BG = "#0a1222"

BRAND = {
    "typescript": "#3178C6", "javascript": "#F7DF1E", "react": "#61DAFB",
    "nextdotjs": "#FFFFFF", "nodedotjs": "#5FA04E", "nestjs": "#E0234E",
    "tailwindcss": "#06B6D4", "supabase": "#3FCF8E", "postgresql": "#4169E1",
    "mysql": "#4479A1", "docker": "#2496ED", "git": "#F05032",
    "telegram": "#26A5E4", "claude": "#D97757", "html5": "#E34F26",
    "css": "#663399", "redis": "#FF4438", "githubactions": "#2088FF",
    "express": "#FFFFFF", "github": "#FFFFFF",
    "mongodb": "#47A248", "apachekafka": "#FFFFFF", "socketdotio": "#FFFFFF",
    "amazonaws": "#FF9900", "amazonsqs": "#FF4F8B", "awslambda": "#FF9900",
    "amazons3": "#569A31", "amazonec2": "#FF9900", "amazoncloudwatch": "#FF4F8B",
    "linkedin": "#0A66C2", "leetcode": "#FFA116", "vercel": "#FFFFFF", "gmail": "#EA4335",
}


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def icon_path(name: str) -> str:
    return re.search(r'<path d="([^"]+)"', (ICONS / f"{name}.svg").read_text()).group(1)


def font_css() -> str:
    faces = [("Pirata", "pirata"), ("Grotesk", "grotesk"), ("Mono", "mono")]
    return "".join(
        f"@font-face{{font-family:'{fam}';src:url(data:font/woff2;base64,{b64(FONTS / (f + '.woff2'))}) format('woff2');}}"
        for fam, f in faces
    )


BASE_CSS = """
.pir{font-family:'Pirata',serif}
.gro{font-family:'Grotesk',system-ui,sans-serif}
.mono{font-family:'Mono',ui-monospace,monospace}
"""


def card_defs(uid: str, w: int, h: int) -> str:
    return f"""
<linearGradient id="{uid}-edge" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{GOLD}"/><stop offset=".5" stop-color="{TEAL}"/><stop offset="1" stop-color="{RED}"/>
</linearGradient>
<radialGradient id="{uid}-sea" cx=".5" cy="0" r="1.1">
  <stop offset="0" stop-color="#16294a"/><stop offset=".6" stop-color="#0c1730"/><stop offset="1" stop-color="{BG}"/>
</radialGradient>
<pattern id="{uid}-dots" width="18" height="18" patternUnits="userSpaceOnUse">
  <circle cx="2" cy="2" r="1" fill="#ffffff" opacity=".06"/>
</pattern>
<clipPath id="{uid}-clip"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="22"/></clipPath>"""


def card_bg(uid: str, w: int, h: int) -> str:
    return f"""
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="22" fill="url(#{uid}-sea)"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="22" fill="url(#{uid}-dots)"/>"""


def card_border(uid: str, w: int, h: int) -> str:
    return f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="22" fill="none" stroke="url(#{uid}-edge)" stroke-opacity=".7" stroke-width="1.5"/>'


def svg_doc(w: int, h: int, title: str, defs: str, body: str, extra_css: str = "") -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">
<title>{title}</title>
<style>{font_css()}{BASE_CSS}{extra_css}</style>
<defs>{defs}</defs>
{body}
</svg>
"""


def stars(uid: str, n: int, w: int, h: int, seed: int) -> str:
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rnd.uniform(10, w - 10), rnd.uniform(10, h)
        r = rnd.choice([0.7, 0.9, 1.2, 1.5])
        dur = rnd.uniform(2.5, 5.5)
        lo = rnd.uniform(.15, .4)
        out.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fff" opacity=".8">'
            f'<animate attributeName="opacity" values=".8;{lo:.2f};.8" dur="{dur:.1f}s" begin="0s" repeatCount="indefinite"/></circle>'
        )
    return "\n".join(out)


def waves(w: int, y: int, color: str, opacity: float, amp: float, dur: float, period: int = 250) -> str:
    pts = []
    for x in range(0, w + period * 2 + 1, 10):
        pts.append(f"{x},{y + amp * math.sin(2 * math.pi * x / period):.1f}")
    d = "M" + " L".join(pts) + f" L{w + period * 2},{y + 200} L0,{y + 200} Z"
    return (
        f'<g opacity="{opacity}"><path d="{d}" fill="{color}">'
        f'<animateTransform attributeName="transform" type="translate" values="0 0;-{period} 0" dur="{dur}s" begin="0s" repeatCount="indefinite"/>'
        f"</path></g>"
    )


def build_hero(portrait_b64: str, repo_count: int) -> str:
    W, H = 1000, 440
    u = "h"
    roles = [
        "Tech Lead at Primathon Technologies",
        "7+ years of distributed backend systems",
        "Node.js \u00b7 TypeScript \u00b7 NestJS \u00b7 Kafka \u00b7 AWS",
        "Built a 4-agent AI engineering pipeline",
    ]
    cycle = 12
    role_els = []
    n = len(roles)
    for i, r in enumerate(roles):
        a, b = i / n, (i + 1) / n
        eps = 0.02
        kt = sorted({0, max(a - eps, 0), a, b - eps, b, 1})
        vals = []
        for t in kt:
            vals.append("1" if a <= t < b - eps or (t == 0 and i == 0) else "0")
        if i == 0:
            kt, vals = [0, b - eps, b, 1 - eps, 1], ["1", "1", "0", "0", "1"]
        else:
            kt, vals = [0, a - eps, a, b - eps, b, 1], ["0", "0", "1", "1", "0", "0"]
        role_els.append(
            f'<text x="48" y="246" class="mono" font-size="17" fill="{SKY}" opacity="{1 if i == 0 else 0}">'
            f'<tspan fill="{GOLD}">&gt; </tspan>{r}'
            f'<animate attributeName="opacity" values="{";".join(vals)}" keyTimes="{";".join(f"{k:.3f}" for k in kt)}" dur="{cycle}s" begin="0s" repeatCount="indefinite"/></text>'
        )

    px, py, pw, ph = 650, 46, 290, 372
    nail_x = px + pw / 2
    poster_shape = (
        f"M{px + 4},{py + 2} L{px + 70},{py + 6} L{px + 150},{py} L{px + 230},{py + 5} L{px + pw - 2},{py + 1} "
        f"L{px + pw + 2},{py + 90} L{px + pw - 3},{py + 200} L{px + pw + 1},{py + ph - 4} "
        f"L{px + 200},{py + ph + 2} L{px + 110},{py + ph - 3} L{px + 2},{py + ph + 1} "
        f"L{px - 2},{py + 260} L{px + 3},{py + 140} Z"
    )
    fx, fy, fw, fh = px + 35, py + 92, pw - 70, 178

    defs = card_defs(u, W, H) + f"""
<linearGradient id="h-name" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="420" y2="0" spreadMethod="reflect">
  <stop offset="0" stop-color="{GOLD}"/><stop offset=".5" stop-color="#ffe9a8"/><stop offset="1" stop-color="{RED}"/>
  <animate attributeName="x1" values="0;420;0" dur="6s" begin="0s" repeatCount="indefinite"/>
  <animate attributeName="x2" values="420;840;420" dur="6s" begin="0s" repeatCount="indefinite"/>
</linearGradient>
<linearGradient id="h-paper" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#f6e7bf"/><stop offset="1" stop-color="#dcc188"/>
</linearGradient>
<radialGradient id="h-burn" cx=".5" cy=".5" r=".75">
  <stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#6b4316" stop-opacity=".45"/>
</radialGradient>
<radialGradient id="h-moon" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="#fff6d8"/><stop offset=".55" stop-color="#ffe9a8" stop-opacity=".9"/><stop offset="1" stop-color="#ffe9a8" stop-opacity="0"/>
</radialGradient>
<mask id="h-reveal" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
  <rect x="0" y="120" width="640" height="100" fill="#fff">
    <animate attributeName="y" values="220;220;120" keyTimes="0;.3;1" dur="1.6s" begin="0s" fill="freeze" calcMode="spline" keySplines="0 0 1 1;.2 .8 .2 1"/>
  </rect>
</mask>
<clipPath id="h-type"><rect x="46" y="86" width="150" height="40">
  <animate attributeName="width" values="0;20;40;60;80;100;120;150" dur="0.9s" begin="0s" fill="freeze" calcMode="discrete"/>
</rect></clipPath>
<clipPath id="h-photo"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}"/></clipPath>
<filter id="h-glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>"""

    meta = [
        ("M6,13 C2,8 1,6 1,4.5 a5,5 0 0 1 10,0 C11,6 10,8 6,13 z M6,3 a1.6,1.6 0 1 0 .01,0", "Gurgaon, India"),
        ("M1,12 V3 h6 v9 M7,6 h4 v6 M0,12 h12 M3,5 h2 M3,8 h2", "Primathon Technologies"),
        ("M0,2 h12 v10 h-12 z M0,5 h12 M3,0 v3 M9,0 v3", "7+ yrs backend"),
    ]
    meta_els, mx = [], 48
    for d, label in meta:
        meta_els.append(
            f'<g transform="translate({mx},341)"><path d="{d}" fill="none" stroke="{GOLD}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<text x="20" y="11" class="mono" font-size="13" fill="{MUTED}">{label}</text></g>'
        )
        mx += 34 + len(label) * 8.2

    body = f"""
<g clip-path="url(#h-clip)">
{card_bg(u, W, H)}
<circle cx="600" cy="92" r="70" fill="url(#h-moon)" opacity=".55"/>
<circle cx="600" cy="92" r="26" fill="#fff3cf" opacity=".9"/>
{stars(u, 46, W, 260, 7)}
{waves(W, 392, "#123a5c", .9, 6, 9)}
{waves(W, 404, "#0d2c4a", 1, 8, 6, 320)}
{waves(W, 418, "#0a2038", 1, 5, 4.5, 200)}

<g transform="translate(48,40)">
  <rect width="190" height="30" rx="15" fill="{TEAL}" fill-opacity=".12" stroke="{TEAL}" stroke-opacity=".6"/>
  <circle cx="18" cy="15" r="9" fill="{TEAL}" opacity="0">
    <animate attributeName="r" values="4;11;4" dur="1.8s" begin="0s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values=".5;0;0" dur="1.8s" begin="0s" repeatCount="indefinite"/>
  </circle>
  <circle cx="18" cy="15" r="4.5" fill="{TEAL}"/>
  <text x="34" y="20" class="mono" font-size="12" fill="{TEAL}" letter-spacing="1">OPEN TO COLLABS</text>
</g>

<text x="48" y="116" class="mono" font-size="20" fill="{SKY}" clip-path="url(#h-type)">Ahoy, I'm</text>
<rect x="162" y="98" width="10" height="22" fill="{SKY}">
  <animate attributeName="opacity" values="1;0;1" dur="1s" begin="0s" repeatCount="indefinite" calcMode="discrete"/>
</rect>

<g mask="url(#h-reveal)">
  <text x="44" y="200" class="pir" font-size="82" fill="url(#h-name)">Shubham Jindal</text>
</g>

{"".join(role_els)}

<text class="gro" font-size="16" fill="{TEXT}" opacity=".85">
  <tspan x="48" y="290">I design event-driven backends and microservices that stay up</tspan>
  <tspan x="48" y="312">under load, and AI workflows that ship code 3-5x faster.</tspan>
</text>
{"".join(meta_els)}

<g>
  <animateTransform attributeName="transform" type="translate" values="0 -470;0 -470;0 12;0 -4;0 0" keyTimes="0;.15;.6;.8;1" dur="1.3s" begin="0s" fill="freeze" calcMode="spline" keySplines="0 0 1 1;.5 0 .9 .6;.2 .6 .4 1;.4 0 .6 1"/>
  <g>
    <animateTransform attributeName="transform" type="rotate" values="0 {nail_x} 24;0 {nail_x} 24;6 {nail_x} 24;-4.5 {nail_x} 24;3 {nail_x} 24;-1.8 {nail_x} 24;1 {nail_x} 24;0 {nail_x} 24" keyTimes="0;.24;.38;.5;.62;.74;.87;1" dur="5.4s" begin="0s" fill="freeze" calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1"/>
    <g>
      <animateTransform attributeName="transform" type="rotate" values="0 {nail_x} 24;0 {nail_x} 24;.9 {nail_x} 24;0 {nail_x} 24;-.9 {nail_x} 24;0 {nail_x} 24" keyTimes="0;.4;.55;.7;.85;1" dur="13.5s" begin="0s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1"/>
      <path d="M{nail_x},24 L{px + 40},{py + 8} M{nail_x},24 L{px + pw - 40},{py + 8}" stroke="#a07a3c" stroke-width="1.6" fill="none"/>
      <path d="{poster_shape}" fill="#000" opacity=".35" transform="translate(6,8)"/>
      <path d="{poster_shape}" fill="url(#h-paper)"/>
      <path d="{poster_shape}" fill="url(#h-burn)"/>
      <circle cx="{px + 60}" cy="{py + 300}" r="22" fill="#8a5a22" opacity=".08"/>
      <circle cx="{px + 230}" cy="{py + 120}" r="14" fill="#8a5a22" opacity=".07"/>
      <text x="{nail_x}" y="{py + 76}" text-anchor="middle" class="pir" font-size="66" fill="{INK}" letter-spacing="3">WANTED</text>
      <rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="#e3c992"/>
      <image href="data:image/png;base64,{portrait_b64}" x="{fx - 6}" y="{fy + 2}" width="{fw + 12}" height="{(fw + 12) * 334 / 360:.0f}" clip-path="url(#h-photo)"/>
      <rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="{INK}" stroke-width="3"/>
      <rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="none" stroke="{GOLD}" stroke-width="3" stroke-dasharray="70 726" stroke-linecap="round" filter="url(#h-glow)">
        <animate attributeName="stroke-dashoffset" values="0;-796" dur="4s" begin="0s" repeatCount="indefinite"/>
      </rect>
      <text x="{nail_x}" y="{fy + fh + 30}" text-anchor="middle" class="pir" font-size="26" fill="{INK}" letter-spacing="4">CODE OR ALIVE</text>
      <text x="{nail_x}" y="{fy + fh + 54}" text-anchor="middle" class="mono" font-size="15" font-weight="700" fill="{INK}" letter-spacing="2">SHUBHAM JINDAL</text>
      <text x="{nail_x}" y="{fy + fh + 86}" text-anchor="middle" class="pir" font-size="28" fill="#7a2a1a">7+ YEARS AT SEA</text>
    </g>
  </g>
</g>
<circle cx="{nail_x}" cy="24" r="5" fill="#6b6f78" stroke="#2a2d33" stroke-width="1.5"/>

</g>
{card_border(u, W, H)}"""
    return svg_doc(W, H, "Shubham Jindal, backend tech lead", defs, body)


def tilted_ellipse(cx, cy, rx, ry, tilt_deg, phase_deg, steps=72):
    t = math.radians(tilt_deg)
    pts = []
    for k in range(steps + 1):
        a = math.radians(phase_deg) + 2 * math.pi * k / steps
        x, y = rx * math.cos(a), ry * math.sin(a)
        pts.append((cx + x * math.cos(t) - y * math.sin(t), cy + x * math.sin(t) + y * math.cos(t)))
    return pts


def icon_badge(name: str, r: int = 17, scale: float = None) -> str:
    s = scale or (r * 1.15) / 24
    color = BRAND[name]
    return (
        f'<circle r="{r}" fill="#0e1a30" stroke="{color}" stroke-opacity=".7" stroke-width="1.5"/>'
        f'<path d="{icon_path(name)}" fill="{color}" transform="translate({-12 * s:.2f},{-12 * s:.2f}) scale({s:.3f})"/>'
    )


def orbiter(name, pts, dur, r=17, children=""):
    sx, sy = pts[0]
    rel = "M0,0 " + " ".join(f"L{x - sx:.1f},{y - sy:.1f}" for x, y in pts[1:])
    return (
        f'<g transform="translate({sx:.1f},{sy:.1f})">'
        f'<animateMotion path="{rel}" dur="{dur}s" begin="0s" repeatCount="indefinite"/>'
        f"{icon_badge(name, r)}{children}</g>"
    )


def build_stack() -> str:
    W, H = 1000, 430
    u = "s"
    cx, cy = 250, 222
    orbits = [
        (220, 96, -14, 30, ["nodedotjs", "nestjs", "mysql", "mongodb", "apachekafka"]),
        (168, 80, 18, 22, ["redis", "amazonaws", "docker"]),
        (112, 56, 42, 15, ["git", "claude", "socketdotio"]),
    ]
    orbit_paths, riders = [], []
    for rx, ry, tilt, dur, names in orbits:
        base = tilted_ellipse(cx, cy, rx, ry, tilt, 0)
        orbit_paths.append(
            f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x, y in base)} Z" fill="none" stroke="{SKY}" stroke-opacity=".22" stroke-dasharray="3 6"/>'
        )
        for i, n in enumerate(names):
            pts = tilted_ellipse(cx, cy, rx, ry, tilt, 360 * i / len(names) + 20)
            kids = ""
            if n == "nodedotjs":
                for j, moon in enumerate(["typescript", "javascript"]):
                    mp = tilted_ellipse(0, 0, 32, 32, 0, 180 * j, 36)
                    kids += orbiter(moon, mp, 6, r=9)
            riders.append(orbiter(n, pts, dur, children=kids))

    rose = []
    for k in range(8):
        L = 24 if k % 2 == 0 else 14
        a = math.radians(45 * k)
        b1, b2 = a + math.radians(90), a - math.radians(90)
        tip = (L * math.sin(a), -L * math.cos(a))
        s1 = (4 * math.sin(b1), -4 * math.cos(b1))
        s2 = (4 * math.sin(b2), -4 * math.cos(b2))
        rose.append(f'<path d="M{s1[0]:.1f},{s1[1]:.1f} L{tip[0]:.1f},{tip[1]:.1f} L{s2[0]:.1f},{s2[1]:.1f} Z" fill="{GOLD if k % 2 == 0 else "#b98a2e"}"/>')

    groups = [
        ("CORE", [("nodedotjs", "Node.js"), ("typescript", "TypeScript"), ("nestjs", "NestJS"), ("javascript", "JavaScript")]),
        ("DATA & STREAMING", [("mysql", "MySQL"), ("mongodb", "MongoDB"), ("redis", "Redis"), ("apachekafka", "Kafka")]),
        ("AWS", [("amazonsqs", "SQS"), ("amazons3", "S3"), ("amazonec2", "EC2"), ("awslambda", "Lambda"), ("amazoncloudwatch", "CloudWatch")]),
        ("ARCHITECTURE", [(None, "Microservices"), (None, "Event-driven"), ("socketdotio", "WebSockets")]),
        ("SHIP IT", [(None, "API gateway"), ("docker", "Docker"), ("githubactions", "CI/CD"), ("git", "Git")]),
        ("AI", [("claude", "Multi-agent AI workflows")]),
    ]
    total = sum(len(c) for _, c in groups)
    T = total * 0.45
    chips, gy, idx = [], 52, 0
    for title, items in groups:
        chips.append(f'<text x="520" y="{gy}" class="mono" font-size="11" fill="{MUTED}" letter-spacing="2">{title.replace("&", "&amp;")}</text>')
        cx0 = 520
        for name, label in items:
            w = 34 + len(label) * 7.6
            a = idx / total
            b = a + 1 / total
            kt = f"0;{a:.3f};{min(a + .02, 1):.3f};{min(b + .04, 1):.3f};1"
            col = GOLD if name is None else (BRAND[name] if BRAND[name] != "#FFFFFF" else "#cfd8e6")
            chips.append(
                f'<g transform="translate({cx0:.0f},{gy + 9})">'
                f'<rect width="{w:.0f}" height="26" rx="8" fill="#0f1c33" stroke="{col}" stroke-opacity=".25"/>'
                f'<rect width="{w:.0f}" height="26" rx="8" fill="none" stroke="{col}" stroke-width="1.5" opacity="0">'
                f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="{kt}" dur="{T:.1f}s" begin="0s" repeatCount="indefinite"/></rect>'
                + (f'<circle cx="16" cy="13" r="4" fill="none" stroke="{col}" stroke-width="2"/>' if name is None else f'<path d="{icon_path(name)}" fill="{col}" transform="translate(9,6) scale(.58)"/>')
                + f'<text x="27" y="17.5" class="mono" font-size="12" fill="{TEXT}">{label}</text></g>'
            )
            cx0 += w + 8
            idx += 1
        gy += 58

    defs = card_defs(u, W, H) + f"""
<radialGradient id="s-core" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="{GOLD}" stop-opacity=".55"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
</radialGradient>"""
    body = f"""
<g clip-path="url(#s-clip)">
{card_bg(u, W, H)}
{stars(u, 24, 470, H, 11)}
<text x="40" y="48" class="pir" font-size="34" fill="{GOLD}">The Ship's Toolkit</text>
<text x="40" y="70" class="mono" font-size="12" fill="{MUTED}">what I sail with, every day</text>
{"".join(orbit_paths)}
<circle cx="{cx}" cy="{cy}" r="44" fill="url(#s-core)">
  <animate attributeName="r" values="40;52;40" dur="3s" begin="0s" repeatCount="indefinite"/>
</circle>
<circle cx="{cx}" cy="{cy}" r="27" fill="#13233f" stroke="{GOLD}" stroke-width="1.5"/>
<g transform="translate({cx},{cy})">
  <g>{"".join(rose)}
    <animateTransform attributeName="transform" type="rotate" values="0;360" dur="40s" begin="0s" repeatCount="indefinite"/>
  </g>
  <circle r="3" fill="{INK}" stroke="{GOLD}"/>
</g>
{"".join(riders)}
<line x1="490" y1="40" x2="490" y2="{H - 40}" stroke="{SKY}" stroke-opacity=".12"/>
{"".join(chips)}
</g>
{card_border(u, W, H)}"""
    return svg_doc(W, H, "Tech stack", defs, body)


def count_frames(x, y, final: int, size: int, color: str, suffix: str = "", frames: int = 10, dur: float = 1.6) -> str:
    out = []
    vals = [round(final * (k / (frames - 1)) ** 0.6) for k in range(frames)]
    for k, v in enumerate(vals):
        seq = ["1" if j == k else "0" for j in range(frames)]
        last = k == frames - 1
        out.append(
            f'<text x="{x}" y="{y}" class="gro" font-weight="700" font-size="{size}" fill="{color}" opacity="{1 if last else 0}">{v}{suffix}'
            f'<animate attributeName="opacity" values="{";".join(seq)}" dur="{dur}s" begin="0s" fill="freeze" calcMode="discrete"/></text>'
        )
    return "".join(out)


def build_crew(portrait_b64: str, data: dict) -> str:
    W, H = 1000, 450
    u = "c"
    bx, by, bw, bh = 70, 118, 240, 310
    pivot = (bx + bw / 2, 0)
    rnd = random.Random(3)
    bars, xx = [], bx + 24
    while xx < bx + bw - 24:
        wbar = rnd.choice([1, 1, 2, 3])
        bars.append(f'<rect x="{xx}" y="{by + bh - 48}" width="{wbar}" height="26" fill="{TEXT}" opacity=".85"/>')
        xx += wbar + rnd.choice([1, 2, 2, 3])

    kpis = [
        (7, "+", "years in backend", GOLD),
        (4, "", "AI agents in my team", TEAL),
        (90, "%+", "AI-assisted code", SKY),
    ]
    kpi_els = []
    for i, (v, suf, label, col) in enumerate(kpis):
        x = 400 + i * 190
        kpi_els.append(
            f'<rect x="{x}" y="40" width="175" height="92" rx="14" fill="#0f1c33" stroke="{col}" stroke-opacity=".35"/>'
            + count_frames(x + 20, 96, v, 40, col, suf)
            + f'<text x="{x + 20}" y="118" class="mono" font-size="12" fill="{MUTED}">{label}</text>'
        )

    voyages = [
        ("2025 - now", "Tech Lead \u00b7 Primathon Technologies", "Multi-tenant app marketplace, zero-downtime DB migration"),
        ("2020 - 2025", "Senior Software Developer \u00b7 QuickReply.ai", "Real-time WhatsApp messaging, Flow Builder workflow engine"),
        ("2015 - 2019", "B.Tech, Computer Science \u00b7 GJUST, Hisar", "Where the voyage started"),
    ]
    voy_els = [
        f'<line x1="496" y1="190" x2="496" y2="306" stroke="{GOLD}" stroke-opacity=".5" stroke-width="2" stroke-dasharray="116" stroke-dashoffset="0">'
        f'<animate attributeName="stroke-dashoffset" values="116;116;0" keyTimes="0;.3;1" dur="1.8s" begin="0s" fill="freeze"/></line>',
        f'<circle cx="496" cy="190" r="11" fill="none" stroke="{GOLD}" opacity=".6">'
        f'<animate attributeName="r" values="6;14;6" dur="2s" begin="0s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".6;0;.6" dur="2s" begin="0s" repeatCount="indefinite"/></circle>',
    ]
    for i, (yrs, title, sub) in enumerate(voyages):
        y = 190 + i * 58
        voy_els.append(
            f'<text x="400" y="{y + 5}" class="mono" font-size="12" fill="{MUTED}">{yrs}</text>'
            f'<circle cx="496" cy="{y}" r="6" fill="{BG}" stroke="{GOLD}" stroke-width="2"/>'
            f'<circle cx="496" cy="{y}" r="2.5" fill="{GOLD if i == 0 else MUTED}"/>'
            f'<text x="514" y="{y + 5}" class="gro" font-size="15" font-weight="700" fill="{TEXT}">{title}</text>'
            f'<text x="514" y="{y + 24}" class="mono" font-size="11" fill="{MUTED}">{sub}</text>'
        )

    now_lines = [
        "Built a 4-agent AI system: PM, TL, SDE and Reviewer",
        "AI Telegram Sprint Planner for backlog and blockers",
        "Founder-level recognition for critical platform work",
    ]
    now_els = []
    for i, v in enumerate(now_lines):
        y = 380 + i * 22
        now_els.append(
            f'<text x="400" y="{y}" class="mono" font-size="12"><tspan fill="{GOLD}">\u25b8 </tspan><tspan fill="{TEXT}">{v}</tspan></text>'
        )

    defs = card_defs(u, W, H) + f"""
<linearGradient id="c-card" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#1a2c4f"/><stop offset="1" stop-color="#0d1730"/>
</linearGradient>
<linearGradient id="c-foil" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#fff" stop-opacity="0"/>
  <stop offset=".35" stop-color="{TEAL}" stop-opacity=".25"/>
  <stop offset=".5" stop-color="#ffffff" stop-opacity=".35"/>
  <stop offset=".65" stop-color="{RED}" stop-opacity=".2"/>
  <stop offset="1" stop-color="#fff" stop-opacity="0"/>
</linearGradient>
<linearGradient id="c-chip" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#f7d77c"/><stop offset="1" stop-color="#b8862a"/>
</linearGradient>
<clipPath id="c-cardclip"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="16"/></clipPath>
<clipPath id="c-photo"><rect x="{bx + 60}" y="{by + 46}" width="120" height="120" rx="12"/></clipPath>
<filter id="c-glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.5"/></filter>"""

    strap_text = " SHUBJ DEV CREW ·" * 4
    body = f"""
<g clip-path="url(#c-clip)">
{card_bg(u, W, H)}
<g>
  <animateTransform attributeName="transform" type="translate" values="0 -460;0 -460;0 10;0 -3;0 0" keyTimes="0;.1;.6;.8;1" dur="1.3s" begin="0s" fill="freeze" calcMode="spline" keySplines="0 0 1 1;.5 0 .9 .6;.2 .6 .4 1;.4 0 .6 1"/>
  <g>
    <animateTransform attributeName="transform" type="rotate" values="0 {pivot[0]} 0;0 {pivot[0]} 0;5 {pivot[0]} 0;-3.6 {pivot[0]} 0;2.4 {pivot[0]} 0;-1.4 {pivot[0]} 0;.6 {pivot[0]} 0;0 {pivot[0]} 0" keyTimes="0;.22;.36;.49;.62;.75;.88;1" dur="5s" begin="0s" fill="freeze" calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1"/>
    <path d="M{pivot[0] - 60},-10 L{pivot[0] - 14},{by - 16} L{pivot[0] + 14},{by - 16} L{pivot[0] + 60},-10" fill="none" stroke="{RED}" stroke-width="22" stroke-linejoin="round"/>
    <path id="c-strap" d="M{pivot[0] - 66},0 L{pivot[0] - 15},{by - 22}" fill="none"/>
    <text class="mono" font-size="9" font-weight="700" fill="#fff" letter-spacing="1.5" dy="3"><textPath href="#c-strap">{strap_text}</textPath></text>
    <rect x="{pivot[0] - 16}" y="{by - 26}" width="32" height="20" rx="5" fill="#9aa3b2" stroke="#59606d" stroke-width="2"/>
    <rect x="{pivot[0] - 6}" y="{by - 10}" width="12" height="16" rx="3" fill="none" stroke="#9aa3b2" stroke-width="3"/>
    <rect x="{bx + 6}" y="{by + 8}" width="{bw}" height="{bh}" rx="16" fill="#000" opacity=".35"/>
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="16" fill="url(#c-card)" stroke="{GOLD}" stroke-width="2"/>
    <g clip-path="url(#c-cardclip)">
      <rect x="{bx}" y="{by}" width="{bw}" height="34" fill="{GOLD}"/>
      <text x="{bx + 16}" y="{by + 23}" class="pir" font-size="20" fill="{INK}">CREW ID</text>
      <text x="{bx + bw - 16}" y="{by + 22}" text-anchor="end" class="mono" font-size="10" fill="{INK}">No. 0007</text>
      <rect x="{bx + 60}" y="{by + 46}" width="120" height="120" rx="12" fill="#e3c992"/>
      <image href="data:image/png;base64,{portrait_b64}" x="{bx + 32}" y="{by + 46}" width="176" height="{176 * 334 / 360:.0f}" clip-path="url(#c-photo)"/>
      <rect x="{bx + 60}" y="{by + 46}" width="120" height="120" rx="12" fill="none" stroke="{GOLD}" stroke-opacity=".5" stroke-width="2"/>
      <rect x="{bx + 60}" y="{by + 46}" width="120" height="120" rx="12" fill="none" stroke="{TEAL}" stroke-width="3" stroke-dasharray="50 410" stroke-linecap="round" filter="url(#c-glow)">
        <animate attributeName="stroke-dashoffset" values="0;-460" dur="3.5s" begin="0s" repeatCount="indefinite"/>
      </rect>
      <text x="{bx + bw / 2}" y="{by + 194}" text-anchor="middle" class="gro" font-size="20" font-weight="700" fill="{TEXT}">Shubham Jindal</text>
      <text x="{bx + bw / 2}" y="{by + 214}" text-anchor="middle" class="mono" font-size="11" fill="{GOLD}">TECH LEAD · BACKEND</text>
      <rect x="{bx + 24}" y="{by + 228}" width="34" height="26" rx="5" fill="url(#c-chip)"/>
      <path d="M{bx + 24},{by + 241} h34 M{bx + 41},{by + 228} v26 M{bx + 32},{by + 228} v8 M{bx + 50},{by + 246} v8" stroke="#8a6420" stroke-width="1"/>
      <text x="{bx + 70}" y="{by + 240}" class="mono" font-size="10" fill="{MUTED}">HOME PORT</text>
      <text x="{bx + 70}" y="{by + 254}" class="mono" font-size="11" fill="{TEXT}">shubhamjindal.vercel.app</text>
      {"".join(bars)}
      <rect x="{bx - bw}" y="{by}" width="{bw}" height="{bh}" fill="url(#c-foil)" transform="skewX(-20)">
        <animateTransform attributeName="transform" type="translate" values="0 0;0 0;{bw * 2.6:.0f} 0" keyTimes="0;.55;1" dur="4.5s" begin="0s" repeatCount="indefinite" additive="sum"/>
      </rect>
    </g>
  </g>
</g>
{"".join(kpi_els)}
<text x="400" y="166" class="mono" font-size="11" fill="{MUTED}" letter-spacing="2">VOYAGES</text>
{"".join(voy_els)}
<text x="400" y="356" class="mono" font-size="11" fill="{MUTED}" letter-spacing="2">CAPTAIN'S LOG</text>
<circle cx="526" cy="352" r="4" fill="{RED}"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" begin="0s" repeatCount="indefinite"/></circle>
{"".join(now_els)}
</g>
{card_border(u, W, H)}"""
    return svg_doc(W, H, "Crew ID and stats", defs, body)


def build_connect(pointing_b64: str, repo_count: int) -> str:
    W, H = 1000, 400
    u = "k"
    cards = [
        ("vercel", "shubhamjindal.vercel.app", "portfolio, projects and resume"),
        ("linkedin", "linkedin.com/in/shubhamj130", "let's talk backend and AI"),
        ("gmail", "jindalshubham130@gmail.com", "open to collabs"),
    ]
    els = []
    for i, (ic, title, sub) in enumerate(cards):
        y = 92 + i * 92
        col = BRAND[ic]
        els.append(
            f'<g transform="translate(470,{y})">'
            f'<rect width="470" height="74" rx="16" fill="#0f1c33" stroke="{GOLD}" stroke-opacity=".3"/>'
            f'<g transform="translate(40,37)">{icon_badge(ic, 22)}</g>'
            f'<text x="78" y="32" class="gro" font-size="18" font-weight="700" fill="{TEXT}">{title}</text>'
            f'<text x="78" y="54" class="mono" font-size="12" fill="{MUTED}">{sub}</text>'
            f'<g><path d="M420,37 h22 m-8,-8 l8,8 l-8,8" fill="none" stroke="{col if col != "#FFFFFF" else GOLD}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;8 0;0 0;0 0" keyTimes="0;.15;.3;1" dur="2.4s" begin="{i * 0.3:.1f}s" repeatCount="indefinite"/></g>'
            f"</g>"
        )
    defs = card_defs(u, W, H)
    body = f"""
<g clip-path="url(#k-clip)">
{card_bg(u, W, H)}
{stars(u, 30, W, 200, 21)}
{waves(W, 360, "#123a5c", .9, 5, 8)}
{waves(W, 372, "#0d2c4a", 1, 7, 5.5, 320)}
<g>
  <animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="3.2s" begin="0s" repeatCount="indefinite" calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1"/>
  <image href="data:image/png;base64,{pointing_b64}" x="40" y="20" width="{355 * 369 / 400:.0f}" height="355"/>
</g>
<text x="470" y="60" class="pir" font-size="38" fill="{GOLD}">Set sail together</text>
{"".join(els)}
</g>
{card_border(u, W, H)}"""
    return svg_doc(W, H, "Connect with Shubham", defs, body)


def main() -> None:
    data = json.loads((ROOT / "data" / "github.json").read_text())
    repo_count = len([r for r in data["repos"] if not r["fork"] and r["name"] != "ShubJ"])
    portrait = b64(BUILD / "portrait.png")
    pointing = b64(BUILD / "pointing.png")
    files = {
        "hero.svg": build_hero(portrait, repo_count),
        "stack.svg": build_stack(),
        "crew.svg": build_crew(portrait, data),
        "connect.svg": build_connect(pointing, repo_count),
    }
    for name, svg in files.items():
        (ROOT / name).write_text(svg)
        print(name, len(svg) // 1024, "KB")


if __name__ == "__main__":
    main()
