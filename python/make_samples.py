#!/usr/bin/env python3
"""Draw the book's three fixed simple random samples of Tonmick joiners, once.

    python -I python/make_samples.py            write samples/ (only if a file is missing)
    python -I python/make_samples.py --check    redraw in memory and compare with samples/, byte for byte

The 1,219 students who joined the study serve as a population whose true values are known,
so a one-sample interval or test can be checked against the truth. The seed, 2027, was
fixed before any sample was drawn, and no sample is ever redrawn to get nicer numbers.

The draw uses only random.Random(2027).random(), whose sequence Python guarantees across
versions for a given seed (random.sample's algorithm is not guaranteed). For each sample, in
this order, the eligible students are sorted by student ID, and a partial Fisher-Yates
shuffle picks k of them: for i = 0, 1, ..., k-1, j = i + int(u * (m - i)) with u the next
random() value and m the number eligible, and positions i and j swap. The first k, in draw
order, are the sample.

1. tonmick-sample-100.csv: 100 of the 1,208 joiners whose first-year outcome is known
   (withdrew is 0 or 1), for intervals and tests for a proportion.
2. tonmick-sample-120.csv: 120 of the same 1,208, drawn separately, for the chi-square test
   of independence (120 is at most 10% of 1,208).
3. tonmick-sample-20.csv: 20 of the 1,116 joiners with a 12-month college grade, for the
   t procedures with a small sample, including paired data.

Each file has a `draw` column (1 to k, in draw order) followed by the columns of
data/tonmick-classroom.csv. Standard library only; Python 3.10 or later.
"""
import csv
import io
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = 2027
SAMPLES = [  # (file, size, who is eligible), drawn in this order from one generator
    ("tonmick-sample-100.csv", 100, "known outcome"),
    ("tonmick-sample-120.csv", 120, "known outcome"),
    ("tonmick-sample-20.csv", 20, "college grade"),
]


def eligible(rows, rule):
    if rule == "known outcome":
        keep = [r for r in rows if r["withdrew"] in ("0", "1")]
    elif rule == "college grade":
        keep = [r for r in rows if r["grade_12"] != ""]
    else:
        raise ValueError(rule)
    return sorted(keep, key=lambda r: r["student_id"])


def draw(rng, pool, k):
    pool = list(pool)
    m = len(pool)
    for i in range(k):
        j = i + int(rng.random() * (m - i))
        pool[i], pool[j] = pool[j], pool[i]
    return pool[:k]


def build():
    with open(ROOT / "data" / "tonmick-classroom.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)
    rng = random.Random(SEED)
    out = {}
    for name, k, rule in SAMPLES:
        chosen = draw(rng, eligible(rows, rule), k)
        buf = io.StringIO(newline="")
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(["draw"] + fields)
        for i, r in enumerate(chosen, 1):
            w.writerow([i] + [r[c] for c in fields])
        out[name] = buf.getvalue().encode("utf-8")
    return out


def main():
    files = build()
    folder = ROOT / "samples"
    if "--check" in sys.argv:
        bad = [n for n, b in files.items() if not (folder / n).is_file() or (folder / n).read_bytes() != b]
        extra = sorted(p.name for p in folder.glob("*") if p.name not in files) if folder.is_dir() else []
        if bad or extra:
            for n in bad:
                print(f"MISMATCH samples/{n} does not equal the draw from seed {SEED}")
            for n in extra:
                print(f"MISMATCH samples/{n} is not one of the drawn samples")
            print("SAMPLES_CHECK_FAILED")
            sys.exit(1)
        print(f"SAMPLES_CHECK_OK files={len(files)} seed={SEED}")
        return
    folder.mkdir(exist_ok=True)
    for n, b in files.items():
        p = folder / n
        if p.exists():
            print(f"kept samples/{n} (it exists; samples are drawn once and never redrawn)")
        else:
            p.write_bytes(b)
            print(f"wrote samples/{n}")


if __name__ == "__main__":
    main()
