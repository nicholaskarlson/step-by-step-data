#!/usr/bin/env python3
"""Make the data files from the public Tonmick files in the Predictive companion.

    python -I python/make_data.py PREDICT            write data/
    python -I python/make_data.py PREDICT --check    rebuild in memory and compare with data/, byte for byte

PREDICT is a checkout of github.com/nicholaskarlson/predict at v1.0.1, for example
    git clone --depth 1 --branch v1.0.1 https://github.com/nicholaskarlson/predict.git build/predict

This is the classroom guide's classroom/make_data.py (book-tour-00-classroom at 86a5308), with
only its paths changed: it writes data/ here, and data/SOURCE.md is not one of its files.
Standard library only. The companion is the Predictive companion
(github.com/nicholaskarlson/predict, v1.0.1); its Tonmick v1.0.0 files hold the
1,600 invited students, the 1,219 who joined and were randomized, and their first
year. Nothing is sampled or drawn at random: every file is a selection of rows and
columns, sorted by student ID, so the rebuild is exact.

Calculators hold numbers, not words, so every column a student will
analyze is a number (1 = yes, 0 = no; blank = not known). A TI-84 list holds at most
999 entries, so each file meant for calculator lists stays under that; the larger
files are for a spreadsheet. The dictionary file describes every column.

tonmick-lists.csv is for TI Connect CE's Data Import, which turns a CSV into
calculator lists. Its rules: numbers only, so no header row; data from cell A1; at
most six columns (A to F become six lists), each at most 999 cells; the first empty
cell ends a list. So the file has no header, and its columns may differ in length:
L1 and L2 for the students offered mentoring (609), L3 and L4 for those not offered
(610), L5 and L6 for those not offered who have a 12-month grade (555). This script
refuses the file if it breaks any of those rules.
"""
import csv, io, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data"
NOT_MADE_HERE = {"SOURCE.md"}
SRC = Path("open-materials") / "predictive-reasoning-with-statistics" / "source"
TI84_MAX = 999
TI_IMPORT_COLUMNS = 6
CALCULATOR_FILES = {"tonmick-offered.csv", "tonmick-not-offered.csv", "tonmick-grades-not-offered.csv"}
LISTS_FILE = "tonmick-lists.csv"

DICTIONARY = [
    ("file", "column", "meaning"),
    ("tonmick-classroom.csv", "student_id", "Fictional student ID"),
    ("tonmick-classroom.csv", "college", "College ID (16 colleges); the offer was randomized within each college"),
    ("tonmick-classroom.csv", "offer", "1 = randomly offered peer mentoring; 0 = not offered"),
    ("tonmick-classroom.csv", "part_time", "1 = enrolled part-time at entry; 0 = full-time"),
    ("tonmick-classroom.csv", "entry_grade", "Grade average from school records at entry, 1.5 to 4.0"),
    ("tonmick-classroom.csv", "visits", "Visits to student support services in the first year, while enrolled"),
    ("tonmick-classroom.csv", "withdrew", "1 = withdrew within the first year; 0 = did not (a transfer out counts as 0); blank = not known (consent withdrawn)"),
    ("tonmick-classroom.csv", "grade_12", "College grade average after 12 months (or at exit, for a student who left after month 4); blank = none recorded"),
    ("tonmick-classroom.csv", "exit", "How the first year ended: stayed, withdrew, transferred, or consent withdrawn"),
    ("tonmick-offered.csv", "entry_grade", "As above, for the 609 students offered mentoring (calculator lists)"),
    ("tonmick-offered.csv", "visits", "As above, for the 609 students offered mentoring (calculator lists)"),
    ("tonmick-not-offered.csv", "entry_grade", "As above, for the 610 students not offered mentoring (calculator lists)"),
    ("tonmick-not-offered.csv", "visits", "As above, for the 610 students not offered mentoring (calculator lists)"),
    ("tonmick-grades-not-offered.csv", "entry_grade", "Students not offered mentoring who have a 12-month grade (calculator lists)"),
    ("tonmick-grades-not-offered.csv", "grade_12", "Their college grade average after 12 months"),
    ("tonmick-invited.csv", "student_id", "Fictional student ID, for all 1,600 students invited to the study"),
    ("tonmick-invited.csv", "college", "College ID"),
    ("tonmick-invited.csv", "part_time", "1 = enrolled part-time at entry; 0 = full-time"),
    ("tonmick-invited.csv", "joined", "1 = answered the baseline survey and joined the study; 0 = did not"),
    ("tonmick-lists.csv", "A (L1)", "School grade at entry, students offered mentoring (609 rows); no header row, for TI Connect CE's Data Import"),
    ("tonmick-lists.csv", "B (L2)", "Support visits in the first year, students offered mentoring (609 rows)"),
    ("tonmick-lists.csv", "C (L3)", "School grade at entry, students not offered (610 rows)"),
    ("tonmick-lists.csv", "D (L4)", "Support visits in the first year, students not offered (610 rows)"),
    ("tonmick-lists.csv", "E (L5)", "School grade at entry, students not offered who have a 12-month grade (555 rows)"),
    ("tonmick-lists.csv", "F (L6)", "College grade after 12 months, the same 555 students"),
]
EXIT = {"none": "stayed", "withdrawal": "withdrew", "transfer": "transferred", "consent_withdrawn": "consent withdrawn"}


