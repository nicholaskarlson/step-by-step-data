# The outline

From overlay D1, this folder holds the outline of *Statistics Step by Step with a Graphing
Calculator, 2027 Edition*, chapter by chapter: for each section, the question its worked example
asks of the Tonmick data, the numbers the answer prints, the calculator inputs, and the values to
expect on the screen.

Each chapter's numbers come from two routes, standard-library Python and base R, that share no
code, and `run_all.py` requires them to agree with the values in `expected/`. The book's own
checks then require every printed number to match.

- D1: Chapters 1 to 4 (the calculator; data and variables; one quantitative variable; collecting data).
- D2: Chapters 5 to 8 (probability; random variables; sampling distributions; inference for proportions).
- D3: Chapters 9 to 12 (chi-square tests; inference for means; regression; the eight investigations).
