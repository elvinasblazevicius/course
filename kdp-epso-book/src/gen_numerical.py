"""Generate numerical-reasoning items with computed answers and error-model distractors (rev. 2)."""
import json
import math
import random
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LETTERS = "ABCD"

COUNTRIES = ["Austria", "Belgium", "Croatia", "Czechia", "Denmark", "Estonia", "Finland", "France", "Greece",
             "Ireland", "Latvia", "Lithuania", "Netherlands", "Poland", "Portugal", "Slovakia", "Slovenia",
             "Spain", "Sweden", "Hungary", "Romania", "Italy", "Germany"]
TOWNS = ["Northport", "Eastbay", "Westfield", "Southmere", "Midvale", "Riverton", "Lakeside", "Hillcrest",
         "Brookhaven", "Stonebridge", "Fairhaven", "Kingsford"]
UNITS = ["Unit A", "Unit B", "Unit C", "Unit D", "Unit E"]
SECTORS = ["Transport", "Energy", "Research", "Health", "Education", "Agriculture", "Digital", "Culture"]
# non-euro currencies outside the EU (evergreen: none of these will be replaced by the euro)
CURRENCIES = [("Swiss franc", "CHF", 0.95, 2), ("Norwegian krone", "NOK", 11.6, 2), ("Pound sterling", "GBP", 0.85, 2),
              ("US dollar", "USD", 1.08, 2), ("Japanese yen", "JPY", 160.0, 1), ("Icelandic króna", "ISK", 150.0, 1),
              ("Canadian dollar", "CAD", 1.47, 2)]

FALLBACKS = Counter()


def the(c):
    return "the Netherlands" if c == "Netherlands" else c


def fmt_num(x, dp=0):
    return f"{x:,.{dp}f}".replace("-", "−")


def fmt_eur(x, dp=0):
    return "€" + fmt_num(x, dp)


def fmt_pct(x, dp=1):
    return f"{x:.{dp}f}%".replace("-", "−")


def signed(x, dp=1):
    return (f"{x:+.{dp}f}").replace("-", "−")


class Builder:
    def __init__(self, rng):
        self.rng = rng

    def options(self, correct, pool, fmt, target_idx, min_rel_gap=0.03, band=(0.35, 2.8), abs_gap=None):
        """Options in fixed (unsorted) order with the key at target_idx. Distractors come from `pool`
        (error models, in order of preference); a nearby-error fallback is used only if the pool is short."""
        cf = fmt(correct)

        def ok(p, chosen):
            if p is None or p <= 0 or not (band[0] * correct <= p <= band[1] * correct):
                return False
            if fmt(p) == cf or any(fmt(p) == fmt(q) for q in chosen):
                return False
            for q in chosen + [correct]:
                if abs_gap is not None:
                    if abs(p - q) < abs_gap:
                        return False
                elif abs(p - q) / max(abs(q), 1e-9) < min_rel_gap:
                    return False
            return True

        chosen = []
        for p in pool:
            if len(chosen) == 3:
                break
            if ok(p, chosen):
                chosen.append(p)
        if len(chosen) < 3:
            extra = [2 * correct - p for p in chosen] + [correct * m for m in (1.18, 0.84, 1.33, 0.72)]
            for p in extra:
                if len(chosen) == 3:
                    break
                if ok(p, chosen):
                    chosen.append(p); FALLBACKS["fallback"] += 1
        assert len(chosen) == 3, (correct, pool)
        if abs_gap is None and min(abs(p - correct) / correct for p in chosen) > 0.10:
            # exam-realistic near miss: make one option close (5-8%) so estimation alone cannot decide
            def num(t):
                mm = re.search(r"[\d,]+(?:\.(\d+))?", t)
                return float(mm.group(0).replace(",", "")), len(mm.group(1) or "")
            cv, dec = num(cf)
            for m in self.rng.sample([1.06, 0.94, 1.07, 0.93, 1.05, 0.95, 1.08, 0.92], 8):
                v = correct * m
                nv, _ = num(fmt(v))
                if abs(nv - cv) < 2 * 10 ** (-dec) - 1e-9:
                    continue
                if ok(v, chosen[:2]):
                    chosen[2] = v; FALLBACKS["near"] += 1
                    break
        self.rng.shuffle(chosen)
        vals = chosen[:target_idx] + [correct] + chosen[target_idx:]
        strs = [fmt(v) for v in vals]
        assert len(set(strs)) == 4
        return strs, LETTERS[target_idx]


def table_fig(title, columns, rows, note=None):
    return {"type": "table", "title": title, "columns": columns, "rows": rows, "note": note}


def bar_fig(title, categories, series, unit):
    return {"type": "bar", "title": title, "categories": categories, "series": series, "unit": unit}


def line_fig(title, categories, series, unit):
    return {"type": "line", "title": title, "categories": categories, "series": series, "unit": unit}


def pie_fig(title, labels, values, total_label):
    return {"type": "pie", "title": title, "labels": labels, "values": values, "total_label": total_label}


def order_choices(best, others, tgt):
    o = others[:3]
    o.insert(tgt, best)
    return o


# ---------------------------------------------------------------- templates
def t_pct_change(rng, B, tgt):
    ctry = rng.sample(COUNTRIES, 5)
    data = {}
    for c in ctry:
        v1 = rng.randint(180, 950)
        v2 = round(v1 * rng.uniform(0.88, 1.18))
        v3 = round(v2 * rng.uniform(0.9, 1.22))
        data[c] = [v1, v2, v3]
    c = rng.choice(ctry)
    v1, v2, v3 = data[c]
    if abs(v3 - v1) / v1 < 0.08:
        v3 = round(v1 * rng.choice([1.14, 1.19, 0.86, 1.23])); data[c][2] = v3
    ans = (v3 - v1) / v1 * 100
    direction = "increase" if ans > 0 else "decrease"
    a = abs(ans)
    pool = [abs(v3 - v1) / v3 * 100, abs((v2 - v1) / v1 * 100 + (v3 - v2) / v2 * 100),
            abs(v3 - v2) / v2 * 100, abs(v2 - v1) / v1 * 100, abs(v3 - v1) / v2 * 100]
    opts, key = B.options(a, pool, fmt_pct, tgt, 0.04)
    title, measure = rng.choice([("Visitors to national science museums (thousands)", "the number of visitors to science museums"),
                                 ("Visitors to national art galleries (thousands)", "the number of visitors to art galleries"),
                                 ("Overnight stays in campsites (thousands)", "the number of overnight stays in campsites")])
    fig = table_fig(title, ["Country", "Year 1", "Year 2", "Year 3"], [[k] + [fmt_num(x) for x in data[k]] for k in ctry])
    q = f"By approximately what percentage did {measure} in {the(c)} {direction} between Year 1 and Year 3?"
    expl = [f"Percentage change uses the earlier value as the base: ({fmt_num(v3)} − {fmt_num(v1)}) ÷ {fmt_num(v1)} × 100.",
            f"= {fmt_num(v3 - v1)} ÷ {fmt_num(v1)} × 100 ≈ {fmt_pct(ans)}, i.e. {'an' if direction == 'increase' else 'a'} {direction} of about {fmt_pct(a)}.",
            "Typical errors: dividing by the Year 3 value (wrong base), or adding the two year-on-year percentage changes (percentages do not add)."]
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="foundation", skill="Percentage change")


