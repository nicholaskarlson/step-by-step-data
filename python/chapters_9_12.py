#!/usr/bin/env python3
"""Route 1 for Chapters 9 to 12: every number the chapters, their Try It answers, their
reviews, and the eight investigations print, rebuilt from the data files and the fixed
samples of 20, 100, and 120 with standard-library Python.

    python -I python/chapters_9_12.py ROOT OUT.csv

Each value is written as the book prints it (name,value), so run_all.py can compare the
routes and expected/chapters_9_12.csv character for character. Conventions, as in Chapters 1
to 8:

- Arithmetic the text shows on the home screen starts from the numbers the book prints, so a
  reader who types them gets the same digits. Values a calculator command computes from the
  data or the counts (chi-square tests, TInterval, LinReg) start from the data.
- Lists a reader types in (the sixteen colleges' counts, the sample of 20, Section 11.5's
  groups) are used as printed.
- Quartiles are the TI-84's: the medians of the lower and upper halves, the median left out
  when the count is odd.

The t and chi-square distributions are not in Python's standard library, so this route works
them out from the regularized incomplete beta and gamma functions (continued fractions and
series), and inverts them by bisection. Route 2 uses base R's pt, qt, pchisq, and qchisq.

The outline that says where each value appears is outline/chapters-9-12.md.
"""
import csv
import math
import sys
from collections import Counter
from pathlib import Path
from statistics import NormalDist

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
N01 = NormalDist()
Z95 = N01.inv_cdf(0.975)
V = {}


def put(name, value):
    if name in V:
        raise SystemExit(f"duplicate name {name}")
    V[name] = str(value)


def f(x, places):
    s = f"{x:.{places}f}"
    return "0." + "0" * places if s == "-0." + "0" * places else s


def pct(num, den, places=1):
    return f(100 * num / den, places)


def big(n):
    return f"{n:,}"


def join(xs):
    return ", ".join(xs)


