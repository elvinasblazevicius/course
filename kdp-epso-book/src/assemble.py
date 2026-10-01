"""Assemble all content into the final book structure (shared by the print PDF and the EPUB builders)."""
import json
import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C = ROOT / "content"
ORDER = {"foundation": 0, "intermediate": 1, "advanced": 2}

META = {
    "title": "Reasoning Tests Workbook for EPSO Exams",
    "subtitle": "400+ Practice Questions: Verbal, Numerical and Abstract Reasoning, Situational Judgement and Assistant-Level Skills, 3 Timed Mock Exams and Worked Solutions",
    "short_title": "Reasoning Tests Workbook for EPSO Exams",
    "author": "Concours Prep",
    "imprint": "Concours Prep",
    "year": "2026",
    "isbn_paperback": "",
    "isbn_hardcover": "",
}


def no_runs(items, key="answer", band="difficulty", rng=None):
    """Reorder within difficulty bands so that no answer letter appears 3+ times in a row."""
    rng = rng or random.Random(5)
    for _ in range(2000):
        bad = None
        for i in range(2, len(items)):
            if items[i][key] == items[i - 1][key] == items[i - 2][key]:
                bad = i; break
        if bad is None:
            return items
        cands = [j for j in range(len(items)) if j != bad and items[j].get(band) == items[bad].get(band)
                 and items[j][key] != items[bad][key]]
        j = rng.choice(cands) if cands else rng.randrange(len(items))
        items[bad], items[j] = items[j], items[bad]
    return items


import re

DASH = re.compile(r"\s*—\s*|\s+–\s+")


def dashes(x):
    if isinstance(x, str):
        return DASH.sub(" – ", x)
    if isinstance(x, list):
        return [dashes(v) for v in x]
    if isinstance(x, dict):
        return {k: dashes(v) for k, v in x.items()}
    return x


def load():
    rng = random.Random(42)
    verbal = []
    for k in range(1, 6):
        verbal += [dashes(v) for v in json.loads((C / f"verbal_{k}.json").read_text())]
    # mock exams take a balanced difficulty mix (5 F / 8 I / 7 A where available)
    by = {d: [v for v in verbal if v["difficulty"] == d] for d in ORDER}
    for d in by:
        rng.shuffle(by[d])
    mocks_v = [[], [], []]
    need = {"foundation": 5, "intermediate": 8, "advanced": 7}
    for m in range(3):
        for d, n in need.items():
            take = by[d][:n]; by[d] = by[d][n:]
            mocks_v[m] += take
        short = 20 - len(mocks_v[m])
        for d in ("intermediate", "advanced", "foundation"):
            while short and by[d]:
                mocks_v[m].append(by[d].pop()); short -= 1
        mocks_v[m].sort(key=lambda x: ORDER[x["difficulty"]])
        mocks_v[m] = no_runs(mocks_v[m], rng=rng)
    verbal_practice = sorted(sum(by.values(), []), key=lambda x: ORDER[x["difficulty"]])
    verbal_practice = no_runs(verbal_practice, rng=rng)

    num = json.loads((C / "numerical.json").read_text())
    num_practice = no_runs(num["practice"], rng=rng)
    num_mocks = [no_runs(sorted(num["mocks"][i * 10:(i + 1) * 10], key=lambda x: ORDER[x["difficulty"]]), rng=rng) for i in range(3)]

    ab = json.loads((C / "abstract.json").read_text())
    ab_practice = ab["practice"]
    ab_mocks = [ab["mocks"][i * 10:(i + 1) * 10] for i in range(3)]

    sjt = [dashes(v) for v in json.loads((C / "sjt.json").read_text())]
    acc = json.loads((C / "accuracy.json").read_text())
    acc = no_runs(acc, band="kind", rng=rng)
    pri = no_runs(json.loads((C / "prioritising.json").read_text()), band="kind", rng=rng)

    sets = [
        {"key": "verbal", "title": "Verbal Reasoning", "items": verbal_practice, "type": "verbal"},
        {"key": "numerical", "title": "Numerical Reasoning", "items": num_practice, "type": "numerical"},
        {"key": "abstract", "title": "Abstract Reasoning", "items": ab_practice, "type": "abstract"},
        {"key": "sjt", "title": "Situational Judgement", "items": sjt, "type": "sjt"},
        {"key": "accuracy", "title": "Accuracy & Precision", "items": acc, "type": "accuracy"},
        {"key": "prioritising", "title": "Prioritising & Organising", "items": pri, "type": "prioritising"},
    ]
    mocks = []
    for m in range(3):
        items = ([dict(x, type="verbal") for x in mocks_v[m]] + [dict(x, type="numerical") for x in num_mocks[m]] +
                 [dict(x, type="abstract") for x in ab_mocks[m]])
        mocks.append({"key": f"mock{m + 1}", "title": f"Mock Exam {m + 1}", "items": items})
    # number questions within each set
    for s in sets:
        for i, it in enumerate(s["items"]):
            it["n"] = i + 1
            it["type"] = s["type"]
    for mk in mocks:
        for i, it in enumerate(mk["items"]):
            it["n"] = i + 1
    total = sum(len(s["items"]) for s in sets) + sum(len(m["items"]) for m in mocks)
    guide = (C / "guide.md").read_text()
    return {"meta": META, "sets": sets, "mocks": mocks, "guide": guide, "total": total}


if __name__ == "__main__":
    b = load()
    print("total questions", b["total"])
    for s in b["sets"]:
        print(s["title"], len(s["items"]), Counter(i.get("answer", i.get("most")) for i in s["items"]))
    for m in b["mocks"]:
        print(m["title"], len(m["items"]), "".join(i["answer"] for i in m["items"]))