def t_share(rng, B, tgt):
    regions = rng.sample(["North", "South", "East", "West", "Central"], 4)
    secs = rng.sample(SECTORS, 4)
    data = {r: [rng.randint(12, 95) * 10 for _ in secs] for r in regions}
    r = rng.choice(regions); si = rng.randrange(4)
    tot_r = sum(data[r]); val = data[r][si]
    col_tot = sum(data[x][si] for x in regions)
    pool = [val / col_tot * 100, val / (tot_r - val) * 100, sum(data[r][:2]) / tot_r * 100 if si >= 2 else sum(data[r][2:]) / tot_r * 100,
            val / sum(data[x][si] for x in regions if x != r) * 100]
    ans = val / tot_r * 100
    opts, key = B.options(ans, pool, fmt_pct, tgt, 0.05)
    tt, unit_word = rng.choice([("Regional development fund allocations by sector (€ million)", "allocation"),
                                ("Research grants awarded by field and region (€ million)", "grant funding"),
                                ("Infrastructure investment by sector and region (€ million)", "investment")])
    fig = table_fig(tt, ["Region"] + secs + ["Total"],
                    [[x] + [fmt_num(v) for v in data[x]] + [fmt_num(sum(data[x]))] for x in regions])
    q = f"What percentage of the {r} region’s total {unit_word} went to {secs[si]}?"
    expl = [f"The {r} region’s total allocation is €{fmt_num(tot_r)} million, of which {secs[si]} received €{fmt_num(val)} million.",
            f"{fmt_num(val)} ÷ {fmt_num(tot_r)} × 100 ≈ {fmt_pct(ans)}.",
            f"Typical errors: dividing by the {secs[si]} column total (the region’s share of that sector) or by the remainder instead of the total."]
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="foundation", skill="Share of total")


def t_currency(rng, B, tgt):
    cs = rng.sample(CURRENCIES, 4)
    rates = [(n, code, round(r * rng.uniform(0.96, 1.04), dp), dp) for n, code, r, dp in cs]
    item = rng.choice(["a standard office laptop", "an annual museum pass", "a conference registration", "an ergonomic office chair"])
    base_eur = rng.uniform(380, 620)
    prices = []
    for _, _, r, _ in rates:
        p = r * base_eur * rng.uniform(0.85, 1.2)
        unit = 10 if r > 50 else 1
        prices.append(round(p / unit) * unit)
    eur = [p / r for p, (_, _, r, _) in zip(prices, rates)]
    i, j = max(range(4), key=lambda k: eur[k]), min(range(4), key=lambda k: eur[k])
    if eur[i] - eur[j] < 40:
        prices[i] = round(prices[i] * 1.2); eur[i] = prices[i] / rates[i][2]
    ei, ej = eur[i], eur[j]
    ans = ei - ej
    mid = sorted(range(4), key=lambda k: eur[k])[1:3]
    pool = [ei - eur[mid[0]], eur[mid[1]] - ej, ei - eur[mid[1]], eur[mid[0]] - ej, ans * 1.5]
    opts, key = B.options(ans, pool, lambda x: fmt_eur(x), tgt, 0.12, band=(0.2, 3))
    fig = table_fig(f"Price of {item} in four markets (fictitious prices and rates)",
                    ["Currency", "Code", "Units per €1", "Local price"],
                    [[n, code, f"{r:.{dp}f}", fmt_num(p)] for (n, code, r, dp), p in zip(rates, prices)])
    q = f"In euros, approximately how much more does {item} cost in the most expensive of the four markets than in the cheapest?"
    expl = ["Convert every price to euros by DIVIDING the local price by the number of units per €1:",
            "; ".join(f"{code}: {fmt_num(p)} ÷ {r:.{dp}f} ≈ {fmt_eur(p / r, 2)}" for (n, code, r, dp), p in zip(rates, prices)) + ".",
            f"Most expensive ({rates[i][1]}) − cheapest ({rates[j][1]}) ≈ {fmt_eur(ei, 2)} − {fmt_eur(ej, 2)} = {fmt_eur(ans, 2)}, i.e. about {fmt_eur(ans)}.",
            "Typical errors: ranking the markets by local price (the currencies are not comparable) or comparing the wrong pair of markets."]
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="intermediate", skill="Currency conversion")


def t_points(rng, B, tgt):
    ctry = rng.sample(COUNTRIES, 4)
    yrs = ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    series = []
    for c in ctry:
        v = rng.uniform(5.0, 12.0); vals = []
        for _ in yrs:
            vals.append(round(v, 1)); v = max(3.0, v + rng.uniform(-1.4, 1.2))
        series.append({"name": c, "values": vals})
    s = rng.choice(series)
    a, b = sorted(rng.sample(range(5), 2))
    if abs(s["values"][b] - s["values"][a]) < 1.2:
        s["values"][b] = round(s["values"][a] + rng.choice([-2.1, -1.6, 1.7, 2.4]), 1)
    va, vb = s["values"][a], s["values"][b]
    mode = rng.choice(["pct", "pp"])
    word = "rise" if vb > va else "fall"
    if mode == "pp":
        ans = abs(vb - va)
        others = [abs(s["values"][k] - va) for k in range(5) if k not in (a, b)]
        pool = [abs(vb - va) / va * 100, abs(vb - va) / vb * 100] + others
        opts, key = B.options(ans, pool, lambda x: f"{x:.1f} percentage points", tgt, 0.08, band=(0.2, 6))
        q = f"By how many percentage points did the unemployment rate in {the(s['name'])} {word} between {yrs[a]} and {yrs[b]}?"
        expl = [f"A change in percentage points is the simple difference between the two rates: {vb:.1f} − {va:.1f} = {signed(vb - va)} points, i.e. a {word} of {ans:.1f} percentage points.",
                "Typical error: computing the relative (percentage) change instead."]
        diff = "foundation"
    else:
        ans = abs(vb - va) / va * 100
        others = [abs(s["values"][k] - va) / va * 100 for k in range(5) if k not in (a, b)]
        pool = [abs(vb - va) / vb * 100, abs(vb - va) * 10] + others + [abs(vb - va)]
        opts, key = B.options(ans, pool, fmt_pct, tgt, 0.08, band=(0.1, 4))
        q = f"By approximately what percentage did the unemployment rate in {the(s['name'])} {word} between {yrs[a]} and {yrs[b]}?"
        expl = [f"Relative change = (new − old) ÷ old × 100 = ({vb:.1f} − {va:.1f}) ÷ {va:.1f} × 100 ≈ {signed((vb - va) / va * 100)}%, i.e. a {word} of about {fmt_pct(ans)}.",
                f"Typical errors: {abs(vb - va):.1f} is the change in percentage points, not a percentage change; another is dividing by the later value."]
        diff = "intermediate"
    fig = line_fig("Unemployment rate (% of labour force)", yrs, series, "%")
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty=diff, skill="Percentage points vs percent")


