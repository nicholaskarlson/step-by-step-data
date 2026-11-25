#!/usr/bin/env python3
"""Draw the book's 29 figures, and check that they draw the numbers both routes computed.

    python figures/draw.py              check: recompute every number in expected/figures.csv, and every
                                        pt.fig value in expected/practice.csv, from the data, draw every
                                        figure into a temporary folder, and check the committed PNGs in
                                        figures/png/ (what CI runs)
    python figures/draw.py --write      draw the figures into figures/png/ (then update SHA256SUMS)

Figures 1 to 21 are the chapters'; Figures 22 to 29 are the practice test's, from the invented
data in practice/. Needs matplotlib (figures/requirements.txt); everything else in this repository
needs only the standard library. This script does not share code with python/figures.py,
python/practice.py, or the R routes: it recomputes, from data/, simulations/, and practice/, every
value it draws or prints, and stops unless each one equals expected/figures.csv or
expected/practice.csv, character for character. The committed PNGs are not compared pixel
for pixel, since fonts and matplotlib versions move pixels; they are checked for their size,
resolution (300 ppi), and grayscale, and SHA256SUMS pins their bytes.

Every figure is 6 inches wide at 300 ppi, in shades of gray, for a black-and-white paperback. The
practice test's figures show the data a question asks about and nothing that gives its answer away.
"""
import csv
import io
import logging
import math
import sys
import tempfile
from pathlib import Path
from statistics import NormalDist

import matplotlib

matplotlib.use("Agg")
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PNG = ROOT / "figures" / "png"
WIDTH, DPI = 6.0, 300
N01 = NormalDist()
INK, DARK, MID, LIGHT, PALE = "0.0", "0.25", "0.5", "0.72", "0.88"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["TeX Gyre Pagella", "Palatino", "DejaVu Serif"],
    "mathtext.fontset": "custom", "mathtext.rm": "TeX Gyre Pagella", "mathtext.it": "TeX Gyre Pagella:italic",
    "mathtext.bf": "TeX Gyre Pagella:bold", "mathtext.cal": "TeX Gyre Pagella", "mathtext.sf": "TeX Gyre Pagella",
    "mathtext.tt": "TeX Gyre Pagella",
    "font.size": 9, "axes.titlesize": 9, "axes.labelsize": 9, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "legend.fontsize": 8, "axes.edgecolor": INK, "axes.linewidth": 0.6, "xtick.major.width": 0.6,
    "ytick.major.width": 0.6, "lines.linewidth": 1.0, "axes.spines.top": False, "axes.spines.right": False,
    "savefig.dpi": DPI, "figure.dpi": DPI,
})


def f(x, places):
    s = f"{x:.{places}f}"
    return s[1:] if s.startswith("-") and float(s) == 0 else s


def j(xs):
    return ", ".join(str(x) for x in xs)


def g(x):
    return f"{x:g}"


