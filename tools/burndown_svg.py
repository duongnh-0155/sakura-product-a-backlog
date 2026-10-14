"""Tiny dependency-free SVG burndown chart (ideal vs actual, light/dark friendly colors)."""


def render(name, b, w=640, h=320, pad=48):
    days, total, rem = b["days"], max(b["committed_swp"], 1), b["remaining"]
    x = lambda d: pad + (w - 2 * pad) * d / days  # noqa: E731
    y = lambda v: h - pad - (h - 2 * pad) * v / total  # noqa: E731
    actual = " ".join(f"{x(d):.1f},{y(v):.1f}" for d, v in enumerate(rem))
    grid = "".join(f'<line x1="{x(d):.1f}" y1="{pad}" x2="{x(d):.1f}" y2="{h - pad}" stroke="#ddd"/>'
                   f'<text x="{x(d):.1f}" y="{h - pad + 16}" font-size="11" text-anchor="middle">{d}</text>' for d in range(days + 1))
    ticks = "".join(f'<text x="{pad - 6}" y="{y(v) + 4:.1f}" font-size="11" text-anchor="end">{v}</text>'
                    for v in sorted({0, total // 2, total}))
    last_d, last_v = len(rem) - 1, rem[-1]
    forecast = ""
    if last_d < days:  # open sprint: straight-line forecast from current velocity
        rate = (total - last_v) / last_d if last_d else 0
        end_v = max(last_v - rate * (days - last_d), 0)
        forecast = (f'<polyline points="{x(last_d):.1f},{y(last_v):.1f} {x(days):.1f},{y(end_v):.1f}" fill="none" '
                    f'stroke="#d97706" stroke-width="2" stroke-dasharray="3 4"/>'
                    f'<text x="{x(days) - 4:.1f}" y="{y(end_v) - 8:.1f}" font-size="11" text-anchor="end" fill="#d97706">予測 残 {end_v:.0f}</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="sans-serif">'
            f'<rect width="{w}" height="{h}" fill="#fff"/>{grid}{ticks}'
            f'<text x="{pad}" y="24" font-size="14" font-weight="bold">{name} バーンダウン（SWP、{b["start"]}〜{b["end"]}）</text>'
            f'<line x1="{x(0)}" y1="{y(total)}" x2="{x(days)}" y2="{y(0)}" stroke="#9ca3af" stroke-width="2" stroke-dasharray="6 4"/>'
            f'<polyline points="{actual}" fill="none" stroke="#2563eb" stroke-width="3"/>{forecast}'
            f'<text x="{w - pad}" y="{pad - 8}" font-size="11" text-anchor="end">灰破線 = 理想 ／ 青 = 実績 ／ 橙点線 = 予測</text>'
            f'<text x="{w / 2}" y="{h - 10}" font-size="11" text-anchor="middle">稼働日</text></svg>')
