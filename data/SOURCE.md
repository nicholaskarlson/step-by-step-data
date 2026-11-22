# Where the data files come from

Every file in `data/`, and `calculator/SHUFFLE.8xp`, is a copy, byte for byte, of the file of the
same name that the book's free classroom companion, *Establishing Facts in the Classroom*,
publishes with its record on Zenodo (December 2026). They were copied from that guide's working
repository at commit `86a5308775d7dcae217fe97488420008f0864002` (November 20, 2026).

`python/make_data.py` rebuilds the seven data files from the public Tonmick v1.0.0 files in
github.com/nicholaskarlson/predict at tag v1.0.1, and `--check` compares the rebuild with `data/`
byte for byte. Nothing is sampled or drawn at random: each file is a selection of rows and columns,
sorted by student ID. `SHA256SUMS` lists every file's SHA-256.

All of the data are fictional. The Tonmick study, its colleges, and its students are invented for
teaching.
