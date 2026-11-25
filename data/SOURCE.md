# Where the data files come from

Every file in `data/`, and `calculator/SHUFFLE.8xp`, is a copy, byte for byte, of the file of the
same name that the book's free classroom companion, *Establishing Facts in the Classroom*,
published with its version 1.0 on Zenodo on November 23, 2026
(https://doi.org/10.5281/zenodo.24391659). The files there have the same bytes. They were copied from that guide's working
repository at commit `86a5308775d7dcae217fe97488420008f0864002` (November 20, 2026).

`python/make_data.py` rebuilds the seven data files from the public Tonmick v1.0.0 files in
github.com/nicholaskarlson/predict at tag v1.0.1, and `--check` compares the rebuild with `data/`
byte for byte. Nothing is sampled or drawn at random: each file is a selection of rows and columns,
sorted by student ID. `SHA256SUMS` lists every file's SHA-256.

All of the data are fictional. The Tonmick study, its colleges, and its students are invented for
teaching.

## The three fixed samples (`samples/`, from overlay D1)

`python/make_samples.py` drew three simple random samples of the Tonmick joiners, once, on
November 24, 2026. The joiners serve as a population whose true values are known, so the book's
one-sample intervals and tests can be checked against the truth.

- **Seed:** 2027, fixed before any sample was drawn. No sample is redrawn to get nicer numbers.
- **Generator:** the only randomness is `random.Random(2027).random()`, whose sequence Python
  guarantees across versions.
- **Order:** the three samples come from one generator, in this order:
  1. `tonmick-sample-100.csv`: 100 of the 1,208 joiners whose outcome is known;
  2. `tonmick-sample-120.csv`: 120 of the same 1,208, drawn separately;
  3. `tonmick-sample-20.csv`: 20 of the 1,116 joiners with a 12-month college grade.
- **Method:** the eligible students are sorted by student ID. A partial Fisher-Yates shuffle
  picks k of them: for i = 0, 1, ..., k-1, j = i + int(u × (m − i)), with u the next random()
  value and m the number eligible, and positions i and j swap.
- **Columns:** each file holds `draw` (1 to k, in draw order) and the columns of
  `tonmick-classroom.csv`.

`make_samples.py --check` redraws them in memory and compares byte for byte. The base R route
does not redraw them: it checks that every row is a row of `tonmick-classroom.csv`, that no
student repeats, and each file's size and MD5. `SHA256SUMS` lists their SHA-256:

| File | Rows | SHA-256 |
| --- | --- | --- |
| `samples/tonmick-sample-100.csv` | 100 | `3db31dce2c1fa5dd2256efb7930ad2059c7ef7eb990905c32eb885ebfb6720ce` |
| `samples/tonmick-sample-120.csv` | 120 | `a94bb6caa6bac9a603146b40d600736c9e86b4e5920653538990f264da230d08` |
| `samples/tonmick-sample-20.csv` | 20 | `c8059c953f18c90ea7ec9dad5bbf60dc8cf3ebb069fa6db979acb377e1327802` |

## The two simulations (`simulations/`, from overlay D4)

`python/make_simulations.py` drew two simulations of the Tonmick joiners, once, on November 25,
2026, for the book's Figures 13 and 14 (`figures/README.md`).

- **Seed:** 2027, the samples' seed, fixed before anything was drawn. Nothing is redrawn to get a
  nicer picture.
- **Generator:** one `random.Random(2027)`, separate from the samples' generator, drawing in this
  order:
  1. `tonmick-sim-means-30.csv`: 1,000 simple random samples of 30 from all 1,219 joiners. Each row
     holds `rep` and the total of the 30 students' support visits (`visits_total`); the sample
     mean is `visits_total / 30`.
  2. `tonmick-sim-samples-100.csv`: 50 simple random samples of 100 from the 1,208 joiners whose
     outcome is known. Each row holds `rep` and how many of the 100 withdrew (`withdrew`).
- **Method:** each sample is drawn as the samples are, by a partial Fisher-Yates shuffle of the
  eligible students sorted by student ID, starting afresh from the sorted list each time.

`make_simulations.py --check` redraws them in memory and compares byte for byte. The base R route
does not redraw them: it checks each file's rows and ranges and summarizes them. Both routes check
that the 1,000 means agree with the model within four standard errors: their mean is 2.362
(the population mean is 2.350), and their SD is 0.560 (0.528 for samples drawn without
replacement), a little high but inside the tolerance. 49 of the 50 intervals capture the true
share, 0.1432.

| File | Rows | SHA-256 |
| --- | --- | --- |
| `simulations/tonmick-sim-means-30.csv` | 1,000 | `99353e7e62076f737c246521308e19c3ad20ecde667e5366e434a7acfc0ec6e5` |
| `simulations/tonmick-sim-samples-100.csv` | 50 | `30de7da987963e20d7c3865cc6fb5eb5a27a1e92559f0418deb9450966f84775` |
