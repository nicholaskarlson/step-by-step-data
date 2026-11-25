#!/usr/bin/env python3
"""Draw the practice test's nine invented data sets, once.

    python -I python/make_practice.py            write practice/ (only if a file is missing)
    python -I python/make_practice.py --check    redraw in memory and compare with practice/, byte for byte

The book's practice test uses new settings, not Tonmick, so a student practices reading an
unfamiliar setting quickly. Every setting is invented, and so are these data. The models below
were written before the first run, the seed is 2027, as for the samples, and nothing is redrawn
to get nicer numbers: the questions are written to fit what was drawn.

The draw uses only random.Random(2027).random(), whose sequence Python guarantees across
versions for a given seed, and arithmetic that every platform does alike: a standard normal
value z is the sum of twelve random() values minus 6 (the Irwin-Hall approximation, from its
first value to its twelfth), and a right-skewed value adds squares of such z values. Values are
rounded with Python's round() to the places shown. One generator draws everything, in this
order (within a row, the values are drawn left to right):

1. practice-waits.csv: 80 riders' waits at a bus stop, in minutes, one place:
   0.5 + 2.6 (z1² + z2²). Right-skewed.
2. practice-batteries.csv: battery life of 30 phones of model A, then 30 of model B, in hours,
   one place: A is 17.5 + 1.6 z, B is 16.0 + 3.2 z.
3. practice-flowering-sim.csv: 200 reruns of a randomized experiment's assignment. Of 80
   seedlings, 32 flowered (20 of the 40 given fertilizer A and 12 of the 40 given B). Each rerun
   shuffles the labels: with the 80 seedlings in a list whose first 32 flowered, a partial
   Fisher-Yates shuffle picks 40 for group A (for i = 0, 1, ..., 39, j = i + int(u * (80 - i)),
   with u the next random() value; positions i and j swap), and the row records how many of the
   40 flowered (flowered_a). The rerun's difference in shares is (2 * flowered_a - 32) / 40.
4. practice-checkout.csv: minutes 12 customers waited at a store's checkout, one place: 11
   values 1.5 + 1.1 (z1² + z2²), then one from a much longer tail, 13.0 + 1.5 |z|, which goes
   into the list of 12 at position int(u * 12) (0 is first), with u the next random() value.
   So the sample is skewed and has an outlier by design.
5. practice-shoes.csv: 10 runners each ran a mile in shoe A and in shoe B, in whole seconds.
   For each runner, base = 420 + 30 z0; shoe A is base + 4 z1 and shoe B is base - 4 + 4 z2.
6. practice-iced.csv: 25 summer days at a snack stand: the day's high, a whole number of
   degrees Fahrenheit from 60 to 95 (60 + int(u * 36)), and iced drinks sold, a whole number,
   -150 + 4.5 x high + 22 z.
7. practice-stopping.csv: 12 braking trials at 20, 25, ..., 75 miles per hour: stopping
   distance in whole feet, 1.1 x speed + 0.055 x speed² + 6 z. The relation curves by design.
8. practice-commute.csv: one-way commutes of 25 students who bike, then 25 who ride the bus, in
   whole minutes: bike is 17 + 3.5 z, bus is 12 + 3.0 (z1² + z2² + z3²).
9. practice-fill.csv: fill of 20 cups from a drink machine set for 12 ounces, two places:
   11.92 + 0.18 z.

practice/givens.csv is not drawn: it holds the numbers the questions state, chosen by hand, and
this script leaves it alone. Standard library only; Python 3.10 or later.
"""
import csv
import io
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = 2027
FOLDER = ROOT / "practice"
NOT_DRAWN = {"givens.csv"}


def z(rng):
    s = 0.0
    for _ in range(12):
        s += rng.random()
    return s - 6.0


def table(header, rows):
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    return buf.getvalue().encode("utf-8")