def t_per_capita(rng, B, tgt):
    regs = rng.sample(["Northern region", "Southern region", "Eastern region", "Western region", "Central region",
                       "Coastal region", "Alpine region", "Island region"], 5)
    FALLBACKS["pc"] += 1
    kind = "highest" if FALLBACKS["pc"] % 2 else "lowest"
    while True:
        pops = [round(rng.uniform(0.4, 6.5), 2) for _ in regs]
        spend = [round(p * rng.uniform(90, 260), 1) for p in pops]
        pc = [s / p for s, p in zip(spend, pops)]
        srt = sorted(pc, reverse=(kind == "highest"))
        best = pc.index(srt[0])
        trap = spend.index(max(spend) if kind == "highest" else min(spend))
        if abs(srt[0] - srt[1]) / srt[1] > 0.05 and trap != best:
            break
    others = [k for k in range(5) if k not in (best, trap)]
    rng.shuffle(others)
    order = order_choices(best, [trap] + others[:2], tgt)
    fig = table_fig("Population and public spending on culture in five regions of one country",
                    ["Region", "Population (million)", "Spending (€ million)"],
                    [[c, f"{p:.2f}", fmt_num(s, 1)] for c, p, s in zip(regs, pops, spend)])
    q = f"Which of the following regions had the {kind} spending on culture per inhabitant?"
    lines = ["Spending per inhabitant = spending ÷ population (€ million ÷ million inhabitants = € per inhabitant):",
             "; ".join(f"{regs[k]} ≈ €{pc[k]:.0f}" for k in order) + ".",
             f"The {kind} figure is for the {regs[best]}. Trap: the {regs[trap]} has the {'largest' if kind == 'highest' else 'smallest'} total spending, but not the {kind} spending per inhabitant."]
    return dict(figure=fig, question=q, options=[regs[k] for k in order], answer=LETTERS[tgt], steps=lines,
                difficulty="intermediate", skill="Per-capita comparison")


WEIGHTED_CTX = [
    ("Staff numbers and average monthly salary by unit", "Unit", "Staff", "Average monthly salary (€)", "monthly salary across all staff", 38, 92, 100, fmt_eur),
    ("Candidates and average test score by test centre", "Centre", "Candidates", "Average score (points)", "score across all candidates", 52, 88, 1, lambda x: f"{x:.1f} points"),
    ("Training participants and average course length by department", "Department", "Participants", "Average hours", "number of training hours per participant", 6, 38, 1, lambda x: f"{x:.1f} hours"),
    ("Translation requests and average turnaround by language unit", "Unit", "Requests", "Average days", "turnaround time per request", 3, 19, 1, lambda x: f"{x:.2f} days"),
]


def t_weighted(rng, B, tgt):
    title, col0, col1, col2, what, lo, hi, mult, ff = rng.choice(WEIGHTED_CTX)
    while True:
        units = rng.sample(["North", "South", "East", "West", "Central"] if col0 != "Unit" else UNITS, 4)
        staff = [rng.randint(6, 48) for _ in units]
        sal = [rng.randint(lo, hi) * mult for _ in units]
        tot = sum(s * w for s, w in zip(staff, sal))
        ans = tot / sum(staff)
        simple = sum(sal) / 4
        if abs(simple - ans) / ans > 0.04:
            break
    big = staff.index(max(staff))
    excl = (tot - staff[big] * sal[big]) / (sum(staff) - staff[big])
    two = sorted(range(4), key=lambda k: -staff[k])[:2]
    two_avg = sum(staff[k] * sal[k] for k in two) / sum(staff[k] for k in two)
    pool = [simple, excl, (max(sal) + min(sal)) / 2, two_avg]
    opts, key = B.options(ans, pool, ff, tgt, 0.02)
    fig = table_fig(title, [col0, col1, col2], [[u, str(s), fmt_num(w)] for u, s, w in zip(units, staff, sal)])
    q = f"What is the average {what} in the four {col0.lower()}s combined?"
    expl = ["Weighted total = " + " + ".join(f"{s} × {fmt_num(w)}" for s, w in zip(staff, sal)) + f" = {fmt_num(tot)}.",
            f"Total {col1.lower()} = {sum(staff)}. Weighted average = {fmt_num(tot)} ÷ {sum(staff)} ≈ {ff(ans)}.",
            f"Typical error: the simple average of the four averages ({ff(simple)}) ignores the different group sizes."]
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="intermediate", skill="Weighted average")


