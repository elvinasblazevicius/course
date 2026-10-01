"""Accuracy & precision and Prioritising & organising items (rev. 2: computed keys, brute-force uniqueness)."""
import itertools
import json
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
L4 = "ABCD"

# culturally coherent (first name, surname, country code) triples
PEOPLE_POOL = [("Anna", "Kowalska", "PL"), ("Piotr", "Wiśniewski", "PL"), ("Jonas", "Petraitis", "LT"),
               ("Marie", "Dumont", "BE"), ("Luca", "Ferrari", "IT"), ("Matteo", "Rossi", "IT"), ("Aoife", "Murphy", "IE"),
               ("Seán", "O’Brien", "IE"), ("Elena", "Popescu", "RO"), ("Henrik", "Andersson", "SE"), ("Sofia", "Lindqvist", "SE"),
               ("Tomás", "García", "ES"), ("Inês", "Silva", "PT"), ("Mateusz", "Nowak", "PL"), ("Clara", "Schmidt", "DE"),
               ("Nikos", "Papadopoulos", "EL"), ("Eva", "Novák", "CZ"), ("Lars", "Hansen", "DK"), ("Zofia", "Horváth", "HU"),
               ("Katarina", "Kovač", "HR"), ("Liis", "Kask", "EE"), ("Jānis", "Bērziņš", "LV"), ("Matej", "Novotný", "SK"),
               ("Ana", "Petrović", "SI"), ("Pieter", "Janssen", "BE"), ("Mika", "Nieminen", "FI"), ("Lucas", "Moreau", "FR"),
               ("Georg", "Fischer", "AT"), ("Maria", "Georgiou", "CY"), ("Joseph", "Borg", "MT"), ("Ivan", "Ivanov", "BG"),
               ("Sophie", "Weber", "LU"), ("Emma", "Peeters", "BE"), ("Hanna", "Virtanen", "FI")]
CC_CONFUSABLE = {"AT": "IT", "IT": "IE", "IE": "IT", "LT": "LV", "LV": "LT", "LU": "LT", "DE": "DK", "DK": "DE",
                 "ES": "EE", "EE": "ES", "SE": "SI", "SI": "SK", "SK": "SI", "CZ": "CY", "CY": "CZ", "HR": "HU",
                 "HU": "HR", "PL": "PT", "PT": "PL", "FI": "FR", "FR": "FI", "BE": "BG", "BG": "BE", "EL": "EE",
                 "MT": "IT", "RO": "PT"}
FIELDS = [("ref", "Reference"), ("name", "Beneficiary"), ("cc", "Country code"), ("amount", "Amount (€)")]


def ref_code(rng):
    letters = "ACDEFGHJKLMNPRTUVWXY"
    num = "".join(rng.choice("0123456789" + "0158") for _ in range(4))
    if num[0] == "0":
        num = "7" + num[1:]
    return f"{rng.choice(['TR', 'GR', 'CN', 'AD', 'FN', 'MS'])}-{num}/{rng.choice(letters)}{rng.choice(letters)}"


def record(rng, used):
    while True:
        first, sur, cc = rng.choice(PEOPLE_POOL)
        if sur not in used:
            used.add(sur); break
    return {"ref": ref_code(rng), "name": f"{sur}, {first}", "cc": cc,
            "amount": f"{rng.randint(120, 98000):,}.{rng.choice(['00', '50', '25', '75', '40', '90', '15'])}"}


def rows_n(rng, n):
    used = set()
    return [record(rng, used) for _ in range(n)]


DIACRITIC = str.maketrans("áčéíóúöäåěšřžýņļāēīūęłńśźżőűâêôãõ", "aceiouoaaesrzynlaeiuelnszzouaeoao")


