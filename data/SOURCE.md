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
