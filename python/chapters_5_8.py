#!/usr/bin/env python3
"""Route 1 for Chapters 5 to 8: every number the chapters, their Try It answers, and their
reviews print, rebuilt from the data files and the fixed sample of 100 with standard-library
Python.

    python -I python/chapters_5_8.py ROOT OUT.csv

Each value is written as the book prints it (name,value), so run_all.py can compare the
routes and expected/chapters_5_8.csv character for character. Conventions, as in Chapters 1
to 4, and two more:

- Arithmetic the text shows on the home screen starts from the numbers the book prints (a
  mean of 2.350, an SD of 2.926), so a reader who types them gets the same digits. Values a
  calculator command computes from the data (1-PropZInt, 2-PropZTest) start from the counts.
- Normal-model values use the printed parameters (3.010 and 0.469 for school grades).

Exact values replace simulation wherever one exists: SHUFFLE's chances (hypergeometric), the
capture rate of 95% intervals from samples of 100 (hypergeometric), and the skewness of means of
30 (the population's skewness over the square root of 30). simulate() then checks each of those
three against a simulation with this route's own random numbers, within a stated tolerance; the
simulations print nothing to OUT.csv, since the two routes draw different numbers.

The outline that says where each value appears is outline/chapters-5-8.md.
"""
import csv
import math
import random
import sys
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
    return f"{x:.{places}f}"


def pct(num, den, places=1):
    return f"{100 * num / den:.{places}f}"


def big(n):
    return f"{n:,}"


