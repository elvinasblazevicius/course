"""Abstract-reasoning series generator (rev. 2).

* Each item = 5 frames + answer; elements ("tracks") carry attributes that follow rules.
* Competing-rule test: every attribute's 5 visible values must admit exactly one next value
  under every rule in the library (constant, constant step, alternating steps, growing step, periods 2-4).
* Distractors are COMBINATIONS of tempting wrong values so the key is never found by the
  "most common value of every attribute" heuristic, nor by "odd one out".
* Near-duplicate geometry and repeated rule signatures are rejected.
"""
import itertools
import json
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LET = "ABCDE"
FILLS = ["white", "grey", "black"]
SHAPES_ORBIT = ["circle", "square", "triangle", "diamond"]
DIR = {1: "clockwise", -1: "anticlockwise"}
POLY_NAMES = {3: "triangle", 4: "square", 5: "pentagon", 6: "hexagon"}


def predict_all(values, modulus=None):
    preds = set()
    n = len(values)
    if len(set(values)) == 1:
        preds.add(values[0])
    if modulus:
        for s in range(modulus):
            if all((values[i + 1] - values[i]) % modulus == s for i in range(n - 1)):
                preds.add((values[-1] + s) % modulus)
        for s1 in range(modulus):
            for s2 in range(modulus):
                if s1 != s2 and all((values[i + 1] - values[i]) % modulus == (s1 if i % 2 == 0 else s2) for i in range(n - 1)):
                    preds.add((values[-1] + (s1 if (n - 1) % 2 == 0 else s2)) % modulus)
        for s in range(modulus):
            for sign in (1, -1):
                if all((values[i + 1] - values[i]) % modulus == (sign * (s + i)) % modulus for i in range(n - 1)):
                    preds.add((values[-1] + sign * (s + n - 1)) % modulus)
    else:
        d = [values[i + 1] - values[i] for i in range(n - 1)]
        if len(set(d)) == 1:
            preds.add(values[-1] + d[0])
        if len(d) >= 2 and d[0] != d[1] and all(d[i] == (d[0] if i % 2 == 0 else d[1]) for i in range(len(d))):
            preds.add(values[-1] + (d[0] if (n - 1) % 2 == 0 else d[1]))
        dd = [d[i + 1] - d[i] for i in range(len(d) - 1)]
        if len(set(dd)) == 1 and dd[0] != 0:
            preds.add(values[-1] + d[-1] + dd[0])
    for p in (2, 3, 4):
        if n > p and all(values[i] == values[i - p] for i in range(p, n)):
            preds.add(values[n - p])
    return preds


def seq_step(start, step, m):
    return [(start + step * i) % m for i in range(6)]


def seq_alt(start, s1, s2, m):
    out = [start]
    for i in range(5):
        out.append((out[-1] + (s1 if i % 2 == 0 else s2)) % m)
    return out


def fill_seq(rng):
    if rng.random() < 0.5:
        f0 = rng.randrange(3)
        return [FILLS[(f0 + i) % 3] for i in range(6)], "cycles " + " → ".join(FILLS[(f0 + i) % 3] for i in range(3))
    a, b = rng.sample(FILLS, 2)
    return [a if i % 2 == 0 else b for i in range(6)], f"alternates between {a} and {b}"


