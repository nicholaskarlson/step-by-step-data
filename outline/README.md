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
- D4: the 21 figures for overlay C6a: `../figures/README.md` lists each figure, its section, and
  the values it draws (75 values in `expected/figures.csv`).
- D5: the practice test for overlay C6b, 40 multiple-choice and 4 written questions in new,
  invented settings, with every choice, trap, and model-answer value, and Figures 22 to 29:
  `practice-test.md` (391 values in `expected/practice.csv`, from the data in `../practice/`).
- D5c: values for overlay C6d, after two outside audits of the book. A TI-84 Plus CE list holds at
  most 999 values, so the calculator steps of Sections 3.4, 6.2, and 7.2 no longer join the two
  groups' lists into one of 1,219: L1's grades and 25L1 (`ch3.units.L1*`), and L2's SD of means of
  30 (`ch7.L2.sd30`). Two figures worked by hand from printed values were halfway values (25 × 0.469
  and 2.193 + 2 × 2.731), so their inputs print to four places (`ch3.entry.sx4`, `ch3.L4.mean4`,
  `ch3.L4.sx4`), and each route checks that they give the calculator's digits. Section 4.2's visit
  means by part-time study are now among the 1,208 whose outcome is known, as the shares beside
  them are (`ch4.visits.*_time.mean`: full-time 2.63, not 2.62). The practice test's plan maps
  Questions 14 and 16 to the sections the book names (5.6 to 5.8, and 6.2). `chapters_1_4.csv` has
  238 values and `chapters_5_8.csv` 235.
