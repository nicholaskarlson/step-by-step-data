#!/usr/bin/env python3
"""Route 1 for the back matter's three tables: the standard normal table, t critical values,
and chi-square critical values, with standard-library Python.

    python -I python/tables.py ROOT OUT.csv

Each table row is one value (name,value), its entries separated by ", ", as the book prints
them, so run_all.py can compare the routes and expected/tables.csv character for character.

- Standard normal: the area to the left of z, to four decimals, for z from -3.49 to 3.49. Row
  table.normal.neg.1.9 holds z = -1.90, -1.91, ..., -1.99; row table.normal.pos.1.9 holds
  z = 1.90, 1.91, ..., 1.99.
- t: the critical value t* with the stated area to its right, to three decimals, for 1 to 30,
  40, 50, 60, 80, 100, and 1,000 degrees of freedom, and the z* row the t values approach.
- Chi-square: the critical value with the stated area to its right, to three decimals, for 1
  to 30, 40, 50, 60, 80, and 100 degrees of freedom.

Python's standard library has the normal distribution (statistics.NormalDist) but not t or
chi-square, so this route computes those from the regularized incomplete beta and gamma
functions and inverts them by bisection; route 2 uses base R's qt and qchisq.
"""
import csv
import math
import sys
from pathlib import Path
from statistics import NormalDist

OUT = Path(sys.argv[2])
N01 = NormalDist()
T_TAILS = ["0.20", "0.10", "0.05", "0.025", "0.01", "0.005", "0.001", "0.0005"]
T_LEVELS = ["60%", "80%", "90%", "95%", "98%", "99%", "99.8%", "99.9%"]
T_DF = list(range(1, 31)) + [40, 50, 60, 80, 100, 1000]
C_TAILS = ["0.25", "0.20", "0.10", "0.05", "0.025", "0.01", "0.005", "0.001"]
C_DF = list(range(1, 31)) + [40, 50, 60, 80, 100]
V = {}


def put(name, value):
    if name in V:
        raise SystemExit(f"duplicate name {name}")
    V[name] = str(value)


def betacf(a, b, x):
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 20000):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d; d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c; c = c if abs(c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d; d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c; c = c if abs(c) > tiny else tiny
        de = d * c
        h *= de
        if abs(de - 1.0) < 1e-16:
            return h
    raise SystemExit("betacf did not converge")


def ibeta(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lb = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log1p(-x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lb) * betacf(a, b, x) / a
    return 1.0 - math.exp(lb) * betacf(b, a, 1.0 - x) / b


def t_upper(t, df):
    return 0.5 * ibeta(df / 2, 0.5, df / (df + t * t))


def gamma_q(a, x):
    if x <= 0:
        return 1.0
    lg = -x + a * math.log(x) - math.lgamma(a)
    if x < a + 1:
        term = s = 1.0 / a
        ap = a
        for _ in range(100000):
            ap += 1
            term *= x / ap
            s += term
            if abs(term) < abs(s) * 1e-17:
                return 1.0 - s * math.exp(lg)
        raise SystemExit("gamma series did not converge")
    tiny = 1e-300
    b = x + 1 - a
    c, d = 1 / tiny, 1 / b
    h = d
    for i in range(1, 100000):
        an = -i * (i - a)
        b += 2
        d = an * d + b; d = d if abs(d) > tiny else tiny
        c = b + an / c; c = c if abs(c) > tiny else tiny
        d = 1 / d
        de = d * c
        h *= de
        if abs(de - 1) < 1e-16:
            return math.exp(lg) * h
    raise SystemExit("gamma fraction did not converge")


def invert(fn, target, lo, hi):
    for _ in range(400):
        mid = (lo + hi) / 2
        if fn(mid) > target:
            lo = mid
        else:
            hi = mid
        if hi - lo < 1e-13 * max(1.0, abs(mid)):
            break
    return (lo + hi) / 2


def t_star(tail, df):
    hi = 1.0
    while t_upper(hi, df) > tail:
        hi *= 2
    return invert(lambda t: t_upper(t, df), tail, 0.0, hi)


def chi2_star(tail, df):
    hi = df + 10.0
    while gamma_q(df / 2, hi / 2) > tail:
        hi *= 2
    return invert(lambda x: gamma_q(df / 2, x / 2), tail, 0.0, hi)


def main():
    for side, sign in (("neg", -1), ("pos", 1)):
        for tenth in range(35):
            row = [f"{N01.cdf(sign * (tenth * 10 + h) / 100):.4f}" for h in range(10)]
            put(f"table.normal.{side}.{tenth // 10}.{tenth % 10}", ", ".join(row))
    put("table.t.tails", ", ".join(T_TAILS))
    put("table.t.levels", ", ".join(T_LEVELS))
    for df in T_DF:
        put(f"table.t.df.{df}", ", ".join(f"{t_star(float(p), df):.3f}" for p in T_TAILS))
    put("table.t.z", ", ".join(f"{N01.inv_cdf(1 - float(p)):.3f}" for p in T_TAILS))
    put("table.chisq.tails", ", ".join(C_TAILS))
    for df in C_DF:
        put(f"table.chisq.df.{df}", ", ".join(f"{chi2_star(float(p), df):.3f}" for p in C_TAILS))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["name", "value"])
        for k in sorted(V):
            w.writerow([k, V[k]])


if __name__ == "__main__":
    main()