def alter(rng, field, val):
    """Return (new_value, description) with one subtle, realistic transcription error."""
    if field == "ref":
        pre, rest = val.split("-"); num, let = rest.split("/")
        k = rng.randrange(4)
        if k == 0:
            n = list(num); i = rng.randrange(3)
            if n[i] != n[i + 1]:
                n[i], n[i + 1] = n[i + 1], n[i]
                new = f"{pre}-{''.join(n)}/{let}"
                return new, f"two digits of the reference are transposed ({val} → {new})"
        if k == 1 and let[0] != let[1]:
            new = f"{pre}-{num}/{let[::-1]}"
            return new, f"the final two letters of the reference are reversed ({let} → {let[::-1]})"
        if k == 2 and any(c in num for c in "0158"):
            look = {"0": "O", "1": "I", "5": "S", "8": "B"}
            i = rng.choice([j for j, c in enumerate(num) if c in look])
            new = f"{pre}-{num[:i]}{look[num[i]]}{num[i + 1:]}/{let}"
            return new, f"a digit has been replaced by a look-alike letter ({num[i]} → {look[num[i]]})"
        n = list(num); i = rng.randrange(4); n[i] = str((int(n[i]) + rng.choice([1, 3, 5])) % 10)
        new = f"{pre}-{''.join(n)}/{let}"
        return new, f"one digit of the reference is wrong ({val} → {new})"
    if field == "name":
        sur, first = val.split(", ")
        opts = []
        if sur.translate(DIACRITIC) != sur:
            opts.append((sur.translate(DIACRITIC), "an accent or diacritic is missing from the surname"))
        if "ss" in sur or "nn" in sur:
            opts.append((sur.replace("ss", "s", 1).replace("nn", "n", 1), "a double letter in the surname has become single"))
        if len(sur) > 4:
            i = rng.randrange(1, len(sur) - 2)
            if sur[i] != sur[i + 1] and sur[i].isalpha() and sur[i + 1].isalpha():
                opts.append((sur[:i] + sur[i + 1] + sur[i] + sur[i + 2:], "two letters of the surname are transposed"))
        if not opts or rng.random() < 0.25:
            alt = {"Anna": "Ana", "Ana": "Anna", "Marie": "Maria", "Maria": "Marie", "Luca": "Luka", "Elena": "Helena",
                   "Henrik": "Hendrik", "Sofia": "Sophia", "Tomás": "Tomas", "Inês": "Ines", "Clara": "Klara",
                   "Nikos": "Nicos", "Eva": "Eve", "Lars": "Lasse", "Zofia": "Sofia", "Katarina": "Katharina",
                   "Matteo": "Mateo", "Jonas": "Jonás", "Aoife": "Aiofe", "Piotr": "Petr", "Mateusz": "Mateus",
                   "Seán": "Sean", "Liis": "Lis", "Jānis": "Janis", "Matej": "Matěj", "Pieter": "Peter", "Mika": "Mikko",
                   "Lucas": "Lukas", "Georg": "George", "Joseph": "Josef", "Ivan": "Iwan",
                   "Sophie": "Sofie", "Emma": "Ema", "Hanna": "Hannah"}[first]
            return f"{sur}, {alt}", f"the first name is spelled differently ({first} → {alt})"
        new_sur, why = rng.choice(opts)
        return f"{new_sur}, {first}", f"{why} ({sur} → {new_sur})"
    if field == "cc":
        new = CC_CONFUSABLE[val]
        return new, f"the country code differs ({val} → {new})"
    whole, cents = val.split(".")
    digits = whole.replace(",", "")
    if len(digits) >= 3 and rng.random() < 0.6:
        d = list(digits); i = rng.randrange(len(d) - 1)
        if d[i] == d[i + 1]:
            d[i + 1] = str((int(d[i + 1]) + 2) % 10)
        else:
            d[i], d[i + 1] = d[i + 1], d[i]
        if d[0] == "0":
            d[0] = "9"
        new = f"{int(''.join(d)):,}.{cents}"
    else:
        new = f"{whole}.{ {'00': '50', '50': '05', '25': '52', '75': '57', '40': '04', '90': '09', '15': '51'}[cents]}"
    if new == val:
        new = f"{int(digits) + 10:,}.{cents}"
    return new, f"the amount differs ({val} → {new})"


AP_TIP = ("Method: compare one field at a time; read codes in chunks of two characters, check accents letter by letter, "
          "and check amounts digit by digit from the left.")


