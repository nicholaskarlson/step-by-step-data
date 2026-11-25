#!/usr/bin/env python3
"""Run every check in this repository and compare the routes.

    python run_all.py                 Python route, and base R if Rscript is found
    python run_all.py --require-r     fail if base R is not found (what CI runs)

1. SHA256SUMS: every file in data/, samples/, simulations/, practice/, calculator/, and
   figures/png/ is listed, and each matches.
2. The three fixed samples in samples/ must equal the draw from seed 2027
   (python/make_samples.py --check), and so must the two simulations in simulations/
   (python/make_simulations.py --check) and the practice test's nine data sets in practice/
   (python/make_practice.py --check; practice/givens.csv is chosen by hand, not drawn).
3. For each set of values (the data summary, Chapters 1 to 4, Chapters 5 to 8, Chapters 9 to 12,
   the back matter's tables, the figures, and the practice test), route 1, standard-library
   Python (python/<set>.py), and route 2, base R (r/<set>.R), each write build/<route>/<set>.csv.
4. Each route's values must equal expected/<set>.csv, name for name, character for
   character. No name may appear in two sets, since the book reads them all together.
   Chapters 5 to 8 also check three simulations against their exact values, each route with
   its own random numbers, within a stated tolerance; those print a line each and are not
   compared between the routes. The figures' set checks its two simulations against the model
   the same way.

The figures themselves are drawn by figures/draw.py, which needs matplotlib; it is not run here.
It recomputes every value in expected/figures.csv, and every pt.fig value in
expected/practice.csv, from the data and stops unless each one matches (CI runs it).

The last line is STEP_BY_STEP_DATA_OK when everything matches. Standard library only;
Python 3.10 or later. R needs no add-on packages.
"""
import argparse
import csv
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FOLDERS = ("data", "samples", "simulations", "practice", "calculator", "figures/png")
problems = []


def sums():
    listed = {}
    for line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, name = line.split(maxsplit=1)
            listed[name.lstrip("*")] = digest
    found = sorted(p.relative_to(ROOT).as_posix() for d in FOLDERS for p in (ROOT / d).iterdir()
                   if p.is_file() and p.name != "SOURCE.md")
    if sorted(listed) != found:
        problems.append(f"SHA256SUMS lists {sorted(listed)}, but {', '.join(d + '/' for d in FOLDERS)} hold {found}")
    for name, digest in listed.items():
        p = ROOT / name
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            problems.append(f"{name}: SHA-256 does not match SHA256SUMS")
    return len(listed)


def rscript():
    found = shutil.which("Rscript")
    if found:
        return found
    if os.name == "nt":
        cands = sorted(Path("C:/Program Files/R").glob("R-*/bin/Rscript.exe"))
        if cands:
            return str(cands[-1])
    return None


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if not rows or rows[0] != ["name", "value"]:
        problems.append(f"{path}: the first line should be name,value")
        return {}
    return {r[0]: r[1] for r in rows[1:] if r}


def run_route(cmd, label, out, env):
    """Run one route; if it stops with an error, record it (its own message is printed above)."""
    if out.exists():
        out.unlink()
    done = subprocess.run(cmd, env=env)
    if done.returncode != 0:
        problems.append(f"{label}: the route stopped with exit status {done.returncode} (its message is above)")
        return False
    return True


def compare(route, got, want):
    for name in sorted(set(want) | set(got)):
        if got.get(name) != want.get(name):
            problems.append(f"{route}: {name} is {got.get(name)!r}, expected {want.get(name)!r}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--require-r", action="store_true", help="fail if base R is not found")
    a = ap.parse_args()
    files = sums()
    env = dict(os.environ, PYTHONUTF8="1")
    check = subprocess.run([sys.executable, "-I", str(ROOT / "python" / "make_samples.py"), "--check"],
                           capture_output=True, text=True, env=env)
    print((check.stdout or "").strip().splitlines()[-1] if check.stdout else "make_samples.py printed nothing")
    if check.returncode != 0:
        problems.append("samples/: the files do not equal the draw from seed 2027 (python/make_samples.py --check)")
    check = subprocess.run([sys.executable, "-I", str(ROOT / "python" / "make_simulations.py"), "--check"],
                           capture_output=True, text=True, env=env)
    print((check.stdout or "").strip().splitlines()[-1] if check.stdout else "make_simulations.py printed nothing")
    if check.returncode != 0:
        problems.append("simulations/: the files do not equal the draw from seed 2027 (python/make_simulations.py --check)")
    check = subprocess.run([sys.executable, "-I", str(ROOT / "python" / "make_practice.py"), "--check"],
                           capture_output=True, text=True, env=env)
    print((check.stdout or "").strip().splitlines()[-1] if check.stdout else "make_practice.py printed nothing")
    if check.returncode != 0:
        problems.append("practice/: the files do not equal the draw from seed 2027 (python/make_practice.py --check)")
    sets = ["data_summary", "chapters_1_4", "chapters_5_8", "chapters_9_12", "tables", "figures", "practice"]
    want = {name: read(ROOT / "expected" / f"{name}.csv") for name in sets}
    seen = {}
    for name in sets:
        for key in want[name]:
            if key in seen:
                problems.append(f"{key} is in expected/{seen[key]}.csv and expected/{name}.csv")
            seen[key] = name
    routes = ["python"]
    for name in sets:
        out = ROOT / "build" / "python" / f"{name}.csv"
        if run_route([sys.executable, "-I", str(ROOT / "python" / f"{name}.py"), str(ROOT), str(out)], f"python {name}", out, env):
            compare(f"python {name}", read(out), want[name])
    r = rscript()
    if r:
        ver = subprocess.run([r, "--version"], capture_output=True, text=True)
        print(((ver.stdout or "") + (ver.stderr or "")).strip().splitlines()[0])
        for name in sets:
            out = ROOT / "build" / "r" / f"{name}.csv"
            if run_route([r, "--vanilla", str(ROOT / "r" / f"{name}.R"), str(ROOT), str(out)], f"r {name}", out, env):
                compare(f"r {name}", read(out), want[name])
        routes.append("r")
    elif a.require_r:
        problems.append("base R was not found (Rscript), and --require-r was given")
    else:
        print("base R not found: the R route was skipped (CI runs it)")
    if problems:
        for p in problems:
            print("MISMATCH", p)
        print(f"STEP_BY_STEP_DATA_FAILED mismatches={len(problems)}")
        sys.exit(1)
    counts = " ".join(f"{name}={len(want[name])}" for name in sets)
    print(f"STEP_BY_STEP_DATA_OK files={files} values={sum(len(v) for v in want.values())} ({counts}) "
          f"samples=3 simulations=2 practice_data=9 routes={','.join(routes)}")


if __name__ == "__main__":
    main()