def t_projection(rng, B, tgt):
    towns = rng.sample(TOWNS, 4)
    vals = [rng.randint(120, 900) * 10 for _ in towns]
    rates = [rng.choice([8, 10, 12, 15, 20]) for _ in towns]
    k = rng.randrange(4); n = 3
    g = 1 + rates[k] / 100
    ans = vals[k] * g ** n
    pool = [vals[k] * (1 + rates[k] * n / 100), vals[k] * g ** (n - 1), vals[k] * g ** (n + 1), vals[k] * (1 + rates[k] / 100 * (n + 1))]
    tt, colh, noun, verb = rng.choice([
        ("Plastic collected for recycling by four municipal schemes this year, and expected annual growth", "Collected this year (tonnes)", "tonnes", "collected"),
        ("Solar capacity installed on public buildings this year, and expected annual growth", "Installed this year (kW)", "kW", "installed"),
        ("Users of four e-government services this year, and expected annual growth", "Users this year", "users", "registered")])
    unit_sfx = {"tonnes": " t", "kW": " kW", "users": ""}[noun]
    opts, key = B.options(ans, pool, lambda x: fmt_num(x) + unit_sfx, tgt, 0.012)
    fig = table_fig(tt, ["Municipality", colh, "Expected annual growth"],
                    [[c, fmt_num(v), f"{r}%"] for c, v, r in zip(towns, vals, rates)])
    q = (f"If the figure for {towns[k]} grows at its expected annual rate, compounded, approximately how many {noun} "
         f"will be {verb} three years from now?")
    f = lambda x: fmt_num(x) + unit_sfx
    names = [(pool[0], f"simple growth, {fmt_num(vals[k])} × (1 + 3 × {rates[k] / 100:g}) = {f(pool[0])}, ignores compounding"),
             (pool[1], f"compounding for only two years gives {f(pool[1])}"),
             (pool[2], f"compounding for four years gives {f(pool[2])}"),
             (pool[3], f"simple growth over four years gives {f(pool[3])}")]
    printed = [t for v, t in names if f(v) in opts]
    expl = [f"Compound growth: {fmt_num(vals[k])} × {g:g}³ = {fmt_num(vals[k])} × {g ** n:.4f} ≈ {fmt_num(ans)} {noun}."]
    if printed:
        expl.append("Traps among the options: " + "; ".join(printed) + ".")
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="advanced", skill="Compound growth")


def t_scaling(rng, B, tgt):
    units = rng.sample(UNITS, 4)
    k = rng.randrange(4)
    inc = rng.choice([10, 20, 25, 40, 50])
    step = {10: 10, 20: 5, 25: 4, 40: 5, 50: 2}[inc]
    while True:
        women = [rng.randint(8, 40) for _ in units]
        men = [rng.randint(8, 40) for _ in units]
        women[k] = rng.randint(2, 8) * step
        men[k] = rng.randint(2, 8) * step
        if women[k] != men[k]:
            break
    tot = women[k] + men[k]
    total_new = tot * (1 + inc / 100)
    ans = total_new * women[k] / tot
    pool = [women[k] + tot * inc / 100, total_new * men[k] / tot, women[k] + inc, total_new / 2]
    pool = [round(x) for x in pool]
    opts, key = B.options(ans, pool, lambda x: f"{x:.0f}", tgt, 0.04)
    grp_t, a_nm, b_nm, whole = rng.choice([("Staff by gender in four units", "Women", "Men", "staff"),
                                         ("Trainees by contract type in four units", "Permanent", "Temporary", "trainees"),
                                         ("Interpreters by booth language in four teams", "French booth", "German booth", "interpreters")])
    fig = bar_fig(grp_t, units, [{"name": a_nm, "values": women}, {"name": b_nm, "values": men}], f"number of {whole}")
    q = (f"If the total number of {whole} in {units[k]} increases by {inc}% and the proportion of the “{a_nm}” group stays the same, "
         f"how many will be in the “{a_nm}” group?")
    expl = [f"{units[k]} has {women[k]} ({a_nm}) and {men[k]} ({b_nm}), {tot} in total.",
            f"New total = {tot} × {1 + inc / 100:g} = {total_new:g}; “{a_nm}” = {total_new:g} × {women[k]}/{tot} = {ans:g}.",
            f"Shortcut: if the proportion is unchanged, the “{a_nm}” group also grows by {inc}%: {women[k]} × {1 + inc / 100:g} = {ans:g}.",
            f"Typical errors: adding the whole increase to one group ({women[k] + round(tot * inc / 100)}) or calculating the other group instead."]
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="foundation", skill="Proportional scaling")


def t_reverse(rng, B, tgt):
    progs = rng.sample(["Student mobility grants", "Rural broadband support", "Cultural heritage restoration",
                        "Youth employment schemes", "Clean-bus procurement", "Coastal flood defences"], 4)
    ch = [rng.choice([-20, -15, -12, -8, 8, 12, 15, 20, 25, 30]) for _ in progs]
    old = [rng.randint(30, 260) * 20 for _ in progs]
    new = [o * (1 + c / 100) for o, c in zip(old, ch)]
    k = rng.randrange(4)
    ans = old[k]
    pool = [new[k] * (1 - ch[k] / 100), new[k] / (1 - ch[k] / 100), new[k] - ch[k] * 10, new[k]]
    opts, key = B.options(ans, pool, lambda x: f"€{fmt_num(x, 1)}k", tgt, 0.015)
    tt = rng.choice(["Budget for this year and change compared with last year", "Grant envelope this year and change on last year",
                     "Spending this year by programme and change compared with last year"])
    fig = table_fig(tt, ["Programme", "This year (€ thousand)", "Change on last year"],
                    [[p, fmt_num(n, 1), signed(c, 0) + "%"] for p, n, c in zip(progs, new, ch)])
    q = rng.choice([f"What was last year’s budget for the “{progs[k]}” programme?",
                    f"How much was allocated to “{progs[k]}” last year?",
                    f"Before this year’s change, what was the budget for “{progs[k]}”?"])
    expl = [f"This year = last year × {1 + ch[k] / 100:g}, so last year = this year ÷ {1 + ch[k] / 100:g}.",
            f"{fmt_num(new[k], 1)} ÷ {1 + ch[k] / 100:g} = {fmt_num(ans, 1)} (€ thousand).",
            f"Typical error: {'reducing' if ch[k] > 0 else 'increasing'} this year’s figure by {abs(ch[k])}% applies the percentage to the wrong base."]
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="intermediate", skill="Reverse percentage")


def t_bar_increase(rng, B, tgt):
    ports = rng.sample(TOWNS, 5)
    while True:
        y1 = [rng.randint(20, 90) * 10 for _ in ports]
        y2 = [round(v * rng.uniform(0.95, 1.45) / 10) * 10 for v in y1]
        inc = [(b - a) / a for a, b in zip(y1, y2)]
        absd = [b - a for a, b in zip(y1, y2)]
        srt = sorted(inc, reverse=True)
        best = inc.index(srt[0]); trap = absd.index(max(absd))
        if srt[0] - srt[1] > 0.04 and trap != best:
            break
    others = [k for k in range(5) if k not in (best, trap)]
    rng.shuffle(others)
    chosen = [trap] + others[:2]; rng.shuffle(chosen)
    order = order_choices(best, chosen, tgt)
    tt, place, what, unit = rng.choice([("Containers handled at five ports (thousand units)", "ports", "containers handled", "thousand containers"),
                                        ("Passengers at five regional airports (thousands)", "airports", "passenger numbers", "thousand passengers"),
                                        ("Visits to five public libraries (thousands)", "libraries", "visits", "thousand visits")])
    fig = bar_fig(tt, ports, [{"name": "Year 1", "values": y1}, {"name": "Year 2", "values": y2}], unit)
    q = f"Which of the following {place} recorded the largest percentage increase in {what} between Year 1 and Year 2?"
    steps = ["Percentage change = (Year 2 − Year 1) ÷ Year 1 × 100:",
             "; ".join(f"{ports[k]}: ({y2[k]} − {y1[k]}) ÷ {y1[k]} ≈ {fmt_pct(inc[k] * 100)}" for k in order) + ".",
             f"Largest: {ports[best]}. Trap: {ports[trap]} has the largest increase in absolute terms (+{absd[trap]} thousand), but from a larger base."]
    return dict(figure=fig, question=q, options=[ports[k] for k in order], answer=LETTERS[tgt], steps=steps,
                difficulty="intermediate", skill="Chart comparison")