def read(companion, rel):
    with open(companion / SRC / rel, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def table(header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    return buf.getvalue().encode("utf-8")


def lists_file(columns):
    """Columns side by side with no header, for TI Connect CE: a short column ends in empty cells."""
    if len(columns) > TI_IMPORT_COLUMNS:
        sys.exit(f"make_data: {LISTS_FILE} has {len(columns)} columns; TI Connect CE imports at most {TI_IMPORT_COLUMNS}")
    for i, col in enumerate(columns, 1):
        if not 0 < len(col) <= TI84_MAX:
            sys.exit(f"make_data: {LISTS_FILE} list L{i} has {len(col)} entries; a TI-84 list holds 1 to {TI84_MAX}")
        for v in col:
            try:
                float(v)
            except ValueError:
                sys.exit(f"make_data: {LISTS_FILE} list L{i} holds {v!r}; TI Connect CE imports numbers only")
            if v.strip() != v or v == "" or "," in v:
                sys.exit(f"make_data: {LISTS_FILE} list L{i} holds {v!r}; an empty cell would end the list early")
    depth = max(len(c) for c in columns)
    rows = [[c[r] if r < len(c) else "" for c in columns] for r in range(depth)]
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows(rows)
    return buf.getvalue().encode("utf-8")


def build(companion):
    invited = {r["student_id"]: r for r in read(companion, "tonmick-v1.0.0/data/anchor/participants.csv")}
    base = {r["student_id"]: r for r in read(companion, "tonmick-v1.0.0/data/anchor/baseline.csv")}
    reg = {r["student_id"]: r for r in read(companion, "tonmick-v1.0.0/data/anchor/registry.csv")}
    if set(base) != set(reg) or not set(base) <= set(invited):
        sys.exit("make_data: the baseline, registry, and participants files do not match")
    rows = []
    for sid in sorted(base):
        b, r, p = base[sid], reg[sid], invited[sid]
        exit_type = EXIT[r["exit_type"]]
        withdrew = "" if r["exit_type"] == "consent_withdrawn" else r["withdrawn_12"]
        rows.append([sid, b["college_id"], b["offer"], p["part_time"], p["prior_grade"], r["visits_12"],
                     withdrew, r["gpa12"], exit_type])
    files = {
        "tonmick-classroom.csv": table(["student_id", "college", "offer", "part_time", "entry_grade", "visits",
                                        "withdrew", "grade_12", "exit"], rows),
        "tonmick-offered.csv": table(["entry_grade", "visits"], [[r[4], r[5]] for r in rows if r[2] == "1"]),
        "tonmick-not-offered.csv": table(["entry_grade", "visits"], [[r[4], r[5]] for r in rows if r[2] == "0"]),
        "tonmick-grades-not-offered.csv": table(["entry_grade", "grade_12"],
                                                [[r[4], r[7]] for r in rows if r[2] == "0" and r[7] != ""]),
        "tonmick-invited.csv": table(["student_id", "college", "part_time", "joined"],
                                     [[s, invited[s]["college_id"], invited[s]["part_time"], invited[s]["responded_baseline"]]
                                      for s in sorted(invited)]),
        "tonmick-classroom-dictionary.csv": table(DICTIONARY[0], DICTIONARY[1:]),
    }
    offered = [r for r in rows if r[2] == "1"]
    not_offered = [r for r in rows if r[2] == "0"]
    graded = [r for r in not_offered if r[7] != ""]
    files[LISTS_FILE] = lists_file([[r[4] for r in offered], [r[5] for r in offered],
                                    [r[4] for r in not_offered], [r[5] for r in not_offered],
                                    [r[4] for r in graded], [r[7] for r in graded]])
    for name in CALCULATOR_FILES:
        n = files[name].count(b"\n") - 1
        if n > TI84_MAX:
            sys.exit(f"make_data: {name} has {n} rows; a TI-84 list holds at most {TI84_MAX}")
    return files


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    companion = Path(args[0]).resolve()
    files = build(companion)
    if "--check" in sys.argv:
        bad = [n for n, data in files.items() if not (OUT / n).is_file() or (OUT / n).read_bytes() != data]
        extra = sorted(p.name for p in OUT.glob("*") if p.name not in files and p.name not in NOT_MADE_HERE) if OUT.is_dir() else []
        for n in bad:
            print("DIFFERS", n)
        for n in extra:
            print("NOT MADE BY THIS SCRIPT", n)
        if bad or extra:
            print(f"CLASSROOM_DATA_FAILED differs={len(bad)} extra={len(extra)}")
            sys.exit(1)
        print(f"CLASSROOM_DATA_OK files={len(files)}")
        return
    OUT.mkdir(exist_ok=True)
    for n, data in files.items():
        (OUT / n).write_bytes(data)
    print(f"wrote {len(files)} files in {OUT}")


if __name__ == "__main__":
    main()
