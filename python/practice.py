#!/usr/bin/env python3
"""Route 1 for the book's practice test: every number its questions, answers, and graphs print,
with standard-library Python.

    python -I python/practice.py ROOT OUT.csv

The plan is outline/practice-test.md. This route and route 2 (r/practice.R) share no code. Names
start pt.qNN for Part 1's 40 multiple-choice questions, pt.wN for Part 2's four written
questions, and pt.figNN for the test's graphs (Figures 22 to 29, drawn by figures/draw.py, which
stops unless what it draws equals these values). Lists are separated by ", ".

- Every number a question states is in practice/givens.csv, chosen by hand, and is copied here
  under its own name (pt.<item>.<name>), so the book prints it from this file too.
- Every number computed from data reads the nine files in practice/ (python/make_practice.py).
- Wrong choices are computed too, each from the mistake the plan names, so the book's
  explanation of each trap prints a checked number.
- Normal values use statistics.NormalDist; t and chi-square use the regularized incomplete beta
  and gamma functions, inverted by bisection.
- Arithmetic shown by hand gives what the calculator gives: where the plan works a figure by
  hand from printed (rounded) numbers, this route computes it both ways and stops if the printed
  digits differ (same()).
"""
import csv
import math
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from statistics import NormalDist

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
N01 = NormalDist()
V = {}
PCT = [("q15", "p_delivery"), ("q15", "p_late_delivery"), ("q15", "p_late_pickup"), ("q19", "p"), ("q23", "p0"),
       ("q24", "p0"), ("w3", "alpha"), ("w4", "p")]


def put(name, value):
    if name in V:
        raise SystemExit(f"duplicate name {name}")
    V[name] = str(value)


def f(x, places):
    # A value exactly halfway between two printed values could round either way in another
    # language's formatting, so none may be printed at a place where it is a tie.
    if (abs(Decimal(x)).scaleb(places) % 1) == Decimal("0.5"):
        raise SystemExit(f"{x!r} is exactly halfway at {places} places; print it with more places")
    s = f"{x:.{places}f}"
    return s[1:] if s.startswith("-") and float(s) == 0 else s


def g(x):
    return f"{x:g}"


def j(xs):
    return ", ".join(str(x) for x in xs)


def same(label, a, b):
    if a != b:
        raise SystemExit(f"{label}: by hand {a}, by the calculator's route {b}")


