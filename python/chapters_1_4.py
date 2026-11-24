#!/usr/bin/env python3
"""Route 1 for Chapters 1 to 4: every number the chapters, their Try It answers, and their
reviews print, rebuilt from the data files with standard-library Python.

    python -I python/chapters_1_4.py ROOT OUT.csv

Each value is written as the book prints it (name,value), so run_all.py can compare the
routes and expected/chapters_1_4.csv character for character. Conventions:

- Quartiles are the TI-84's: the medians of the lower and upper halves, the median left
  out when n is odd.
- Sx divides by n - 1 and sigma-x by n, as on the calculator.
- Negative numbers use the ASCII hyphen-minus here; the book prints a true minus sign.
- Shares print as the book prints them: 0.4996, or 81.4 for 81.4%.

The outline that says where each value appears is outline/chapters-1-4.md.
"""
import csv
import hashlib
import math
import sys
from pathlib import Path
from statistics import NormalDist

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
N01 = NormalDist()
V = {}


def put(name, value):
    if name in V:
        raise SystemExit(f"duplicate name {name}")
    V[name] = value


def f(x, places):
    return f"{x:.{places}f}"


def pct(num, den, places=1):
    return f"{100 * num / den:.{places}f}"


def rows(path):
    with open(ROOT / path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def median(v):
    v = sorted(v)
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def ti(x):
    """1-Var Stats as the TI-84 computes them."""
    v = sorted(x)
    n = len(v)
    h = n // 2
    lower, upper = v[:h], (v[h + 1:] if n % 2 else v[h:])
    mean = math.fsum(v) / n
    ss = math.fsum((a - mean) ** 2 for a in v)
    return {"n": n, "mean": mean, "sum": math.fsum(v), "sum2": math.fsum(a * a for a in v), "ss": ss,
            "sx": math.sqrt(ss / (n - 1)), "sg": math.sqrt(ss / n), "min": v[0], "q1": median(lower),
            "med": median(v), "q3": median(upper), "max": v[-1]}


def g(x):
    """A whole number without a decimal point, as the calculator shows it."""
    return f"{x:g}"


def betacf(a, b, x):
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / d
    h = d
    for m in range(1, 1000):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d; c = 1 + aa / c; d = 1 / d; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d; c = 1 + aa / c; d = 1 / d; de = d * c; h *= de
        if abs(de - 1) < 1e-15:
            break
    return h


def ibeta(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1 - x))
    return bt * betacf(a, b, x) / a if x < (a + 1) / (a + b + 2) else 1 - bt * betacf(b, a, 1 - x) / b


def t_two_sided(t, df):
    return ibeta(df / 2, 0.5, df / (df + t * t))


def histogram(values, start, width, stop):
    counts = []
    lo = start
    while lo < stop:
        counts.append(sum(lo <= x < lo + width for x in values))
        lo += width
    return counts