def t_pie(rng, B, tgt):
    cats = rng.sample(["Staff", "Buildings", "IT systems", "Travel", "Studies", "Translation", "Training", "Communication"], 5)
    while True:
        cuts = sorted(rng.sample(range(5, 95), 4))
        shares = [b - a for a, b in zip([0] + cuts, cuts + [100])]
        if min(shares) >= 6:
            break
    total = rng.randint(24, 160) * 5
    i, j = rng.sample(range(5), 2)
    if shares[i] < shares[j]:
        i, j = j, i
    nxt = rng.choice([5, 10, 15, 20])
    ai, aj = total * shares[i] / 100, total * shares[j] / 100
    ans = ai * (1 + nxt / 100) - aj
    pool = [ai - aj, total * (shares[i] + nxt - shares[j]) / 100, (ai - aj) * (1 + nxt / 100), ai * nxt / 100]
    opts, key = B.options(ans, pool, lambda x: fmt_eur(x, 1) + " million", tgt, 0.025, band=(0.05, 4))
    owner = rng.choice(["an agency’s", "a directorate’s", "a regional office’s"])
    fig = pie_fig(f"Breakdown of {owner} annual budget (total €{total} million)", cats, shares, f"Total: €{total} million")
    q = rng.choice([
        f"Next year the {cats[i]} budget is to rise by {nxt}% while all other items stay unchanged. By how much will the {cats[i]} budget then exceed the {cats[j]} budget?",
        f"If spending on {cats[i]} grows by {nxt}% and every other item is frozen, what will the gap be between {cats[i]} and {cats[j]}?",
        f"After a {nxt}% increase in the {cats[i]} line (all other lines unchanged), how much larger than {cats[j]} will {cats[i]} be?"])
    expl = [f"{cats[i]} now = {shares[i]}% × €{total} million = €{ai:g} million; after +{nxt}%: €{ai * (1 + nxt / 100):.2f} million.",
            f"{cats[j]} = {shares[j]}% × €{total} million = €{aj:g} million.",
            f"Difference = €{ans:.2f} million ≈ €{ans:.1f} million. Typical error: adding {nxt} percentage points to the share instead of raising the amount by {nxt}%."]
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="advanced", skill="Pie chart, two-step")


def t_speed(rng, B, tgt):
    while True:
        towns = rng.sample(TOWNS, 8)
        routes = [f"{towns[2 * r]}–{towns[2 * r + 1]}" for r in range(4)]
        dist = [rng.randint(60, 380) for _ in routes]
        spd = [rng.choice([80, 90, 100, 110, 120, 140, 160]) for _ in routes]
        k = rng.randrange(4)
        new_spd = spd[k] + rng.choice([20, 30, 40, 50])
        t_old = dist[k] / spd[k] * 60; t_new = dist[k] / new_spd * 60
        ans = t_old - t_new
        if abs(ans - round(ans)) < 0.3 and ans >= 8:
            break
    ans_r = round(ans)
    pool = [round(t_old * (new_spd - spd[k]) / spd[k]), round(t_new), round(ans * 1.5), round(ans / 2),
            round(dist[k] / (new_spd - spd[k]) * 60 / 6)]
    opts, key = B.options(ans_r, pool, lambda x: f"{x:.0f} minutes", tgt, abs_gap=3, band=(0.3, 4))
    mode_t, vehicle = rng.choice([("Rail routes: distance and average train speed", "train"), ("Bus routes: distance and average coach speed", "coach"),
                                  ("Ferry routes: distance and average ferry speed", "ferry")])
    fig = table_fig(mode_t, ["Route", "Distance (km)", "Average speed (km/h)"],
                    [[r, str(d), str(s)] for r, d, s in zip(routes, dist, spd)])
    q = f"If the {vehicle}’s average speed on the {routes[k]} route rose to {new_spd} km/h, approximately how many minutes would each journey save?"
    expl = [f"Time = distance ÷ speed. Now: {dist[k]} ÷ {spd[k]} × 60 = {t_old:.1f} minutes. New: {dist[k]} ÷ {new_spd} × 60 = {t_new:.1f} minutes.",
            f"Saving = {t_old:.1f} − {t_new:.1f} = {ans:.1f}, i.e. about {ans_r} minutes.",
            "Typical error: assuming journey time falls by the same percentage as speed rises."]
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="intermediate", skill="Rates and time")