def rows(path):
    with open(ROOT / path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# ---- distributions ----

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
    """The regularized incomplete beta function I_x(a, b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lb = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log1p(-x)
    if x < (a + 1) / (a + b + 2):
        return math.exp(lb) * betacf(a, b, x) / a
    return 1.0 - math.exp(lb) * betacf(b, a, 1.0 - x) / b


def t_upper(t, df):
    """P(T > t) for t >= 0."""
    return 0.5 * ibeta(df / 2, 0.5, df / (df + t * t))


def t_two(t, df):
    return 2 * t_upper(abs(t), df)


def gamma_q(a, x):
    """The regularized upper incomplete gamma function Q(a, x)."""
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


def chi2_upper(x, df):
    return gamma_q(df / 2, x / 2)


def invert(fn, target, lo, hi):
    """The x in [lo, hi] where the decreasing function fn equals target, by bisection."""
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
    while chi2_upper(hi, df) > tail:
        hi *= 2
    return invert(lambda x: chi2_upper(x, df), tail, 0.0, hi)


# ---- summaries ----

def mean(x):
    return math.fsum(x) / len(x)


def sd(x):
    m = mean(x)
    return math.sqrt(math.fsum((a - m) ** 2 for a in x) / (len(x) - 1))


def median(x):
    s = sorted(x)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def five(x):
    """min, Q1, median, Q3, max, as 1-Var Stats gives them."""
    s = sorted(x)
    n = len(s)
    lower, upper = s[: n // 2], s[(n + 1) // 2:]
    return s[0], median(lower), median(s), median(upper), s[-1]


def g(x):
    """A number as the calculator shows it: up to three decimals, no trailing zeros."""
    s = f"{x:.3f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def g4(x):
    """A fence, which can end in a fifth of a hundredth: up to four decimals, no trailing zeros."""
    s = f"{x:.4f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def chisq_table(obs):
    """Expected counts, each cell's part, the statistic, and the degrees of freedom."""
    rt = [sum(r) for r in obs]
    ct = [sum(c) for c in zip(*obs)]
    tot = sum(rt)
    exp = [[rt[i] * ct[j] / tot for j in range(len(ct))] for i in range(len(rt))]
    part = [[(obs[i][j] - exp[i][j]) ** 2 / exp[i][j] for j in range(len(ct))] for i in range(len(rt))]
    stat = math.fsum(math.fsum(r) for r in part)
    return exp, part, stat, (len(rt) - 1) * (len(ct) - 1)


def linreg(x, y):
    mx, my = mean(x), mean(y)
    sxx = math.fsum((a - mx) ** 2 for a in x)
    sxy = math.fsum((a - mx) * (b - my) for a, b in zip(x, y))
    syy = math.fsum((b - my) ** 2 for b in y)
    b = sxy / sxx
    a = my - b * mx
    r = sxy / math.sqrt(sxx * syy)
    res = [yy - (a + b * xx) for xx, yy in zip(x, y)]
    s = math.sqrt(math.fsum(e * e for e in res) / (len(x) - 2))
    return {"a": a, "b": b, "r": r, "res": res, "s": s, "se_b": s / math.sqrt(sxx)}


def welch(m1, s1, n1, m2, s2, n2):
    v1, v2 = s1 * s1 / n1, s2 * s2 / n2
    se = math.sqrt(v1 + v2)
    df = (v1 + v2) ** 2 / (v1 * v1 / (n1 - 1) + v2 * v2 / (n2 - 1))
    t = (m1 - m2) / se
    return t, df, se


def sci(p):
    """A small p value as 3.75 × 10⁻⁶: the mantissa and the exponent."""
    e = math.floor(math.log10(p))
    m = p / 10 ** e
    if f"{m:.2f}" == "10.00":
        m, e = m / 10, e + 1
    return f"{m:.2f}", str(e)


def hyper_pmf(pop, good, n):
    return [math.comb(good, k) * math.comb(pop - good, n - k) / math.comb(pop, n) for k in range(0, n + 1)]


# ---- Chapter 9 ----

def chapter_9(every, invited, s100, s120):
    known = [r for r in every if r["withdrew"] in ("0", "1")]
    # 9.1 goodness of fit: joiners per college, against equal shares
    joined = Counter(r["college"] for r in invited if r["joined"] == "1")
    cols = sorted(joined)
    obs = [joined[c] for c in cols]
    tot = sum(obs)
    put("ch9.gof.colleges", join(cols)); put("ch9.gof.counts", join(str(o) for o in obs))
    put("ch9.gof.k", len(cols)); put("ch9.gof.df", len(cols) - 1)
    e = tot / len(cols)
    put("ch9.gof.expected", f(e, 2)); put("ch9.gof.expected.screen", f(e, 4))
    ep = float(f(e, 2))
    lo, hi = min(obs), max(obs)
    put("ch9.gof.low.part", f((lo - ep) ** 2 / ep, 2)); put("ch9.gof.high.part", f((hi - ep) ** 2 / ep, 2))
    stat = math.fsum((o - e) ** 2 / e for o in obs)
    p = chi2_upper(stat, len(cols) - 1)
    put("ch9.gof.chi2", f(stat, 2)); put("ch9.gof.chi2.screen", f(stat, 4))
    put("ch9.gof.p", f(p, 4)); put("ch9.gof.p.pct", f(100 * p, 1))
    put("ch9.gof.crit", f(chi2_star(0.05, len(cols) - 1), 3))
    # Try it: part-time joiners against the invited mix of 40% part-time
    pt = sum(r["part_time"] == "1" for r in every)
    share = sum(r["part_time"] == "1" for r in invited) / len(invited)
    e1, e2 = len(every) * share, len(every) * (1 - share)
    st = (pt - e1) ** 2 / e1 + (len(every) - pt - e2) ** 2 / e2
    put("ch9.gof.try.expected.part", f(e1, 1)); put("ch9.gof.try.expected.full", f(e2, 1))
    put("ch9.gof.try.chi2", f(st, 2)); put("ch9.gof.try.p", f(chi2_upper(st, 1), 4))
    # 9.2 homogeneity: how the year ended, by offer, among the 1,208 known outcomes
    ends = ["stayed", "withdrew", "transferred"]
    grp = {"offered": [r for r in known if r["offer"] == "1"], "not_offered": [r for r in known if r["offer"] == "0"]}
    tab = [[sum(r["exit"] == x for r in grp[k]) for x in ends] for k in ("offered", "not_offered")]
    exp, part, stat, df = chisq_table(tab)
    for i, k in enumerate(("offered", "not_offered")):
        put(f"ch9.hom.{k}.counts", join(str(c) for c in tab[i]))
        put(f"ch9.hom.{k}.pct", join(pct(c, sum(tab[i])) for c in tab[i]))
        put(f"ch9.hom.{k}.expected", join(f(x, 2) for x in exp[i]))
        put(f"ch9.hom.{k}.parts", join(f(x, 2) for x in part[i]))
    col = [sum(c) for c in zip(*tab)]
    put("ch9.hom.totals", join(str(c) for c in col)); put("ch9.hom.totals.pct", join(pct(c, len(known)) for c in col))
    put("ch9.hom.expected.min", f(min(min(r) for r in exp), 2))
    put("ch9.hom.chi2", f(stat, 2)); put("ch9.hom.chi2.screen", f(stat, 4)); put("ch9.hom.df", df)
    p = chi2_upper(stat, df)
    put("ch9.hom.p", f(p, 4))
    put("ch9.hom.crit", f(chi2_star(0.05, df), 3))
    # collapsed to withdrew or not: chi-square is z squared
    two = [[r[1], r[0] + r[2]] for r in tab]
    _, _, s2, _ = chisq_table(two)
    x1, n1, x2, n2 = two[0][0], sum(two[0]), two[1][0], sum(two[1])
    pp = (x1 + x2) / (n1 + n2)
    z = (x1 / n1 - x2 / n2) / math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
    put("ch9.hom.two.chi2", f(s2, 2)); put("ch9.hom.two.z", f(z, 4)); put("ch9.hom.two.p", f(chi2_upper(s2, 1), 4))
    # 9.3 independence: the sample of 120, part-time study by withdrawal
    cells = [[sum(r["part_time"] == a and r["withdrew"] == b for r in s120) for b in ("1", "0")] for a in ("0", "1")]
    exp, part, stat, df = chisq_table(cells)
    for i, k in enumerate(("full", "part")):
        put(f"ch9.ind.{k}.counts", join(str(c) for c in cells[i])); put(f"ch9.ind.{k}.n", sum(cells[i]))
        put(f"ch9.ind.{k}.withdrew.pct", pct(cells[i][0], sum(cells[i])))
        put(f"ch9.ind.{k}.expected", join(f(x, 2) for x in exp[i]))
    put("ch9.ind.withdrew", cells[0][0] + cells[1][0]); put("ch9.ind.stayed", cells[0][1] + cells[1][1])
    put("ch9.ind.expected.min", f(min(min(r) for r in exp), 2))
    put("ch9.ind.chi2", f(stat, 2)); put("ch9.ind.chi2.screen", f(stat, 4)); put("ch9.ind.df", df)
    p = chi2_upper(stat, df)
    put("ch9.ind.p", f(p, 4))
    # the population the sample came from, all 1,208
    pc = [[sum(r["part_time"] == a and r["withdrew"] == b for r in known) for b in ("1", "0")] for a in ("0", "1")]
    for i, k in enumerate(("full", "part")):
        put(f"ch9.ind.pop.{k}.withdrew.pct", pct(pc[i][0], sum(pc[i])))
    # two contrasts: the offer against part-time study (all 1,219), and joining against it (1,600)
    bal = [[sum(r["offer"] == a and r["part_time"] == b for r in every) for b in ("1", "0")] for a in ("1", "0")]
    _, _, sb, _ = chisq_table(bal)
    put("ch9.ind.balance.chi2", f(sb, 2)); put("ch9.ind.balance.p", f(chi2_upper(sb, 1), 4))
    jt = [[sum(r["part_time"] == a and r["joined"] == b for r in invited) for b in ("1", "0")] for a in ("0", "1")]
    exp, _, sj, _ = chisq_table(jt)
    put("ch9.ind.join.counts", "; ".join(join(str(c) for c in r) for r in jt))
    put("ch9.ind.join.expected", "; ".join(join(f(x, 1) for x in r) for r in exp))
    put("ch9.ind.join.expected.min", f(min(min(r) for r in exp), 1))
    put("ch9.ind.join.chi2", f(sj, 2))
    pj = chi2_upper(sj, 1)
    m, ex = sci(pj)
    put("ch9.ind.join.p.mantissa", m); put("ch9.ind.join.p.exponent", ex)
    x1, n1, x2, n2 = jt[0][0], sum(jt[0]), jt[1][0], sum(jt[1])
    pp = (x1 + x2) / (n1 + n2)
    zj = (x1 / n1 - x2 / n2) / math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
    put("ch9.ind.join.z", f(zj, 4)); put("ch9.ind.join.z2", f(float(f(zj, 4)) ** 2, 2))
    # Chapter 9 review
    spin = [25, 18, 22, 15]
    es = sum(spin) / 4
    ss = math.fsum((o - es) ** 2 / es for o in spin)
    put("ch9.review.spin.expected", f(es, 0)); put("ch9.review.spin.chi2", f(ss, 2)); put("ch9.review.spin.p", f(chi2_upper(ss, 3), 4))
    put("ch9.review.spin.wrong_n", f(math.fsum((o - es) ** 2 / sum(spin) for o in spin), 3))
    c100 = [[sum(r["offer"] == a and r["withdrew"] == b for r in s100) for b in ("1", "0")] for a in ("1", "0")]
    exp, _, s1, _ = chisq_table(c100)
    put("ch9.review.s100.offered", join(str(c) for c in c100[0])); put("ch9.review.s100.not_offered", join(str(c) for c in c100[1]))
    put("ch9.review.s100.offered.n", sum(c100[0])); put("ch9.review.s100.not_offered.n", sum(c100[1]))
    put("ch9.review.s100.expected", "; ".join(join(f(x, 2) for x in r) for r in exp))
    put("ch9.review.s100.expected.min", f(min(min(r) for r in exp), 2))
    put("ch9.review.s100.chi2", f(s1, 2)); put("ch9.review.s100.p", f(chi2_upper(s1, 1), 4))
    jobs = [[54, 39, 63], [150 - 54, 150 - 39, 150 - 63]]
    exp, _, sw, df = chisq_table(jobs)
    put("ch9.review.jobs.expected", "; ".join(join(f(x, 2) for x in r) for r in exp))
    put("ch9.review.jobs.chi2", f(sw, 2)); put("ch9.review.jobs.df", df); put("ch9.review.jobs.p", f(chi2_upper(sw, df), 4))
    put("ch9.review.jobs.pct", join(pct(x, 150) for x in jobs[0]))


# ---- Chapter 10 ----

def chapter_10(every, s20):
    ts19 = t_star(0.025, 19)
    put("ch10.tstar.19", f(ts19, 3)); put("ch10.tstar.608", f(t_star(0.025, 608), 3))
    put("ch10.tstar.9", f(t_star(0.025, 9), 3))
    put("ch10.tstar.19.screen", f(ts19, 4))
    # 10.2 the sample of 20: school grades
    sch_s = [r["entry_grade"] for r in s20]
    col_s = [r["grade_12"] for r in s20]
    sch = [float(x) for x in sch_s]
    col = [float(x) for x in col_s]
    n = len(sch)
    put("ch10.s20.school", join(sch_s)); put("ch10.s20.college", join(col_s))
    m, s = mean(sch), sd(sch)
    se = s / math.sqrt(n)
    put("ch10.s20.school.mean", f(m, 3)); put("ch10.s20.school.sx", f(s, 3)); put("ch10.s20.school.sx.screen", f(s, 5))
    put("ch10.s20.school.se", f(se, 4)); put("ch10.s20.school.se5", f(se, 5))
    me = ts19 * se
    put("ch10.s20.school.me", f(me, 3))
    put("ch10.s20.school.se.hand", f(float(f(s, 5)) / math.sqrt(n), 4))
    put("ch10.s20.school.me.hand", f(float(f(ts19, 3)) * float(f(se, 4)), 3))
    put("ch10.s20.school.low", f(m - me, 3)); put("ch10.s20.school.high", f(m + me, 3))
    put("ch10.s20.school.low.screen", f(m - me, 4)); put("ch10.s20.school.high.screen", f(m + me, 4))
    pop = [r for r in every if r["grade_12"] != ""]
    put("ch10.pop.ten_pct", f(len(pop) / 10, 1))
    fv = five(sch)
    put("ch10.s20.school.five", join(g(x) for x in fv))
    iqr = fv[3] - fv[1]
    put("ch10.s20.school.fences", join(g4(x) for x in (fv[1] - 1.5 * iqr, fv[3] + 1.5 * iqr)))
    put("ch10.s20.school.outliers", sum(x < fv[1] - 1.5 * iqr or x > fv[3] + 1.5 * iqr for x in sch))
    vis = [int(r["visits"]) for r in s20]
    put("ch10.s20.visits", join(str(v) for v in vis))
    fv = five(vis)
    put("ch10.s20.visits.five", join(g(x) for x in fv))
    iqr = fv[3] - fv[1]
    put("ch10.s20.visits.fence", g4(fv[3] + 1.5 * iqr))
    put("ch10.s20.visits.outliers", sum(v > fv[3] + 1.5 * iqr for v in vis))
    # 10.3 a test for a mean: a planner's figure of 2.90
    mu0 = 2.90
    t = (m - mu0) / se
    put("ch10.test.mu0", "2.90"); put("ch10.test.t", f(t, 2)); put("ch10.test.t.screen", f(t, 4))
    put("ch10.test.p", f(t_two(t, 19), 4)); put("ch10.test.p.one", f(t_upper(t, 19), 4))
    put("ch10.test.diff", f(float(f(m, 3)) - mu0, 3))
    put("ch10.test.t.hand", f((float(f(m, 3)) - mu0) / float(f(se, 4)), 2))
    # 10.4 paired data: college grade minus school grade, in hundredths so the differences are exact
    dh = [round(100 * c) - round(100 * s_) for s_, c in zip(sch, col)]
    d = [x / 100 for x in dh]
    put("ch10.pair.d", join(f(x, 2) for x in d))
    md, sdd = mean(d), sd(d)
    sed = sdd / math.sqrt(n)
    put("ch10.pair.mean", f(md, 3)); put("ch10.pair.sd", f(sdd, 3)); put("ch10.pair.se", f(sed, 4))
    tp = md / sed
    put("ch10.pair.t", f(tp, 2)); put("ch10.pair.p", f(t_two(tp, 19), 4))
    put("ch10.pair.me", f(ts19 * sed, 3))
    put("ch10.pair.sd4", f(sdd, 4)); put("ch10.pair.se.hand", f(float(f(sdd, 4)) / math.sqrt(n), 4))
    put("ch10.pair.t.hand", f(float(f(md, 3)) / float(f(sed, 4)), 2))
    put("ch10.pair.me.hand", f(float(f(ts19, 3)) * float(f(sed, 4)), 3))
    put("ch10.pair.low", f(md - ts19 * sed, 3)); put("ch10.pair.high", f(md + ts19 * sed, 3))
    fv = five(d)
    put("ch10.pair.five", join(g(x) for x in fv))
    iqr = fv[3] - fv[1]
    put("ch10.pair.fences", join(g4(x) for x in (fv[1] - 1.5 * iqr, fv[3] + 1.5 * iqr)))
    put("ch10.pair.outliers", sum(x < fv[1] - 1.5 * iqr or x > fv[3] + 1.5 * iqr for x in d))
    put("ch10.pair.positive", sum(x > 0 for x in d))
    # the wrong analysis: a two-sample t test on the two lists
    tw, dfw, sew = welch(mean(col), sd(col), n, m, s, n)
    put("ch10.pair.wrong.se", f(sew, 4)); put("ch10.pair.wrong.t", f(tw, 2)); put("ch10.pair.wrong.p", f(t_two(tw, dfw), 4))
    # every student not offered who has both grades, and all 1,116
    no = [r for r in pop if r["offer"] == "0"]
    dn = [(round(100 * float(r["grade_12"])) - round(100 * float(r["entry_grade"]))) / 100 for r in no]
    put("ch10.pair.not_offered.n", len(no)); put("ch10.pair.not_offered.mean", f(mean(dn), 3)); put("ch10.pair.not_offered.sd", f(sd(dn), 3))
    da = [(round(100 * float(r["grade_12"])) - round(100 * float(r["entry_grade"]))) / 100 for r in pop]
    put("ch10.pair.all.mean", f(mean(da), 3))
    # 10.5 comparing two means: visits, offered minus not offered
    v1 = [int(r["visits"]) for r in every if r["offer"] == "1"]
    v2 = [int(r["visits"]) for r in every if r["offer"] == "0"]
    t2, df2, se2 = welch(mean(v1), sd(v1), len(v1), mean(v2), sd(v2), len(v2))
    diff = mean(v1) - mean(v2)
    ts = t_star(0.025, df2)
    put("ch10.two.diff4", f(diff, 4)); put("ch10.two.tstar", f(ts, 3))
    put("ch10.two.me", f(ts * se2, 3))
    put("ch10.two.low", f(diff - ts * se2, 3)); put("ch10.two.high", f(diff + ts * se2, 3))
    put("ch10.two.df.small", len(v1) - 1 if len(v1) < len(v2) else len(v2) - 1); put("ch10.two.df.sum", big(len(v1) + len(v2) - 2))
    ts608 = t_star(0.025, min(len(v1), len(v2)) - 1)
    put("ch10.two.hand.me", f(float(f(ts608, 3)) * float(f(se2, 4)), 3))
    put("ch10.two.hand.low", f(diff - ts608 * se2, 3)); put("ch10.two.hand.high", f(diff + ts608 * se2, 3))
    put("ch10.two.hand.p", f(t_two(t2, min(len(v1), len(v2)) - 1), 4))
    sp = math.sqrt(((len(v1) - 1) * sd(v1) ** 2 + (len(v2) - 1) * sd(v2) ** 2) / (len(v1) + len(v2) - 2))
    tpool = diff / (sp * math.sqrt(1 / len(v1) + 1 / len(v2)))
    put("ch10.two.pooled.t", f(tpool, 2)); put("ch10.two.pooled.p", f(t_two(tpool, len(v1) + len(v2) - 2), 4))
    put("ch10.two.per100", f(100 * diff, 0)); put("ch10.two.per100.low", f(100 * (diff - ts * se2), 1))
    put("ch10.two.per100.high", f(100 * (diff + ts * se2), 1))
    # the summary for Stats input, as the calculator shows it
    put("ch10.two.offered.summary", join((f(mean(v1), 6), f(sd(v1), 6))))
    put("ch10.two.not_offered.summary", join((f(mean(v2), 6), f(sd(v2), 6))))
    # visits vary more than a count model allows: variance against mean, from the printed SDs and means
    for lab, v in (("offered", v1), ("not_offered", v2)):
        sdp, mp = float(f(sd(v), 3)), float(f(mean(v), 2))
        put(f"ch10.two.{lab}.var", f(sdp ** 2, 2)); put(f"ch10.two.{lab}.mean2", f(mp, 2))
        put(f"ch10.two.{lab}.ratio", f(float(f(sdp ** 2, 2)) / mp, 1))
    # Chapter 10 review
    put("ch10.review.tstar.11", f(t_star(0.025, 11), 3)); put("ch10.review.tstar.12", f(t_star(0.025, 12), 3))
    put("ch10.review.tstar90.11", f(t_star(0.05, 11), 3))
    ts15 = t_star(0.025, 15)
    se16 = 6.4 / math.sqrt(16)
    put("ch10.review.ci.se", f(se16, 1)); put("ch10.review.ci.tstar", f(ts15, 3))
    put("ch10.review.ci.me", f(float(f(ts15, 3)) * se16, 2))
    put("ch10.review.ci", join((f(52.3 - ts15 * se16, 2), f(52.3 + ts15 * se16, 2))))
    put("ch10.review.ci.z", join((f(52.3 - Z95 * se16, 2), f(52.3 + Z95 * se16, 2))))
    t16 = t_star(0.025, 16)
    put("ch10.review.ci.df16", join((f(52.3 - t16 * se16, 2), f(52.3 + t16 * se16, 2))))
    put("ch10.review.ci.sd", join((f(52.3 - ts15 * 6.4, 2), f(52.3 + ts15 * 6.4, 2))))
    mc, sc = mean(col), sd(col)
    sec = sc / math.sqrt(n)
    put("ch10.review.college.mean", f(mc, 3)); put("ch10.review.college.sx", f(sc, 3)); put("ch10.review.college.se", f(sec, 4))
    put("ch10.review.college.me", f(ts19 * sec, 3))
    put("ch10.review.college.se.hand", f(float(f(sc, 3)) / math.sqrt(n), 4))
    put("ch10.review.college.me.hand", f(float(f(ts19, 3)) * float(f(sec, 4)), 3))
    put("ch10.review.college.low", f(mc - ts19 * sec, 3)); put("ch10.review.college.high", f(mc + ts19 * sec, 3))
    fv = five(col)
    put("ch10.review.college.five", join(g(x) for x in fv))
    iqr = fv[3] - fv[1]
    put("ch10.review.college.fences", join(g4(x) for x in (fv[1] - 1.5 * iqr, fv[3] + 1.5 * iqr)))
    put("ch10.review.college.outliers", sum(x < fv[1] - 1.5 * iqr or x > fv[3] + 1.5 * iqr for x in col))
    put("ch10.review.college.true", f(mean([float(r["grade_12"]) for r in pop]), 3))
    tq, dfq, seq = welch(78.4, 8.2, 35, 74.1, 9.5, 32)
    put("ch10.review.methods.diff", f(78.4 - 74.1, 1)); put("ch10.review.methods.se", f(seq, 4))
    put("ch10.review.methods.t.hand", f(4.3 / float(f(seq, 4)), 2))
    put("ch10.review.methods.t", f(tq, 2)); put("ch10.review.methods.df", f(dfq, 2)); put("ch10.review.methods.p", f(t_two(tq, dfq), 4))
    tsq = t_star(0.025, dfq)
    put("ch10.review.methods.low", f(4.3 - tsq * seq, 2)); put("ch10.review.methods.high", f(4.3 + tsq * seq, 2))


# ---- Chapter 11 ----

def chapter_11(every):
    no = [r for r in every if r["offer"] == "0" and r["grade_12"] != ""]
    x = [float(r["entry_grade"]) for r in no]
    y = [float(r["grade_12"]) for r in no]
    L = linreg(x, y)
    a, b, r = L["a"], L["b"], L["r"]
    put("ch11.n", len(x)); put("ch11.a", f(a, 3)); put("ch11.b", f(b, 3)); put("ch11.r", f(r, 3)); put("ch11.r2", f(r * r, 3))
    put("ch11.r4", f(r, 4)); put("ch11.r2.pct", f(100 * r * r, 0)); put("ch11.unexplained.pct", f(100 - 100 * r * r, 0))
    put("ch11.sx", f(sd(x), 4)); put("ch11.sy", f(sd(y), 4)); put("ch11.xbar", f(mean(x), 3)); put("ch11.ybar", f(mean(y), 3))
    put("ch11.slope.hand", f(float(f(r, 4)) * float(f(sd(y), 4)) / float(f(sd(x), 4)), 3))
    ar, br = float(f(a, 3)), float(f(b, 3))
    put("ch11.through", f(ar + br * float(f(mean(x), 3)), 3))
    put("ch11.ceiling.school", sum(v == 4.0 for v in x)); put("ch11.ceiling.college", sum(v == 4.0 for v in y))
    put("ch11.range", join((g(min(x)), g(max(x)))))
    # Try it 11.2: a school grade of 3.0
    put("ch11.try.hand", f(ar + br * 3.0, 3)); put("ch11.try.y1", f(a + b * 3.0, 3))
    # 11.3 residuals: the first student in the file
    first = no[0]
    xf, yf = float(first["entry_grade"]), float(first["grade_12"])
    put("ch11.student", first["student_id"]); put("ch11.student.x", first["entry_grade"]); put("ch11.student.y", first["grade_12"])
    put("ch11.student.pred", f(a + b * xf, 3)); put("ch11.student.pred.hand", f(ar + br * xf, 3))
    put("ch11.student.res", f(yf - (a + b * xf), 3))
    put("ch11.s", f(L["s"], 3))
    put("ch11.try.res.sds", f(-0.9 / float(f(L["s"], 3)), 2))
    put("ch11.try.res.below", sum(e <= -0.9 for e in L["res"])); put("ch11.res.min", f(min(L["res"]), 3))
    put("ch11.res.max", f(max(L["res"]), 3))
    # 11.4 prediction and its limits
    put("ch11.pred.1", f(a + b * 1.0, 3)); put("ch11.pred.1.hand", f(ar + br * 1.0, 3))
    off = [r for r in every if r["offer"] == "1" and r["grade_12"] != ""]
    Lo = linreg([float(r["entry_grade"]) for r in off], [float(r["grade_12"]) for r in off])
    put("ch11.offered.n", len(off)); put("ch11.offered.a", f(Lo["a"], 3)); put("ch11.offered.b", f(Lo["b"], 3)); put("ch11.offered.r", f(Lo["r"], 3))
    # who has no college grade, among the 610 not offered
    nog = [r for r in every if r["offer"] == "0" and r["grade_12"] == ""]
    put("ch11.nograde", len(nog))
    for e in ("withdrew", "transferred", "consent withdrawn"):
        put(f"ch11.nograde.{e.split()[0]}", sum(r["exit"] == e for r in nog))
        put(f"ch11.left.{e.split()[0]}", sum(r["exit"] == e for r in no))
    # regression to the mean, in two groups
    hi = [(a_, b_) for a_, b_ in zip(x, y) if a_ >= 3.5]
    lo = [(a_, b_) for a_, b_ in zip(x, y) if a_ < 2.5]
    for lab, grp in (("high", hi), ("low", lo)):
        put(f"ch11.rtm.{lab}.n", len(grp))
        put(f"ch11.rtm.{lab}.school", f(mean([p[0] for p in grp]), 3)); put(f"ch11.rtm.{lab}.college", f(mean([p[1] for p in grp]), 3))
    # 11.5 departures from linearity: withdrawal share by school grade, among the 1,208 known
    known = [r for r in every if r["withdrew"] in ("0", "1")]
    cuts = [225, 250, 275, 300, 325, 350]
    bands = [[] for _ in range(len(cuts) + 1)]
    for r_ in known:
        gh = round(100 * float(r_["entry_grade"]))
        bands[sum(gh >= c for c in cuts)].append(r_)
    gm, sh, ns, ws = [], [], [], []
    for bnd in bands:
        w = sum(r_["withdrew"] == "1" for r_ in bnd)
        ns.append(str(len(bnd))); ws.append(str(w))
        gm.append(f(mean([float(r_["entry_grade"]) for r_ in bnd]), 3)); sh.append(f(w / len(bnd), 3))
    put("ch11.bands.n", join(ns)); put("ch11.bands.withdrew", join(ws)); put("ch11.bands.k", len(bands))
    put("ch11.bands.grade", join(gm)); put("ch11.bands.share", join(sh))
    put("ch11.bands.pct", join(f(100 * float(s_), 1) for s_ in sh))
    gx, sy = [float(v) for v in gm], [float(v) for v in sh]
    L1 = linreg(gx, sy)
    put("ch11.bands.lin.a", f(L1["a"], 3)); put("ch11.bands.lin.b", f(L1["b"], 3)); put("ch11.bands.lin.r", f(L1["r"], 3))
    put("ch11.bands.lin.r2", f(L1["r"] ** 2, 3)); put("ch11.bands.lin.res", join(f(e, 3) for e in L1["res"]))
    put("ch11.bands.lin.signs", join("+" if e > 0 else "-" for e in L1["res"]))
    ly = [math.log(v) for v in sy]
    put("ch11.bands.ln", join(f(v, 3) for v in ly))
    L2 = linreg(gx, ly)
    put("ch11.bands.log.a", f(L2["a"], 3)); put("ch11.bands.log.b", f(L2["b"], 3)); put("ch11.bands.log.r", f(L2["r"], 3))
    put("ch11.bands.log.r2", f(L2["r"] ** 2, 3)); put("ch11.bands.log.res", join(f(e, 3) for e in L2["res"]))
    put("ch11.bands.log.at3", f(math.exp(L2["a"] + L2["b"] * 3.0), 3))
    put("ch11.bands.log.ratio", f(math.exp(L2["b"] * 0.5), 2))
    # 11.6 inference for a slope
    df = len(x) - 2
    ts = t_star(0.025, df)
    put("ch11.b4", f(b, 4)); put("ch11.se_b5", f(L["se_b"], 5))
    put("ch11.t.hand", f(float(f(b, 4)) / float(f(L["se_b"], 5)), 2))
    put("ch11.slope1.hand", f((float(f(b, 4)) - 1) / float(f(L["se_b"], 5)), 2))
    put("ch11.df", df); put("ch11.se_b", f(L["se_b"], 4)); put("ch11.t", f(b / L["se_b"], 2)); put("ch11.tstar", f(ts, 3))
    put("ch11.slope.low", f(b - ts * L["se_b"], 3)); put("ch11.slope.high", f(b + ts * L["se_b"], 3))
    put("ch11.slope.me", f(float(f(ts, 3)) * float(f(L["se_b"], 4)), 4))
    put("ch11.slope.p.below", "0.0001" if t_two(b / L["se_b"], df) < 0.0001 else "no")
    t1 = (b - 1) / L["se_b"]
    put("ch11.slope1.t", f(t1, 2)); put("ch11.slope1.p.below", "0.0001" if t_two(t1, df) < 0.0001 else f(t_two(t1, df), 4))
    # Chapter 11 review
    put("ch11.review.pred", f(12.5 + 3.2 * 4, 1)); put("ch11.review.res", f(27 - (12.5 + 3.2 * 4), 1))
    put("ch11.review.slope", f(0.8 * 10 / 4, 1)); put("ch11.review.intercept", f(30 - 2.0 * 6, 1))
    vx = [float(r_["entry_grade"]) for r_ in every if r_["offer"] == "0"]
    vy = [float(r_["visits"]) for r_ in every if r_["offer"] == "0"]
    L3 = linreg(vx, vy)
    put("ch11.review.visits.n", len(vx)); put("ch11.review.visits.a", f(L3["a"], 3)); put("ch11.review.visits.b", f(L3["b"], 3))
    put("ch11.review.visits.r", f(L3["r"], 3)); put("ch11.review.visits.r2", f(L3["r"] ** 2, 3))
    put("ch11.review.visits.r2.pct", f(100 * L3["r"] ** 2, 1))
    put("ch11.review.visits.at2", f(L3["a"] + L3["b"] * 2.0, 2)); put("ch11.review.visits.at4", f(L3["a"] + L3["b"] * 4.0, 2))
    put("ch11.review.visits.at2.hand", f(float(f(L3["a"], 3)) + float(f(L3["b"], 3)) * 2.0, 2))
    put("ch11.review.visits.at4.hand", f(float(f(L3["a"], 3)) + float(f(L3["b"], 3)) * 4.0, 2))
    tq = 1.84 / 0.52
    ts23 = t_star(0.025, 23)
    put("ch11.review.slope.t", f(tq, 2)); put("ch11.review.slope.p", f(t_two(tq, 23), 4)); put("ch11.review.slope.tstar", f(ts23, 3))
    put("ch11.review.slope.me", f(float(f(ts23, 3)) * 0.52, 3))
    put("ch11.review.slope.low", f(1.84 - float(f(ts23, 3)) * 0.52, 3)); put("ch11.review.slope.high", f(1.84 + float(f(ts23, 3)) * 0.52, 3))


# ---- Chapter 12: what the investigations print that earlier chapters do not ----

def chapter_12(every):
    # Investigation 1: the offer within each college, and school grades by group
    by = {}
    for r in every:
        by.setdefault(r["college"], []).append(r["offer"] == "1")
    shares = [100 * sum(v) / len(v) for v in by.values()]
    offered = [sum(v) for v in by.values()]
    put("ch12.inv1.offered.range", f"{min(offered)} to {max(offered)}")
    put("ch12.inv1.share.range", f"{f(min(shares), 1)} to {f(max(shares), 1)}")
    for lab, z in (("offered", "1"), ("not_offered", "0")):
        x = [float(r["entry_grade"]) for r in every if r["offer"] == z]
        fv = five(x)
        put(f"ch12.inv1.{lab}.five", join(g(v) for v in fv))
        put(f"ch12.inv1.{lab}.mean", f(mean(x), 3)); put(f"ch12.inv1.{lab}.sx", f(sd(x), 3))
        put(f"ch12.inv1.{lab}.iqr", g(fv[3] - fv[1]))
        put(f"ch12.inv1.{lab}.low_fence", g4(fv[1] - 1.5 * (fv[3] - fv[1])))
        put(f"ch12.inv1.{lab}.below_fence", sum(v < fv[1] - 1.5 * (fv[3] - fv[1]) for v in x))
    put("ch12.inv1.mean_gap", f(mean([float(r["entry_grade"]) for r in every if r["offer"] == "1"])
                                - mean([float(r["entry_grade"]) for r in every if r["offer"] == "0"]), 3))
    # Investigation 3: SHUFFLE's exact chance, both sides, and a shuffle within each college
    known = [r for r in every if r["withdrew"] in ("0", "1")]
    pop, good = len(known), sum(r["withdrew"] == "1" for r in known)
    n = sum(r["offer"] == "1" for r in known)
    obs = sum(r["offer"] == "1" and r["withdrew"] == "1" for r in known)
    pmf = hyper_pmf(pop, n, good)          # K, the withdrawals seated in offered seats
    gap = lambda k: 100 * (k / n - (good - k) / (pop - n))
    cut = min(k for k in range(good + 1) if gap(k) >= abs(gap(obs)))
    low, high = math.fsum(pmf[: obs + 1]), math.fsum(pmf[cut:])
    put("ch12.inv3.of100.sd", f(math.sqrt(100 * (low + high) * (1 - low - high)), 1))
    cdf = 0.0
    q = []
    for k, pk in enumerate(pmf):
        cdf += pk
        q.append(cdf)
    put("ch12.inv3.middle95", f"{min(k for k in range(len(q)) if q[k] >= 0.025)} to {min(k for k in range(len(q)) if q[k] >= 0.975)}")
    dist = [1.0]
    for c in sorted({r["college"] for r in known}):
        kc = [r for r in known if r["college"] == c]
        pc = hyper_pmf(len(kc), sum(r["offer"] == "1" for r in kc), sum(r["withdrew"] == "1" for r in kc))
        new = [0.0] * (len(dist) + len(pc) - 1)
        for i, a in enumerate(dist):
            for j, b in enumerate(pc):
                new[i + j] += a * b
        dist = new
    put("ch12.inv3.within", f(math.fsum(dist[: obs + 1]) + math.fsum(dist[cut:]), 4))
    # Investigation 4: two ways to count the 11 unknown outcomes, and the standard errors by hand
    k_off = [r for r in known if r["offer"] == "1"]
    k_not = [r for r in known if r["offer"] == "0"]
    x1, n1 = sum(r["withdrew"] == "1" for r in k_off), len(k_off)
    x2, n2 = sum(r["withdrew"] == "1" for r in k_not), len(k_not)
    seu = math.sqrt(x1 / n1 * (1 - x1 / n1) / n1 + x2 / n2 * (1 - x2 / n2) / n2)
    pp = (x1 + x2) / (n1 + n2)
    sep = math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
    put("ch12.inv4.se", f(seu, 5)); put("ch12.inv4.se.pooled", f(sep, 5)); put("ch12.inv4.me", f(1.96 * float(f(seu, 5)), 4))
    off = [r for r in every if r["offer"] == "1"]
    notoff = [r for r in every if r["offer"] == "0"]
    u1 = sum(r["withdrew"] == "" for r in off); u2 = sum(r["withdrew"] == "" for r in notoff)
    for lab, a, b in (("stayed", 0, 0), ("withdrew", u1, u2)):
        y1, m1, y2, m2 = x1 + a, len(off), x2 + b, len(notoff)
        p1, p2 = y1 / m1, y2 / m2
        se_ = math.sqrt(p1 * (1 - p1) / m1 + p2 * (1 - p2) / m2)
        put(f"ch12.inv4.{lab}.counts", f"{y1} of {m1} against {y2} of {m2}")
        put(f"ch12.inv4.{lab}.diff", f(p1 - p2, 4))
        put(f"ch12.inv4.{lab}.ci", join((f(p1 - p2 - Z95 * se_, 4), f(p1 - p2 + Z95 * se_, 4))))
    # Investigation 7: by hand with 1197.07 degrees of freedom
    v1 = [int(r["visits"]) for r in off]
    v2 = [int(r["visits"]) for r in notoff]
    _, df, se = welch(mean(v1), sd(v1), len(v1), mean(v2), sd(v2), len(v2))
    ts = t_star(0.025, df)
    put("ch12.inv7.tstar", f(ts, 3)); put("ch12.inv7.me", f(float(f(ts, 3)) * float(f(se, 4)), 3))
    put("ch12.inv7.diff", f(mean(v1) - mean(v2), 4))


# Each figure the text works by hand, from printed numbers, must give what the calculator shows.
SAME = [("ch10.s20.school.se.hand", "ch10.s20.school.se"), ("ch10.s20.school.me.hand", "ch10.s20.school.me"),
        ("ch10.test.t.hand", "ch10.test.t"), ("ch10.pair.se.hand", "ch10.pair.se"), ("ch10.pair.t.hand", "ch10.pair.t"),
        ("ch10.pair.me.hand", "ch10.pair.me"), ("ch10.review.college.se.hand", "ch10.review.college.se"),
        ("ch10.review.college.me.hand", "ch10.review.college.me"), ("ch10.review.methods.t.hand", "ch10.review.methods.t"),
        ("ch10.two.hand.me", "ch10.two.me"), ("ch11.t.hand", "ch11.t"), ("ch11.slope1.hand", "ch11.slope1.t"),
        ("ch11.slope.hand", "ch11.b"), ("ch11.through", "ch11.ybar"), ("ch11.pred.1.hand", "ch11.pred.1"),
        ("ch11.review.visits.at2.hand", "ch11.review.visits.at2"), ("ch11.review.visits.at4.hand", "ch11.review.visits.at4"),
        ("ch9.hom.two.p", "ch9.hom.two.p"), ("ch9.ind.join.z2", "ch9.ind.join.chi2"), ("ch12.inv7.me", "ch10.two.me")]


def main():
    every = rows("data/tonmick-classroom.csv")
    invited = rows("data/tonmick-invited.csv")
    s20 = rows("samples/tonmick-sample-20.csv")
    s100 = rows("samples/tonmick-sample-100.csv")
    s120 = rows("samples/tonmick-sample-120.csv")
    chapter_9(every, invited, s100, s120); chapter_10(every, s20); chapter_11(every); chapter_12(every)
    for hand, calc in SAME:
        if V[hand] != V[calc]:
            raise SystemExit(f"{hand} is {V[hand]}, but {calc} is {V[calc]}: the text's arithmetic would disagree")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["name", "value"])
        for k in sorted(V):
            w.writerow([k, V[k]])


if __name__ == "__main__":
    main()