def chapter_1():
    off = rows("data/tonmick-offered.csv")
    v = [float(r["visits"]) for r in off[:10]]
    put("ch1.ex1.data", ", ".join(g(x) for x in v))
    s = ti(v)
    put("ch1.ex1.mean", g(s["mean"])); put("ch1.ex1.sum", g(s["sum"])); put("ch1.ex1.sx", f(s["sx"], 3))
    put("ch1.ex1.sigma", f(s["sg"], 3)); put("ch1.ex1.n", str(s["n"]))
    put("ch1.ex1.five", ", ".join(g(s[k]) for k in ("min", "q1", "med", "q3", "max")))
    iqr = s["q3"] - s["q1"]
    put("ch1.ex2.iqr", g(iqr)); put("ch1.ex2.fence_low", g(s["q1"] - 1.5 * iqr)); put("ch1.ex2.fence_high", g(s["q3"] + 1.5 * iqr))
    put("ch1.ex2.outliers", str(sum(x < s["q1"] - 1.5 * iqr or x > s["q3"] + 1.5 * iqr for x in v)))
    put("ch1.ex3.bars", ", ".join(str(c) for c in histogram(v, 0, 2, 10)))
    model = NormalDist(3.010, 0.469)
    put("ch1.ex4.above_3_5", f(1 - model.cdf(3.5), 4)); put("ch1.ex4.p90", f(model.inv_cdf(0.9), 3))
    pmf = [math.comb(10, k) * 0.13 ** k * 0.87 ** (10 - k) for k in range(11)]
    put("ch1.ex5.pdf2", f(pmf[2], 4)); put("ch1.ex5.cdf2", f(math.fsum(pmf[:3]), 4))
    x, n = 80, 605
    p = x / n; se = math.sqrt(p * (1 - p) / n); z = N01.inv_cdf(0.975)
    put("ch1.ex7.low", f(p - z * se, 4)); put("ch1.ex7.high", f(p + z * se, 4)); put("ch1.ex7.phat", f(p, 4))
    m1, s1, n1, m2, s2, n2 = 2.507389, 3.104596, 609, 2.193443, 2.731310, 610
    a, b = s1 ** 2 / n1, s2 ** 2 / n2
    t = (m1 - m2) / math.sqrt(a + b); df = (a + b) ** 2 / (a ** 2 / (n1 - 1) + b ** 2 / (n2 - 1))
    put("ch1.ex8.t", f(t, 2)); put("ch1.ex8.p", f(t_two_sided(t, df), 4)); put("ch1.ex8.df", f(df, 2))
    obs = [[80, 525], [93, 510]]
    tot = sum(map(sum, obs)); rs = [sum(r) for r in obs]; cs = [obs[0][j] + obs[1][j] for j in range(2)]
    chi2 = math.fsum((obs[i][j] - rs[i] * cs[j] / tot) ** 2 / (rs[i] * cs[j] / tot) for i in range(2) for j in range(2))
    put("ch1.ex9.chi2", f(chi2, 3)); put("ch1.ex9.p", f(math.erfc(math.sqrt(chi2 / 2)), 4)); put("ch1.ex9.df", "1")
    gr = rows("data/tonmick-grades-not-offered.csv")[:6]
    xs = [float(r["entry_grade"]) for r in gr]; ys = [float(r["grade_12"]) for r in gr]
    put("ch1.ex10.pairs", "; ".join(f"({r['entry_grade']}, {r['grade_12']})" for r in gr))
    mx, my = math.fsum(xs) / 6, math.fsum(ys) / 6
    sxy = math.fsum((a - mx) * (b - my) for a, b in zip(xs, ys))
    sxx = math.fsum((a - mx) ** 2 for a in xs); syy = math.fsum((b - my) ** 2 for b in ys)
    slope = sxy / sxx; r = sxy / math.sqrt(sxx * syy)
    put("ch1.ex10.a", f(my - slope * mx, 3)); put("ch1.ex10.b", f(slope, 3))
    put("ch1.ex10.r2", f(r * r, 3)); put("ch1.ex10.r", f(r, 3))


def chapter_2(every, invited):
    N = len(every)
    put("ch2.invited", f"{len(invited):,}"); put("ch2.colleges", str(len({r['college'] for r in every})))
    put("ch2.joined", f"{N:,}")
    n1 = sum(r["offer"] == "1" for r in every)
    put("ch2.offered", str(n1)); put("ch2.not_offered", str(N - n1)); put("ch2.offer_mean", f(n1 / N, 4))
    first = every[0]
    put("ch2.first_student", first["student_id"]); put("ch2.first_student_visits", first["visits"])
    exits = ["stayed", "withdrew", "transferred", "consent withdrawn"]
    counts = [sum(r["exit"] == e for r in every) for e in exits]
    for e, c in zip(exits, counts):
        key = e.split()[0]
        put(f"ch2.exit.{key}", str(c)); put(f"ch2.exit.{key}.pct", pct(c, N)); put(f"ch2.exit.{key}.share", f(c / N, 4))
    known = [r for r in every if r["withdrew"] in ("0", "1")]
    w = sum(r["withdrew"] == "1" for r in known)
    put("ch2.known", f"{len(known):,}"); put("ch2.withdrew_known.pct", pct(w, len(known))); put("ch2.withdrew_known.share", f(w / len(known), 4))
    for z, lab in (("1", "offered"), ("0", "not_offered")):
        k = [r for r in known if r["offer"] == z]
        ww = sum(r["withdrew"] == "1" for r in k)
        put(f"ch2.{lab}.withdrew", str(ww)); put(f"ch2.{lab}.known", str(len(k))); put(f"ch2.{lab}.withdrew.pct", pct(ww, len(k)))
    w1 = sum(r["offer"] == "1" and r["withdrew"] == "1" for r in every); w0 = sum(r["offer"] == "0" and r["withdrew"] == "1" for r in every)
    put("ch2.try4.height_ratio", f((w0 - 75) / (w1 - 75), 1)); put("ch2.try4.more_pct", f"{100 * (w0 / w1 - 1):.0f}")
    # review: a fictional school district, a fictional cafeteria survey, and Tonmick's exits by group
    put("ch2.review.bus.pct", pct(31, 150))
    put("ch2.review.joined.pct", pct(len(invited) - sum(r["joined"] == "0" for r in invited), len(invited)))
    for item, c in (("pizza", 96), ("salad", 36), ("sandwich", 60), ("other", 48)):
        put(f"ch2.review.cafeteria.{item}.pct", pct(c, 240, 0))
    for z, lab in (("1", "offered"), ("0", "not_offered")):
        k = [r for r in known if r["offer"] == z]
        for e in ("stayed", "withdrew", "transferred"):
            put(f"ch2.review.{lab}.{e}.pct", pct(sum(r["exit"] == e for r in k), len(k)))