def t_ratio_missing(rng, B, tgt):
    ctry = rng.sample(COUNTRIES, 4)
    apps = [x * 100 for x in rng.sample(range(3, 31), 4)]  # distinct multiples of 100 → whole-number counts
    rates = [rng.choice([12, 15, 18, 20, 24, 25, 30, 35, 40]) for _ in ctry]
    k = rng.randrange(4)
    approved = [a * r // 100 for a, r in zip(apps, rates)]
    mode = rng.choice(["rejected", "need"])
    if mode == "rejected":
        ans = apps[k] - approved[k]
        other = (k + 1) % 4
        pool = [approved[k], apps[other] - approved[other], apps[k] - approved[k] * 2, apps[k] * (1 - rates[k] / 200)]
        opts, key = B.options(ans, pool, lambda x: fmt_num(round(x)), tgt, 0.04)
        q = f"How many applications from {the(ctry[k])} were rejected?"
        expl = [f"Approved = {fmt_num(apps[k])} × {rates[k]}% = {fmt_num(approved[k])}.",
                f"Rejected = {fmt_num(apps[k])} − {fmt_num(approved[k])} = {fmt_num(ans)}.",
                "Typical errors: giving the number approved instead of rejected, or reading another country’s row."]
        diff = "foundation"
    else:
        tr = rng.choice([30, 40, 45, 50])
        while tr <= rates[k] + 5:
            tr += 10
        ans = apps[k] * tr // 100 - approved[k]
        pool = [apps[k] * tr // 100, (tr - rates[k]) * 10, apps[k] * (tr - rates[k]) / 100 * 1.25, apps[k] * (tr - rates[k]) / 100 * 0.75]
        opts, key = B.options(ans, pool, lambda x: fmt_num(round(x)), tgt, 0.06)
        q = (f"If the number of applications stayed the same, how many additional applications from {the(ctry[k])} would need to be approved "
             f"for its approval rate to reach {tr}%?")
        expl = [f"Approvals needed = {fmt_num(apps[k])} × {tr}% = {fmt_num(apps[k] * tr // 100)}.",
                f"Currently approved = {fmt_num(apps[k])} × {rates[k]}% = {fmt_num(approved[k])}. Additional approvals = {fmt_num(ans)}.",
                "Typical error: giving the total number of approvals needed instead of the additional ones."]
        diff = "intermediate"
    fig = table_fig("Grant applications received and approval rate", ["Country", "Applications", "Approval rate"],
                    [[c, fmt_num(a), f"{r}%"] for c, a, r in zip(ctry, apps, rates)])
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty=diff, skill="Rates and counts")


def t_two_tables(rng, B, tgt):
    courses = rng.sample(["Project management", "Negotiation skills", "Data analysis", "Drafting legislation",
                          "Public speaking", "Financial rules", "Leadership basics"], 4)
    quarters = ["Q1", "Q2", "Q3", "Q4"]
    parts = {c: [rng.randint(4, 30) for _ in quarters] for c in courses}
    cost = {c: rng.randint(12, 60) * 10 for c in courses}
    c = rng.choice(courses)
    q0 = rng.choice([0, 1]); q1 = q0 + rng.choice([1, 2])
    sel = list(range(q0, q1 + 1))
    n = sum(parts[c][x] for x in sel)
    ans = n * cost[c]
    nxt = courses[(courses.index(c) + 1) % 4]
    pool = [(parts[c][q0] + parts[c][q1]) * cost[c] if len(sel) > 2 else (n + parts[c][min(3, q1 + 1)]) * cost[c],
            sum(parts[c]) * cost[c], n * cost[nxt], sum(parts[nxt][x] for x in sel) * cost[c]]
    opts, key = B.options(ans, pool, lambda x: fmt_eur(x), tgt, 0.05)
    fig = {"type": "tables", "tables": [
        table_fig("Table 1 — Participants per training course", ["Course"] + quarters,
                  [[x] + [str(v) for v in parts[x]] for x in courses]),
        table_fig("Table 2 — Cost per participant (€)", ["Course", "Cost (€)"], [[x, fmt_num(cost[x])] for x in courses])]}
    qtxt = f"{quarters[q0]} to {quarters[q1]} inclusive"
    q = rng.choice([f"What was the total cost of the “{c}” course for {qtxt}?",
                    f"How much did the “{c}” course cost in total over {qtxt}?",
                    f"Over {qtxt}, what did the “{c}” course cost altogether?"])
    expl = [f"Participants {qtxt}: " + " + ".join(str(parts[c][x]) for x in sel) + f" = {n}.",
            f"Total cost = {n} × €{fmt_num(cost[c])} = {fmt_eur(ans)}.",
            "Typical errors: including the wrong quarters, using the whole year, or reading the wrong row of either table."]
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="intermediate", skill="Combining two tables")


def t_index(rng, B, tgt):
    ctry = rng.sample(COUNTRIES, 4)
    yrs = ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    data = {}
    for c in ctry:
        v = 100.0; row = [100.0]
        for _ in yrs[1:]:
            v = v * rng.uniform(1.0, 1.09); row.append(round(v, 1))
        data[c] = row
    c = rng.choice(ctry)
    a, b = 2, 4
    if data[c][b] - data[c][a] < 6:
        data[c][b] = round(data[c][a] * rng.choice([1.08, 1.11, 1.14]), 1)
    ia, ib = data[c][a], data[c][b]
    ans = (ib - ia) / ia * 100
    pool = [ib - ia, ib - 100, (ib - ia) / ib * 100, (ib - data[c][1]) / data[c][1] * 100, ia - 100]
    opts, key = B.options(ans, pool, fmt_pct, tgt, 0.06, band=(0.2, 5))
    idx_t, idx_w = rng.choice([("Index of average house prices (Year 1 = 100)", "average house prices"),
                               ("Index of consumer prices for public transport (Year 1 = 100)", "public-transport prices"),
                               ("Index of average energy bills (Year 1 = 100)", "average energy bills")])
    fig = table_fig(idx_t, ["Country"] + yrs,
                    [[k] + [f"{v:.1f}" for v in data[k]] for k in ctry])
    q = f"By approximately what percentage did {idx_w} in {the(c)} rise between Year 3 and Year 5?"
    expl = ["With index numbers, the percentage change between two years is (later index − earlier index) ÷ earlier index × 100.",
            f"({ib:.1f} − {ia:.1f}) ÷ {ia:.1f} × 100 ≈ {fmt_pct(ans)}.",
            f"Typical errors: subtracting the indices ({ib - ia:.1f} is a change in index points, not per cent) or measuring from the base year (index − 100)."]
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="intermediate", skill="Index numbers")


def t_ratio(rng, B, tgt):
    langs = rng.sample(["English", "French", "German", "Spanish", "Italian", "Polish", "Dutch", "Swedish"], 4)
    a, b = rng.choice([(3, 2), (4, 3), (5, 3), (5, 4), (7, 4), (2, 5), (3, 4), (3, 5), (7, 5), (5, 2)])
    m = rng.randint(6, 25)
    x, y = a * m, b * m
    other = [rng.randint(20, 160) for _ in range(2)]
    vals = [x, y] + other
    rows = list(zip(langs, vals)); rng.shuffle(rows)
    key_s = f"{a}:{b}"
    cands = [f"{b}:{a}"]
    for da, db in [(1, 0), (0, 1), (1, 1), (-1, 0), (0, -1), (2, 1)]:
        aa, bb = a + da, b + db
        if aa > 0 and bb > 0 and math.gcd(aa, bb) == 1 and aa != bb:
            cands.append(f"{aa}:{bb}")
    opts_d = []
    for p in cands:
        if p != key_s and p not in opts_d:
            opts_d.append(p)
    opts_d = [opts_d[0]] + rng.sample(opts_d[1:], 2)
    rng.shuffle(opts_d)
    opts = opts_d[:tgt] + [key_s] + opts_d[tgt:]
    tt, noun = rng.choice([("Translation requests received by a language unit in one month, by source language", "requests"),
                           ("Interpreting assignments in one quarter, by booth language", "assignments"),
                           ("Documents published in one year, by original language", "documents")])
    fig = table_fig(tt, ["Language", noun.capitalize()], [[l, str(v)] for l, v in rows])
    q = f"What is the ratio of {noun} in {langs[0]} to {noun} in {langs[1]}, in its simplest form?"
    g = math.gcd(x, y)
    expl = [f"{langs[0]} : {langs[1]} = {x} : {y}. Both numbers divide by {g}, giving {a}:{b}.",
            f"Typical error: reversing the order of the ratio ({b}:{a})."]
    return dict(figure=fig, question=q, options=opts, answer=LETTERS[tgt], steps=expl, difficulty="foundation", skill="Ratios")


