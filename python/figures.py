#!/usr/bin/env python3
"""Route 1 for the book's figures: every number a figure draws or prints, with standard-library
Python.

    python -I python/figures.py ROOT OUT.csv

The figures themselves are drawn by figures/draw.py, which needs matplotlib and stops unless
what it draws equals these values. This route and route 2 (r/figures.R) share no code. Names
start fig.NN, where NN is the figure's number in figures/README.md. Lists are separated by ", ".

- Counts and bars come from data/tonmick-classroom.csv and data/tonmick-grades-not-offered.csv.
- Exact distributions: the hypergeometric distribution of K (Figure 7) from whole-number
  binomial coefficients; binomial probabilities (Figures 9 and 12) from the formula.
- Normal, t, and chi-square values use statistics.NormalDist and, for t and chi-square, the
  regularized incomplete beta and gamma functions, inverted by bisection.
- Figures 13 and 14 read the two files in simulations/ (python/make_simulations.py). Figure 13
  also checks that the 1,000 means agree with the model within four standard errors.
"""
import csv
import math
import sys
from fractions import Fraction
from pathlib import Path
from statistics import NormalDist

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
N01 = NormalDist()
V = {}


def put(name, value):
    if name in V:
        raise SystemExit(f"duplicate name {name}")
    V[name] = str(value)


def f(x, places):
    s = f"{x:.{places}f}"
    return s[1:] if s.startswith("-") and float(s) == 0 else s


def j(xs):
    return ", ".join(str(x) for x in xs)


