#!/usr/bin/env python3
"""Draw the two simulations behind the book's Figures 13 and 14, once.

    python -I python/make_simulations.py            write simulations/ (only if a file is missing)
    python -I python/make_simulations.py --check    redraw in memory and compare with simulations/, byte for byte

The figures show what a sampling distribution is by drawing many samples from the Tonmick
joiners, a population whose true values are known. The seed, 2027, is the samples' seed,
fixed before anything was drawn, and nothing is redrawn to get a nicer picture.

The draw uses only random.Random(2027).random(), whose sequence Python guarantees across
versions for a given seed. Each sample is drawn as python/make_samples.py draws: the eligible
students are sorted by student ID, and a partial Fisher-Yates shuffle picks k of them (for
i = 0, 1, ..., k-1, j = i + int(u * (m - i)), with u the next random() value and m the number
eligible; positions i and j swap). Every sample starts again from the sorted list, so the
samples are independent simple random samples. One generator draws them all, in this order:

1. tonmick-sim-means-30.csv: 1,000 samples of 30 from all 1,219 joiners. Each row holds the
   sample's number (rep) and the total of its 30 students' support visits (visits_total); the
   sample mean is visits_total / 30. Figure 13: the central limit theorem.
2. tonmick-sim-samples-100.csv: 50 samples of 100 from the 1,208 joiners whose outcome is
   known. Each row holds the sample's number (rep) and how many of its 100 withdrew
   (withdrew); p-hat is withdrew / 100. Figure 14: fifty 95% intervals.

Standard library only; Python 3.10 or later.
"""
import csv
import io
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = 2027
FOLDER = ROOT / "simulations"


def draw(rng, pool, k):
    pool = list(pool)
    m = len(pool)
    for i in range(k):
        j = i + int(rng.random() * (m - i))
        pool[i], pool[j] = pool[j], pool[i]
    return pool[:k]


def build():
    with open(ROOT / "data" / "tonmick-classroom.csv", newline="", encoding="utf-8") as f:
        rows = sorted(csv.DictReader(f), key=lambda r: r["student_id"])
    joiners = rows
    known = [r for r in rows if r["withdrew"] in ("0", "1")]
    rng = random.Random(SEED)
    out = {}
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["rep", "visits_total"])
    for rep in range(1, 1001):
        s = draw(rng, joiners, 30)
        w.writerow([rep, sum(int(r["visits"]) for r in s)])
    out["tonmick-sim-means-30.csv"] = buf.getvalue().encode("utf-8")
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["rep", "withdrew"])
    for rep in range(1, 51):
        s = draw(rng, known, 100)
        w.writerow([rep, sum(int(r["withdrew"]) for r in s)])
    out["tonmick-sim-samples-100.csv"] = buf.getvalue().encode("utf-8")
    return out


def main():
    files = build()
    if "--check" in sys.argv:
        bad = [n for n, b in files.items() if not (FOLDER / n).is_file() or (FOLDER / n).read_bytes() != b]
        extra = sorted(p.name for p in FOLDER.glob("*") if p.name not in files) if FOLDER.is_dir() else []
        if bad or extra:
            for n in bad:
                print(f"MISMATCH simulations/{n} does not equal the draw from seed {SEED}")
            for n in extra:
                print(f"MISMATCH simulations/{n} is not one of the drawn simulations")
            print("SIMULATIONS_CHECK_FAILED")
            sys.exit(1)
        print(f"SIMULATIONS_CHECK_OK files={len(files)} seed={SEED}")
        return
    FOLDER.mkdir(exist_ok=True)
    for n, b in files.items():
        p = FOLDER / n
        if p.exists():
            print(f"kept simulations/{n} (it exists; simulations are drawn once and never redrawn)")
        else:
            p.write_bytes(b)
            print(f"wrote simulations/{n}")


if __name__ == "__main__":
    main()