def ap_field(rng, tgt):
    rows = rows_n(rng, 8)
    r = rng.randrange(8)
    rec = dict(rows[r])
    fields = rng.sample(FIELDS, 3)
    opts = [f[1] for f in fields] + ["No error"]
    level = "intermediate"
    if tgt == 3:
        why = f"every field of the copy matches row {r + 1} exactly, so “No error” is correct"
    else:
        f = fields[tgt]
        rec[f[0]], desc = alter(rng, f[0], rows[r][f[0]])
        why = f"{desc}; all other fields match, so the answer is “{f[1]}”"
        if f[0] == "cc":
            level = "foundation"
    return {"kind": "field", "reference": rows, "record": rec, "row": r + 1,
            "question": f"The record below was copied from row {r + 1} of the reference table. Which part of the copy, if any, contains an error?",
            "options": opts, "answer": L4[tgt], "explanation": f"Compare the copy with row {r + 1}: {why}. {AP_TIP}",
            "difficulty": level}


def ap_match(rng, tgt):
    rows = rows_n(rng, 10)
    picks = rng.sample(range(10), 4)
    cands, whys = [], []
    for i, rr in enumerate(picks):
        rec = dict(rows[rr])
        if i == tgt:
            whys.append(f"matches row {rr + 1} exactly")
        else:
            f = rng.choice(FIELDS)
            rec[f[0]], d = alter(rng, f[0], rec[f[0]])
            whys.append(f"compare with row {rr + 1}: {d}")
        cands.append(rec)
    return {"kind": "match", "reference": rows, "candidates": cands,
            "question": "Which of the following records appears in the reference table EXACTLY as shown?",
            "options": [L4[i] for i in range(4)], "answer": L4[tgt],
            "explanation": " ".join(f"{L4[i]}: {w}." for i, w in enumerate(whys)) + " " + AP_TIP, "difficulty": "intermediate"}


def ap_count(rng, tgt):
    rows = rows_n(rng, 10)
    sel = rng.sample(range(10), 5)
    n_err = rng.choice([1, 2, 2, 3, 3, 4])
    tgt = rng.choice([t for t in (0, 1, 1, 2, 2, 3) if 0 <= n_err - t and n_err - t + 3 <= 5])
    lo = n_err - tgt
    counts = [lo + i for i in range(4)]
    err_idx = set(rng.sample(range(5), n_err))
    copies, whys = [], []
    for i, rr in enumerate(sel):
        rec = dict(rows[rr])
        if i in err_idx:
            f = rng.choice(FIELDS)
            rec[f[0]], d = alter(rng, f[0], rec[f[0]])
            whys.append(f"copy {i + 1} (row {rr + 1}): {d}")
        else:
            whys.append(f"copy {i + 1} (row {rr + 1}): no error")
        copies.append((rr + 1, rec))
    return {"kind": "count", "reference": rows, "copies": copies,
            "question": "Five records were copied from the reference table (the source row is shown for each). How many of the copies contain at least one error?",
            "options": [str(c) for c in counts], "answer": L4[tgt],
            "explanation": "; ".join(whys) + f". Copies with an error: {n_err}. " + AP_TIP, "difficulty": "advanced"}


# ------------------------------------------------------------------ prioritising & organising
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
DAYS_FULL = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
SLOTS = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
NAMES = ["Anna", "Bruno", "Chiara", "Dawid", "Eleni", "Filip"]
GRID_NOTE = ("The table shows who is BUSY (unavailable) during the one-hour slot starting at the time shown; "
             "— means that all four colleagues are free. No meetings are held between 12:00 and 14:00.")


def earliest(busy, req, excl_day, latest):
    for d in range(5):
        for s in range(6):
            if (excl_day is None or d != excl_day) and (latest is None or s <= latest) and all((d, s) not in busy[p] for p in req):
                return (d, s)
    return None