def t_avg_time(rng, B, tgt):
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    teams = rng.sample(["Team North", "Team South", "Team East", "Team West"], 3)
    t = teams[rng.randrange(3)]
    for _ in range(200):
        data = {x: [rng.randint(18, 64) for _ in months] for x in teams}
        target = rng.choice([40, 45, 50, 55])
        first5 = sum(data[t][:5])
        need = target * 6 - first5
        if 15 <= need <= 110 and abs(need - target) > 6 and abs(need - first5 / 5) > 6:
            break
    data[t][5] = None
    pool = [target, round(first5 / 5), target * 5 - first5 if target * 5 - first5 > 0 else None, need + target // 5 * 2, need - target // 5 * 2]
    opts, key = B.options(need, pool, lambda v: f"{v:.0f}", tgt, 0.06, band=(0.15, 6))
    noun_avg = rng.choice(["cases", "files", "requests"])
    q = f"How many {noun_avg} would {t} need to close in June for its average over January to June to be exactly {target} per month?"
    expl = [f"For an average of {target} over 6 months, the total must be {target} × 6 = {target * 6}.",
            "January–May total = " + " + ".join(str(v) for v in data[t][:5]) + f" = {first5}.",
            f"June must therefore be {target * 6} − {first5} = {need}.",
            f"Typical errors: answering with the target itself ({target}) or with the current average (about {first5 / 5:.0f})."]
    rows = [[x] + [("—" if v is None else str(v)) for v in data[x]] for x in teams]
    fig = table_fig(f"{noun_avg.capitalize()} closed per month by three teams", ["Team"] + months, rows, note="— = figure not yet available")
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="intermediate", skill="Averages over time")


def t_share_pp(rng, B, tgt):
    secs = rng.sample(SECTORS, 5)
    y1 = [rng.randint(15, 90) * 10 for _ in secs]
    y2 = [round(v * rng.uniform(0.85, 1.35) / 10) * 10 for v in y1]
    k = rng.randrange(5)
    s1, s2 = y1[k] / sum(y1) * 100, y2[k] / sum(y2) * 100
    if abs(s2 - s1) < 1.0:
        y2[k] = round(y2[k] * (1.3 if s2 >= s1 else 0.7) / 10) * 10
        s2 = y2[k] / sum(y2) * 100
    ans = abs(s2 - s1)
    word = "rise" if s2 > s1 else "fall"
    pool = [abs(y2[k] - y1[k]) / y1[k] * 100, abs(s2 - s1) / s1 * 100, abs(y2[k] / sum(y1) - y1[k] / sum(y1)) * 100, s2 if s2 != ans else None]
    opts, key = B.options(ans, pool, lambda x: f"{x:.1f} percentage points", tgt, 0.06, band=(0.15, 8))
    fig = table_fig("Programme spending by sector (€ million)", ["Sector", "Year 1", "Year 2"],
                    [[c, fmt_num(a), fmt_num(b)] for c, a, b in zip(secs, y1, y2)] + [["Total", fmt_num(sum(y1)), fmt_num(sum(y2))]])
    q = f"By how many percentage points did {secs[k]}’s share of total spending {word} between Year 1 and Year 2?"
    expl = [f"Year 1 share = {fmt_num(y1[k])} ÷ {fmt_num(sum(y1))} = {s1:.2f}%. Year 2 share = {fmt_num(y2[k])} ÷ {fmt_num(sum(y2))} = {s2:.2f}%.",
            f"Change = {s2:.2f} − {s1:.2f} = {signed(s2 - s1, 2)} points, i.e. a {word} of about {ans:.1f} percentage points.",
            "Typical errors: giving the percentage change in the amount spent, or the relative change in the share, instead of the change in percentage points."]
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="advanced", skill="Shares and percentage points")


def t_harmonic(rng, B, tgt):
    while True:
        towns = rng.sample(TOWNS, 2)
        d = rng.choice([60, 80, 90, 120, 150, 180])
        v1, v2 = rng.sample([40, 45, 50, 60, 72, 75, 80, 90, 100, 120], 2)
        ans = 2 * d / (d / v1 + d / v2)
        if abs(ans - round(ans, 1)) < 1e-9 or True:
            break
    simple = (v1 + v2) / 2
    pool = [simple, max(v1, v2) - (max(v1, v2) - min(v1, v2)) / 4, ans * 2 / 1.9 if False else None, min(v1, v2) + (simple - min(v1, v2)) * 0.5]
    opts, key = B.options(ans, pool, lambda x: f"{x:.1f} km/h", tgt, 0.03, band=(0.5, 2))
    vt, vn = rng.choice([("Delivery van journey between two depots", "van"), ("Courier cyclist’s round trip between two offices", "courier"),
                         ("Shuttle bus round trip between two sites", "shuttle bus")])
    fig = table_fig(vt, ["Leg", "Distance (km)", "Average speed (km/h)"],
                    [[f"{towns[0]} → {towns[1]}", str(d), str(v1)], [f"{towns[1]} → {towns[0]}", str(d), str(v2)]])
    q = f"What was the {vn}’s average speed for the whole round trip?"
    t1, t2 = d / v1, d / v2
    expl = [f"Average speed = total distance ÷ total time. Times: {d} ÷ {v1} = {t1:.3f} h and {d} ÷ {v2} = {t2:.3f} h.",
            f"Average = {2 * d} ÷ {t1 + t2:.3f} ≈ {ans:.1f} km/h.",
            f"Typical error: averaging the two speeds ({simple:.1f} km/h). More time is spent at the lower speed, so the true average is lower."]
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="advanced", skill="Average speed")


