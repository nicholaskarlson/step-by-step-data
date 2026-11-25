# The outline

From overlay D1 on, this folder holds the outline of *Statistics Step by Step with a Graphing
Calculator, 2027 Edition*, chapter by chapter: for each section, the question its worked example
asks of the Tonmick data, the numbers the answer prints, the calculator inputs, and the values to
expect on the screen.

Each chapter's numbers come from two routes, standard-library Python and base R, that share no
code, and `run_all.py` requires them to agree with the values in `expected/`. The book's own
checks then require every printed number to match.

- D1: Chapters 1 to 4 (the calculator; data and variables; one quantitative variable; collecting data),
  with the chapter reviews and the three fixed samples: `chapters-1-4.md` (231 values).
- D2: Chapters 5 to 8 (two categorical variables and probability; random variables; sampling
  distributions; inference for proportions), with the chapter reviews and the items the outline
  left open: `chapters-5-8.md` (234 values).
- D3: Chapters 9 to 12 (chi-square tests; inference for means; regression; the eight investigations),
  with the chapter reviews, the items the outline left open, and the back matter's three tables:
  `chapters-9-12.md` (324 values, and 145 table rows).