def rows(name):
    with open(ROOT / "practice" / name, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def mean(v):
    return math.fsum(v) / len(v)


def sd(v):
    m = mean(v)
    return math.sqrt(math.fsum((a - m) ** 2 for a in v) / (len(v) - 1))


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


def corr(x, y):
    mx, my = mean(x), mean(y)
    sxy = math.fsum((a - mx) * (b - my) for a, b in zip(x, y))
    return sxy / math.sqrt(math.fsum((a - mx) ** 2 for a in x) * math.fsum((b - my) ** 2 for b in y))


def linreg(x, y):
    mx, my = mean(x), mean(y)
    b = math.fsum((a - mx) * (c - my) for a, c in zip(x, y)) / math.fsum((a - mx) ** 2 for a in x)
    return my - b * mx, b


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
    """P(T > t) for t >= 0."""
    return 0.5 * ibeta(df / 2, 0.5, df / (df + t * t))


def t_cdf(t, df):
    return 1.0 - t_upper(t, df) if t >= 0 else t_upper(-t, df)


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


def tstar(conf, df):
    return bisect(lambda t: t_upper(t, df), (1 - conf) / 2, 0.0, 1000.0)


def chi2_test(table):
    rt = [sum(r) for r in table]
    ct = [sum(c) for c in zip(*table)]
    n = sum(rt)
    exp = [[a * b / n for b in ct] for a in rt]
    stat = math.fsum((o - e) ** 2 / e for ro, re in zip(table, exp) for o, e in zip(ro, re))
    df = (len(rt) - 1) * (len(ct) - 1)
    return rt, ct, n, exp, stat, df, gamma_upper(df / 2, stat / 2)


def main():
    giv = {}
    with open(ROOT / "practice" / "givens.csv", newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            giv.setdefault(r["item"], {})[r["name"]] = r["value"]
            put(f"pt.{r['item']}.{r['name']}", r["value"])

    def G(item, name):
        return float(giv[item][name])

    # Givens a question states as percents, printed that way too
    for item, name in PCT:
        put(f"pt.{item}.{name}_pct", g(100 * G(item, name)))

    # Q2 (3.2, 3.3; Figure 22): waits at a bus stop
    w = [float(r["minutes"]) for r in rows("practice-waits.csv")]
    put("pt.q02.n", len(w)); put("pt.q02.mean", f(mean(w), 2)); put("pt.q02.median", g(median(w)))
    put("pt.q02.sd", f(sd(w), 2)); put("pt.q02.five", j(g(x) for x in five(w)))
    put("pt.fig22.n", len(w)); put("pt.fig22.top", g(max(w)))
    put("pt.fig22.bars", j(sum(4 * i <= x < 4 * i + 4 for x in w) for i in range(9)))

    # Q3 (3.4): Celsius to Fahrenheit
    m, s, a, b = G("q03", "mean_c"), G("q03", "sd_c"), G("q03", "factor"), G("q03", "shift")
    put("pt.q03.mean_f", f(a * m + b, 1)); put("pt.q03.sd_f", f(a * s, 1))
    put("pt.q03.trap.sd_shifted", f(a * s + b, 1)); put("pt.q03.trap.mean_unshifted", f(a * m, 1))

    # Q4 (3.5, 3.7; Figure 23): battery life of two models
    bat = rows("practice-batteries.csv")
    for mod in ("A", "B"):
        v = [float(r["hours"]) for r in bat if r["model"] == mod]
        s5 = five(v)
        iqr = s5[3] - s5[1]
        lo, hi = s5[1] - 1.5 * iqr, s5[3] + 1.5 * iqr
        outs = sorted(x for x in v if x < lo or x > hi)
        inside = [x for x in v if lo <= x <= hi]
        put(f"pt.q04.{mod}.n", len(v)); put(f"pt.q04.{mod}.iqr", f(iqr, 1)); put(f"pt.q04.{mod}.range", f(s5[4] - s5[0], 1))
        put(f"pt.q04.{mod}.fences", j([f(lo, 2), f(hi, 2)])); put(f"pt.q04.{mod}.mean", f(mean(v), 2))
        put(f"pt.q04.{mod}.sd", f(sd(v), 2))
        put(f"pt.fig23.{mod}.five", j(g(x) for x in s5))
        put(f"pt.fig23.{mod}.whiskers", j([g(min(inside)), g(max(inside))]))
        put(f"pt.fig23.{mod}.out", j(g(x) for x in outs) if outs else "none")

    # Q5 (3.6): z-scores
    put("pt.q05.z_1", f((G("q05", "score_1") - G("q05", "mean_1")) / G("q05", "sd_1"), 2))
    put("pt.q05.z_2", f((G("q05", "score_2") - G("q05", "mean_2")) / G("q05", "sd_2"), 2))

    # Q6 (3.5): the 1.5 x IQR rule from a five-number summary
    q1, q3 = G("q06", "q1"), G("q06", "q3")
    put("pt.q06.iqr", g(q3 - q1)); put("pt.q06.fence_lo", g(q1 - 1.5 * (q3 - q1)))
    put("pt.q06.fence_hi", g(q3 + 1.5 * (q3 - q1))); put("pt.q06.trap.two_iqr", g(q3 + 2 * (q3 - q1)))

    # Q11 (5.1): audio guide by age group
    t = {k: int(giv["q11"][k]) for k in giv["q11"]}
    users = t["child_yes"] + t["adult_yes"] + t["senior_yes"]
    n = sum(t.values())
    adults = t["adult_yes"] + t["adult_no"]
    put("pt.q11.rows", j([t["child_yes"] + t["child_no"], adults, t["senior_yes"] + t["senior_no"]]))
    put("pt.q11.users", users); put("pt.q11.nonusers", n - users); put("pt.q11.n", n)
    put("pt.q11.adults_of_users", f(t["adult_yes"] / users, 3)); put("pt.q11.trap.users_of_adults", f(t["adult_yes"] / adults, 3))
    put("pt.q11.trap.joint", f(t["adult_yes"] / n, 3)); put("pt.q11.trap.users", f(users / n, 3))

    # Q12 (5.3): the share of red in the first spins
    put("pt.q12.pct", g(100 * G("q12", "red") / G("q12", "spins")))

    # Q13 (5.4; Figure 24): 200 reruns of the seedlings' random assignment
    sim = [int(r["flowered_a"]) for r in rows("practice-flowering-sim.csv")]
    na, nb, fa, fb = (int(giv["q13"][k]) for k in ("n_a", "n_b", "flowered_a", "flowered_b"))
    tot = fa + fb
    diff = fa / na - fb / nb
    put("pt.q13.share_a", f(fa / na, 2)); put("pt.q13.share_b", f(fb / nb, 2)); put("pt.q13.diff", f(diff, 2))
    put("pt.q13.flowered", tot); put("pt.q13.seedlings", na + nb)
    diffs = [(k / na - (tot - k) / nb) for k in sim]
    ge = sum(d >= diff - 1e-9 for d in diffs)
    put("pt.q13.ge", ge); put("pt.q13.share", f(ge / len(sim), 2))
    put("pt.q13.trap.per100", f(ge / 100, 2)); put("pt.q13.trap.complement", f(1 - ge / len(sim), 2))
    big, draws = na + nb, na
    exact = sum(Fraction(math.comb(tot, k) * math.comb(big - tot, draws - k), math.comb(big, draws))
                for k in range(fa, min(tot, draws) + 1))
    put("pt.q13.exact", f(float(exact), 4))
    lo_k, hi_k = min(sim), max(sim)
    put("pt.fig24.reruns", len(sim)); put("pt.fig24.ge", ge)
    put("pt.fig24.diffs", j(f(k / na - (tot - k) / nb, 2) for k in range(lo_k, hi_k + 1)))
    put("pt.fig24.counts", j(sum(x == k for x in sim) for k in range(lo_k, hi_k + 1)))

    # Q14 (5.5 to 5.8): probability rules
    pa, pb, pab = G("q14", "p_a"), G("q14", "p_b"), G("q14", "p_ab")
    put("pt.q14.union", f(pa + pb - pab, 2)); put("pt.q14.trap.union_no_overlap", f(pa + pb, 2))
    put("pt.q14.product", f(pa * pb, 2)); put("pt.q14.a_given_b", f(pab / pb, 2)); put("pt.q14.b_given_a", f(pab / pa, 2))

    # Q15 (5.7): late orders
    pd, ld, lp = G("q15", "p_delivery"), G("q15", "p_late_delivery"), G("q15", "p_late_pickup")
    put("pt.q15.p_pickup", f(1 - pd, 2)); put("pt.q15.joint_delivery", f(pd * ld, 3)); put("pt.q15.joint_pickup", f((1 - pd) * lp, 3))
    late = pd * ld + (1 - pd) * lp
    put("pt.q15.p_late", f(late, 3)); put("pt.q15.trap.late_given_delivery", f(ld, 3)); put("pt.q15.delivery_given_late", f(pd * ld / late, 3))

    # Q16 (6.1, 6.2): a probability distribution's mean and SD
    xs = [float(x) for x in giv["q16"]["x"].split(", ")]
    ps = [float(x) for x in giv["q16"]["p"].split(", ")]
    if abs(math.fsum(ps) - 1) > 1e-12:
        raise SystemExit("Q16: the probabilities do not add to 1")
    mu = math.fsum(x * p for x, p in zip(xs, ps))
    var = math.fsum((x - mu) ** 2 * p for x, p in zip(xs, ps))
    put("pt.q16.mu", f(mu, 1)); put("pt.q16.var", f(var, 2)); put("pt.q16.sigma", f(math.sqrt(var), 2))
    mv = mean(xs)
    put("pt.q16.trap.mean_values", f(mv, 1))
    put("pt.q16.trap.sd_values", f(math.sqrt(math.fsum((x - mv) ** 2 for x in xs) / len(xs)), 2))

    # Q17 (6.4): binomial, n = 10, p = 0.2
    bn, bp = int(giv["q17"]["n"]), G("q17", "p")
    pk = [math.comb(bn, k) * bp ** k * (1 - bp) ** (bn - k) for k in range(bn + 1)]
    put("pt.q17.p0", f(pk[0], 4)); put("pt.q17.p1", f(pk[1], 4))
    put("pt.q17.ge2", f(1 - pk[0] - pk[1], 4)); put("pt.q17.trap.eq2", f(pk[2], 4))
    put("pt.q17.trap.le2", f(pk[0] + pk[1] + pk[2], 4)); put("pt.q17.trap.gt2", f(1 - pk[0] - pk[1] - pk[2], 4))
    same("Q17 by hand", f(1 - float(f(pk[0], 4)) - float(f(pk[1], 4)), 4), f(1 - pk[0] - pk[1], 4))

    # Q18 (6.7): the cutoff for the heaviest 5%
    m, s, top = G("q18", "mean"), G("q18", "sd"), G("q18", "top_pct") / 100
    z = N01.inv_cdf(1 - top)
    put("pt.q18.area", f(1 - top, 2)); put("pt.q18.z", f(z, 3)); put("pt.q18.cutoff", f(m + z * s, 1))
    same("Q18 by hand", f(m + float(f(z, 3)) * s, 1), f(m + z * s, 1))
    put("pt.q18.trap.two_tailed", f(m + N01.inv_cdf(1 - top / 2) * s, 1)); put("pt.q18.trap.lower", f(m - z * s, 1))
    put("pt.q18.trap.area", f(m + (1 - top) * s, 1))

    # Q19 (7.1): the sampling distribution of p-hat
    p, n, cut = G("q19", "p"), G("q19", "n"), G("q19", "cut")
    sdp = math.sqrt(p * (1 - p) / n)
    zz = (cut - p) / sdp
    put("pt.q19.q", f(1 - p, 2)); put("pt.q19.np", g(n * p)); put("pt.q19.nq", g(n * (1 - p)))
    put("pt.q19.sd", f(sdp, 3)); put("pt.q19.z", f(zz, 2)); put("pt.q19.prob", f(1 - N01.cdf(zz), 4))
    same("Q19 by hand", f(1 - N01.cdf(float(f(zz, 2))), 4), f(1 - N01.cdf(zz), 4))
    put("pt.q19.trap.lower", f(N01.cdf(zz), 4)); put("pt.q19.trap.two_tails", f(2 * (1 - N01.cdf(zz)), 4))
    one = math.sqrt(p * (1 - p))
    put("pt.q19.trap.sd_one", f(one, 2)); put("pt.q19.trap.one", f(1 - N01.cdf((cut - p) / one), 4))

    # Q20 (8.1): a 95% interval for a proportion
    n, x = G("q20", "n"), G("q20", "x")
    ph = x / n
    se = math.sqrt(ph * (1 - ph) / n)
    z95, z90 = N01.inv_cdf(0.975), N01.inv_cdf(0.95)
    put("pt.q20.phat", f(ph, 2)); put("pt.q20.se", f(se, 4)); put("pt.q20.zstar", f(z95, 3))
    put("pt.q20.me", f(z95 * se, 4)); put("pt.q20.ci", j([f(ph - z95 * se, 3), f(ph + z95 * se, 3)]))
    same("Q20 by hand", f(float(f(z95, 3)) * float(f(se, 4)), 4), f(z95 * se, 4))
    me4 = float(f(z95 * se, 4))
    same("Q20 interval by hand", j([f(ph - me4, 3), f(ph + me4, 3)]), j([f(ph - z95 * se, 3), f(ph + z95 * se, 3)]))
    put("pt.q20.trap.ci90", j([f(ph - z90 * se, 3), f(ph + z90 * se, 3)]))
    put("pt.q20.trap.no_root", j([f(ph - z95 * se * se, 3), f(ph + z95 * se * se, 3)]))
    put("pt.q20.trap.no_zstar", j([f(ph - se, 3), f(ph + se, 3)]))

    # Q22 (8.3): the sample size for a margin of 0.03
    me, ps_ = G("q22", "margin"), G("q22", "p_star")
    exact_n = (z95 / me) ** 2 * ps_ * (1 - ps_)
    put("pt.q22.exact", f(exact_n, 1)); put("pt.q22.n", math.ceil(exact_n))
    same("Q22 by hand", f((float(f(z95, 3)) / me) ** 2 * ps_ * (1 - ps_), 1), f(exact_n, 1))
    put("pt.q22.trap.down", math.floor(exact_n)); put("pt.q22.trap.n90", math.ceil((z90 / me) ** 2 * ps_ * (1 - ps_)))
    put("pt.q22.trap.no_square", math.ceil(z95 * math.sqrt(ps_ * (1 - ps_)) / me))

    # Q23 (8.4, 8.5): a one-sided test for a proportion
    p0, n, x = G("q23", "p0"), G("q23", "n"), G("q23", "x")
    ph = x / n
    sd0 = math.sqrt(p0 * (1 - p0) / n)
    zz = (ph - p0) / sd0
    put("pt.q23.phat", f(ph, 2)); put("pt.q23.np0", g(n * p0)); put("pt.q23.nq0", g(n * (1 - p0)))
    put("pt.q23.sd0", f(sd0, 3)); put("pt.q23.z", f(zz, 2)); put("pt.q23.p", f(N01.cdf(zz), 4))
    put("pt.q23.trap.two_sided", f(2 * N01.cdf(-abs(zz)), 4)); put("pt.q23.trap.upper", f(1 - N01.cdf(zz), 4))
    sep = math.sqrt(ph * (1 - ph) / n)
    put("pt.q23.trap.se_phat", f(sep, 4)); put("pt.q23.trap.z_phat", f((ph - p0) / sep, 2))
    put("pt.q23.trap.p_phat", f(N01.cdf((ph - p0) / sep), 4))

    # Q25 (8.7, 8.8): two proportions from a randomized experiment
    n1, x1, n2, x2 = G("q25", "n_1"), G("q25", "x_1"), G("q25", "n_2"), G("q25", "x_2")
    p1, p2 = x1 / n1, x2 / n2
    pool = (x1 + x2) / (n1 + n2)
    sep = math.sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2))
    seu = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    zz = (p1 - p2) / sep
    put("pt.q25.n", g(n1 + n2)); put("pt.q25.phat_1", f(p1, 2)); put("pt.q25.phat_2", f(p2, 2)); put("pt.q25.diff", f(p1 - p2, 2))
    put("pt.q25.pooled", f(pool, 3)); put("pt.q25.se", f(sep, 5)); put("pt.q25.z", f(zz, 2))
    same("Q25 by hand", f((p1 - p2) / float(f(sep, 5)), 2), f(zz, 2))
    put("pt.q25.p", f(2 * (1 - N01.cdf(abs(zz))), 4)); put("pt.q25.trap.one_sided", f(1 - N01.cdf(zz), 4))
    put("pt.q25.trap.se_unpooled", f(seu, 4)); put("pt.q25.trap.z_unpooled", f((p1 - p2) / seu, 2))
    same("Q25 unpooled by hand", f((p1 - p2) / float(f(seu, 4)), 2), f((p1 - p2) / seu, 2))
    put("pt.q25.trap.p_unpooled", f(2 * (1 - N01.cdf(abs((p1 - p2) / seu))), 4))
    se1 = math.sqrt(pool * (1 - pool) / (n1 + n2))
    put("pt.q25.trap.z_one_n", f((p1 - p2) / se1, 2)); put("pt.q25.trap.p_one_n", f(2 * (1 - N01.cdf(abs((p1 - p2) / se1))), 4))
    put("pt.q25.ci", j([f(p1 - p2 - z95 * seu, 3), f(p1 - p2 + z95 * seu, 3)]))

    # Q26 (9.3; Figure 25): news source by age group, one random sample
    q = giv["q26"]
    tab = [[int(q[f"{a}_{s}"]) for s in ("phone", "tv", "print")] for a in ("under40", "over40")]
    rt, ct, n, exp, stat, df, pv = chi2_test(tab)
    put("pt.q26.rows", j(rt)); put("pt.q26.cols", j(ct)); put("pt.q26.n", n)
    put("pt.q26.expected", j(f(e, 1) for r in exp for e in r)); put("pt.q26.chi2", f(stat, 2))
    put("pt.q26.df", df); put("pt.q26.p", f(pv, 4)); put("pt.q26.trap.cells_less_one", len(rt) * len(ct) - 1)
    for a, r, tot in zip(("under40", "over40"), tab, rt):
        put(f"pt.fig25.{a}.pct", j(f(100 * c / tot, 1) for c in r))

    # Q27 (9.2): survival by watering schedule, an experiment
    q = giv["q27"]
    tab = [[int(q[f"{a}_survived"]), int(q[f"{a}_died"])] for a in ("daily", "alternate", "weekly")]
    rt, ct, n, exp, stat, df, pv = chi2_test(tab)
    put("pt.q27.rows", j(rt)); put("pt.q27.cols", j(ct)); put("pt.q27.n", n)
    put("pt.q27.expected", j(f(e, 2) for r in exp for e in r)); put("pt.q27.expected_weekly_died", f(exp[2][1], 2))
    put("pt.q27.trap.equal_split", f(ct[1] / 3, 2)); put("pt.q27.trap.weekly_survived", f(exp[2][0], 2))
    put("pt.q27.chi2", f(stat, 2)); put("pt.q27.df", df); put("pt.q27.p", f(pv, 4))

    # Q28 (7.2): the sampling distribution of x-bar
    mu, sg, n, cut = G("q28", "mu"), G("q28", "sigma"), G("q28", "n"), G("q28", "cut")
    sdx = sg / math.sqrt(n)
    zz = (cut - mu) / sdx
    put("pt.q28.sd", g(sdx)); put("pt.q28.z", f(zz, 2)); put("pt.q28.prob", f(1 - N01.cdf(zz), 4))
    put("pt.q28.trap.sigma", f(1 - N01.cdf((cut - mu) / sg), 4))
    put("pt.q28.trap.lower", f(N01.cdf(zz), 4)); put("pt.q28.trap.two_tails", f(2 * (1 - N01.cdf(zz)), 4))

    # Q29 (10.2): a t interval from summary statistics
    n, xb, s_ = G("q29", "n"), G("q29", "mean"), G("q29", "s")
    df = int(n) - 1
    ts, ts90 = tstar(0.95, df), tstar(0.90, df)
    se = s_ / math.sqrt(n)
    put("pt.q29.df", df); put("pt.q29.tstar", f(ts, 3)); put("pt.q29.se", f(se, 2)); put("pt.q29.me", f(ts * se, 2))
    put("pt.q29.ci", j([f(xb - ts * se, 2), f(xb + ts * se, 2)]))
    same("Q29 by hand", j([f(xb - float(f(ts, 3)) * se, 2), f(xb + float(f(ts, 3)) * se, 2)]), j([f(xb - ts * se, 2), f(xb + ts * se, 2)]))
    put("pt.q29.trap.z", j([f(xb - z95 * se, 2), f(xb + z95 * se, 2)])); put("pt.q29.trap.tstar90", f(ts90, 3))
    put("pt.q29.trap.ci90", j([f(xb - ts90 * se, 2), f(xb + ts90 * se, 2)]))
    put("pt.q29.trap.no_root", j([f(xb - ts * s_, 2), f(xb + ts * s_, 2)]))

    # Q30 (10.2, 10.3; Figure 26): twelve checkout waits
    c = [float(r["minutes"]) for r in rows("practice-checkout.csv")]
    s5 = five(c)
    iqr = s5[3] - s5[1]
    put("pt.q30.n", len(c)); put("pt.q30.values", j(g(x) for x in c)); put("pt.q30.five", j(g(x) for x in s5))
    put("pt.q30.iqr", g(iqr)); put("pt.q30.fence_hi", g(s5[3] + 1.5 * iqr)); put("pt.q30.mean", f(mean(c), 2))
    put("pt.q30.out", j(g(x) for x in sorted(x for x in c if x > s5[3] + 1.5 * iqr or x < s5[1] - 1.5 * iqr)))
    put("pt.fig26.values", j(g(x) for x in sorted(c)))

    # Q32 (10.4): ten runners in two shoes
    sh = rows("practice-shoes.csv")
    a_, b_ = [float(r["shoe_a"]) for r in sh], [float(r["shoe_b"]) for r in sh]
    d = [x - y for x, y in zip(a_, b_)]
    n = len(d)
    md, sdd = mean(d), sd(d)
    tt = md / (sdd / math.sqrt(n))
    put("pt.q32.n", n); put("pt.q32.diffs", j(g(x) for x in d)); put("pt.q32.mean", f(md, 2)); put("pt.q32.sd", f(sdd, 3))
    put("pt.q32.se", f(sdd / math.sqrt(n), 3)); put("pt.q32.t", f(tt, 2)); put("pt.q32.df", n - 1)
    put("pt.q32.p", f(2 * t_upper(abs(tt), n - 1), 4))
    same("Q32 by hand", f(float(f(md, 2)) / (float(f(sdd, 3)) / math.sqrt(n)), 2), f(tt, 2))
    put("pt.q32.trap.two_sample", f((mean(a_) - mean(b_)) / math.sqrt(sd(a_) ** 2 / n + sd(b_) ** 2 / n), 2))
    put("pt.q32.trap.over_n", f(md / (sdd / n), 2)); put("pt.q32.trap.no_root", f(md / sdd, 2))

    # Q33 (10.5): two means from summary statistics
    n1, m1, s1 = G("q33", "n_1"), G("q33", "mean_1"), G("q33", "s_1")
    n2, m2, s2 = G("q33", "n_2"), G("q33", "mean_2"), G("q33", "s_2")
    se = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2)
    put("pt.q33.diff", f(m1 - m2, 1)); put("pt.q33.se", f(se, 4)); put("pt.q33.t", f((m1 - m2) / se, 2))
    same("Q33 by hand", f((m1 - m2) / float(f(se, 4)), 2), f((m1 - m2) / se, 2))
    put("pt.q33.trap.add_se", f((m1 - m2) / (s1 / math.sqrt(n1) + s2 / math.sqrt(n2)), 2))
    put("pt.q33.trap.no_square", f((m1 - m2) / math.sqrt(s1 / n1 + s2 / n2), 2))
    put("pt.q33.trap.no_n", f((m1 - m2) / math.sqrt(s1 ** 2 + s2 ** 2), 2))

    # Q35 to Q37 and Q39 (11.1 to 11.4; Figure 27): iced drinks and the day's high
    ic = rows("practice-iced.csv")
    x = [float(r["high_f"]) for r in ic]
    y = [float(r["drinks"]) for r in ic]
    a, b = linreg(x, y)
    r = corr(x, y)
    put("pt.q35.n", len(x)); put("pt.q35.r", f(r, 3)); put("pt.q35.x_range", j([g(min(x)), g(max(x))]))
    put("pt.q36.a", f(a, 3)); put("pt.q36.b", f(b, 3)); put("pt.q39.r2", f(r * r, 3)); put("pt.q39.r2_pct", f(100 * r * r, 1))
    res = [yy - (a + b * xx) for xx, yy in zip(x, y)]
    k = max(range(len(res)), key=lambda i: abs(res[i]))
    xk, yk = x[k], y[k]
    put("pt.q37.day", ic[k]["day"]); put("pt.q37.high", g(xk)); put("pt.q37.drinks", g(yk))
    put("pt.q37.predicted", f(a + b * xk, 1)); put("pt.q37.residual", f(yk - (a + b * xk), 1))
    same("Q37 by hand", f(float(f(a, 3)) + float(f(b, 3)) * xk, 1), f(a + b * xk, 1))
    put("pt.q37.trap.sign", f((a + b * xk) - yk, 1)); put("pt.q37.trap.no_intercept", f(yk - b * xk, 1))
    put("pt.fig27.n", len(x)); put("pt.fig27.line", j([f(a, 3), f(b, 3)])); put("pt.fig27.x_range", j([g(min(x)), g(max(x))]))

    # Q38 (11.3; Figure 28): stopping distance and speed
    sp = rows("practice-stopping.csv")
    x = [float(r["speed_mph"]) for r in sp]
    y = [float(r["distance_ft"]) for r in sp]
    a, b = linreg(x, y)
    put("pt.q38.n", len(x)); put("pt.q38.r", f(corr(x, y), 3)); put("pt.q38.line", j([f(a, 3), f(b, 3)]))
    put("pt.fig28.speeds", j(g(v) for v in x)); put("pt.fig28.res", j(f(yy - (a + b * xx), 1) for xx, yy in zip(x, y)))

    # Q40 (11.2): the line from summary statistics
    r, mx, sx, my, sy, xn = (G("q40", k) for k in ("r", "mean_x", "sd_x", "mean_y", "sd_y", "x_new"))
    b = r * sy / sx
    a = my - b * mx
    put("pt.q40.b", f(b, 2)); put("pt.q40.a", f(a, 1)); put("pt.q40.predicted", f(a + b * xn, 1))
    put("pt.q40.trap.flipped_b", f(r * sx / sy, 2)); put("pt.q40.trap.flipped_a", f(my - r * sx / sy * mx, 1))
    put("pt.q40.trap.no_r_b", f(sy / sx, 2)); put("pt.q40.trap.no_r_a", f(my - sy / sx * mx, 1))
    put("pt.q40.trap.swapped_a", f(mx - b * my, 1))

    # W2 (3.2 to 3.7; Figure 29): commutes by bike and by bus
    cm = rows("practice-commute.csv")
    for mode in ("bike", "bus"):
        v = [float(r["minutes"]) for r in cm if r["mode"] == mode]
        s5 = five(v)
        iqr = s5[3] - s5[1]
        lo, hi = s5[1] - 1.5 * iqr, s5[3] + 1.5 * iqr
        put(f"pt.w2.{mode}.n", len(v)); put(f"pt.w2.{mode}.five", j(g(x_) for x_ in s5)); put(f"pt.w2.{mode}.iqr", g(iqr))
        put(f"pt.w2.{mode}.fences", j([g(lo), g(hi)])); put(f"pt.w2.{mode}.mean", f(mean(v), 2)); put(f"pt.w2.{mode}.sd", f(sd(v), 2))
        outs = sorted(x_ for x_ in v if x_ < lo or x_ > hi)
        put(f"pt.w2.{mode}.out", j(g(x_) for x_ in outs) if outs else "none")
        put(f"pt.fig29.{mode}", j(g(x_) for x_ in sorted(v)))
    bus = [float(r["minutes"]) for r in cm if r["mode"] == "bus"]
    zb = (30 - mean(bus)) / sd(bus)
    put("pt.w2.bus.z30", f(zb, 2))
    same("W2 by hand", f((30 - float(f(mean(bus), 2))) / float(f(sd(bus), 2)), 2), f(zb, 2))

    # W3 (8.9, 10.2, 10.3): twenty cups from a machine set for 12 ounces
    fl = [float(r["ounces"]) for r in rows("practice-fill.csv")]
    n, mu0 = len(fl), G("w3", "target")
    xb, s_ = mean(fl), sd(fl)
    se = s_ / math.sqrt(n)
    tt = (xb - mu0) / se
    ts = tstar(0.95, n - 1)
    put("pt.w3.n", n); put("pt.w3.values", j(f(v, 2) for v in fl)); put("pt.w3.mean", f(xb, 3)); put("pt.w3.sd", f(s_, 4))
    put("pt.w3.se", f(se, 4)); put("pt.w3.t", f(tt, 2)); put("pt.w3.df", n - 1); put("pt.w3.p", f(t_cdf(tt, n - 1), 4))
    put("pt.w3.tstar", f(ts, 3)); put("pt.w3.me", f(ts * se, 3)); put("pt.w3.ci", j([f(xb - ts * se, 3), f(xb + ts * se, 3)]))
    put("pt.w3.median", g(median(fl))); put("pt.w3.range", j([f(min(fl), 2), f(max(fl), 2)]))
    s5 = five(fl)
    iqr = s5[3] - s5[1]
    lo, hi = s5[1] - 1.5 * iqr, s5[3] + 1.5 * iqr
    put("pt.w3.five", j(g(v) for v in s5)); put("pt.w3.iqr", g(iqr)); put("pt.w3.fences", j([g(lo), g(hi)]))
    outs = sorted(v for v in fl if v < lo or v > hi)
    put("pt.w3.out", j(f(v, 2) for v in outs) if outs else "none")
    same("W3 t by hand", f((float(f(xb, 3)) - mu0) / (float(f(s_, 4)) / math.sqrt(n)), 2), f(tt, 2))
    same("W3 t from the SE", f((float(f(xb, 3)) - mu0) / float(f(se, 4)), 2), f(tt, 2))
    same("W3 interval by hand", j([f(float(f(xb, 3)) - float(f(ts, 3)) * float(f(se, 4)), 3),
                                   f(float(f(xb, 3)) + float(f(ts, 3)) * float(f(se, 4)), 3)]),
         j([f(xb - ts * se, 3), f(xb + ts * se, 3)]))

    # W4 (6.4, 7.1, 8.4, 8.5): defective parts
    p, ns, n, x = G("w4", "p"), int(giv["w4"]["n_small"]), G("w4", "n"), G("w4", "x")
    put("pt.w4.p_none", f((1 - p) ** ns, 4)); put("pt.w4.p_some", f(1 - (1 - p) ** ns, 4))
    sdp = math.sqrt(p * (1 - p) / n)
    ph = x / n
    zz = (ph - p) / sdp
    put("pt.w4.q", f(1 - p, 2)); put("pt.w4.np", g(n * p)); put("pt.w4.nq", g(n * (1 - p))); put("pt.w4.sd", f(sdp, 5)); put("pt.w4.phat", f(ph, 3))
    put("pt.w4.z", f(zz, 2)); put("pt.w4.prob", f(1 - N01.cdf(zz), 4))
    same("W4 by hand", f((float(f(ph, 3)) - p) / float(f(sdp, 5)), 2), f(zz, 2))
    nn = int(n)
    exact = math.fsum(math.comb(nn, k) * p ** k * (1 - p) ** (nn - k) for k in range(int(x), nn + 1))
    put("pt.w4.exact", f(exact, 4))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w_ = csv.writer(fh, lineterminator="\n")
        w_.writerow(["name", "value"])
        for k_ in sorted(V):
            w_.writerow([k_, V[k_]])
    print(f"python route: {len(V)} values in {OUT}")


if __name__ == "__main__":
    main()