def t_successive(rng, B, tgt):
    progs = rng.sample(["Membership fees", "Software licences", "Office rents", "Conference fees", "Translation tariffs"], 3)
    ch1 = [rng.choice([-20, -15, -10, 10, 15, 20, 25, 30]) for _ in progs]
    ch2 = [rng.choice([-25, -20, -15, -10, 10, 15, 20]) for _ in progs]
    k = rng.randrange(3)
    if ch1[k] + ch2[k] == 0 or ch1[k] * ch2[k] > 0 and rng.random() < 0.5:
        ch2[k] = -ch2[k] if ch2[k] * ch1[k] > 0 else ch2[k]
    net = ((1 + ch1[k] / 100) * (1 + ch2[k] / 100) - 1) * 100
    if abs(net) < 1:
        ch2[k] += 5; net = ((1 + ch1[k] / 100) * (1 + ch2[k] / 100) - 1) * 100
    ans = abs(net)
    word = "higher" if net > 0 else "lower"
    pool = [abs(ch1[k] + ch2[k]), abs(ch1[k]) + abs(ch2[k]), abs(ch1[k] * ch2[k]) / 100, ans * 1.5]
    opts, key = B.options(ans, pool, lambda x: f"{x:.1f}%", tgt, 0.05, band=(0.1, 10))
    fig = table_fig("Price changes over two years", ["Item", "Change in Year 1", "Change in Year 2"],
                    [[pname, signed(a, 0) + "%", signed(b, 0) + "%"] for pname, a, b in zip(progs, ch1, ch2)])
    q = f"Compared with the start of Year 1, by what percentage are {progs[k].lower()} {word} at the end of Year 2?"
    expl = [f"Successive changes multiply: (1 {'+' if ch1[k] > 0 else '−'} {abs(ch1[k]) / 100:g}) × (1 {'+' if ch2[k] > 0 else '−'} {abs(ch2[k]) / 100:g}) = {(1 + ch1[k] / 100) * (1 + ch2[k] / 100):.4f}.",
            f"So the price is {signed(net, 1)}% compared with the start, i.e. about {ans:.1f}% {word}.",
            f"Typical error: adding the two changes ({signed(ch1[k] + ch2[k], 0)}%). Percentages applied one after another do not add."]
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="advanced", skill="Successive percentage changes")


def t_currency_change(rng, B, tgt):
    n, code, r0, dp = rng.choice(CURRENCIES)
    r1 = round(r0 * rng.uniform(0.95, 1.0), dp); r2 = round(r0 * rng.uniform(1.03, 1.12), dp)
    if rng.random() < 0.5:
        r1, r2 = r2, r1
    p1 = round(r1 * rng.uniform(300, 700) / (10 if r0 > 50 else 1)) * (10 if r0 > 50 else 1)
    inc = rng.choice([4, 5, 6, 8, 10, 12])
    p2 = round(p1 * (1 + inc / 100), 2 if r0 < 50 else 0)
    e1, e2 = p1 / r1, p2 / r2
    net = (e2 - e1) / e1 * 100
    ans = abs(net); word = "risen" if net > 0 else "fallen"
    pool = [inc, abs((r2 - r1) / r1 * 100), abs(inc - (r2 - r1) / r1 * 100), abs(p2 * r2 - p1 * r1) / (p1 * r1) * 100]
    opts, key = B.options(ans, pool, lambda x: f"{x:.1f}%", tgt, 0.06, band=(0.05, 20))
    fig = table_fig(f"A supplier’s price in {n} and the exchange rate", ["", "Year 1", "Year 2"],
                    [[f"Price ({code})", fmt_num(p1, 0 if r0 > 50 else 2), fmt_num(p2, 0 if r0 > 50 else 2)],
                     [f"{code} per €1", f"{r1:.{dp}f}", f"{r2:.{dp}f}"]])
    q = f"In euro terms, by approximately what percentage has the supplier’s price {word} between Year 1 and Year 2?"
    expl = [f"Convert each year to euros: Year 1 {fmt_num(p1, 2)} ÷ {r1:.{dp}f} = {fmt_eur(e1, 2)}; Year 2 {fmt_num(p2, 2)} ÷ {r2:.{dp}f} = {fmt_eur(e2, 2)}.",
            f"Change = ({fmt_eur(e2, 2)} − {fmt_eur(e1, 2)}) ÷ {fmt_eur(e1, 2)} ≈ {signed(net, 1)}%.",
            f"Typical errors: quoting the {inc}% rise in local currency, or the change in the exchange rate alone; both ignore the other effect."]
    return dict(figure=fig, question=q, options=opts, answer=key, steps=expl, difficulty="advanced", skill="Currency and percentage change")


TEMPLATES = [t_pct_change, t_share, t_currency, t_points, t_per_capita, t_weighted, t_projection, t_scaling,
             t_reverse, t_bar_increase, t_pie, t_speed, t_ratio_missing, t_two_tables, t_index, t_ratio, t_avg_time,
             t_share_pp, t_harmonic, t_successive, t_currency_change]


def balanced_targets(n, rng):
    seq = []
    while len(seq) < n:
        block = list(range(4)); rng.shuffle(block)
        if seq and block[0] == seq[-1]:
            block[0], block[1] = block[1], block[0]
        seq += block
    return seq[:n]


def main(n=105, seed=20261002):
    rng = random.Random(seed)
    B = Builder(rng)
    targets = balanced_targets(n, rng)
    items = []
    t_cycle = []
    while len(items) < n:
        if not t_cycle:
            t_cycle = TEMPLATES[:]; rng.shuffle(t_cycle)
        tmpl = t_cycle.pop()
        try:
            it = tmpl(rng, B, targets[len(items)])
        except AssertionError:
            t_cycle.append(tmpl)
            continue
        assert it["answer"] == LETTERS[targets[len(items)]]
        assert len(set(it["options"])) == 4
        items.append(it)
    order = {"foundation": 0, "intermediate": 1, "advanced": 2}
    practice = sorted(items[:75], key=lambda x: order[x["difficulty"]])
    for i, it in enumerate(practice):
        it["id"] = f"N-{i + 1:03d}"
    mocks = items[75:]
    for i, it in enumerate(mocks):
        it["id"] = f"NM-{i + 1:02d}"
    # keys in final practice order must not run 3+ identical
    out = {"practice": practice, "mocks": mocks}
    (ROOT / "content" / "numerical.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print("numerical", len(practice), len(mocks), Counter(i["answer"] for i in items), dict(FALLBACKS))
    print(Counter(i["skill"] for i in items))
    print(Counter(i["difficulty"] for i in practice))
    seq = "".join(i["answer"] for i in practice)
    print("practice key seq", seq)


if __name__ == "__main__":
    main()
