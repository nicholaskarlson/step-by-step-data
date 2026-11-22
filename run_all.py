#!/usr/bin/env python3
"""Run every check in this repository and compare the routes.

    python run_all.py                 Python route, and base R if Rscript is found
    python run_all.py --require-r     fail if base R is not found (what CI runs)

1. SHA256SUMS: every file in data/ and calculator/ is listed, and each matches.
2. Route 1, standard-library Python (python/data_summary.py), and route 2, base R
   (r/data_summary.R), each write build/<route>/data_summary.csv.
3. Each route's values must equal expected/data_summary.csv, name for name, character
   for character.

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
problems = []


def sums():
    listed = {}
    for line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        if line.strip():
            digest, name = line.split(maxsplit=1)
            listed[name.lstrip("*")] = digest
    found = sorted(p.relative_to(ROOT).as_posix() for d in ("data", "calculator") for p in (ROOT / d).iterdir()
                   if p.is_file() and p.name != "SOURCE.md")
    if sorted(listed) != found:
        problems.append(f"SHA256SUMS lists {sorted(listed)}, but data/ and calculator/ hold {found}")
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
    want = read(ROOT / "expected" / "data_summary.csv")
    routes = []
    out = ROOT / "build" / "python" / "data_summary.csv"
    subprocess.run([sys.executable, "-I", str(ROOT / "python" / "data_summary.py"), str(ROOT), str(out)], check=True, env=env)
    compare("python", read(out), want)
    routes.append("python")
    r = rscript()
    if r:
        ver = subprocess.run([r, "--version"], capture_output=True, text=True)
        print(((ver.stdout or "") + (ver.stderr or "")).strip().splitlines()[0])
        out = ROOT / "build" / "r" / "data_summary.csv"
        subprocess.run([r, "--vanilla", str(ROOT / "r" / "data_summary.R"), str(ROOT), str(out)], check=True, env=env)
        compare("r", read(out), want)
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
    print(f"STEP_BY_STEP_DATA_OK files={files} values={len(want)} routes={','.join(routes)}")


if __name__ == "__main__":
    main()
