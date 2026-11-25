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

## The practice test's data (`practice/`, from overlay D5)

These data are not Tonmick data: every setting in the book's practice test is invented, and so
are its numbers, so a student practices reading an unfamiliar setting.

- **`givens.csv`** holds every number a question states (a sample size, a mean, a table's counts),
  chosen by hand. It is not drawn, and `make_practice.py` leaves it alone.
- **Nine data sets**, for the questions and figures that show data, were drawn once by
  `python/make_practice.py` on November 25, 2026, with seed 2027. Its models were written before
  the first run and not changed after; the questions were then written to fit what was drawn.
  The draw uses only `random.Random(2027).random()` and arithmetic every platform does alike: a
  standard normal value is the sum of twelve `random()` values minus 6, and a right-skewed value
  adds squares of such values. `make_practice.py` lists each model and the order of the draws.
- **What came out**, for the record: the waits are skewed right (mean 6.43, median 4.95); Model A
  has one high outlier and Model B none; 12 of the 200 reruns gave a difference of 0.20 or more
  (the exact share is 0.0548); the checkout sample has its outlier at 14.6; the runners' mean
  difference is 1.60 seconds (t = 1.18); the iced-drink line has r = 0.929; the stopping
  distances' residuals curve; the bus commutes have one outlier, 48; and the cups' mean fill is
  11.922 ounces (t = −2.23).

`make_practice.py --check` redraws the nine files in memory and compares byte for byte. Both
routes read them; neither redraws them.

| File | Rows | SHA-256 |
| --- | --- | --- |
| `practice/givens.csv` | 113 | `7c2a3a340135a1fc44c011d612545cf4265994be464eb29140cef1fa9a11931a` |
| `practice/practice-batteries.csv` | 60 | `0020a77ba616f5df3c98e03ac523161ef9c533320e69f885743134bd7c27dbc7` |
| `practice/practice-checkout.csv` | 12 | `4834cc260dd0772460669fa8b45d9287a91386c20d7db48bd4fde4181c622718` |
| `practice/practice-commute.csv` | 50 | `7ce40a76d56640b50ed00719347b6c9ec639362225d62508cc405e19a0b5f0db` |
| `practice/practice-fill.csv` | 20 | `495d03a5d905208438c886dba931b9e743bf2eb5df15c37d4ef2b6c31464df36` |
| `practice/practice-flowering-sim.csv` | 200 | `5058f61947ba10263e1523a78c52aff1aafbd917b5116f5b99eed431eb85453d` |
| `practice/practice-iced.csv` | 25 | `0e68fff06f4b204312c118eae7336d1f5c5b534fb3e7c4f244122215d70721c3` |
| `practice/practice-shoes.csv` | 10 | `46bec4aefe545d9a357ff059d1ff32c4cd15a1ec60d84ca0aa97718df5ef60b7` |
| `practice/practice-stopping.csv` | 12 | `8121cff804ccfbe301ac19323dccde3db5619e015330c9874adfd21b41755ebb` |
| `practice/practice-waits.csv` | 80 | `56bb756bcb596b764cb827063f971e8524a49467e9938053c6f51d90517016ff` |
