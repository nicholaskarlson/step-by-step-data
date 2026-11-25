# The figures

From overlay D4, the book's 21 figures, drawn by `draw.py` from the data files and the two
simulations, as grayscale PNGs, 6 inches wide at 300 ppi, for a black-and-white paperback. Every
number a figure draws or prints is in `expected/figures.csv`, computed twice (`python/figures.py`
and `r/figures.R`). `draw.py` recomputes each one from the data and stops unless it matches.

| # | File | Book section | What it shows | Values (`fig.NN.*`) |
| --- | --- | --- | --- | --- |
| 1 | `png/fig01.png` | 2.4 | Bar chart of how the first year ended: stayed, withdrew, transferred, consent withdrawn | counts 992, 173, 43, 11 |
| 2 | `png/fig02.png` | 2.4 | The same two bars (80 and 93 withdrawals), on an axis from 0 and on one from 75 | ratio 1.16; from 75 it looks 3.6 |
| 3 | `png/fig03.png` | 3.1 | Histogram of the offered students' support visits, bars 2 wide | the 13 bar counts |
| 4 | `png/fig04.png` | 3.1 | Dotplot of the joiners at each of the 16 colleges | 65 to 86 |
| 5 | `png/fig05.png` | 3.5, 3.7 | Modified box plots of visits, offered and not offered | five-number summaries, fences −4.5 and 7.5, whiskers to 7, 49 and 37 outliers |
| 6 | `png/fig06.png` | 5.2 | Segmented bars and side-by-side bars of how the year ended, by offer | the eight percentages |
| 7 | `png/fig07.png` | 5.4 | The exact randomization distribution of K, the withdrawals a shuffle deals to the offered group | mean 86.6; K ≤ 80: 0.1564; K ≥ 94: 0.1300; together 0.2864 |
| 8 | `png/fig08.png` | 6.1 | Probability histogram of a joiner's support visits | the nine probabilities |
| 9 | `png/fig09.png` | 6.4 | The binomial distribution with n = 10 and p = 0.13 | the eleven probabilities |
| 10 | `png/fig10.png` | 6.6 | School grades: a histogram with the normal model (3.010, 0.469), and the normal probability plot | the 11 bar counts; the plot's correlation 0.9971 |
| 11 | `png/fig11.png` | 6.6, 6.7 | The normal model, the area above 3.5, and the 90th percentile | 0.1481; 3.611 |
| 12 | `png/fig12.png` | 7.1 | p̂ in samples of 100 when p = 0.1432, as randBin(100,0.1432)/100 simulates it, with the normal model | SD 0.0350 |
| 13 | `png/fig13.png` | 7.2 | The 1,219 joiners' visits beside the means of 1,000 random samples of 30 | mean 2.362 against 2.350; SD 0.560 against 0.534 |
| 14 | `png/fig14.png` | 8.2 | Fifty 95% intervals from random samples of 100, and the true share 0.1432 | 49 of the 50 capture it; sample 26 does not |
| 15 | `png/fig15.png` | 8.5 | The standard normal curve with the goal test's p value shaded | z = 0.00; p = 0.5000 |
| 16 | `png/fig16.png` | 8.6 | Power: p̂ if H0 is true and under the truth, with the cutoff | cutoff 0.0913; power 0.0690 |
| 17 | `png/fig17.png` | 9.2 | Chi-square curves for 2, 5, and 10 degrees of freedom | 5.991 |
| 18 | `png/fig18.png` | 10.1 | t curves for 2 and 19 degrees of freedom, and the standard normal | 4.303, 2.093, 1.960 |
| 19 | `png/fig19.png` | 11.1, 11.2 | Scatterplot of college grade against school grade (555 students), with the least-squares line | 0.636 + 0.772x; r = 0.618 |
| 20 | `png/fig20.png` | 11.3 | The residual plot for that line | residuals from −1.592 to 1.480 |
| 21 | `png/fig21.png` | 11.5 | The seven grade bands: the straight line's residuals bend; the log line's do not | both sets of seven residuals |

## Draw or check them

`draw.py` needs matplotlib (`requirements.txt`; CI uses Python 3.12 and matplotlib 3.11.2, the
version that drew the committed files). Everything else here needs only the standard library.

```bash
python3 -m venv build/figenv
build/figenv/bin/pip install -r figures/requirements.txt
build/figenv/bin/python figures/draw.py            # check (what CI runs); the last line is FIGURES_OK
build/figenv/bin/python figures/draw.py --write    # redraw figures/png/, then update SHA256SUMS
```

On Python 3.10, install `matplotlib>=3.8` instead: the check compares numbers, not pixels, so any
recent matplotlib gives the same result. The committed PNGs are not redrawn in CI: `SHA256SUMS`
pins their bytes, and `draw.py` checks their size, resolution, and grayscale. The fonts are TeX
Gyre Pagella where installed (the book's font); elsewhere matplotlib falls back to DejaVu Serif,
which changes the pixels but not the check.
