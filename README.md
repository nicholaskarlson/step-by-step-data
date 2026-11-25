# step-by-step-data

Data, independent checks, and (from overlay D1) the chapter-by-chapter outline for
*Statistics Step by Step with a Graphing Calculator, 2027 Edition: A Complete First Course for
High School, Dual-Enrollment, and College-Bound Students* (Nicholas Elliott Karlson, NEKpress
Research; in preparation, free on Zenodo and in print from January 2027).

Every example in the book uses one fictional randomized study, the Tonmick mentoring study. A
college system invited 1,600 first-year students at 16 colleges; 1,219 joined, and within each
college about half were offered peer mentoring, by chance. The colleges recorded who left, how
often students visited support services, and their grades. All of it is invented for teaching.

## What is here

| Path | What it holds |
| --- | --- |
| `data/` | Seven CSV files: every student who joined, the 1,600 invited, smaller files for calculator lists, one file that loads six lists at once through TI Connect™ CE, and a dictionary of every column. `data/SOURCE.md` says where they come from |
| `calculator/SHUFFLE.8xp` | SHUFFLE, a short program for a TI-84 Plus CE™ graphing calculator that simulates the chance assignment |
| `samples/` | Three simple random samples of the joiners (100, 120, and 20), drawn once with seed 2027 for the book's one-sample examples; `data/SOURCE.md` says how |
| `simulations/` | Two simulations behind Figures 13 and 14 (from overlay D4): 1,000 random samples of 30 joiners and 50 random samples of 100, drawn once with seed 2027; `data/SOURCE.md` says how |
| `practice/` | The practice test's data (from overlay D5): nine small invented data sets for new settings, not Tonmick, drawn once with seed 2027, and `givens.csv`, the numbers the questions state, chosen by hand; `outline/practice-test.md` is the plan |
| `figures/` | The book's 29 figures (21 from overlay D4, 8 for the practice test from D5): `png/`, the grayscale PNGs; `draw.py`, which draws them with matplotlib and checks every number they draw; `README.md`, the list |
| `SHA256SUMS` | The SHA-256 of every file in `data/`, `samples/`, `simulations/`, `practice/`, `calculator/`, and `figures/png/` |
| `python/make_data.py` | Rebuilds the data files from the public Tonmick files in [predict](https://github.com/nicholaskarlson/predict) v1.0.1 |
| `python/make_samples.py` | Draws the samples, or with `--check` redraws them in memory and compares |
| `python/make_simulations.py` | Draws the two simulations the same way |
| `python/make_practice.py` | Draws the practice test's nine data sets, or with `--check` redraws them and compares |
| `python/data_summary.py`, `r/data_summary.R` | Two independent routes, standard-library Python and base R, that summarize every file |
| `python/chapters_1_4.py`, `r/chapters_1_4.R` | The same two routes for every number in Chapters 1 to 4, their Try It answers, and their reviews |
| `python/chapters_5_8.py`, `r/chapters_5_8.R` | The same for Chapters 5 to 8, with exact values (hypergeometric, binomial, normal) where the book could have simulated, and a simulation check of three of them |
| `python/chapters_9_12.py`, `r/chapters_9_12.R` | The same for Chapters 9 to 12: chi-square tests, t procedures on the samples of 20 and 120, regression, and what the eight investigations print; each figure the text works by hand must give the calculator's digits |
| `python/tables.py`, `r/tables.R` | The back matter's three tables: the standard normal table, t critical values, and chi-square critical values |
| `python/figures.py`, `r/figures.R` | Every number the chapters' 21 figures draw or print |
| `python/practice.py`, `r/practice.R` | Every number the practice test prints: its 40 multiple-choice questions, each wrong choice computed from the mistake it stands for, its four written questions, and its 8 figures |
| `expected/` | The values both routes must give, character for character |
| `outline/` | The book's outline, chapter by chapter, with every number named and computed (`chapters-1-4.md` from D1, `chapters-5-8.md` from D2, `chapters-9-12.md` from D3), and the practice test's plan (`practice-test.md` from D5) |
| `run_all.py` | Runs the checks and compares the routes |
| `scripts/` | `check.sh` runs `run_all.py`; `apply-overlay.sh` and `pr.sh` apply the project's overlays as pull requests |

## Run the checks

Python 3.10 or later, standard library only. If R is installed (no add-on packages), the base R
route runs too; `--require-r` makes it required. The last line is `STEP_BY_STEP_DATA_OK`, with
the number of files and values checked, the samples, simulations, and practice data sets, and the
routes that ran.

Ubuntu or macOS:

```bash
git clone https://github.com/nicholaskarlson/step-by-step-data.git
cd step-by-step-data
python3 run_all.py
```

Windows (PowerShell, with Python from python.org):

```powershell
git clone https://github.com/nicholaskarlson/step-by-step-data.git
cd step-by-step-data
py -3 run_all.py
```

To rebuild the data files from the Tonmick files and compare them byte for byte (the last line is
`CLASSROOM_DATA_OK files=7`):

```bash
git clone --depth 1 --branch v1.0.1 https://github.com/nicholaskarlson/predict.git build/predict
python3 -I python/make_data.py build/predict --check
```

GitHub Actions runs both routes on Ubuntu, Windows, and macOS, the rebuild, and the figures'
check, on every push.

The figures need matplotlib, so `run_all.py` does not draw them. To check them, see
`figures/README.md`; the last line is `FIGURES_OK`.

## Rights

The data files, the samples, the simulations, the practice data, the figures, SHUFFLE, and the outline are CC BY 4.0; the code is MIT (`LICENSE`). See
`LICENSES.md`. TI-84 Plus CE and TI Connect CE are trademarks of Texas Instruments, which is not
affiliated with, and does not endorse, this repository.

## Cite

Karlson, N. E. (2026). *step-by-step-data: Data and checks for Statistics Step by Step with a
Graphing Calculator, 2027 Edition* [Data set and code]. GitHub.
https://github.com/nicholaskarlson/step-by-step-data