def po_meeting(rng, tgt, ans_day):
    for _ in range(200000):
        ppl = rng.sample(NAMES, 4)
        pb = rng.uniform(0.35, 0.7)
        busy = {p: {(d, s) for d in range(5) for s in range(6) if rng.random() < pb} for p in ppl}
        req, opt = ppl[:3], ppl[3]
        excl_day = rng.choice([d for d in range(5) if d != ans_day])
        latest = rng.choice([3, 4])
        ans = earliest(busy, req, excl_day, latest)
        if not ans or ans[0] != ans_day:
            continue
        no_day = earliest(busy, req, None, latest)
        no_lim = earliest(busy, req, excl_day, None)
        with_opt = earliest(busy, ppl, excl_day, latest)
        mattering = sum([no_day != ans, no_lim != ans, with_opt != ans])
        if mattering < 2 or ans not in busy[opt]:
            continue
        pool = [x for x in (no_day, no_lim) if x and x != ans]
        later = [(d, s) for d in range(5) for s in range(6) if (d, s) > ans and d != excl_day and s <= latest
                 and all((d, s) not in busy[p] for p in req)]
        clash = [(d, s) for d in range(5) for s in range(6) if (d, s) < ans and d != excl_day and s <= latest
                 and sum((d, s) in busy[p] for p in req) == 1]
        if later:
            pool.append(rng.choice(later))
        if clash:
            pool.append(rng.choice(clash))
        pool = list(dict.fromkeys(pool))
        if len(pool) < 3:
            continue
        pool = pool[:3]
        rng.shuffle(pool)
        opts = pool[:tgt] + [ans] + pool[tgt:]

        def lab(x):
            return f"{DAYS_FULL[x[0]]} {SLOTS[x[1]]}"
        whys = []
        for x in opts:
            if x == ans:
                whys.append(f"{lab(x)}: {', '.join(req)} are all free and no earlier slot meets every condition — correct ({opt} is busy, but attendance is optional)")
            elif x[0] == excl_day:
                whys.append(f"{lab(x)}: everyone required is free, but {DAYS_FULL[excl_day]} is excluded")
            elif x[1] > latest:
                whys.append(f"{lab(x)}: everyone required is free, but it starts after {SLOTS[latest]}")
            elif all(x not in busy[p] for p in req):
                whys.append(f"{lab(x)}: possible, but not the earliest suitable slot")
            else:
                who = [p for p in req if x in busy[p]]
                whys.append(f"{lab(x)}: {', '.join(who)} {'is' if len(who) == 1 else 'are'} busy")
        grid = [[SLOTS[s]] + [(" ".join(p[0] for p in ppl if (d, s) in busy[p]) or "—") for d in range(5)] for s in range(6)]
        q = (f"A one-hour meeting must be attended by {req[0]}, {req[1]} and {req[2]}; {opt}’s attendance is optional, so "
             f"{opt}’s availability can be ignored. The room is unavailable on {DAYS_FULL[excl_day]}, and the meeting must start "
             f"no later than {SLOTS[latest]}. What is the earliest suitable slot in the week?")
        return {"kind": "meeting", "grid": {"columns": ["Start"] + DAYS, "rows": grid,
                                             "legend": ", ".join(f"{p[0]} = {p}" for p in ppl), "note": GRID_NOTE},
                "question": q, "options": [lab(x) for x in opts], "answer": L4[tgt],
                "explanation": "Check the slots in time order, applying every condition. " + "; ".join(whys) + ".",
                "difficulty": "intermediate"}
    raise RuntimeError