def chapter_3(every):
    L2 = [float(r["visits"]) for r in every if r["offer"] == "1"]
    L4 = [float(r["visits"]) for r in every if r["offer"] == "0"]
    put("ch3.hist2.bars", ", ".join(str(c) for c in histogram(L2, 0, 2, 18)))
    put("ch3.hist2.top", g(max(L2))); put("ch3.hist2.after18", str(sum(x >= 18 for x in L2)))
    zero = sum(x == 0 for x in L2)
    put("ch3.L2.zero", str(zero)); put("ch3.L2.zero.pct", pct(zero, len(L2)))
    s = ti(L2)
    put("ch3.L2.mean", f(s["mean"], 3)); put("ch3.L2.sx", f(s["sx"], 3)); put("ch3.L2.n", str(s["n"]))
    put("ch3.L2.five", ", ".join(g(s[k]) for k in ("min", "q1", "med", "q3", "max")))
    put("ch3.L2.sum", g(s["sum"])); put("ch3.L2.sum2", g(s["sum2"])); put("ch3.L2.sigma", f(s["sg"], 3))
    put("ch3.L2.mean_without_max", f((s["sum"] - s["max"]) / (s["n"] - 1), 3))
    iqr = s["q3"] - s["q1"]; lo, hi = s["q1"] - 1.5 * iqr, s["q3"] + 1.5 * iqr
    put("ch3.L2.iqr", g(iqr)); put("ch3.L2.fences", f"{g(lo)}, {g(hi)}")
    out = [x for x in L2 if x > hi]
    put("ch3.L2.outliers", str(len(out))); put("ch3.L2.outliers.range", f"{g(min(out))} to {g(max(out))}")
    put("ch3.L2.whisker", g(max(x for x in L2 if x <= hi)))
    two = s["mean"] + 2 * s["sx"]
    put("ch3.L2.two_sd", f(two, 2)); put("ch3.L2.two_sd.count", str(sum(x > two for x in L2)))
    put("ch3.L2.two_sd.from", g(min(x for x in L2 if x > two)))
    p1 = ti([x + 1 for x in L2])
    put("ch3.units.plus1.mean", f(p1["mean"], 3)); put("ch3.units.plus1.med", g(p1["med"]))
    put("ch3.units.plus1.quartiles", f"{g(p1['q1'])}, {g(p1['q3'])}"); put("ch3.units.plus1.sx", f(p1["sx"], 3))
    eg = [float(r["entry_grade"]) for r in every]
    e = ti(eg)
    put("ch3.entry.mean", f(e["mean"], 3)); put("ch3.entry.sx", f(e["sx"], 3))
    t25 = ti([25 * x for x in eg])
    put("ch3.units.times25.mean", f(t25["mean"], 2)); put("ch3.units.times25.sx", f(t25["sx"], 2))
    m25 = ti([x - 0.25 for x in eg])
    put("ch3.units.minus025.mean", f(m25["mean"], 3)); put("ch3.units.minus025.med", f(m25["med"], 2))
    put("ch3.units.minus025.sx", f(m25["sx"], 3)); put("ch3.units.minus025.iqr", f(m25["q3"] - m25["q1"], 2))
    put("ch3.entry.med", f(e["med"], 2)); put("ch3.entry.iqr", f(e["q3"] - e["q1"], 2))
    # joiners by college, worked by hand
    colleges = sorted({r["college"] for r in every})
    jc = [sum(r["college"] == c for r in every) for c in colleges]
    c = ti(jc)
    put("ch3.college.sorted", ", ".join(str(x) for x in sorted(jc)))
    stems = {}
    for x in sorted(jc):
        stems.setdefault(x // 10, []).append(str(x % 10))
    put("ch3.college.stems", "; ".join(f"{k} | {''.join(v)}" for k, v in sorted(stems.items())))
    put("ch3.college.mean", f(c["mean"], 2)); put("ch3.college.med", g(c["med"])); put("ch3.college.ss", f(c["ss"], 2))
    put("ch3.college.var", f(c["ss"] / (c["n"] - 1), 2)); put("ch3.college.sx", f(c["sx"], 2))
    put("ch3.college.quartiles", f"{g(c['q1'])}, {g(c['q3'])}"); put("ch3.college.range", g(c["max"] - c["min"]))
    low = min(zip(jc, colleges)); high = max(zip(jc, colleges))
    put("ch3.college.min", f"{low[0]} ({low[1]})"); put("ch3.college.max", f"{high[0]} ({high[1]})")
    ci = c["q3"] - c["q1"]
    put("ch3.college.fences", f"{f(c['q1'] - 1.5 * ci, 1)}, {f(c['q3'] + 1.5 * ci, 1)}")
    # relative position
    first = every[0]
    g12 = [float(r["grade_12"]) for r in every if r["grade_12"] != ""]
    gs = ti(g12)
    x1, x2 = float(first["entry_grade"]), float(first["grade_12"])
    put("ch3.z.student", first["student_id"]); put("ch3.z.entry", first["entry_grade"]); put("ch3.z.college", first["grade_12"])
    put("ch3.z.entry.z", f((x1 - e["mean"]) / e["sx"], 2)); put("ch3.z.entry.z_sigma", f((x1 - e["mean"]) / e["sg"], 2))
    put("ch3.z.entry.pctile", pct(sum(x <= x1 for x in eg), len(eg)))
    put("ch3.z.g12.n", f"{len(g12):,}"); put("ch3.z.g12.mean", f(gs["mean"], 3)); put("ch3.z.g12.sx", f(gs["sx"], 3))
    put("ch3.z.college.z", f((x2 - gs["mean"]) / gs["sx"], 2)); put("ch3.z.college.z_sigma", f((x2 - gs["mean"]) / gs["sg"], 2))
    put("ch3.z.college.pctile", pct(sum(x <= x2 for x in g12), len(g12)))
    put("ch3.z.try.2_50", f((2.50 - e["mean"]) / e["sx"], 2))
    # comparing the groups
    s4 = ti(L4)
    z4 = sum(x == 0 for x in L4)
    put("ch3.L4.zero", str(z4)); put("ch3.L4.zero.pct", pct(z4, len(L4)))
    put("ch3.L4.five", ", ".join(g(s4[k]) for k in ("min", "q1", "med", "q3", "max")))
    put("ch3.L4.mean", f(s4["mean"], 3)); put("ch3.L4.sx", f(s4["sx"], 3)); put("ch3.gap", f(s["mean"] - s4["mean"], 3))
    i4 = s4["q3"] - s4["q1"]
    put("ch3.L4.fences", f"{g(s4['q1'] - 1.5 * i4)}, {g(s4['q3'] + 1.5 * i4)}")
    put("ch3.L4.outliers", str(sum(x > s4["q3"] + 1.5 * i4 for x in L4)))
    two4 = s4["mean"] + 2 * s4["sx"]
    put("ch3.L4.two_sd", f(two4, 2)); put("ch3.L4.two_sd.count", str(sum(x > two4 for x in L4)))
    put("ch3.L2.eight_plus", str(sum(x >= 8 for x in L2))); put("ch3.L4.eight_plus", str(sum(x >= 8 for x in L4)))
    # back-to-back stemplot: withdrawal percent by college, among known outcomes
    for z, lab in (("1", "offered"), ("0", "not_offered")):
        pcts = []
        for col in colleges:
            k = [r for r in every if r["college"] == col and r["offer"] == z and r["withdrew"] in ("0", "1")]
            w = sum(r["withdrew"] == "1" for r in k)
            ratio = 100 * w / len(k)
            if abs(ratio - math.floor(ratio) - 0.5) < 1e-9:
                raise SystemExit(f"a tie at .5: {col} {lab}")
            pcts.append(round(ratio))
        put(f"ch3.b2b.{lab}", ", ".join(str(x) for x in sorted(pcts)))
        put(f"ch3.b2b.{lab}.median", g(median(pcts)))
    # review: fictional numbers worked as the book prints them
    mins = [5, 8, 12, 15, 15, 20, 25, 60]
    m = ti(mins)
    put("ch3.review.minutes.mean", f(m["mean"], 1)); put("ch3.review.minutes.med", g(m["med"])); put("ch3.review.minutes.sx", f(m["sx"], 2))
    put("ch3.review.minutes.quartiles", f"{g(m['q1'])}, {g(m['q3'])}")
    mi = m["q3"] - m["q1"]
    put("ch3.review.minutes.upper_fence", f(m["q3"] + 1.5 * mi, 2))
    w60 = ti(mins[:-1])
    put("ch3.review.minutes.without60.mean", f(w60["mean"], 2)); put("ch3.review.minutes.without60.sx", f(w60["sx"], 2))
    put("ch3.review.minutes.without60.med", g(w60["med"]))
    put("ch3.review.five.fences", f"{g(10 - 1.5 * 8)}, {g(18 + 1.5 * 8)}")
    put("ch3.review.scale.mean", f(2 * 38.6, 1)); put("ch3.review.scale.sd", f(2 * 5.2, 1))
    put("ch3.review.z.first", f((82 - 74) / 6, 2)); put("ch3.review.z.second", f((88 - 81) / 4, 2))


def chapter_4(every, invited):
    N = len(every)
    known = [r for r in every if r["withdrew"] in ("0", "1")]
    for z, lab in (("1", "withdrew"), ("0", "stayed_or_transferred")):
        v = [float(r["visits"]) for r in known if r["withdrew"] == z]
        put(f"ch4.visits.{lab}.mean", f(math.fsum(v) / len(v), 2))
    for z, lab in (("1", "part_time"), ("0", "full_time")):
        v = [float(r["visits"]) for r in every if r["part_time"] == z]
        put(f"ch4.visits.{lab}.mean", f(math.fsum(v) / len(v), 2))
        k = [r for r in known if r["part_time"] == z]
        w = sum(r["withdrew"] == "1" for r in k)
        put(f"ch4.{lab}.withdrew", str(w)); put(f"ch4.{lab}.known", str(len(k))); put(f"ch4.{lab}.withdrew.pct", pct(w, len(k)))
    put("ch4.consent_withdrawn", str(sum(r["exit"] == "consent withdrawn" for r in every)))
    pt = sum(r["part_time"] == "1" for r in every)
    put("ch4.part_time", str(pt)); put("ch4.full_time", str(N - pt))
    for n, key in ((30, "srs30"), (40, "try40"), (60, "review60")):
        share = n * pt / N
        put(f"ch4.{key}.part_time_exact", f(share, 2 if key == "review60" else 1))
        put(f"ch4.{key}.split", f"{round(share)} and {n - round(share)}")
    put("ch4.systematic.k", "40")
    sizes = sorted({len(range(start, N + 1, 40)) for start in range(1, 41)})
    put("ch4.systematic.sizes", " or ".join(str(x) for x in sizes))
    put("ch4.systematic.31_if_start_at_most", str(max(st for st in range(1, 41) if len(range(st, N + 1, 40)) == 31)))
    put("ch4.review.systematic.size", str(1200 // 25))
    notj = sum(r["joined"] == "0" for r in invited)
    put("ch4.not_joined", str(notj)); put("ch4.not_joined.pct", pct(notj, len(invited)))
    for z, lab in (("0", "full_time"), ("1", "part_time")):
        inv = [r for r in invited if r["part_time"] == z]
        j = sum(r["joined"] == "1" for r in inv)
        put(f"ch4.invited.{lab}", str(len(inv))); put(f"ch4.invited.{lab}.joined", str(j)); put(f"ch4.invited.{lab}.joined.pct", pct(j, len(inv)))
    put("ch4.part_time.share_invited.pct", pct(sum(r["part_time"] == "1" for r in invited), len(invited), 0))
    put("ch4.part_time.share_joined.pct", pct(pt, N))
    colleges = sorted({r["college"] for r in every})
    shares = [100 * sum(r["college"] == c and r["offer"] == "1" for r in every) / sum(r["college"] == c for r in every) for c in colleges]
    put("ch4.blocks.offered.range", f"{min(shares):.1f} to {max(shares):.1f}")
    for z, lab in (("1", "offered"), ("0", "not_offered")):
        grp = [r for r in every if r["offer"] == z]
        p = sum(r["part_time"] == "1" for r in grp)
        put(f"ch4.balance.{lab}.part_time", str(p)); put(f"ch4.balance.{lab}.part_time.pct", pct(p, len(grp)))
    a = 100 * sum(r["offer"] == "1" and r["part_time"] == "1" for r in every) / sum(r["offer"] == "1" for r in every)
    b = 100 * sum(r["offer"] == "0" and r["part_time"] == "1" for r in every) / sum(r["offer"] == "0" for r in every)
    put("ch4.balance.gap_points", f(a - b, 1))


def samples(every):
    ids = {r["student_id"]: r for r in every}
    for n, rule in (("100", "known outcome"), ("120", "known outcome"), ("20", "college grade")):
        path = ROOT / "samples" / f"tonmick-sample-{n}.csv"
        s = rows(f"samples/tonmick-sample-{n}.csv")
        put(f"samples.{n}.size", str(len(s)))
        put(f"samples.{n}.distinct", str(len({r['student_id'] for r in s})))
        ok = all(r["student_id"] in ids and all(r[k] == ids[r["student_id"]][k] for k in ids[r["student_id"]]) for r in s)
        ok = ok and all((r["withdrew"] in ("0", "1")) if rule == "known outcome" else (r["grade_12"] != "") for r in s)
        ok = ok and [r["draw"] for r in s] == [str(i) for i in range(1, len(s) + 1)]
        put(f"samples.{n}.rows_match_population", "yes" if ok else "no")
        put(f"samples.{n}.md5", hashlib.md5(path.read_bytes()).hexdigest())
        put(f"samples.{n}.withdrew", str(sum(r["withdrew"] == "1" for r in s)))
        put(f"samples.{n}.part_time", str(sum(r["part_time"] == "1" for r in s)))
        put(f"samples.{n}.offered", str(sum(r["offer"] == "1" for r in s)))
        eg = [float(r["entry_grade"]) for r in s]
        put(f"samples.{n}.entry.mean", f(math.fsum(eg) / len(eg), 3))
        if n == "20":
            g12 = [float(r["grade_12"]) for r in s]
            put("samples.20.g12.mean", f(math.fsum(g12) / len(g12), 3))
    known = [r for r in every if r["withdrew"] in ("0", "1")]
    put("samples.population.known", f"{len(known):,}")
    put("samples.population.withdrew.share", f(sum(r["withdrew"] == "1" for r in known) / len(known), 4))
    g = [r for r in every if r["grade_12"] != ""]
    put("samples.population.college_grade", f"{len(g):,}")
    put("samples.population.college_grade.entry.mean", f(math.fsum(float(r["entry_grade"]) for r in g) / len(g), 3))
    put("samples.population.college_grade.g12.mean", f(math.fsum(float(r["grade_12"]) for r in g) / len(g), 3))


def main():
    every = rows("data/tonmick-classroom.csv")
    invited = rows("data/tonmick-invited.csv")
    chapter_1(); chapter_2(every, invited); chapter_3(every); chapter_4(every, invited); samples(every)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["name", "value"])
        for k in sorted(V):
            w.writerow([k, V[k]])


if __name__ == "__main__":
    main()