def rows(path):
    with open(ROOT / path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def median(v):
    v = sorted(v)
    n = len(v)
    return v[n // 2] if n % 2 else (v[n // 2 - 1] + v[n // 2]) / 2


def five(x):
    """The five-number summary as the TI-84 computes it (the median left out of both halves when n is odd)."""
    v = sorted(x)
    n, h = len(v), len(v) // 2
    lower, upper = v[:h], (v[h + 1:] if n % 2 else v[h:])
    return [v[0], median(lower), median(v), median(upper), v[-1]]


def g(x):
    return f"{x:g}"


def bars(values, start, width, count):
    out = []
    for i in range(count):
        lo = start + i * width
        out.append(sum(lo <= x < lo + width for x in values))
    return out


def mean(v):
    return math.fsum(v) / len(v)


def sd(v):
    m = mean(v)
    return math.sqrt(math.fsum((a - m) ** 2 for a in v) / (len(v) - 1))


def corr(x, y):
    mx, my = mean(x), mean(y)
    sxy = math.fsum((a - mx) * (b - my) for a, b in zip(x, y))
    return sxy / math.sqrt(math.fsum((a - mx) ** 2 for a in x) * math.fsum((b - my) ** 2 for b in y))


def linreg(x, y):
    mx, my = mean(x), mean(y)
    sxx = math.fsum((a - mx) ** 2 for a in x)
    b = math.fsum((a - mx) * (c - my) for a, c in zip(x, y)) / sxx
    a = my - b * mx
    return a, b, [c - (a + b * xx) for xx, c in zip(x, y)]


def binom(n, p, k):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


# t and chi-square quantiles: incomplete beta and gamma, inverted by bisection
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


def gamma_upper(a, x):
    """Q(a, x), the upper regularized incomplete gamma function."""
    if x <= 0:
        return 1.0
    lg = -x + a * math.log(x) - math.lgamma(a)
    if x < a + 1:
        s, term, ap = 1.0 / a, 1.0 / a, a
        for _ in range(100000):
            ap += 1
            term *= x / ap
            s += term
            if abs(term) < abs(s) * 1e-17:
                break
        return 1.0 - s * math.exp(lg)
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
        if abs(de - 1) < 1e-17:
            break
    return math.exp(lg) * h


def bisect(fun, target, lo, hi):
    """The x where the decreasing fun(x) equals target."""
    for _ in range(300):
        mid = (lo + hi) / 2
        if fun(mid) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    every = rows("data/tonmick-classroom.csv")
    known = [r for r in every if r["withdrew"] in ("0", "1")]
    L2 = [float(r["visits"]) for r in every if r["offer"] == "1"]
    L4 = [float(r["visits"]) for r in every if r["offer"] == "0"]

    # Figure 1: how the first year ended
    ends = ["stayed", "withdrew", "transferred", "consent withdrawn"]
    put("fig.01.counts", j(sum(r["exit"] == e for r in every) for e in ends)); put("fig.01.n", len(every))

    # Figure 2: the same two bars from 0 and from 75
    w_off = sum(r["withdrew"] == "1" and r["offer"] == "1" for r in known)
    w_not = sum(r["withdrew"] == "1" and r["offer"] == "0" for r in known)
    put("fig.02.counts", j([w_off, w_not])); put("fig.02.base", 75)
    put("fig.02.ratio", f(w_not / w_off, 2)); put("fig.02.ratio_cut", f((w_not - 75) / (w_off - 75), 1))

    # Figure 3: histogram of the offered students' visits, bars 2 wide
    put("fig.03.bars", j(bars(L2, 0, 2, 13))); put("fig.03.n", len(L2)); put("fig.03.top", g(max(L2)))

    # Figure 4: dotplot of the 16 colleges' joiners
    joined = {}
    for r in every:
        joined[r["college"]] = joined.get(r["college"], 0) + 1
    put("fig.04.joined", j(sorted(joined.values()))); put("fig.04.colleges", len(joined))

    # Figure 5: parallel modified box plots of visits
    for lab, v in (("offered", L2), ("not", L4)):
        s = five(v)
        iqr = s[3] - s[1]
        lo, hi = s[1] - 1.5 * iqr, s[3] + 1.5 * iqr
        put(f"fig.05.{lab}.five", j(g(x) for x in s)); put(f"fig.05.{lab}.fences", j([g(lo), g(hi)]))
        put(f"fig.05.{lab}.whisker", g(max(x for x in v if x <= hi)))
        put(f"fig.05.{lab}.outliers", sum(x < lo or x > hi for x in v))

    # Figure 6: segmented bar chart and mosaic plot of how the year ended, by offer
    sizes = []
    for lab, z in (("offered", "1"), ("not", "0")):
        grp = [r for r in every if r["offer"] == z]
        sizes.append(len(grp))
        put(f"fig.06.{lab}.pct", j(f(100 * sum(r["exit"] == e for r in grp) / len(grp), 1) for e in ends))
    put("fig.06.sizes", j(sizes))

    # Figure 7: the exact randomization distribution of K
    big_n, withdrawals, offered = len(known), sum(r["withdrew"] == "1" for r in known), sum(r["offer"] == "1" for r in known)
    total = math.comb(big_n, offered)

    def hyper(k):
        return Fraction(math.comb(withdrawals, k) * math.comb(big_n - withdrawals, offered - k), total)

    k_from, k_to = 64, 110
    put("fig.07.k_range", j([k_from, k_to]))
    put("fig.07.pmf", j(f(float(hyper(k)), 4) for k in range(k_from, k_to + 1)))
    put("fig.07.mean", f(withdrawals * offered / big_n, 1))
    low = sum(hyper(k) for k in range(0, 81))
    high = sum(hyper(k) for k in range(94, min(withdrawals, offered) + 1))
    put("fig.07.low", f(float(low), 4)); put("fig.07.high", f(float(high), 4)); put("fig.07.p", f(float(low + high), 4))
    put("fig.07.outside", f(float(1 - sum(hyper(k) for k in range(k_from, k_to + 1))), 4))

    # Figure 8: probability histogram of a joiner's visits
    cnt = [sum(int(r["visits"]) == x for r in every) for x in range(8)] + [sum(int(r["visits"]) >= 8 for r in every)]
    put("fig.08.probs", j(f(c / len(every), 4) for c in cnt))

    # Figure 9: binomial, n = 10, p = 0.13
    put("fig.09.probs", j(f(binom(10, 0.13, k), 4) for k in range(11)))

    # Figure 10: school grades, a histogram with the normal model, and the normal probability plot
    eg = [float(r["entry_grade"]) for r in every]
    put("fig.10.bars", j(bars(eg, 1.5, 0.25, 11))); put("fig.10.n", len(eg))
    put("fig.10.mean", f(mean(eg), 3)); put("fig.10.sd", f(sd(eg), 3))
    xs = sorted(eg)
    zs = [N01.inv_cdf((i - 0.5) / len(xs)) for i in range(1, len(xs) + 1)]
    put("fig.10.npp_r", f(corr(xs, zs), 4))

    # Figure 11: the school-grade model, the share above 3.5 and the 90th percentile
    model = NormalDist(3.010, 0.469)
    put("fig.11.above", f(1 - model.cdf(3.5), 4)); put("fig.11.p90", f(model.inv_cdf(0.9), 3))

    # Figure 12: p-hat for samples of 100 when p = 0.1432, as randBin(100,0.1432)/100 simulates it
    k_from, k_to = 3, 30
    put("fig.12.k_range", j([k_from, k_to]))
    put("fig.12.pmf", j(f(binom(100, 0.1432, k), 4) for k in range(k_from, k_to + 1)))
    put("fig.12.sd", f(math.sqrt(0.1432 * 0.8568 / 100), 4))

    # Figure 13: the population of visits beside 1,000 means of 30
    vis = [int(r["visits"]) for r in every]
    put("fig.13.pop.counts", j(sum(x == k for x in vis) for k in range(max(vis) + 1)))
    mu, sigma = mean(vis), math.sqrt(math.fsum((x - mean(vis)) ** 2 for x in vis) / len(vis))
    put("fig.13.pop.mean", f(mu, 3)); put("fig.13.pop.sd", f(sigma, 3))
    put("fig.13.model.sd", f(sigma / math.sqrt(30), 3))
    sims = rows("simulations/tonmick-sim-means-30.csv")
    means = [int(r["visits_total"]) / 30 for r in sims]
    put("fig.13.reps", len(means)); put("fig.13.means.bars", j(bars(means, 1.0, 0.25, 16)))
    put("fig.13.means.mean", f(mean(means), 3)); put("fig.13.means.sd", f(sd(means), 3))
    put("fig.13.means.range", j([f(min(means), 3), f(max(means), 3)]))
    big_m = len(vis)
    sd_srs = sigma / math.sqrt(30) * math.sqrt((big_m - 30) / (big_m - 1))
    kurt = math.fsum((x - mu) ** 4 for x in vis) / big_m / sigma ** 4
    se_sd = sd_srs * math.sqrt((2 + (kurt - 3) / 30) / (4 * len(means)))
    if abs(mean(means) - mu) > 4 * sd_srs / math.sqrt(len(means)) or abs(sd(means) - sd_srs) > 4 * se_sd:
        raise SystemExit("Figure 13: the 1,000 means do not agree with the model within four standard errors")
    print(f"python figures: 1,000 means of 30, mean {mean(means):.3f} against {mu:.3f}, "
          f"SD {sd(means):.3f} against {sd_srs:.3f} (within four standard errors)")

    # Figure 14: fifty 95% intervals from samples of 100
    sims = rows("simulations/tonmick-sim-samples-100.csv")
    counts = [int(r["withdrew"]) for r in sims]
    p_true = withdrawals / big_n
    z = N01.inv_cdf(0.975)
    caught, missed = 0, []
    for i, c in enumerate(counts, 1):
        ph = c / 100
        m = z * math.sqrt(ph * (1 - ph) / 100)
        if ph - m <= p_true <= ph + m:
            caught += 1
        else:
            missed.append(i)
    put("fig.14.counts", j(counts)); put("fig.14.captured", caught); put("fig.14.missed", j(missed))
    put("fig.14.p", f(p_true, 4)); put("fig.14.reps", len(counts))

    # Figure 15: the goal test's p value (H0: p = 0.15, p-hat = 0.15, n = 100, Ha: p < 0.15)
    z15 = (0.15 - 0.15) / math.sqrt(0.15 * 0.85 / 100)
    put("fig.15.z", f(z15, 2)); put("fig.15.p", f(N01.cdf(z15), 4))

    # Figure 16: power of the goal test when p = 173/1,208
    sd0, sd1 = math.sqrt(0.15 * 0.85 / 100), math.sqrt(p_true * (1 - p_true) / 100)
    cut = 0.15 - N01.inv_cdf(0.95) * sd0
    put("fig.16.sd0", f(sd0, 4)); put("fig.16.sd1", f(sd1, 4)); put("fig.16.cut", f(cut, 4))
    put("fig.16.alpha", f(N01.cdf((cut - 0.15) / sd0), 4)); put("fig.16.power", f(N01.cdf((cut - p_true) / sd1), 4))

    # Figure 17: chi-square curves; the 5% critical value for 2 degrees of freedom
    put("fig.17.dfs", j([2, 5, 10]))
    put("fig.17.crit", f(bisect(lambda x: gamma_upper(1.0, x / 2), 0.05, 0.0, 100.0), 3))

    # Figure 18: t curves for 2 and 19 degrees of freedom, and the standard normal
    put("fig.18.dfs", j([2, 19]))
    put("fig.18.crit", j([f(bisect(lambda t: t_upper(t, 2), 0.025, 0.0, 100.0), 3),
                          f(bisect(lambda t: t_upper(t, 19), 0.025, 0.0, 100.0), 3), f(N01.inv_cdf(0.975), 3)]))

    # Figures 19 and 20: the 555 students not offered with a college grade
    gr = rows("data/tonmick-grades-not-offered.csv")
    x = [float(r["entry_grade"]) for r in gr]
    y = [float(r["grade_12"]) for r in gr]
    a, b, res = linreg(x, y)
    put("fig.19.n", len(x)); put("fig.19.a", f(a, 3)); put("fig.19.b", f(b, 3)); put("fig.19.r", f(corr(x, y), 3))
    put("fig.20.res_range", j([f(min(res), 3), f(max(res), 3)]))

    # Figure 21: withdrawal by school-grade band, the line's residuals and the log line's
    cuts = [225, 250, 275, 300, 325, 350]
    bands = [[] for _ in range(len(cuts) + 1)]
    for r_ in known:
        bands[sum(round(100 * float(r_["entry_grade"])) >= c for c in cuts)].append(r_)
    gm = [f(mean([float(r_["entry_grade"]) for r_ in bd]), 3) for bd in bands]
    sh = [f(sum(r_["withdrew"] == "1" for r_ in bd) / len(bd), 3) for bd in bands]
    gx, sy = [float(v) for v in gm], [float(v) for v in sh]
    put("fig.21.grade", j(gm)); put("fig.21.share", j(sh))
    put("fig.21.lin.res", j(f(e, 3) for e in linreg(gx, sy)[2]))
    put("fig.21.log.res", j(f(e, 3) for e in linreg(gx, [math.log(v) for v in sy])[2]))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["name", "value"])
        for k in sorted(V):
            w.writerow([k, V[k]])
    print(f"python route: {len(V)} values in {OUT}")


if __name__ == "__main__":
    main()