def rows(path):
    with open(ROOT / path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def expected():
    out = {}
    for name in ("figures", "practice"):
        with open(ROOT / "expected" / f"{name}.csv", newline="", encoding="utf-8") as fh:
            r = list(csv.reader(fh))
        out.update({a: b for a, b in r[1:] if name == "figures" or a.startswith("pt.fig")})
    return out


def ti_five(v):
    v = np.sort(np.asarray(v, dtype=float))
    n, h = len(v), len(v) // 2
    lower, upper = v[:h], (v[h + 1:] if n % 2 else v[h:])
    return [float(v[0]), float(np.median(lower)), float(np.median(v)), float(np.median(upper)), float(v[-1])]


def counts_in(values, start, width, count):
    v = np.asarray(values, dtype=float)
    edges = start + width * np.arange(count + 1)
    return [int(((v >= edges[i]) & (v < edges[i + 1])).sum()) for i in range(count)]


def comb_pmf_hyper(k, big_n, good, draws):
    return math.comb(good, k) * math.comb(big_n - good, draws - k) / math.comb(big_n, draws)


def binom_pmf(n, p, k):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def t_pdf(x, df):
    x = np.asarray(x, dtype=float)
    c = math.gamma((df + 1) / 2) / (math.sqrt(df * math.pi) * math.gamma(df / 2))
    return c * (1 + x * x / df) ** (-(df + 1) / 2)


def chi2_pdf(x, df):
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    pos = x > 0
    out[pos] = x[pos] ** (df / 2 - 1) * np.exp(-x[pos] / 2) / (2 ** (df / 2) * math.gamma(df / 2))
    return out


def quantile_upper(pdf, tail, hi):
    """The x with area `tail` above it, by integrating pdf on a fine grid from x to hi."""
    xs = np.linspace(0, hi, 2_000_001)
    ys = pdf(xs)
    cum = np.concatenate([[0.0], np.cumsum((ys[1:] + ys[:-1]) / 2 * np.diff(xs))])
    above = cum[-1] - cum
    return float(np.interp(-tail, -above, xs))


def finish(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=DPI, metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("L")


def new(height, cols=1):
    fig, axes = plt.subplots(1, cols, figsize=(WIDTH, height), layout="constrained")
    return fig, axes


# ---------------------------------------------------------------- the data each figure draws

class Data:
    def __init__(self):
        self.every = rows("data/tonmick-classroom.csv")
        self.known = [r for r in self.every if r["withdrew"] in ("0", "1")]
        self.L2 = [float(r["visits"]) for r in self.every if r["offer"] == "1"]
        self.L4 = [float(r["visits"]) for r in self.every if r["offer"] == "0"]
        self.vis = [int(r["visits"]) for r in self.every]
        self.ends = ["stayed", "withdrew", "transferred", "consent withdrawn"]
        self.big_n = len(self.known)
        self.withdrawals = sum(r["withdrew"] == "1" for r in self.known)
        self.offered = sum(r["offer"] == "1" for r in self.known)
        self.p_true = self.withdrawals / self.big_n
        gr = rows("data/tonmick-grades-not-offered.csv")
        self.x = np.array([float(r["entry_grade"]) for r in gr])
        self.y = np.array([float(r["grade_12"]) for r in gr])


def fig01(d):
    c = [sum(r["exit"] == e for r in d.every) for e in d.ends]
    fig, ax = new(2.3)
    labels = ["Stayed", "Withdrew", "Transferred", "Consent\nwithdrawn"]
    ax.bar(labels, c, width=0.6, color=LIGHT, edgecolor=INK, linewidth=0.6)
    for i, v in enumerate(c):
        ax.text(i, v + 15, str(v), ha="center", va="bottom")
    ax.set_ylabel("Students")
    ax.set_ylim(0, 1100)
    return fig, {"fig.01.counts": j(c), "fig.01.n": str(len(d.every))}


def fig02(d):
    w_off = sum(r["withdrew"] == "1" and r["offer"] == "1" for r in d.known)
    w_not = sum(r["withdrew"] == "1" and r["offer"] == "0" for r in d.known)
    fig, axes = new(2.3, 2)
    for ax, base, title in ((axes[0], 0, "The axis starts at 0"), (axes[1], 75, "The axis starts at 75")):
        ax.bar(["Offered", "Not offered"], [w_off - base, w_not - base], bottom=base, width=0.55,
               color=LIGHT, edgecolor=INK, linewidth=0.6)
        ax.set_ylim(base, 100)
        ax.set_title(title)
        ax.set_ylabel("Students who withdrew")
    return fig, {"fig.02.counts": j([w_off, w_not]), "fig.02.base": "75", "fig.02.ratio": f(w_not / w_off, 2),
                 "fig.02.ratio_cut": f((w_not - 75) / (w_off - 75), 1)}


def fig03(d):
    c = counts_in(d.L2, 0, 2, 13)
    fig, ax = new(2.4)
    ax.bar(np.arange(0, 26, 2), c, width=2, align="edge", color=LIGHT, edgecolor=INK, linewidth=0.6)
    ax.set_xticks(range(0, 27, 2))
    ax.set_xlabel("Support visits in the first year, students offered mentoring")
    ax.set_ylabel("Students")
    return fig, {"fig.03.bars": j(c), "fig.03.n": str(len(d.L2)), "fig.03.top": g(max(d.L2))}


def fig04(d):
    joined = {}
    for r in d.every:
        joined[r["college"]] = joined.get(r["college"], 0) + 1
    vals = sorted(joined.values())
    fig, ax = new(1.5)
    seen = {}
    for v in vals:
        seen[v] = seen.get(v, 0) + 1
        ax.plot(v, seen[v], "o", color=INK, markersize=5)
    ax.set_ylim(0.3, 3.5)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlim(63, 88)
    ax.set_xticks(range(64, 89, 2))
    ax.set_xlabel("Students who joined the study, one dot for each of the 16 colleges")
    return fig, {"fig.04.joined": j(vals), "fig.04.colleges": str(len(vals))}


def fig05(d):
    fig, ax = new(2.0)
    facts = {}
    for row, lab, name, v in ((1, "offered", "Offered", d.L2), (0, "not", "Not offered", d.L4)):
        s = ti_five(v)
        iqr = s[3] - s[1]
        lo, hi = s[1] - 1.5 * iqr, s[3] + 1.5 * iqr
        whisker = max(x for x in v if x <= hi)
        outs = [x for x in v if x < lo or x > hi]
        ax.add_patch(plt.Rectangle((s[1], row - 0.22), s[3] - s[1], 0.44, facecolor=PALE, edgecolor=INK, linewidth=0.8))
        ax.plot([s[2], s[2]], [row - 0.22, row + 0.22], color=INK, linewidth=1.6)
        ax.plot([s[3], whisker], [row, row], color=INK, linewidth=0.8)
        ax.plot([whisker, whisker], [row - 0.1, row + 0.1], color=INK, linewidth=0.8)
        uniq = sorted(set(outs))
        ax.plot(uniq, [row] * len(uniq), "o", markerfacecolor="white", markeredgecolor=INK, markersize=3.5)
        facts.update({f"fig.05.{lab}.five": j(g(x) for x in s), f"fig.05.{lab}.fences": j([g(lo), g(hi)]),
                      f"fig.05.{lab}.whisker": g(whisker), f"fig.05.{lab}.outliers": str(len(outs))})
    ax.set_yticks([0, 1], ["Not offered", "Offered"])
    ax.set_ylim(-0.6, 1.6)
    ax.set_xlim(-0.5, 26)
    ax.set_xticks(range(0, 27, 2))
    ax.set_xlabel("Support visits in the first year (each open dot is one or more outliers)")
    return fig, facts


def fig06(d):
    facts, pcts, sizes = {}, {}, []
    for lab, z in (("offered", "1"), ("not", "0")):
        grp = [r for r in d.every if r["offer"] == z]
        sizes.append(len(grp))
        pcts[lab] = [100 * sum(r["exit"] == e for r in grp) / len(grp) for e in d.ends]
        facts[f"fig.06.{lab}.pct"] = j(f(p, 1) for p in pcts[lab])
    facts["fig.06.sizes"] = j(sizes)
    shades = [PALE, DARK, MID, "white"]
    names = ["Stayed", "Withdrew", "Transferred", "Consent withdrawn"]
    fig, axes = new(2.5, 2)
    ax = axes[0]
    for i, lab in enumerate(("offered", "not")):
        bottom = 0
        for k, p in enumerate(pcts[lab]):
            ax.bar(i, p, bottom=bottom, width=0.6, color=shades[k], edgecolor=INK, linewidth=0.5,
                   hatch="////" if k == 3 else None, label=names[k] if i == 0 else None)
            bottom += p
    ax.set_xticks([0, 1], ["Offered", "Not offered"])
    ax.set_ylabel("Percent of the group")
    ax.set_ylim(0, 100)
    ax.set_title("Segmented bars")
    ax = axes[1]
    for k in range(4):
        for i, lab in enumerate(("offered", "not")):
            ax.bar(k + (i - 0.5) * 0.38, pcts[lab][k], width=0.38, color=(LIGHT if i == 0 else DARK),
                   edgecolor=INK, linewidth=0.5, label=(["Offered", "Not offered"][i] if k == 0 else None))
    ax.set_xticks(range(4), ["Stayed", "Withdrew", "Transferred", "Consent\nwithdrawn"])
    ax.set_ylabel("Percent of the group")
    ax.set_ylim(0, 100)
    ax.set_title("Side-by-side bars")
    ax.legend(frameon=False, loc="upper right")
    axes[0].legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2)
    return fig, facts


def fig07(d):
    ks = list(range(64, 111))
    pmf = [comb_pmf_hyper(k, d.big_n, d.withdrawals, d.offered) for k in ks]
    low = sum(comb_pmf_hyper(k, d.big_n, d.withdrawals, d.offered) for k in range(0, 81))
    high = sum(comb_pmf_hyper(k, d.big_n, d.withdrawals, d.offered) for k in range(94, d.withdrawals + 1))
    fig, ax = new(2.4)
    ax.bar(ks, pmf, width=0.85, color=[DARK if (k <= 80 or k >= 94) else PALE for k in ks], edgecolor=INK, linewidth=0.3)
    mean = d.withdrawals * d.offered / d.big_n
    ax.axvline(mean, color=INK, linestyle="--", linewidth=0.7)
    ax.text(mean + 0.6, max(pmf) * 1.02, f"mean {f(mean, 1)}", va="bottom")
    ax.text(70.5, max(pmf) * 0.55, f"K ≤ 80: {f(low, 4)}", ha="center")
    ax.text(102.5, max(pmf) * 0.55, f"K ≥ 94: {f(high, 4)}", ha="center")
    ax.set_xlabel("K, the withdrawals a shuffle deals to the offered group")
    ax.set_ylabel("Probability")
    ax.set_ylim(0, max(pmf) * 1.18)
    return fig, {"fig.07.k_range": "64, 110", "fig.07.pmf": j(f(p, 4) for p in pmf), "fig.07.mean": f(mean, 1),
                 "fig.07.low": f(low, 4), "fig.07.high": f(high, 4), "fig.07.p": f(low + high, 4),
                 "fig.07.outside": f(1 - sum(pmf), 4)}


def fig08(d):
    c = [sum(x == k for x in d.vis) for k in range(8)] + [sum(x >= 8 for x in d.vis)]
    p = [v / len(d.vis) for v in c]
    fig, ax = new(2.2)
    ax.bar(range(9), p, width=0.9, color=LIGHT, edgecolor=INK, linewidth=0.6)
    ax.set_xticks(range(9), [str(k) for k in range(8)] + ["8+"])
    ax.set_xlabel("x, the support visits of a joiner chosen at random")
    ax.set_ylabel("P(X = x)")
    return fig, {"fig.08.probs": j(f(v, 4) for v in p)}


def fig09(d):
    p = [binom_pmf(10, 0.13, k) for k in range(11)]
    fig, ax = new(2.2)
    ax.bar(range(11), p, width=0.9, color=LIGHT, edgecolor=INK, linewidth=0.6)
    ax.set_xticks(range(11))
    ax.set_xlabel("k, the number of the 10 who withdraw")
    ax.set_ylabel("P(X = k)")
    return fig, {"fig.09.probs": j(f(v, 4) for v in p)}


def fig10(d):
    eg = np.array([float(r["entry_grade"]) for r in d.every])
    c = counts_in(eg, 1.5, 0.25, 11)
    fig, axes = new(2.5, 2)
    ax = axes[0]
    ax.bar(1.5 + 0.25 * np.arange(11), c, width=0.25, align="edge", color=PALE, edgecolor=INK, linewidth=0.5)
    xs = np.linspace(1.4, 4.4, 400)
    model = NormalDist(3.010, 0.469)
    ax.plot(xs, [model.pdf(x) * len(eg) * 0.25 for x in xs], color=INK, linewidth=1.1)
    ax.set_xlabel("School grade at entry")
    ax.set_ylabel("Students")
    ax.set_title("Histogram, with the normal model")
    ax = axes[1]
    srt = np.sort(eg)
    zs = np.array([N01.inv_cdf((i - 0.5) / len(srt)) for i in range(1, len(srt) + 1)])
    ax.plot(srt, zs, ".", color=INK, markersize=1.6)
    ax.set_xlabel("School grade at entry")
    ax.set_ylabel("z")
    ax.set_title("Normal probability plot")
    r = float(np.corrcoef(srt, zs)[0, 1])
    return fig, {"fig.10.bars": j(c), "fig.10.n": str(len(eg)), "fig.10.mean": f(float(eg.mean()), 3),
                 "fig.10.sd": f(float(eg.std(ddof=1)), 3), "fig.10.npp_r": f(r, 4)}


def fig11(d):
    model = NormalDist(3.010, 0.469)
    above, p90 = 1 - model.cdf(3.5), model.inv_cdf(0.9)
    xs = np.linspace(1.5, 4.5, 500)
    ys = np.array([model.pdf(x) for x in xs])
    fig, ax = new(2.3)
    ax.plot(xs, ys, color=INK)
    ax.fill_between(xs, ys, where=xs >= 3.5, color=MID, linewidth=0)
    ax.axvline(p90, color=INK, linestyle="--", linewidth=0.8)
    ax.text(p90 + 0.04, max(ys) * 0.82, f"90th percentile\n{f(p90, 3)}", va="center")
    ax.annotate(f"area above 3.5: {f(above, 4)}", xy=(3.75, model.pdf(3.75) * 0.5), xytext=(4.0, max(ys) * 0.45),
                arrowprops={"arrowstyle": "-", "color": INK, "linewidth": 0.6})
    ax.set_xlabel("School grade at entry, under a normal model with mean 3.010 and SD 0.469")
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    return fig, {"fig.11.above": f(above, 4), "fig.11.p90": f(p90, 3)}


def fig12(d):
    ks = list(range(3, 31))
    p = [binom_pmf(100, 0.1432, k) for k in ks]
    sd = math.sqrt(0.1432 * 0.8568 / 100)
    fig, ax = new(2.3)
    ax.bar([k / 100 for k in ks], p, width=0.0085, color=PALE, edgecolor=INK, linewidth=0.4)
    xs = np.linspace(0.02, 0.31, 400)
    ax.plot(xs, [NormalDist(0.1432, sd).pdf(x) * 0.01 for x in xs], color=INK, linewidth=1.1)
    ax.axvline(0.1432, color=INK, linestyle="--", linewidth=0.7)
    ax.set_xlabel(r"$\hat{p}$, the share who withdrew in a sample of 100 (p = 0.1432)")
    ax.set_ylabel("Probability")
    return fig, {"fig.12.k_range": "3, 30", "fig.12.pmf": j(f(v, 4) for v in p), "fig.12.sd": f(sd, 4)}


def fig13(d):
    vis = np.array(d.vis)
    pop = [int((vis == k).sum()) for k in range(int(vis.max()) + 1)]
    mu, sigma = float(vis.mean()), float(vis.std(ddof=0))
    means = np.array([int(r["visits_total"]) / 30 for r in rows("simulations/tonmick-sim-means-30.csv")])
    c = counts_in(means, 1.0, 0.25, 16)
    fig, axes = new(2.5, 2)
    ax = axes[0]
    ax.bar(range(len(pop)), pop, width=1, align="edge", color=PALE, edgecolor=INK, linewidth=0.4)
    ax.axvline(mu, color=INK, linestyle="--", linewidth=0.7)
    ax.set_xlabel("Support visits, all 1,219 joiners")
    ax.set_ylabel("Students")
    ax.set_title("The population")
    ax = axes[1]
    ax.bar(1.0 + 0.25 * np.arange(16), c, width=0.25, align="edge", color=PALE, edgecolor=INK, linewidth=0.4)
    ax.axvline(mu, color=INK, linestyle="--", linewidth=0.7)
    ax.set_xlabel("Mean visits in a sample of 30")
    ax.set_ylabel("Samples")
    ax.set_title("1,000 sample means")
    return fig, {"fig.13.pop.counts": j(pop), "fig.13.pop.mean": f(mu, 3), "fig.13.pop.sd": f(sigma, 3),
                 "fig.13.model.sd": f(sigma / math.sqrt(30), 3), "fig.13.reps": str(len(means)),
                 "fig.13.means.bars": j(c), "fig.13.means.mean": f(float(means.mean()), 3),
                 "fig.13.means.sd": f(float(means.std(ddof=1)), 3),
                 "fig.13.means.range": j([f(float(means.min()), 3), f(float(means.max()), 3)])}


def fig14(d):
    counts = [int(r["withdrew"]) for r in rows("simulations/tonmick-sim-samples-100.csv")]
    z = N01.inv_cdf(0.975)
    fig, ax = new(3.4)
    caught, missed = 0, []
    for i, c in enumerate(counts, 1):
        ph = c / 100
        m = z * math.sqrt(ph * (1 - ph) / 100)
        hit = ph - m <= d.p_true <= ph + m
        caught += hit
        if not hit:
            missed.append(i)
        ax.plot([ph - m, ph + m], [i, i], color=(MID if hit else INK), linewidth=(0.9 if hit else 1.8))
        ax.plot(ph, i, "o", color=INK, markersize=1.8)
    ax.axvline(d.p_true, color=INK, linewidth=0.8)
    ax.set_ylim(0, len(counts) + 1)
    ax.set_yticks([1, 10, 20, 30, 40, 50])
    ax.set_ylabel("Sample")
    ax.set_xlabel(f"95% interval for the share who withdrew (the vertical line is p = {f(d.p_true, 4)})")
    return fig, {"fig.14.counts": j(counts), "fig.14.captured": str(caught), "fig.14.missed": j(missed),
                 "fig.14.p": f(d.p_true, 4), "fig.14.reps": str(len(counts))}


def fig15(d):
    z = (0.15 - 0.15) / math.sqrt(0.15 * 0.85 / 100)
    p = N01.cdf(z)
    xs = np.linspace(-3.6, 3.6, 500)
    ys = np.array([N01.pdf(x) for x in xs])
    fig, ax = new(2.2)
    ax.plot(xs, ys, color=INK)
    ax.fill_between(xs, ys, where=xs <= z, color=LIGHT, linewidth=0)
    ax.axvline(z, color=INK, linewidth=0.8)
    ax.annotate(f"p value = {f(p, 4)}", xy=(-0.9, 0.12), xytext=(-2.9, 0.28), ha="center",
                arrowprops={"arrowstyle": "-", "color": INK, "linewidth": 0.6})
    ax.text(z + 0.1, 0.405, f"z = {f(z, 2)}", va="bottom")
    ax.set_xlabel("z, if H0 is true (the standard normal)")
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_ylim(0, 0.46)
    return fig, {"fig.15.z": f(z, 2), "fig.15.p": f(p, 4)}


def fig16(d):
    sd0, sd1 = math.sqrt(0.15 * 0.85 / 100), math.sqrt(d.p_true * (1 - d.p_true) / 100)
    cut = 0.15 - N01.inv_cdf(0.95) * sd0
    h0, h1 = NormalDist(0.15, sd0), NormalDist(d.p_true, sd1)
    alpha, power = h0.cdf(cut), h1.cdf(cut)
    xs = np.linspace(0.02, 0.28, 600)
    y0, y1 = np.array([h0.pdf(x) for x in xs]), np.array([h1.pdf(x) for x in xs])
    fig, ax = new(2.4)
    ax.plot(xs, y0, color=INK, linestyle="--", label="If H0 is true: p = 0.15")
    ax.plot(xs, y1, color=INK, label=f"The truth: p = {f(d.p_true, 4)}")
    ax.fill_between(xs, y1, where=xs <= cut, color=MID, linewidth=0, label=f"Power: {f(power, 4)}")
    ax.axvline(cut, color=INK, linewidth=0.8)
    ax.text(cut - 0.003, max(y1) * 1.02, f"reject H0 below {f(cut, 4)}", ha="right", va="bottom")
    ax.set_xlabel(r"$\hat{p}$ in a sample of 100")
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_ylim(0, max(y1) * 1.2)
    ax.legend(frameon=False, loc="upper right")
    return fig, {"fig.16.sd0": f(sd0, 4), "fig.16.sd1": f(sd1, 4), "fig.16.cut": f(cut, 4),
                 "fig.16.alpha": f(alpha, 4), "fig.16.power": f(power, 4)}


def fig17(d):
    crit = quantile_upper(lambda x: chi2_pdf(x, 2), 0.05, 200.0)
    xs = np.linspace(1e-6, 25, 600)
    fig, ax = new(2.3)
    for df, style in ((2, "-"), (5, "--"), (10, ":")):
        ax.plot(xs, chi2_pdf(xs, df), color=INK, linestyle=style, label=f"{df} degrees of freedom")
    y2 = chi2_pdf(xs, 2)
    ax.fill_between(xs, y2, where=xs >= crit, color=MID, linewidth=0)
    ax.annotate(f"area 0.05 above {f(crit, 3)}", xy=(crit + 0.6, 0.012), xytext=(crit + 3.0, 0.15),
                arrowprops={"arrowstyle": "-", "color": INK, "linewidth": 0.6})
    ax.set_xlabel("χ²")
    ax.set_ylim(0, 0.52)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.legend(frameon=False)
    return fig, {"fig.17.dfs": "2, 5, 10", "fig.17.crit": f(crit, 3)}


def fig18(d):
    crit = [quantile_upper(lambda x, df=df: t_pdf(x, df), 0.025, 2000.0) for df in (2, 19)]
    crit.append(N01.inv_cdf(0.975))
    xs = np.linspace(-4.2, 4.2, 600)
    fig, ax = new(2.3)
    ax.plot(xs, [N01.pdf(x) for x in xs], color=INK, label="Standard normal")
    ax.plot(xs, t_pdf(xs, 19), color=INK, linestyle="--", label="t, 19 degrees of freedom")
    ax.plot(xs, t_pdf(xs, 2), color=INK, linestyle=":", label="t, 2 degrees of freedom")
    ax.set_xlabel("t or z")
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.legend(frameon=False, loc="upper right")
    return fig, {"fig.18.dfs": "2, 19", "fig.18.crit": j(f(c, 3) for c in crit)}


def fit(x, y):
    b = float(((x - x.mean()) * (y - y.mean())).sum() / ((x - x.mean()) ** 2).sum())
    a = float(y.mean() - b * x.mean())
    return a, b, y - (a + b * x)


def fig19(d):
    a, b, _ = fit(d.x, d.y)
    r = float(np.corrcoef(d.x, d.y)[0, 1])
    fig, ax = new(3.0)
    ax.plot(d.x, d.y, "o", markerfacecolor="none", markeredgecolor=MID, markersize=2.6, markeredgewidth=0.5)
    xs = np.array([1.5, 4.0])
    ax.plot(xs, a + b * xs, color=INK, linewidth=1.3)
    ax.set_xlabel("School grade at entry")
    ax.set_ylabel("College grade after 12 months")
    ax.set_xlim(1.4, 4.1)
    ax.set_ylim(0.9, 4.1)
    return fig, {"fig.19.n": str(len(d.x)), "fig.19.a": f(a, 3), "fig.19.b": f(b, 3), "fig.19.r": f(r, 3)}


def fig20(d):
    _, _, res = fit(d.x, d.y)
    fig, ax = new(2.4)
    ax.plot(d.x, res, "o", markerfacecolor="none", markeredgecolor=MID, markersize=2.6, markeredgewidth=0.5)
    ax.axhline(0, color=INK, linewidth=0.8)
    ax.set_xlabel("School grade at entry")
    ax.set_ylabel("Residual")
    ax.set_xlim(1.4, 4.1)
    return fig, {"fig.20.res_range": j([f(float(res.min()), 3), f(float(res.max()), 3)])}


def fig21(d):
    cuts = [225, 250, 275, 300, 325, 350]
    groups = [[] for _ in range(7)]
    for r in d.known:
        groups[sum(round(100 * float(r["entry_grade"])) >= c for c in cuts)].append(r)
    gm = [f(sum(float(r["entry_grade"]) for r in grp) / len(grp), 3) for grp in groups]
    sh = [f(sum(r["withdrew"] == "1" for r in grp) / len(grp), 3) for grp in groups]
    gx, sy = np.array([float(v) for v in gm]), np.array([float(v) for v in sh])
    lin = fit(gx, sy)[2]
    log = fit(gx, np.log(sy))[2]
    fig, axes = new(2.3, 2)
    for ax, res, title, lab in ((axes[0], lin, "The straight line's residuals", "Residual (share)"),
                                (axes[1], log, "The log line's residuals", "Residual (log of share)")):
        ax.plot(gx, res, "o-", color=INK, markersize=3.5, linewidth=0.6)
        ax.axhline(0, color=INK, linewidth=0.6, linestyle="--")
        ax.set_title(title)
        ax.set_xlabel("Mean school grade of the band")
        ax.set_ylabel(lab)
    return fig, {"fig.21.grade": j(gm), "fig.21.share": j(sh), "fig.21.lin.res": j(f(e, 3) for e in lin),
                 "fig.21.log.res": j(f(e, 3) for e in log)}


# ---------------------------------------------------------------- the practice test's figures

def givens():
    out = {}
    for r in rows("practice/givens.csv"):
        out[(r["item"], r["name"])] = r["value"]
    return out


def box_row(ax, row, v):
    s = ti_five(v)
    iqr = s[3] - s[1]
    lo, hi = s[1] - 1.5 * iqr, s[3] + 1.5 * iqr
    inside = [x for x in v if lo <= x <= hi]
    outs = sorted(x for x in v if x < lo or x > hi)
    ax.add_patch(plt.Rectangle((s[1], row - 0.22), s[3] - s[1], 0.44, facecolor=PALE, edgecolor=INK, linewidth=0.8))
    ax.plot([s[2], s[2]], [row - 0.22, row + 0.22], color=INK, linewidth=1.6)
    for a, b in ((s[1], min(inside)), (s[3], max(inside))):
        ax.plot([a, b], [row, row], color=INK, linewidth=0.8)
        ax.plot([b, b], [row - 0.1, row + 0.1], color=INK, linewidth=0.8)
    ax.plot(outs, [row] * len(outs), "o", markerfacecolor="white", markeredgecolor=INK, markersize=3.5)
    return s, [min(inside), max(inside)], outs


def stack(ax, values, y0=0.0, step=1.0, size=3.2, hollow=False):
    seen = {}
    for v in sorted(values):
        seen[v] = seen.get(v, 0) + 1
        ax.plot(v, y0 + seen[v] * step, "o", markersize=size, markeredgecolor=INK, markeredgewidth=0.7,
                markerfacecolor=("white" if hollow else INK))
    return max(seen.values())


def fig22(d):
    w = [float(r["minutes"]) for r in rows("practice/practice-waits.csv")]
    c = counts_in(w, 0, 4, 9)
    fig, ax = new(2.3)
    ax.bar(np.arange(0, 36, 4), c, width=4, align="edge", color=LIGHT, edgecolor=INK, linewidth=0.6)
    ax.set_xticks(range(0, 37, 4))
    ax.set_xlabel("Wait at the bus stop (minutes)")
    ax.set_ylabel("Riders")
    return fig, {"pt.fig22.bars": j(c), "pt.fig22.n": str(len(w)), "pt.fig22.top": g(max(w))}


def fig23(d):
    bat = rows("practice/practice-batteries.csv")
    fig, ax = new(1.9)
    facts = {}
    for row, mod in ((1, "A"), (0, "B")):
        v = [float(r["hours"]) for r in bat if r["model"] == mod]
        s, wh, outs = box_row(ax, row, v)
        facts.update({f"pt.fig23.{mod}.five": j(g(x) for x in s), f"pt.fig23.{mod}.whiskers": j(g(x) for x in wh),
                      f"pt.fig23.{mod}.out": j(g(x) for x in outs) if outs else "none"})
    ax.set_yticks([0, 1], ["Model B", "Model A"])
    ax.set_ylim(-0.6, 1.6)
    ax.set_xlim(10, 25)
    ax.set_xticks(range(10, 26, 1))
    ax.set_xlabel("Battery life (hours; an open dot is an outlier)")
    return fig, facts


def fig24(d):
    gv = givens()
    na, nb = int(gv[("q13", "n_a")]), int(gv[("q13", "n_b")])
    fa, fb = int(gv[("q13", "flowered_a")]), int(gv[("q13", "flowered_b")])
    tot = fa + fb
    ks = [int(r["flowered_a"]) for r in rows("practice/practice-flowering-sim.csv")]
    diffs = [k / na - (tot - k) / nb for k in ks]
    observed = fa / na - fb / nb
    grid = list(range(min(ks), max(ks) + 1))
    fig, ax = new(2.9)
    ax.axvline(observed, color=MID, linestyle="--", linewidth=0.8, zorder=0)
    top = stack(ax, [round(x, 6) for x in diffs], size=2.6)
    ax.text(observed + 0.006, top * 0.92, f"Observed\ndifference, {f(observed, 2)}", va="top", ha="left")
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_ylim(0, top + 2)
    ax.set_xlim(-0.33, 0.33)
    ticks = [round(-0.3 + 0.1 * i, 1) for i in range(7)]
    ax.set_xticks(ticks, [f(t, 2).replace("-", "\u2212") for t in ticks])
    ax.set_xlabel("Difference in shares that flowered, A minus B, in each of 200 reruns (one dot each)")
    return fig, {"pt.fig24.reruns": str(len(ks)), "pt.fig24.ge": str(sum(x >= observed - 1e-9 for x in diffs)),
                 "pt.fig24.diffs": j(f(k / na - (tot - k) / nb, 2) for k in grid),
                 "pt.fig24.counts": j(ks.count(k) for k in grid)}


def fig25(d):
    gv = givens()
    groups = (("under40", "Under 40"), ("over40", "40 and over"))
    srcs = (("phone", "Phone", PALE), ("tv", "TV", MID), ("print", "Print", DARK))
    fig, ax = new(2.4)
    facts = {}
    for i, (key, lab) in enumerate(groups):
        c = [int(gv[("q26", f"{key}_{s}")]) for s, _, _ in srcs]
        pct = [100 * x / sum(c) for x in c]
        facts[f"pt.fig25.{key}.pct"] = j(f(p, 1) for p in pct)
        bottom = 0
        for (s, name, shade), p in zip(srcs, pct):
            ax.bar(i, p, bottom=bottom, width=0.55, color=shade, edgecolor=INK, linewidth=0.5,
                   label=name if i == 0 else None)
            ax.text(i, bottom + p / 2, f"{f(p, 1)}%", ha="center", va="center",
                    color=("white" if shade == DARK else INK))
            bottom += p
    ax.set_xticks([0, 1], [lab for _, lab in groups])
    ax.set_xlim(-0.6, 2.2)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Percent of the age group")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1], frameon=False, loc="center right", title="Main news source")
    return fig, facts


def fig26(d):
    v = [float(r["minutes"]) for r in rows("practice/practice-checkout.csv")]
    fig, ax = new(1.3)
    stack(ax, v, size=5, hollow=True)
    ax.set_ylim(0.3, 2.2)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlim(0, 16)
    ax.set_xticks(range(0, 17, 1))
    ax.set_xlabel("Minutes at the checkout, one circle for each of the 12 customers")
    return fig, {"pt.fig26.values": j(g(x) for x in sorted(v))}


def fig27(d):
    ic = rows("practice/practice-iced.csv")
    x = np.array([float(r["high_f"]) for r in ic])
    y = np.array([float(r["drinks"]) for r in ic])
    a, b, _ = fit(x, y)
    fig, ax = new(2.8)
    ax.plot(x, y, "o", markerfacecolor="none", markeredgecolor=INK, markersize=4, markeredgewidth=0.7)
    xs = np.array([58.0, 97.0])
    ax.plot(xs, a + b * xs, color=INK, linewidth=1.0)
    ax.set_xlim(57, 98)
    ax.set_xlabel("The day's high (degrees Fahrenheit)")
    ax.set_ylabel("Iced drinks sold")
    return fig, {"pt.fig27.n": str(len(x)), "pt.fig27.line": j([f(a, 3), f(b, 3)]),
                 "pt.fig27.x_range": j([g(float(x.min())), g(float(x.max()))])}


def fig28(d):
    sp = rows("practice/practice-stopping.csv")
    x = np.array([float(r["speed_mph"]) for r in sp])
    y = np.array([float(r["distance_ft"]) for r in sp])
    _, _, res = fit(x, y)
    fig, ax = new(2.2)
    ax.plot(x, res, "o", color=INK, markersize=4)
    ax.axhline(0, color=INK, linewidth=0.7)
    ax.set_xticks(range(20, 80, 5))
    ax.set_xlabel("Speed (miles per hour)")
    ax.set_ylabel("Residual (feet)")
    return fig, {"pt.fig28.speeds": j(g(float(v)) for v in x), "pt.fig28.res": j(f(float(e), 1) for e in res)}


def fig29(d):
    cm = rows("practice/practice-commute.csv")
    fig, axes = plt.subplots(2, 1, figsize=(WIDTH, 2.6), layout="constrained", sharex=True)
    facts = {}
    for ax, mode, lab in ((axes[0], "bike", "Bike"), (axes[1], "bus", "Bus")):
        v = [float(r["minutes"]) for r in cm if r["mode"] == mode]
        top = stack(ax, v, size=4)
        ax.set_ylim(0.3, max(top, 5) + 0.7)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.set_ylabel(lab, rotation=0, ha="right", va="center")
        facts[f"pt.fig29.{mode}"] = j(g(x) for x in sorted(v))
    axes[1].set_xlim(5, 50)
    axes[1].set_xticks(range(5, 51, 5))
    axes[1].set_xlabel("One-way commute (minutes), one dot for each student")
    return fig, facts


FIGURES = [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10, fig11, fig12, fig13, fig14,
           fig15, fig16, fig17, fig18, fig19, fig20, fig21, fig22, fig23, fig24, fig25, fig26, fig27, fig28, fig29]


def main():
    write = "--write" in sys.argv
    want = expected()
    d = Data()
    problems, got = [], {}
    out = PNG if write else Path(tempfile.mkdtemp(prefix="figures-"))
    out.mkdir(parents=True, exist_ok=True)
    for i, make in enumerate(FIGURES, 1):
        fig, facts = make(d)
        img = finish(fig)
        img.save(out / f"fig{i:02d}.png", dpi=(DPI, DPI))
        for k, v in facts.items():
            if k in got:
                problems.append(f"{k} is drawn by two figures")
            got[k] = v
    for k in sorted(set(want) | set(got)):
        if want.get(k) != got.get(k):
            problems.append(f"{k}: the figure draws {got.get(k)!r}, expected {want.get(k)!r}")
    names = [f"fig{i:02d}.png" for i in range(1, len(FIGURES) + 1)]
    found = sorted(p.name for p in PNG.glob("*.png")) if PNG.is_dir() else []
    if found != names:
        problems.append(f"figures/png/ should hold {names[0]} to {names[-1]}, and holds {found}")
    for n in names:
        p = PNG / n
        if not p.is_file():
            continue
        im = Image.open(p)
        dpi = im.info.get("dpi", (0, 0))
        if im.mode != "L" or round(dpi[0]) != DPI or im.size[0] != int(WIDTH * DPI):
            problems.append(f"figures/png/{n}: should be grayscale, {DPI} ppi, {int(WIDTH * DPI)} pixels wide "
                            f"(it is {im.mode}, {dpi[0]:.0f} ppi, {im.size[0]} wide)")
    if problems:
        for p in problems:
            print("MISMATCH", p)
        print(f"FIGURES_FAILED mismatches={len(problems)}")
        sys.exit(1)
    where = "figures/png/ (update SHA256SUMS)" if write else f"a temporary folder ({out})"
    print(f"drew {len(FIGURES)} figures into {where}; matplotlib {matplotlib.__version__}")
    print(f"FIGURES_OK figures={len(FIGURES)} values={len(got)}")


if __name__ == "__main__":
    main()