def pos_track(rng, level, shape, with_fill=False):
    start = rng.randrange(8)
    d = rng.choice([1, -1])
    r = rng.random()
    if level == "advanced" and r < 0.35:
        s1, s2 = rng.choice([(1, 2), (2, 1), (1, 3), (3, 1)])
        pos = seq_alt(start, s1 * d % 8, s2 * d % 8, 8)
        desc = f"the {shape} moves {DIR[d]} around the frame, alternately {s1} and {s2} positions at a time"
        sig = ("pos-alt", s1, s2)
    elif level == "advanced" and r < 0.55:
        pos = [(start + d * (i * (i + 1)) // 2) % 8 for i in range(6)]
        desc = f"the {shape} moves {DIR[d]} by 1, then 2, then 3, then 4 positions (one more each time)"
        sig = ("pos-grow",)
    else:
        s = rng.choice({"foundation": [1, 2], "intermediate": [1, 2, 3], "advanced": [1, 2, 3]}[level])
        pos = seq_step(start, s * d % 8, 8)
        desc = f"the {shape} moves {s} position{'s' if s > 1 else ''} {DIR[d]} around the frame each time"
        sig = ("pos", s, d)
    tr = {"kind": "orbit", "shape": shape, "pos": pos, "fill": ["black"] * 6, "desc": [desc], "sig": [sig]}
    if with_fill:
        tr["fill"], fd = fill_seq(rng)
        tr["desc"].append(f"the {shape}’s shading {fd}")
        tr["sig"].append(("fill",))
    return tr


def rot_track(rng, level):
    start = rng.randrange(8)
    d = rng.choice([1, -1])
    if level == "advanced" and rng.random() < 0.45:
        s1, s2 = rng.choice([(1, 2), (2, 1), (2, 3), (3, 2), (1, 3)])
        rot = seq_alt(start, s1 * d % 8, s2 * d % 8, 8)
        return {"kind": "arrow", "rot": rot, "desc": [f"the arrow rotates {DIR[d]}, alternately by {45 * s1}° and {45 * s2}°"],
                "sig": [("rot-alt", s1, s2)]}
    s = rng.choice({"foundation": [1, 2], "intermediate": [1, 2, 3], "advanced": [1, 2, 3]}[level])
    rot = seq_step(start, s * d % 8, 8)
    return {"kind": "arrow", "rot": rot, "desc": [f"the arrow rotates {45 * s}° {DIR[d]} each time"], "sig": [("rot", s, d)]}


def poly_track(rng, with_fill):
    cyc = rng.choice([[3, 4, 5], [3, 4, 5, 6], [6, 5, 4], [6, 5, 4, 3], [4, 5, 6]])
    off = rng.randrange(len(cyc))
    sides = [cyc[(off + i) % len(cyc)] for i in range(6)]
    desc = "the central shape cycles " + " → ".join(POLY_NAMES[c] for c in cyc) + " and then repeats"
    tr = {"kind": "polygon", "sides": sides, "fill": ["white"] * 6, "desc": [desc], "sig": [("poly", tuple(sides[:5]))]}
    if with_fill:
        tr["fill"], fd = fill_seq(rng)
        tr["desc"].append(f"the central shape’s shading {fd}")
        tr["sig"].append(("fill",))
    return tr


def dots_track(rng, level):
    if level == "advanced" and rng.random() < 0.5:
        d1, d2 = rng.choice([(2, -1), (-1, 2), (3, -1)])
        cnt = [rng.randint(1, 2)]
        for i in range(5):
            cnt.append(cnt[-1] + (d1 if i % 2 == 0 else d2))
        if min(cnt) < 1 or max(cnt) > 7:
            cnt = [1, 3, 2, 4, 3, 5]; d1, d2 = 2, -1
        return {"kind": "dots", "count": cnt,
                "desc": [f"the number of dots changes by {d1:+d}, then {d2:+d}, alternately".replace("-", "−")],
                "sig": [("dots-alt", d1, d2)]}
    d = rng.choice([1, -1])
    a = rng.randint(1, 2) if d > 0 else rng.randint(6, 7)
    cnt = [a + d * i for i in range(6)]
    return {"kind": "dots", "count": cnt, "desc": [f"the number of dots {'increases' if d > 0 else 'decreases'} by 1 each time"],
            "sig": [("dots", d, a)]}


def quad_track(rng):
    start = rng.randrange(4)
    d = rng.choice([1, -1])
    q = [(start + d * i) % 4 for i in range(6)]
    return {"kind": "quadrant", "quad": q, "desc": [f"the shaded quarter of the square moves one quarter {DIR[d]} each time"],
            "sig": [("quad", d)]}


def fshape_track(rng, level, alt=False):
    start = rng.randrange(4)
    d = rng.choice([1, -1])
    m0 = rng.randrange(2)
    mir = [(m0 + i) % 2 for i in range(6)]
    mir_desc = "the F-shape is shown in mirror image (flipped left to right) in every other figure"
    if alt:
        s1, s2 = rng.choice([(1, 2), (2, 1)])
        rot = seq_alt(start, s1 * d % 4, s2 * d % 4, 4)
        return {"kind": "fshape", "rot4": rot, "mir": mir,
                "desc": [f"the F-shape’s upright stroke (follow the end that carries the top bar) turns {DIR[d]}, "
                         f"alternately by {90 * s1}° and {90 * s2}°", mir_desc],
                "sig": [("frot-alt", s1, s2, d), ("mir",)]}
    rot = [(start + d * i) % 4 for i in range(6)]
    return {"kind": "fshape", "rot4": rot, "mir": mir,
            "desc": [f"the F-shape’s upright stroke (follow the end that carries the top bar) turns 90° {DIR[d]} each time", mir_desc],
            "sig": [("frot", d), ("mir",)]}


TEMPLATES = {
    "foundation": ["pos", "rot", "dots", "posfill", "pos", "rot"],
    "intermediate": ["rot+pos", "polyfill", "dots+pos", "quad+pos", "posfill", "rot+dots", "poly+pos", "flipalt"],
    "advanced": ["rot+posfill", "polyfill+pos", "dots+posfill", "rot+pos+pos2", "quad+posfill",
                 "polyfill+posfill", "rot+posfill+pos2", "quad+pos+pos2", "flipalt+pos"],
}


def build_tracks(rng, level, tmpl):
    t, used = [], []
    if "poly" in tmpl:
        used += ["square", "triangle"]
    for p in tmpl.split("+"):
        if p in ("pos", "posfill", "pos2"):
            sh = rng.choice([s for s in SHAPES_ORBIT if s not in used]); used.append(sh)
            tr = pos_track(rng, level if p != "pos2" else "intermediate", sh, with_fill=(p == "posfill"))
            if p == "pos2":
                tr["fill"] = ["white"] * 6
            t.append(tr)
        elif p == "rot":
            t.append(rot_track(rng, level))
        elif p == "poly":
            t.append(poly_track(rng, False))
        elif p == "polyfill":
            t.append(poly_track(rng, True))
        elif p == "dots":
            t.append(dots_track(rng, level))
        elif p == "quad":
            t.append(quad_track(rng))
        elif p in ("flip", "flipalt"):
            t.append(fshape_track(rng, level, alt=(p == "flipalt")))
    return t


ATTRS = {"orbit": [("pos", 8), ("fill", 3)], "arrow": [("rot", 8)], "polygon": [("sides", None), ("fill", 3)],
         "dots": [("count", None)], "quadrant": [("quad", 4)], "fshape": [("rot4", 4), ("mir", 2)]}


def frame(tracks, i):
    f = []
    for tr in tracks:
        e = {"kind": tr["kind"]}
        if tr["kind"] == "orbit":
            e["shape"] = tr["shape"]
        for a, _ in ATTRS[tr["kind"]]:
            e[a] = tr[a][i]
        f.append(e)
    return f


def varying_attrs(tracks):
    return [(k, a, m) for k, tr in enumerate(tracks) for a, m in ATTRS[tr["kind"]] if len(set(tr[a])) > 1]


def as_num(a, v):
    return FILLS.index(v) if a == "fill" else v


def unambiguous(tracks):
    for tr in tracks:
        for a, m in ATTRS[tr["kind"]]:
            vals = [as_num(a, v) for v in tr[a]]
            if predict_all(vals[:5], m) != {vals[5]}:
                return False
    return True


def collide(fr):
    poss = [e["pos"] for e in fr if e["kind"] == "orbit"]
    return len(poss) != len(set(poss))


def key_of(fr):
    return json.dumps(fr, sort_keys=True)


def wrong_values(tr, a):
    vals = tr[a]; ans = vals[5]; prev = vals[4]
    if a in ("pos", "rot"):
        step = (vals[5] - vals[4]) % 8
        cands = [prev, (ans + 1) % 8, (ans - 1) % 8, (prev - step) % 8, (ans + 4) % 8, (ans + 2) % 8, (ans - 2) % 8]
    elif a in ("quad", "rot4"):
        cands = [prev, (ans + 2) % 4, (ans + 1) % 4, (ans + 3) % 4]
    elif a == "mir":
        cands = [1 - ans]
    elif a == "fill":
        cands = [prev] + [f for f in FILLS if f != prev]
    elif a == "sides":
        cands = [c for c in [prev, ans + 1, ans - 1, ans + 2, ans - 2] if 3 <= c <= 6]
    else:  # count
        cands = [c for c in [prev, ans + 1, ans - 1, ans + 2, ans - 2, ans + 3, ans - 3] if 1 <= c <= 8]
    out = []
    for c in cands:
        if c != ans and c not in out:
            out.append(c)
    return out


def describe(tr, a, v, ans):
    if a in ("pos", "rot"):
        what = f"the {tr['shape']}" if a == "pos" else "the arrow"
        d = (v - ans) % 8
        if v == tr[a][4]:
            return f"{what} has not {'moved' if a == 'pos' else 'rotated'} on from the fifth figure"
        if a == "pos":
            return {1: f"{what} is one position too far clockwise", 7: f"{what} is one position too far anticlockwise",
                    4: f"{what} is on the opposite side of the frame", 2: f"{what} is two positions too far clockwise",
                    6: f"{what} is two positions too far anticlockwise"}.get(d, f"{what} is in the wrong position")
        return {1: f"{what} is rotated 45° too far clockwise", 7: f"{what} is rotated 45° too far anticlockwise",
                4: f"{what} points the opposite way", 2: f"{what} is rotated 90° too far clockwise",
                6: f"{what} is rotated 90° too far anticlockwise"}.get(d, f"{what} points in the wrong direction")
    if a == "fill":
        who = f"the {tr['shape']}" if tr["kind"] == "orbit" else "the central shape"
        return f"{who} is {v} instead of {ans}"
    if a == "sides":
        return f"the central shape is a {POLY_NAMES[v]} instead of a {POLY_NAMES[ans]}"
    if a == "count":
        return f"there {'is' if v == 1 else 'are'} {v} dot{'s' if v != 1 else ''} instead of {ans}"
    if a == "rot4":
        if v == tr["rot4"][4]:
            return "the F-shape has not turned on from the fifth figure"
        return {1: "the F-shape is turned 90° too far clockwise", 3: "the F-shape is turned 90° too far anticlockwise",
                2: "the F-shape is upside down relative to the answer"}[(v - ans) % 4]
    if a == "mir":
        return "the F-shape is mirrored the wrong way"
    return "the wrong quarter of the square is shaded"


def modal_scores(opts, attrs):
    return [sum(sum(1 for p in opts if p[k][a] == o[k][a]) for k, a, _ in attrs) for o in opts]


def build_distractors(rng, tracks, ans_frame):
    attrs = varying_attrs(tracks)
    if len(attrs) == 1:
        k, a, m = attrs[0]
        vals = wrong_values(tracks[k], a)
        if len(vals) < 4:
            return None
        out = []
        for v in vals[:4]:
            fr = [dict(e) for e in ans_frame]; fr[k][a] = v
            out.append((fr, [describe(tracks[k], a, v, ans_frame[k][a])]))
        return out
    pools = [[ans_frame[k][a]] + wrong_values(tracks[k], a)[:2] for k, a, m in attrs]
    combos = [c for c in itertools.product(*[range(len(p)) for p in pools]) if any(c)]
    if len(combos) < 4:
        return None
    for _ in range(4000):
        pick = rng.sample(combos, 4)
        opts, bad = [ans_frame], False
        for c in pick:
            fr = [dict(e) for e in ans_frame]
            for (k, a, m), idx, pool in zip(attrs, c, pools):
                fr[k][a] = pool[idx]
            if collide(fr):
                bad = True; break
            opts.append(fr)
        if bad or len({key_of(o) for o in opts}) != 5:
            continue
        sc = modal_scores(opts, attrs)
        if sc[0] > max(sc[1:]) or sc[0] < min(sc[1:]):
            continue
        if sorted(sc, reverse=True)[0] > sorted(sc, reverse=True)[1]:
            continue
        uniq = 0
        for k, a, _ in attrs:
            top = Counter(o[k][a] for o in opts).most_common()
            if top[0][0] == ans_frame[k][a] and (len(top) == 1 or top[0][1] > top[1][1]):
                uniq += 1
        if uniq > len(attrs) // 2:
            continue
        if not any(sum(1 for x in c if x) >= 2 for c in pick):
            continue
        out = []
        for c, fr in zip(pick, opts[1:]):
            whys = [describe(tracks[k], a, fr[k][a], ans_frame[k][a]) for (k, a, m), idx in zip(attrs, c) if idx]
            out.append((fr, whys))
        return out
    return None


def difficulty_score(tracks):
    s = 0
    for tr in tracks:
        for sig in tr["sig"]:
            s += {"pos": 1, "rot": 1, "dots": 1, "poly": 1.5, "quad": 1, "fill": 1}.get(sig[0], 2.5)
            if sig[0] in ("pos", "rot") and sig[1] == 3:
                s += 0.6
    return s


def make_item(rng, level, seen_geom, sig_count, no_flip=False):
    for _ in range(5000):
        tmpl = rng.choice(TEMPLATES[level])
        if no_flip and "flip" in tmpl:
            continue
        tracks = build_tracks(rng, level, tmpl)
        frames = [frame(tracks, i) for i in range(6)]
        if any(collide(f) for f in frames) or len({key_of(f) for f in frames[:5]}) < 4:
            continue
        if not unambiguous(tracks):
            continue
        if "flip" in tmpl and key_of(frames[5]) in {key_of(f) for f in frames[:5]}:
            continue  # the answer must never be a copy of a figure already shown
        geom = json.dumps(sorted([[tr["kind"]] + [tr[a] for a, _ in ATTRS[tr["kind"]] if a != "fill"] for tr in tracks]))
        if geom in seen_geom:
            continue
        sig = json.dumps(sorted(str(s) for tr in tracks for s in tr["sig"]))
        if sig_count[sig] >= 2:
            continue
        comps = [str(s) for tr in tracks for s in tr["sig"] if s[0] in ("pos-grow", "poly")]
        if any(sig_count["c" + c] >= (5 if c.startswith("('pos-grow'") else 2) for c in comps):
            continue
        dist = build_distractors(rng, tracks, frames[5])
        if not dist:
            continue
        seen_geom.add(geom); sig_count[sig] += 1
        for c in comps:
            sig_count["c" + c] += 1
        return {"difficulty": level, "template": tmpl, "series": frames[:5], "key_frame": frames[5],
                "distractors": dist, "rules": [d for tr in tracks for d in tr["desc"]],
                "score": difficulty_score(tracks), "sig": sig}
    raise RuntimeError("could not build item " + level)


def place(items, rng):
    seq = []
    while len(seq) < len(items):
        b = list(range(5)); rng.shuffle(b)
        if seq and b[0] == seq[-1]:
            b[0], b[1] = b[1], b[0]
        seq += b
    for it, t in zip(items, seq):
        opts = [d[0] for d in it["distractors"]]
        whys = [d[1] for d in it["distractors"]]
        opts.insert(t, it["key_frame"]); whys.insert(t, None)
        it["options"] = opts
        it["answer"] = LET[t]
        it["why_wrong"] = {LET[i]: "; ".join(w) for i, w in enumerate(whys) if w}
        for k in ("key_frame", "distractors", "sig"):
            it.pop(k, None)


def main(seed=8128):
    rng = random.Random(seed)
    seen, sigc = set(), Counter()
    practice = ([make_item(rng, "foundation", seen, sigc) for _ in range(20)] +
                [make_item(rng, "intermediate", seen, sigc) for _ in range(30)] +
                [make_item(rng, "advanced", seen, sigc) for _ in range(25)])
    order = {"foundation": 0, "intermediate": 1, "advanced": 2}
    practice.sort(key=lambda x: (order[x["difficulty"]], x["score"]))
    def clash(i):
        return 0 < i < len(practice) and practice[i]["template"] == practice[i - 1]["template"]
    for _ in range(500):  # no two neighbours share a template (swaps stay within a difficulty band)
        bad = [i for i in range(1, len(practice)) if clash(i)]
        if not bad:
            break
        i = bad[0]
        for j in sorted(range(len(practice)), key=lambda j: abs(j - i)):
            if j in (i, i - 1) or practice[j]["difficulty"] != practice[i]["difficulty"]:
                continue
            practice[i], practice[j] = practice[j], practice[i]
            if not any(clash(k) for k in (i, i + 1, j, j + 1)):
                break
            practice[i], practice[j] = practice[j], practice[i]
    for i in range(1, len(practice)):
        if practice[i]["sig"] == practice[i - 1]["sig"]:
            for j in range(i + 1, len(practice)):
                if practice[j]["difficulty"] == practice[i]["difficulty"] and practice[j]["sig"] != practice[i]["sig"]:
                    practice[i], practice[j] = practice[j], practice[i]; break
    mocks = []
    for _ in range(3):
        block = []
        for lv in ["intermediate"] * 3 + ["advanced"] * 7:  # at most two F-shape series per mock
            block.append(make_item(rng, lv, seen, sigc, no_flip=sum("flip" in b["template"] for b in block) >= 2))
        block.sort(key=lambda x: x["score"])
        mocks += block
    place(practice, rng)
    place(mocks, rng)
    for i, it in enumerate(practice):
        it["id"] = f"A-{i + 1:03d}"
    for i, it in enumerate(mocks):
        it["id"] = f"AM-{i + 1:02d}"
    (ROOT / "content" / "abstract.json").write_text(json.dumps({"practice": practice, "mocks": mocks}, ensure_ascii=False, indent=1))
    hits = tot = 0
    for it in practice + mocks:
        opts = it["options"]
        var = [(k, a, None) for k, e in enumerate(opts[0]) for a in e if a not in ("kind", "shape")
               and len({json.dumps(o[k][a]) for o in opts}) > 1]
        if len(var) < 2:
            continue
        sc = modal_scores(opts, var)
        best = [i for i, s in enumerate(sc) if s == max(sc)]
        tot += 1; hits += (len(best) == 1 and LET[best[0]] == it["answer"])
    print("abstract", Counter(i["answer"] for i in practice + mocks), Counter(i["template"] for i in practice + mocks))
    print(f"modal-heuristic unique hits: {hits}/{tot}")


if __name__ == "__main__":
    main()