SCENARIOS = [
    ("A unit must publish a policy report.",
     ["Collect data", "Draft analysis", "Legal check", "Translation", "Layout", "Final approval"],
     [{1: [0], 2: [1], 3: [1], 4: [3], 5: [2, 4]}, {1: [0], 2: [1], 3: [1], 4: [1], 5: [2, 3, 4]}]),
    ("A team is organising a stakeholder conference.",
     ["Book venue", "Draft programme", "Invite speakers", "Open registration", "Print materials", "Final briefing"],
     [{1: [], 2: [1], 3: [0, 1], 4: [2], 5: [3, 4]}, {1: [], 2: [1], 3: [0, 2], 4: [1], 5: [3, 4]}]),
    ("An IT team is rolling out a new case-management tool.",
     ["Gather requirements", "Configure system", "Security review", "Migrate data", "Train users", "Go-live check"],
     [{1: [0], 2: [1], 3: [1], 4: [1], 5: [2, 3, 4]}, {1: [0], 2: [1], 3: [1], 4: [3], 5: [2, 4]}]),
    ("A selection board is running a recruitment exercise.",
     ["Publish vacancy", "Screen applications", "Prepare tests", "Run tests", "Hold interviews", "Final decision"],
     [{1: [0], 2: [], 3: [1, 2], 4: [3], 5: [4]}, {1: [0], 2: [0], 3: [1, 2], 4: [3], 5: [4]}]),
]
CRIT_COUNT = Counter()


def po_critical(rng, tgt):
    sc_i = CRIT_COUNT["n"] % len(SCENARIOS); CRIT_COUNT["n"] += 1
    intro, names, layouts = SCENARIOS[sc_i]
    for _ in range(20000):
        lay = rng.choice(layouts)
        dur = {n: rng.randint(1, 6) for n in names}
        deps = {names[0]: []}
        for k in range(1, 6):
            deps[names[k]] = [names[j] for j in lay[k]]
        fin = {}
        for n in names:
            fin[n] = max([fin[d] for d in deps[n]], default=0) + dur[n]
        ans = max(fin.values())
        paths = []

        def walk(n, acc, chain):
            nxt = [m for m in names if n in deps[m]]
            if not nxt:
                paths.append((acc, chain)); return
            for m in nxt:
                walk(m, acc + dur[m], chain + [m])
        for root in [n for n in names if not deps[n]]:
            walk(root, dur[root], [root])
        lengths = sorted({p[0] for p in paths if p[0] != ans}, reverse=True)
        total = sum(dur.values())
        crit_chain = max(paths)[1]
        off = [n for n in names if n not in crit_chain]
        pool = [total] + lengths + [ans - dur[crit_chain[-1]]] + ([ans + max(dur[n] for n in off)] if off else [])
        cands = []
        for p in pool:
            if abs(p - ans) >= 2 and p not in cands and p > 0:
                cands.append(p)
        if len(cands) < 3:
            continue
        cands = cands[:3]
        rng.shuffle(cands)
        opts = cands[:tgt] + [ans] + cands[tgt:]
        crit = max(paths)[1]
        rows = [[n, str(dur[n]), ", ".join(deps[n]) if deps[n] else "—"] for n in names]
        return {"kind": "critical", "table": {"columns": ["Task", "Working days", "Can start only after"], "rows": rows},
                "question": (f"{intro} Tasks can run in parallel as soon as all their prerequisites are complete, and there are enough "
                             "staff to work on any number of tasks at once. What is the minimum number of working days needed to complete everything?"),
                "options": [str(x) for x in opts], "answer": L4[tgt],
                "explanation": ("Earliest finish of each task = its duration + the latest finish among its prerequisites: "
                                + "; ".join(f"{n} {fin[n]}" for n in names) + ". The longest chain (the critical path) is "
                                + " → ".join(crit) + f", so the project needs {ans} days. Typical errors: adding all durations ({total}) wrongly assumes that nothing runs in parallel; "
                                "following a shorter branch underestimates the time; forgetting the final task, or adding a parallel task in series, also gives a wrong total."),
                "difficulty": "advanced"}
    raise RuntimeError