def build():
    rng = random.Random(SEED)
    out = {}

    rows = []
    for i in range(1, 81):
        a = z(rng)
        b = z(rng)
        rows.append([i, f"{round(0.5 + 2.6 * (a * a + b * b), 1):.1f}"])
    out["practice-waits.csv"] = table(["rider", "minutes"], rows)

    rows = []
    for i in range(1, 31):
        rows.append([i, "A", f"{round(17.5 + 1.6 * z(rng), 1):.1f}"])
    for i in range(31, 61):
        rows.append([i, "B", f"{round(16.0 + 3.2 * z(rng), 1):.1f}"])
    out["practice-batteries.csv"] = table(["phone", "model", "hours"], rows)

    rows = []
    for rep in range(1, 201):
        pool = list(range(80))
        for i in range(40):
            j = i + int(rng.random() * (80 - i))
            pool[i], pool[j] = pool[j], pool[i]
        rows.append([rep, sum(p < 32 for p in pool[:40])])
    out["practice-flowering-sim.csv"] = table(["rerun", "flowered_a"], rows)

    vals = []
    for _ in range(11):
        a = z(rng)
        b = z(rng)
        vals.append(round(1.5 + 1.1 * (a * a + b * b), 1))
    far = round(13.0 + 1.5 * abs(z(rng)), 1)
    vals.insert(int(rng.random() * 12), far)
    out["practice-checkout.csv"] = table(["customer", "minutes"], [[i, f"{v:.1f}"] for i, v in enumerate(vals, 1)])

    rows = []
    for i in range(1, 11):
        base = 420 + 30 * z(rng)
        a = round(base + 4 * z(rng))
        b = round(base - 4 + 4 * z(rng))
        rows.append([i, a, b])
    out["practice-shoes.csv"] = table(["runner", "shoe_a", "shoe_b"], rows)

    rows = []
    for i in range(1, 26):
        x = 60 + int(rng.random() * 36)
        rows.append([i, x, round(-150 + 4.5 * x + 22 * z(rng))])
    out["practice-iced.csv"] = table(["day", "high_f", "drinks"], rows)

    rows = []
    for i, s in enumerate(range(20, 80, 5), 1):
        rows.append([i, s, round(1.1 * s + 0.055 * s * s + 6 * z(rng))])
    out["practice-stopping.csv"] = table(["trial", "speed_mph", "distance_ft"], rows)

    rows = []
    for i in range(1, 26):
        rows.append([i, "bike", round(17 + 3.5 * z(rng))])
    for i in range(26, 51):
        a = z(rng)
        b = z(rng)
        c = z(rng)
        rows.append([i, "bus", round(12 + 3.0 * (a * a + b * b + c * c))])
    out["practice-commute.csv"] = table(["student", "mode", "minutes"], rows)

    rows = []
    for i in range(1, 21):
        rows.append([i, f"{round(11.92 + 0.18 * z(rng), 2):.2f}"])
    out["practice-fill.csv"] = table(["cup", "ounces"], rows)
    return out


def main():
    files = build()
    if "--check" in sys.argv:
        bad = [n for n, b in files.items() if not (FOLDER / n).is_file() or (FOLDER / n).read_bytes() != b]
        extra = sorted(p.name for p in FOLDER.glob("*") if p.name not in files and p.name not in NOT_DRAWN) \
            if FOLDER.is_dir() else []
        if bad or extra:
            for n in bad:
                print(f"MISMATCH practice/{n} does not equal the draw from seed {SEED}")
            for n in extra:
                print(f"MISMATCH practice/{n} is not one of the drawn data sets (or givens.csv)")
            print("PRACTICE_CHECK_FAILED")
            sys.exit(1)
        print(f"PRACTICE_CHECK_OK files={len(files)} seed={SEED}")
        return
    FOLDER.mkdir(exist_ok=True)
    for n, b in files.items():
        p = FOLDER / n
        if p.exists():
            print(f"kept practice/{n} (it exists; the practice data are drawn once and never redrawn)")
        else:
            p.write_bytes(b)
            print(f"wrote practice/{n}")


if __name__ == "__main__":
    main()
