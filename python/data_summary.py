#!/usr/bin/env python3
"""Route 1 (standard-library Python): summarize the data files, as data_summary.R does in base R.

    python -I python/data_summary.py ROOT OUT.csv

Writes OUT.csv with two columns, name and value: file sizes, list lengths, counts, and a few
means and standard deviations, each formatted the same way in both routes (whole numbers as
they are; other numbers to six decimals; 1 or 0 for a check that holds or fails). run_all.py
compares the two routes with expected/data_summary.csv.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2])
res = {}


def rows(name, header=True):
    with open(ROOT / "data" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f)) if header else list(csv.reader(f))


def put(name, value):
    res[name] = value if isinstance(value, str) else (str(value) if isinstance(value, int) else f"{value:.6f}")


def mean_sd(x):
    m = math.fsum(x) / len(x)
    return m, math.sqrt(math.fsum((a - m) ** 2 for a in x) / (len(x) - 1))


def leading(col):
    """A TI-84 list from the lists file: the entries before the first empty cell."""
    out = []
    for v in col:
        if v == "":
            break
        out.append(v)
    return out


cls = rows("tonmick-classroom.csv")
off, noff = rows("tonmick-offered.csv"), rows("tonmick-not-offered.csv")
grd, inv = rows("tonmick-grades-not-offered.csv"), rows("tonmick-invited.csv")
dic, lst = rows("tonmick-classroom-dictionary.csv"), rows("tonmick-lists.csv", header=False)

for key, table in (("classroom", cls), ("offered", off), ("not_offered", noff), ("grades_not_offered", grd),
                   ("invited", inv), ("dictionary", dic), ("lists", lst)):
    put(f"files.{key}.rows", len(table))
cols = [[r[i] if i < len(r) else "" for r in lst] for i in range(6)]
L = [leading(c) for c in cols]
for i, v in enumerate(L, 1):
    put(f"lists.L{i}.n", len(v))
    put(f"lists.L{i}.no_gaps", int(all(x == "" for x in cols[i - 1][len(v):])))

o = [r for r in cls if r["offer"] == "1"]
n = [r for r in cls if r["offer"] == "0"]
g = [r for r in n if r["grade_12"] != ""]
put("check.offered_file_is_classroom", int([[r["entry_grade"], r["visits"]] for r in o] == [[r["entry_grade"], r["visits"]] for r in off]))
put("check.not_offered_file_is_classroom", int([[r["entry_grade"], r["visits"]] for r in n] == [[r["entry_grade"], r["visits"]] for r in noff]))
put("check.grades_file_is_classroom", int([[r["entry_grade"], r["grade_12"]] for r in g] == [[r["entry_grade"], r["grade_12"]] for r in grd]))
put("check.L1_L2_are_offered", int(L[0] == [r["entry_grade"] for r in off] and L[1] == [r["visits"] for r in off]))
put("check.L3_L4_are_not_offered", int(L[2] == [r["entry_grade"] for r in noff] and L[3] == [r["visits"] for r in noff]))
put("check.L5_L6_are_grades", int(L[4] == [r["entry_grade"] for r in grd] and L[5] == [r["grade_12"] for r in grd]))
joined = [r for r in inv if r["joined"] == "1"]
put("check.joined_are_classroom", int(sorted(r["student_id"] for r in joined) == sorted(r["student_id"] for r in cls)))

put("classroom.offered", len(o))
put("classroom.not_offered", len(n))
put("classroom.colleges", len({r["college"] for r in cls}))
put("classroom.part_time", sum(r["part_time"] == "1" for r in cls))
put("invited.joined", len(joined))
put("invited.part_time", sum(r["part_time"] == "1" for r in inv))
put("invited.part_time_joined", sum(r["part_time"] == "1" for r in joined))
for label, key in (("stayed", "stayed"), ("withdrew", "withdrew"), ("transferred", "transferred"),
                   ("consent_withdrawn", "consent withdrawn")):
    put(f"exit.{label}", sum(r["exit"] == key for r in cls))
for label, grp in (("offered", o), ("not_offered", n)):
    put(f"withdrew.{label}", sum(r["withdrew"] == "1" for r in grp))
    put(f"known.{label}", sum(r["withdrew"] in ("0", "1") for r in grp))
    v = [int(r["visits"]) for r in grp]
    put(f"visits.{label}.sum", sum(v))
    m, s = mean_sd([float(x) for x in v])
    put(f"visits.{label}.mean", m)
    put(f"visits.{label}.sd", s)
    put(f"grade_12.{label}.n", sum(r["grade_12"] != "" for r in grp))
m, s = mean_sd([float(r["entry_grade"]) for r in cls])
put("entry_grade.all.mean", m)
put("entry_grade.all.sd", s)
m, s = mean_sd([float(r["grade_12"]) for r in g])
put("grade_12.not_offered.mean", m)
put("grade_12.not_offered.sd", s)

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["name", "value"])
    w.writerows(res.items())
print(f"python route: {len(res)} values in {OUT}")
