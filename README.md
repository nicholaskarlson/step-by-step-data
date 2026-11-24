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
| `SHA256SUMS` | The SHA-256 of every file in `data/`, `samples/`, and `calculator/` |
| `python/make_data.py` | Rebuilds the data files from the public Tonmick files in [predict](https://github.com/nicholaskarlson/predict) v1.0.1 |
| `python/make_samples.py` | Draws the samples, or with `--check` redraws them in memory and compares |
| `python/data_summary.py`, `r/data_summary.R` | Two independent routes, standard-library Python and base R, that summarize every file |
| `python/chapters_1_4.py`, `r/chapters_1_4.R` | The same two routes for every number in Chapters 1 to 4, their Try It answers, and their reviews |
| `python/chapters_5_8.py`, `r/chapters_5_8.R` | The same for Chapters 5 to 8, with exact values (hypergeometric, binomial, normal) where the book could have simulated, and a simulation check of three of them |
| `expected/` | The values both routes must give, character for character |
| `outline/` | The book's outline, chapter by chapter, with every number named and computed (`chapters-1-4.md` from D1, `chapters-5-8.md` from D2) |
| `run_all.py` | Runs the checks and compares the routes |
| `scripts/` | `check.sh` runs `run_all.py`; `apply-overlay.sh` and `pr.sh` apply the project's overlays as pull requests |

## Run the checks

Python 3.10 or later, standard library only. If R is installed (no add-on packages), the base R
route runs too; `--require-r` makes it required. The last line is `STEP_BY_STEP_DATA_OK`, with
the number of files and values checked, the samples, and the routes that ran.

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

GitHub Actions runs both routes on Ubuntu, Windows, and macOS, and the rebuild, on every push.

## Rights

The data files, the samples, SHUFFLE, and the outline are CC BY 4.0; the code is MIT (`LICENSE`). See
`LICENSES.md`. TI-84 Plus CE and TI Connect CE are trademarks of Texas Instruments, which is not
affiliated with, and does not endorse, this repository.

## Cite

Karlson, N. E. (2026). *step-by-step-data: Data and checks for Statistics Step by Step with a
Graphing Calculator, 2027 Edition* [Data set and code]. GitHub.
https://github.com/nicholaskarlson/step-by-step-data