def rows(path):
    with open(ROOT / path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def hyper(k, pop, good, n):
    """P(K = k) when n are drawn without replacement from pop, of which good are marked."""
    if k < 0 or k > n or k > good or n - k > pop - good:
        return 0.0
    return math.comb(good, k) * math.comb(pop - good, n - k) / math.comb(pop, n)


def binom(k, n, p):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def pop_sd(x):
    m = math.fsum(x) / len(x)
    return math.sqrt(math.fsum((a - m) ** 2 for a in x) / len(x))


def two_prop(x1, n1, x2, n2):
    """2-PropZTest: z and the two-sided p value, with the pooled share."""
    p1, p2, pp = x1 / n1, x2 / n2, (x1 + x2) / (n1 + n2)
    z = (p1 - p2) / math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
    return z, 2 * N01.cdf(-abs(z)), pp


def chapter_5(every):
    N = len(every)
    exits = ["stayed", "withdrew", "transferred", "consent withdrawn"]
    groups = {"offered": [r for r in every if r["offer"] == "1"], "not_offered": [r for r in every if r["offer"] == "0"]}
    for lab, grp in groups.items():
        counts = [sum(r["exit"] == e for r in grp) for e in exits]
        for e, c in zip(exits, counts):
            put(f"ch5.table.{lab}.{e.split()[0]}", c)
        put(f"ch5.table.{lab}.total", len(grp))
        # 5.2: how the year ended within each group, of all its students
        put(f"ch5.seg.{lab}", ", ".join(pct(c, len(grp)) for c in counts))
    off, notoff = groups["offered"], groups["not_offered"]
    w_off = sum(r["exit"] == "withdrew" for r in off)
    w_all = sum(r["exit"] == "withdrew" for r in every)
    t_all = sum(r["exit"] == "transferred" for r in every)
    t_not = sum(r["exit"] == "transferred" for r in notoff)
    known = [r for r in every if r["withdrew"] in ("0", "1")]
    k_off = [r for r in known if r["offer"] == "1"]
    k_not = [r for r in known if r["offer"] == "0"]
    # 5.1
    put("ch5.joint.offered_withdrew", f(w_off / N, 4))
    put("ch5.marginal.withdrew", f(w_all / N, 4))
    put("ch5.cond.offered.withdrew.pct", pct(w_off, len(k_off)))
    put("ch5.cond.not_offered.withdrew.pct", pct(sum(r["withdrew"] == "1" for r in k_not), len(k_not)))
    put("ch5.try1.offered.transferred.pct", pct(sum(r["exit"] == "transferred" for r in off), len(off)))
    put("ch5.try1.not_offered.transferred.pct", pct(t_not, len(notoff)))
    # 5.3: the model of one offered student's year
    put("ch5.lln.ten.none", f(0.87 ** 10, 4)); put("ch5.lln.ten.expected", f(10 * 0.13, 1))
    put("ch5.lln.twenty.expected", f(20 * 0.13, 1))
    # 5.4: SHUFFLE deals the withdrawals among the known outcomes; K = withdrawals dealt to the offered
    pop, good, n = len(known), sum(r["withdrew"] == "1" for r in known), len(k_off)
    put("ch5.shuffle.n", big(pop)); put("ch5.shuffle.withdrawals", good); put("ch5.shuffle.offered", n)
    put("ch5.shuffle.expected", f(n * good / pop, 1))
    gap = lambda k: 100 * (k / n - (good - k) / (pop - n))
    obs = w_off
    put("ch5.shuffle.observed", obs); put("ch5.shuffle.gap", f(gap(obs), 1))
    extreme_high = min(k for k in range(n + 1) if gap(k) >= abs(gap(obs)))
    put("ch5.shuffle.cut_high", extreme_high); put("ch5.shuffle.gap_cut_high", f(gap(extreme_high), 1))
    put("ch5.shuffle.gap_below_cut", f(gap(extreme_high - 1), 1))
    lo = math.fsum(hyper(k, pop, good, n) for k in range(0, obs + 1))
    hi = math.fsum(hyper(k, pop, good, n) for k in range(extreme_high, good + 1))
    put("ch5.shuffle.low", f(lo, 4)); put("ch5.shuffle.high", f(hi, 4)); put("ch5.shuffle.p", f(lo + hi, 4))
    put("ch5.shuffle.of100", f"{100 * (lo + hi):.0f}")
    # 5.5 to 5.8
    pt = sum(r["part_time"] == "1" for r in every)
    put("ch5.p.offered", f(len(off) / N, 4)); put("ch5.p.part_time", f(pt / N, 4))
    put("ch5.p.full_time", f((N - pt) / N, 4))
    put("ch5.p.not_withdrew_known", f(1 - good / pop, 4))
    put("ch5.count.withdrew_or_transferred", w_all + t_all)
    put("ch5.p.withdrew_or_transferred", f((w_all + t_all) / N, 4))
    put("ch5.p.withdrew_given_offered", f(w_off / len(k_off), 4))
    put("ch5.p.offered_given_withdrew", f(w_off / w_all, 4))
    put("ch5.p.not_offered_given_transferred", f(t_not / t_all, 4))
    kpt = [r for r in known if r["part_time"] == "1"]
    kft = [r for r in known if r["part_time"] == "0"]
    wpt = sum(r["withdrew"] == "1" for r in kpt); wft = sum(r["withdrew"] == "1" for r in kft)
    put("ch5.tree.part_time", f(len(kpt) / pop, 4)); put("ch5.tree.withdrew_given_part_time", f(wpt / len(kpt), 4))
    put("ch5.tree.product", f(float(f(len(kpt) / pop, 4)) * float(f(wpt / len(kpt), 4)), 4))
    put("ch5.tree.full_time", f(len(kft) / pop, 4)); put("ch5.tree.withdrew_given_full_time", f(wft / len(kft), 4))
    put("ch5.tree.full_time_product", f(float(f(len(kft) / pop, 4)) * float(f(wft / len(kft), 4)), 4))
    put("ch5.tree.total", f(good / pop, 4))
    pt_off = sum(r["part_time"] == "1" for r in off); pt_not = sum(r["part_time"] == "1" for r in notoff)
    put("ch5.p.part_time_given_offered", f(pt_off / len(off), 4))
    put("ch5.p.part_time_given_not_offered", f(pt_not / len(notoff), 4))
    put("ch5.union.count", pt + len(off) - pt_off); put("ch5.union.p", f((pt + len(off) - pt_off) / N, 4))
    # Chapter 5 review
    put("ch5.review.union", f(0.40 + 0.30 - 0.12, 2)); put("ch5.review.product", f(0.40 * 0.30, 2))
    put("ch5.review.atleast1", f(1 - 0.87 ** 10, 4))
    put("ch5.review.pt.withdrew", wpt); put("ch5.review.pt.stayed", len(kpt) - wpt); put("ch5.review.pt.total", len(kpt))
    put("ch5.review.ft.withdrew", wft); put("ch5.review.ft.stayed", len(kft) - wft); put("ch5.review.ft.total", len(kft))
    put("ch5.review.total.stayed", big(pop - good)); put("ch5.review.p_pt_given_withdrew", f(wpt / good, 4))
    put("ch5.review.freethrow", f(binom(4, 5, 0.7) + binom(5, 5, 0.7), 4))


def chapter_6(every):
    visits = [int(r["visits"]) for r in every]
    N = len(visits)
    counts = [sum(v == k for v in visits) for k in range(8)] + [sum(v >= 8 for v in visits)]
    put("ch6.dist.counts", ", ".join(str(c) for c in counts))
    put("ch6.dist.probs", ", ".join(f(c / N, 4) for c in counts))
    run = 0
    cum = []
    for c in counts:
        run += c
        cum.append(f(run / N, 4))
    put("ch6.dist.cum", ", ".join(cum))
    put("ch6.p0", f(counts[0] / N, 4)); put("ch6.p1", f(counts[1] / N, 4)); put("ch6.p8plus", f(counts[8] / N, 4))
    put("ch6.count8plus", counts[8]); put("ch6.cum2", f(sum(counts[:3]) / N, 4))
    vals = sorted(set(visits))
    put("ch6.freq.values", ", ".join(str(v) for v in vals))
    put("ch6.freq.counts", ", ".join(str(sum(x == v for x in visits)) for v in vals))
    mu = math.fsum(visits) / N
    sg = pop_sd(visits)
    put("ch6.sum", sum(visits)); put("ch6.mu", f(mu, 3)); put("ch6.sigma", f(sg, 3))
    put("ch6.sx", f(math.sqrt(sg ** 2 * N / (N - 1)), 3))
    # 6.3, from the printed values
    m, s = float(f(mu, 3)), float(f(sg, 3))
    put("ch6.two.mean", f(2 * m, 3)); put("ch6.two.sd", f(math.sqrt(2) * s, 3))
    put("ch6.three.mean", f(3 * m, 3)); put("ch6.three.sd", f(math.sqrt(3) * s, 3))
    L2 = [int(r["visits"]) for r in every if r["offer"] == "1"]
    L4 = [int(r["visits"]) for r in every if r["offer"] == "0"]
    m2, m4 = float(f(math.fsum(L2) / len(L2), 3)), float(f(math.fsum(L4) / len(L4), 3))
    s2, s4 = float(f(pop_sd(L2), 3)), float(f(pop_sd(L4), 3))
    put("ch6.sigma.not_offered", f(pop_sd(L4), 3))
    put("ch6.diff.mean", f(m2 - m4, 3)); put("ch6.diff.sd", f(math.sqrt(s2 ** 2 + s4 ** 2), 3))
    # 6.4 binomial, 6.5 geometric
    put("ch6.binom.comb", math.comb(10, 2)); put("ch6.binom.pdf2", f(binom(2, 10, 0.13), 4))
    cdf2 = math.fsum(binom(k, 10, 0.13) for k in range(3))
    put("ch6.binom.cdf2", f(cdf2, 4)); put("ch6.binom.ge3", f(1 - cdf2, 4))
    put("ch6.binom.mean", f(10 * 0.13, 1)); put("ch6.binom.sd", f(math.sqrt(10 * 0.13 * 0.87), 3))
    put("ch6.geom.p3", f(0.87 ** 2 * 0.13, 4)); put("ch6.geom.cdf5", f(1 - 0.87 ** 5, 4))
    put("ch6.geom.mean", f(1 / 0.13, 2)); put("ch6.geom.after10", f(0.87 ** 10, 4))
    # 6.6 and 6.7: school grades and the normal model with the printed parameters
    eg = [float(r["entry_grade"]) for r in every]
    mean, sd = 3.010, 0.469
    model = NormalDist(mean, sd)
    for k in (1, 2, 3):
        inside = sum(mean - k * sd <= x <= mean + k * sd for x in eg)
        put(f"ch6.normal.within{k}", pct(inside, N))
        put(f"ch6.normal.rule{k}", f(100 * (N01.cdf(k) - N01.cdf(-k)), 1))
    put("ch6.normal.model_above_3_5", f(100 * (1 - model.cdf(3.5)), 1))
    put("ch6.normal.data_above_3_5", pct(sum(x > 3.5 for x in eg), N))
    put("ch6.normal.z_3_5", f((3.5 - mean) / sd, 2))
    put("ch6.normal.model_below_2_5", f(model.cdf(2.5), 4)); put("ch6.normal.model_below_2_5.pct", f(100 * model.cdf(2.5), 1))
    put("ch6.normal.data_below_2_5", pct(sum(x < 2.5 for x in eg), N))
    put("ch6.cut.p90", f(model.inv_cdf(0.9), 3)); put("ch6.cut.z90", f(N01.inv_cdf(0.9), 3))
    put("ch6.cut10.low", f(model.inv_cdf(0.05), 3)); put("ch6.cut10.high", f(model.inv_cdf(0.95), 3))
    put("ch6.cut10.z", f(N01.inv_cdf(0.95), 3))
    put("ch6.cut10.table.low", f(mean - 1.645 * sd, 3)); put("ch6.cut10.table.high", f(mean + 1.645 * sd, 3))
    put("ch6.cut.top25", f(model.inv_cdf(0.75), 3))
    # Chapter 6 review
    xs, ps = [0, 1, 2, 3], [0.1, 0.3, 0.4, 0.2]
    rm = math.fsum(x * p for x, p in zip(xs, ps))
    put("ch6.review.dist.mean", f(rm, 1)); put("ch6.review.dist.sd", f(math.sqrt(math.fsum(p * (x - rm) ** 2 for x, p in zip(xs, ps))), 1))
    put("ch6.review.sum.mean", f(20 + 15, 0)); put("ch6.review.sum.sd", f(math.sqrt(3 ** 2 + 4 ** 2), 0))
    put("ch6.review.height.z", f((68 - 64) / 2.5, 1)); put("ch6.review.height.p", f(1 - NormalDist(64, 2.5).cdf(68), 4))
    put("ch6.review.height.below", f(NormalDist(64, 2.5).cdf(68), 4))
    put("ch6.review.binom20.p3", f(binom(3, 20, 0.13), 4))
    put("ch6.review.binom20.le2", f(math.fsum(binom(k, 20, 0.13) for k in range(3)), 4))
    put("ch6.review.binom20.mean", f(20 * 0.13, 1)); put("ch6.review.binom20.sd", f(math.sqrt(20 * 0.13 * 0.87), 3))
    g12 = [float(r["grade_12"]) for r in every if r["grade_12"] != ""]
    gm = NormalDist(2.996, 0.561)
    put("ch6.review.g12.n", big(len(g12)))
    put("ch6.review.g12.model_above_3_5", f(100 * (1 - gm.cdf(3.5)), 1))
    put("ch6.review.g12.data_above_3_5", pct(sum(x > 3.5 for x in g12), len(g12)))
    put("ch6.review.g12.top10", f(gm.inv_cdf(0.9), 3))
    put("ch6.review.g12.model_above_4", f(100 * (1 - gm.cdf(4.0)), 1))
    put("ch6.review.g12.at_4", sum(x == 4.0 for x in g12)); put("ch6.review.g12.at_4.pct", pct(sum(x == 4.0 for x in g12), len(g12)))


def chapter_7(every):
    known = [r for r in every if r["withdrew"] in ("0", "1")]
    pop, good = len(known), sum(r["withdrew"] == "1" for r in known)
    p = float(f(good / pop, 4))                     # the printed 0.1432
    put("ch7.p", f(p, 4)); put("ch7.ten_pct", f(pop / 10, 1))
    sd100 = float(f(math.sqrt(p * (1 - p) / 100), 4))
    put("ch7.sd100", f(sd100, 4)); put("ch7.np100", f(100 * p, 1)); put("ch7.nq100", f(100 * (1 - p), 1))
    s100 = rows("samples/tonmick-sample-100.csv")
    ph = sum(r["withdrew"] == "1" for r in s100) / len(s100)
    put("ch7.sample100.phat", f(ph, 2)); put("ch7.sample100.z", f((ph - p) / sd100, 2))
    put("ch7.sd25", f(math.sqrt(p * (1 - p) / 25), 4)); put("ch7.np25", f(25 * p, 1))
    visits = [int(r["visits"]) for r in every]
    N = len(visits)
    mu = math.fsum(visits) / N
    m2 = math.fsum((v - mu) ** 2 for v in visits) / N
    m3 = math.fsum((v - mu) ** 3 for v in visits) / N
    skew = m3 / m2 ** 1.5
    s = float(f(math.sqrt(m2), 3))                   # the printed 2.926
    put("ch7.sd30", f(s / math.sqrt(30), 3)); put("ch7.sd120", f(s / math.sqrt(120), 3))
    put("ch7.skew.pop", f(skew, 2)); put("ch7.skew.mean30", f(skew / math.sqrt(30), 2))
    # D5c: the calculator's simulation draws from L2 (609 visits), since a list holds at most 999
    # values; its sigma-x, 3.102 as printed in Section 3.3, over the square root of 30
    L2 = [int(r["visits"]) for r in every if r["offer"] == "1"]
    s2 = float(f(pop_sd(L2), 3))
    put("ch7.L2.sd30", f(s2 / math.sqrt(30), 3))
    if f(pop_sd(L2) / math.sqrt(30), 3) != V["ch7.L2.sd30"]:
        raise SystemExit("ch7.L2.sd30 differs when worked from the unrounded sigma-x")
    put("ch7.ten_pct.joiners", f(N / 10, 1))
    k_off = [r for r in known if r["offer"] == "1"]; k_not = [r for r in known if r["offer"] == "0"]
    gap = float(f(sum(r["withdrew"] == "1" for r in k_off) / len(k_off) - sum(r["withdrew"] == "1" for r in k_not) / len(k_not), 4))
    sdg = float(f(math.sqrt(p * (1 - p) * (1 / len(k_off) + 1 / len(k_not))), 4))
    put("ch7.gap", f(gap, 4)); put("ch7.gap.sd", f(sdg, 4)); put("ch7.gap.z", f(gap / sdg, 2))
    put("ch7.gap.try", f(0.04 / sdg, 2))
    off = [r for r in every if r["offer"] == "1"]; notoff = [r for r in every if r["offer"] == "0"]
    se = float(f(math.sqrt(3.105 ** 2 / len(off) + 2.731 ** 2 / len(notoff)), 4))
    put("ch7.means.se", f(se, 4)); put("ch7.means.z", f(0.314 / se, 2))
    put("ch7.means.se4", f(math.sqrt(3.105 ** 2 / (4 * len(off)) + 2.731 ** 2 / (4 * len(notoff))), 4))
    # Chapter 7 review
    put("ch7.review.sd_phat", f(math.sqrt(0.30 * 0.70 / 50), 4)); put("ch7.review.sd_xbar", f(12 / math.sqrt(36), 0))
    put("ch7.review.np", f(0.04 * 150, 0)); put("ch7.review.nq", f(0.96 * 150, 0))
    z20 = (0.20 - p) / sd100
    put("ch7.review.z20", f(z20, 2)); put("ch7.review.p20", f(1 - N01.cdf(float(f(z20, 2))), 4))
    put("ch7.review.exact20", f(math.fsum(hyper(k, pop, good, 100) for k in range(20, 101)), 4))
    sd50 = float(f(s / math.sqrt(50), 3))
    put("ch7.review.sd50", f(sd50, 3)); put("ch7.review.z3", f((3 - float(f(mu, 3))) / sd50, 2))
    put("ch7.review.p3", f(1 - N01.cdf(float(f((3 - float(f(mu, 3))) / sd50, 2))), 4))


def chapter_8(every):
    known = [r for r in every if r["withdrew"] in ("0", "1")]
    pop, good = len(known), sum(r["withdrew"] == "1" for r in known)
    s100 = rows("samples/tonmick-sample-100.csv")
    n = len(s100)
    x = sum(r["withdrew"] == "1" for r in s100)
    ph = x / n
    se = math.sqrt(ph * (1 - ph) / n)
    put("ch8.x", x); put("ch8.n", n); put("ch8.failures", n - x); put("ch8.phat", f(ph, 2))
    put("ch8.se", f(se, 4)); put("ch8.zstar", f(Z95, 3)); put("ch8.me", f(Z95 * se, 4))
    put("ch8.ci.low", f(ph - Z95 * se, 4)); put("ch8.ci.high", f(ph + Z95 * se, 4))
    z90 = N01.inv_cdf(0.95)
    put("ch8.zstar90", f(z90, 3)); put("ch8.ci90.low", f(ph - z90 * se, 4)); put("ch8.ci90.high", f(ph + z90 * se, 4))
    put("ch8.true", f(good / pop, 4))
    cover = math.fsum(hyper(k, pop, good, n) for k in range(n + 1)
                      if k / n - Z95 * math.sqrt(k / n * (1 - k / n) / n) <= good / pop <= k / n + Z95 * math.sqrt(k / n * (1 - k / n) / n))
    put("ch8.coverage", f(100 * cover, 1))
    put("ch8.me400", f(Z95 * math.sqrt(ph * (1 - ph) / 400), 4))
    put("ch8.n.guess", big(math.ceil((Z95 / 0.03) ** 2 * ph * (1 - ph))))
    put("ch8.n.half", big(math.ceil((Z95 / 0.03) ** 2 * 0.25)))
    put("ch8.n.try", big(math.ceil((Z95 / 0.02) ** 2 * 0.25)))
    p0 = 0.15
    put("ch8.null", f(p0, 2)); put("ch8.null.expected", f(n * p0, 0)); put("ch8.null.expected_fail", f(n * (1 - p0), 0))
    z = (ph - p0) / math.sqrt(p0 * (1 - p0) / n)
    put("ch8.test.z", f(z + 0.0, 2)); put("ch8.test.p", f(N01.cdf(z), 4)); put("ch8.test.p2", f(2 * N01.cdf(-abs(z)), 4))
    # 8.6 power: the goal test when the truth is 0.1432 (one-sided, 5%, n = 100)
    truth = good / pop
    cut = p0 - N01.inv_cdf(0.95) * math.sqrt(p0 * (1 - p0) / n)
    power = N01.cdf((cut - truth) / math.sqrt(truth * (1 - truth) / n))
    put("ch8.power.goal.cut", f(cut, 4)); put("ch8.power.goal", f(power, 4)); put("ch8.power.goal.pct", f(100 * power, 1))
    put("ch8.power.goal.type2.pct", f(100 * (1 - power), 1))
    # the offer: true shares 80/605 and 93/603, two-sided 5%, normal approximation
    k_off = [r for r in known if r["offer"] == "1"]; k_not = [r for r in known if r["offer"] == "0"]
    x1, n1 = sum(r["withdrew"] == "1" for r in k_off), len(k_off)
    x2, n2 = sum(r["withdrew"] == "1" for r in k_not), len(k_not)
    p1, p2 = x1 / n1, x2 / n2
    d = abs(p1 - p2); pp = (x1 + x2) / (n1 + n2)
    se0 = math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2)); se1 = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    pw = N01.cdf((d - Z95 * se0) / se1) + N01.cdf((-d - Z95 * se0) / se1)
    put("ch8.power.two", f(pw, 4)); put("ch8.power.two.pct", f(100 * pw, 1))
    put("ch8.power.p1", f(p1, 4)); put("ch8.power.p2", f(p2, 4))
    put("ch8.power.n80", big(math.ceil((Z95 + N01.inv_cdf(0.8)) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / d ** 2)))
    # 8.7 and 8.8
    se_u = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    put("ch8.two.diff", f(p1 - p2, 4)); put("ch8.two.se", f(se_u, 4))
    put("ch8.two.ci.low", f(p1 - p2 - Z95 * se_u, 4)); put("ch8.two.ci.high", f(p1 - p2 + Z95 * se_u, 4))
    z2, pv, pooled = two_prop(x1, n1, x2, n2)
    put("ch8.pooled", f(pooled, 4)); put("ch8.two.z", f(z2, 2)); put("ch8.two.p", f(pv, 4))
    put("ch8.pooled.expected.offered", f(n1 * pooled, 1)); put("ch8.pooled.expected.not_offered", f(n2 * pooled, 1))
    off = [r for r in every if r["offer"] == "1"]; notoff = [r for r in every if r["offer"] == "0"]
    u1 = sum(r["withdrew"] == "" for r in off); u2 = sum(r["withdrew"] == "" for r in notoff)
    put("ch8.unknown.offered", u1); put("ch8.unknown.not_offered", u2)
    for lab, a, b in (("stayed", 0, 0), ("withdrew", u1, u2), ("against", u1, 0), ("for", 0, u2)):
        put(f"ch8.sens.{lab}.p", f(two_prop(x1 + a, len(off), x2 + b, len(notoff))[1], 4))
    # Chapter 8 review
    pr = 312 / 600; mer = Z95 * math.sqrt(pr * (1 - pr) / 600)
    put("ch8.review.poll.phat", f(pr, 2)); put("ch8.review.poll.me", f(mer, 4))
    put("ch8.review.poll.low", f(pr - mer, 4)); put("ch8.review.poll.high", f(pr + mer, 4))
    put("ch8.review.n", math.ceil((Z95 / 0.04) ** 2 * 0.25))
    xpt = sum(r["part_time"] == "1" for r in s100)
    ppt = xpt / n; sept = math.sqrt(ppt * (1 - ppt) / n)
    put("ch8.review.pt.x", xpt); put("ch8.review.pt.fail", n - xpt); put("ch8.review.pt.phat", f(ppt, 2))
    put("ch8.review.pt.se", f(sept, 4)); put("ch8.review.pt.me", f(Z95 * sept, 4))
    put("ch8.review.pt.low", f(ppt - Z95 * sept, 4)); put("ch8.review.pt.high", f(ppt + Z95 * sept, 4))
    put("ch8.review.pt.true", f(sum(r["part_time"] == "1" for r in known) / pop, 4))
    zr, pr2, pool = two_prop(52, 200, 38, 200)
    put("ch8.review.remind.phat1", f(52 / 200, 2)); put("ch8.review.remind.phat2", f(38 / 200, 2)); put("ch8.review.remind.pooled", f(pool, 3))
    put("ch8.review.remind.se", f(math.sqrt(pool * (1 - pool) * (2 / 200)), 4))
    put("ch8.review.remind.z", f(zr, 2)); put("ch8.review.remind.p", f(1 - N01.cdf(zr), 4)); put("ch8.review.remind.p_two", f(pr2, 4))