def po_assign(rng, tgt):
    tasks = ["Budget report", "Event logistics", "Website update", "Press summary"]
    for _ in range(50000):
        staff = rng.sample(NAMES, 4)
        pool = [("cannot", s, t) for s in staff for t in tasks]
        rng.shuffle(pool)
        cons = pool[:rng.randint(3, 6)]
        if rng.random() < 0.6:
            s = rng.choice(staff); t1, t2 = rng.sample(tasks, 2)
            cons = [c for c in cons if c[1] != s]  # avoid self-cancelling / implied 'cannot' for this person
            cons.append(("either", s, (t1, t2)))

        def solutions(cs):
            out = []
            for perm in itertools.permutations(staff):
                asg = dict(zip(tasks, perm))
                if all(not (c[0] == "cannot" and asg[c[2]] == c[1]) for c in cs) and \
                   all(not (c[0] == "either" and asg[c[2][0]] != c[1] and asg[c[2][1]] != c[1]) for c in cs):
                    out.append(asg)
            return out
        sols = solutions(cons)
        if len(sols) != 1:
            continue
        # every constraint must be needed (no decorative constraints)
        if any(len(solutions([c for c in cons if c is not x])) == 1 for x in cons):
            continue
        sol = sols[0]
        qt = rng.choice(tasks)
        ans = sol[qt]
        # not trivial: the asked task must not be settled by its own 'cannot' constraints alone
        allowed_t = [s for s in staff if ("cannot", s, qt) not in cons]
        allowed_p = [t for t in tasks if ("cannot", ans, t) not in cons]
        if len(allowed_t) <= 1 or len(allowed_p) <= 1:
            continue
        if any(c[0] == "either" and c[1] == ans and qt in c[2] for c in cons):
            continue
        others = [s for s in staff if s != ans]
        rng.shuffle(others)
        opts = others[:tgt] + [ans] + others[tgt:]

        def ctext(c):
            if c[0] == "cannot":
                return f"{c[1]} cannot take the {c[2].lower()}."
            return f"{c[1]} must take either the {c[2][0].lower()} or the {c[2][1].lower()}."
        lines = [ctext(c) for c in cons]
        rng.shuffle(lines)
        return {"kind": "assign", "constraints": lines,
                "question": (f"Four colleagues — {', '.join(staff)} — must each take exactly one of four tasks: the "
                             f"{', the '.join(t.lower() for t in tasks[:-1])} and the {tasks[-1].lower()}. "
                             f"Taking all the constraints below into account, who must take the {qt.lower()}?"),
                "options": opts, "answer": L4[tgt],
                "explanation": ("List, for each task, who is still allowed to take it, and start with the task or person that has the fewest "
                                "possibilities; each forced choice removes that person from the other tasks. The only allocation that satisfies "
                                "every constraint is: " + "; ".join(f"{t.lower()} — {sol[t]}" for t in tasks) + f". So the {qt.lower()} must go to {ans}."),
                "difficulty": "advanced"}
    raise RuntimeError


def balanced(n, rng, k=4):
    seq = []
    while len(seq) < n:
        b = list(range(k)); rng.shuffle(b)
        if seq and b[0] == seq[-1]:
            b[0], b[1] = b[1], b[0]
        seq += b
    return seq[:n]


def main(seed=2027):
    rng = random.Random(seed)
    tg = balanced(12, rng) + [0, 3, 0, 3, 1, 0, 3, 2, 0, 3] + [None] * 8
    ap = []
    for i, f in enumerate([ap_field] * 12 + [ap_match] * 10 + [ap_count] * 8):
        it = f(rng, tg[i]); it["id"] = f"AP-{i + 1:02d}"; ap.append(it)
    tg = balanced(24, rng)
    days = [1, 2, 3, 1, 2, 3, 2, 1, 3]
    rng.shuffle(days)
    po = []
    for i in range(9):
        it = po_meeting(rng, tg[i], days[i]); it["id"] = f"PO-{i + 1:02d}"; po.append(it)
    for i in range(9, 17):
        it = po_critical(rng, tg[i]); it["id"] = f"PO-{i + 1:02d}"; po.append(it)
    for i in range(17, 24):
        it = po_assign(rng, tg[i]); it["id"] = f"PO-{i + 1:02d}"; po.append(it)
    (ROOT / "content" / "accuracy.json").write_text(json.dumps(ap, ensure_ascii=False, indent=1))
    (ROOT / "content" / "prioritising.json").write_text(json.dumps(po, ensure_ascii=False, indent=1))
    print("AP", Counter(i["answer"] for i in ap), "PO", Counter(i["answer"] for i in po))


if __name__ == "__main__":
    main()