def simulate(every):
    """Each simulation against its exact value, within a stated tolerance (about six standard errors)."""
    rng = random.Random(2027)
    out = []
    # the law of large numbers: 10,000 offered students, each withdrawing with chance 0.13
    share = sum(rng.random() < 0.13 for _ in range(10000)) / 10000
    out.append(("law of large numbers, share of 10,000", share, 0.13, 0.02))
    # the central limit theorem: 4,000 means of 30 visits, drawn with replacement from all 1,219
    visits = [int(r["visits"]) for r in every]
    mu = math.fsum(visits) / len(visits); sd = pop_sd(visits) / math.sqrt(30)
    means = [math.fsum(rng.choice(visits) for _ in range(30)) / 30 for _ in range(4000)]
    mm = math.fsum(means) / len(means); ms = pop_sd(means)
    out.append(("means of 30, their mean", mm, mu, 0.05)); out.append(("means of 30, their SD", ms, sd, 0.03))
    # the capture rate: 4,000 samples of 100 from the 1,208 known outcomes
    known = [r["withdrew"] == "1" for r in every if r["withdrew"] in ("0", "1")]
    truth = sum(known) / len(known)
    hits = 0
    for _ in range(4000):
        k = sum(rng.sample(known, 100)) / 100
        m = Z95 * math.sqrt(k * (1 - k) / 100)
        hits += k - m <= truth <= k + m
    exact = float(V["ch8.coverage"]) / 100
    out.append(("capture rate of 95% intervals, samples of 100", hits / 4000, exact, 0.02))
    bad = [o for o in out if abs(o[1] - o[2]) > o[3]]
    for name, got, want, tol in out:
        print(f"simulation (python): {name} {got:.4f}, exact {want:.4f}, tolerance {tol}")
    if bad:
        raise SystemExit(f"simulation outside its tolerance: {bad}")


def main():
    every = rows("data/tonmick-classroom.csv")
    chapter_5(every); chapter_6(every); chapter_7(every); chapter_8(every)
    simulate(every)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["name", "value"])
        for k in sorted(V):
            w.writerow([k, V[k]])


if __name__ == "__main__":
    main()
