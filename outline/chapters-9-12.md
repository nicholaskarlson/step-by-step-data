# Chapters 9 to 12 and the tables: the outline and its numbers

This file is the source for the book's Chapters 9 to 12 and the three tables in its back matter.
For each section it gives the worked example, the values the text prints, the calculator steps
and screens, and the Try It answer; for Chapters 9 to 11, the one-page review; for Chapter 12, what
each investigation prints that earlier chapters have not. Every value is named as in
`expected/chapters_9_12.csv` or `expected/tables.csv`. `python/chapters_9_12.py` and
`python/tables.py` (standard-library Python) and `r/chapters_9_12.R` and `r/tables.R` (base R)
compute each one independently, and `run_all.py` requires both routes to match the expected files
character for character. Values appear here as the book prints them, except that the book uses a
true minus sign (−) where this file has a hyphen. Names from earlier chapters
(`expected/chapters_1_4.csv`, `expected/chapters_5_8.csv`) are used where a number was already
printed there.

The data are fictional: the Tonmick study is invented for teaching.

Conventions, beyond those of Chapters 1 to 8:

- **p values have four places**, as in Chapter 8 (0.5340, not 0.534), and chi-square statistics
  two in the text and four where a screen is quoted (χ² = 1.25; the screen shows 1.2549).
- **Arithmetic shown by hand gives what the calculator gives.** Where the text works a figure by
  hand from printed numbers, the printed inputs carry enough digits for the last digit to agree
  with the command's. Both routes compute each hand figure from the printed inputs and stop if it
  differs from the command's value (`SAME` in the Python route, `same` in R). The pairs are listed
  under each section.
- **Lists a reader types in are used as printed**: the sixteen colleges' counts, the sample of 20,
  and Section 11.5's groups. Named lists keep L1 to L6 intact, as Sections 3.4 and 6.1 do with
  GRADE and VIS2 (suggested names below; C4 and C5 decide).
- **Quartiles are the TI-84's**, and a fence that falls on a half-hundredth is printed in full
  (2.0175, not 2.018).
- **The distributions.** Route 1 computes t and chi-square from the regularized incomplete beta
  and gamma functions, which Python's standard library lacks, and inverts them by bisection;
  route 2 uses base R's pt, qt, pchisq, and qchisq.

## Settled in D3 (the outline's open items, and its corrections)

| Item | Outline (November 22) | Settled |
| --- | --- | --- |
| 9.1's Try it | Why Investigation 6's two-way test fits better | χ² = 5.09, p = 0.0240 against the invited 40%; the joiners are most of the invited, not a sample of them, so the right comparison is joiners against non-joiners (`ch9.gof.try.*`) |
| 9.3's sample of 120 | Drawn by D3; smallest expected count about 6.4 | Drawn in D1. Part-time by withdrawal: 9 of 77 full-time and 10 of 43 part-time withdrew; smallest expected count 6.81; χ² = 2.77, p = 0.0960, so the sample does not show an association, although the 1,208 it came from have one (9.5% against 22.5%): a Type II error, which links to 8.6 (`ch9.ind.*`) |
| 10.2's sample of 20 | Drawn by D3 | Drawn in D1, from the 1,116 with a college grade. School grades: x̄ = 3.056, Sx = 0.432, 95% interval (2.854, 3.258); the 1,116's mean, 3.016, is inside (`ch10.s20.*`) |
| 10.3's stated figure | D3 picks one the data do not settle at a glance | A planner's figure of 2.90, two-sided: t = 1.62, p = 0.1226 (one-sided 0.0613). The true mean is 3.016, so H0 is false and the test misses it: another Type II error (`ch10.test.*`) |
| 10.4's lists | Must not overwrite L1 to L6 | Named lists: SCHL and COLL for the 20 grades, DIFF = COLL − SCHL. Mean difference 0.101, t = 1.00, p = 0.3297, interval (−0.110, 0.312) (`ch10.pair.*`) |
| 10.5's by-hand df | Use 608 | 608: t* = 1.964, margin 0.329, the same interval to three places, p = 0.0614 against the calculator's 0.0611 (`ch10.two.hand.*`) |
| 11.4's offered line | LinReg on L1 needs the classroom file (D3 decides) | Printed, not keyed: for the 561 offered students with a college grade, predicted college grade = 0.943 + 0.691 × (school grade), r = 0.590, from `tonmick-classroom.csv`; the six lists hold no college grades for them (`ch11.offered.*`) |
| 11.5's groups | Eight groups of 151 | Seven groups cut by school grade, so no tie falls across a boundary: below 2.25, four bands a quarter of a grade wide, 3.25 to 3.5, and 3.5 and above (the top quarter alone, 81 students with 5 withdrawals, is too small to be steady). Shares 0.368 down to 0.048 (`ch11.bands.*`) |
| 11.3's residual | Rebuilt by D3 | S1000017: 3.370 from Y1, 3.369 by hand from the rounded line; residual 0.300 (`ch11.student.*`) |
| Investigations 3 and 4 | 0.286; −0.021 and −0.026 with three places | Four places, as the book's Chapters 5 and 8 print them: 0.2864 (`ch5.shuffle.p`); within colleges 0.2843; the 11 unknowns counted as staying, −0.0211 (−0.0603, 0.0181), p = 0.2913, and as withdrawing, −0.0260 (−0.0662, 0.0142), p = 0.2048 (`ch12.inv4.*`, `ch8.sens.*`) |
| The tables | "Computed by step-by-step-data by both routes" | Standard normal to four places for z from −3.49 to 3.49; t* for eight tail areas and 36 df rows plus z*; chi-square for eight tail areas and 35 df rows (`table.*`) |

## Chapter 9. Chi-Square Tests

| Section | Worked example and values | On the TI-84 Plus CE | Try it (answer) |
| --- | --- | --- | --- |
| 9.1 Goodness of Fit (Going further) | Each of the 16 colleges invited 100 students. Joiners, in college order TC01 to TC36: 71, 75, 82, 83, 77, 77, 86, 83, 71, 80, 65, 76, 75, 74, 72, 72 (`ch9.gof.colleges`, `ch9.gof.counts`). Equal shares expect 1,219 ÷ 16 = 76.19 (`ch9.gof.expected`). TC25's part: (65 − 76.19)² ÷ 76.19 = 1.64; TC15's 1.26 (`ch9.gof.low.part`, `.high.part`). χ² = 6.04 with 15 df, p = 0.9790: chance alone gives counts this far from equal 97.9% of the time (`ch9.gof.chi2`, `.df`, `.p`, `.p.pct`). The 5% critical value for 15 df is 24.996 (`ch9.gof.crit`) | The counts in a named list, JOIN; 0JOIN+1219/16 → EXPT gives 76.1875 sixteen times (`ch9.gof.expected.screen`). χ²GOF-Test, Observed JOIN, Expected EXPT, df 15: χ² = 6.0435, p = 0.9790, and a CNTRB list (`ch9.gof.chi2.screen`) | 449 of the 1,219 joiners studied part-time, against 40% of those invited: expected 487.6 and 731.4, χ² = 5.09 with 1 df, p = 0.0240 (`ch9.gof.try.*`). Fewer joiners studied part-time than the invited mix predicts, but the joiners are most of the invited, not a sample from them; Investigation 6 compares joiners with non-joiners |
| 9.2 Homogeneity | How the year ended, by offer, among the 1,208 known outcomes: offered 504, 80, 21 (83.3%, 13.2%, 3.5%); not offered 488, 93, 22 (80.9%, 15.4%, 3.6%) (`ch9.hom.*.counts`, `.pct`). All 1,208: 992, 173, 43 (82.1%, 14.3%, 3.6%) (`ch9.hom.totals*`). Expected = row total × column total ÷ table total: 605 × 992 ÷ 1,208 = 496.82; offered 496.82, 86.64, 21.54, not offered 495.18, 86.36, 21.46; the smallest is 21.46 (`ch9.hom.*.expected`, `.expected.min`). Each cell's part: 0.10, 0.51, 0.01 in both rows (`ch9.hom.*.parts`). χ² = 1.25 with 2 df, p = 0.5340 (`ch9.hom.chi2`, `.df`, `.p`); the 5% critical value for 2 df is 5.991 (`ch9.hom.crit`). Collapsed to withdrew or not: χ² = 1.19 = (−1.0913)², p = 0.2751, Section 8.8's z test (`ch9.hom.two.*`). Conditions: a randomized experiment, and every expected count more than 5; df = (rows − 1)(columns − 1) | Matrix [A] 2 × 3 (the six counts, no totals); χ²-Test, Observed [A], Expected [B]: χ² = 1.2549, p = 0.5340, df = 2 (`ch9.hom.chi2.screen`); [B] holds the expected counts | Which cells add most? The two withdrawal cells, 0.51 each: 80 against 86.64 expected and 93 against 86.36 |
| 9.3 Independence | One random sample, two variables: the sample of 120 (Section 4.4; drawn in D1) from the 1,208 known outcomes, by part-time study and withdrawal. Full-time 9 withdrew and 68 did not (77); part-time 10 and 33 (43); 19 and 101 in all (`ch9.ind.*`). Withdrew: 11.7% of full-time, 23.3% of part-time. Conditions: random; 120 is under 10% of 1,208, which is 120.8 (`ch7.ten_pct`); expected counts 12.19, 64.81, 6.81, 36.19, the smallest 6.81 (`ch9.ind.*.expected`, `.expected.min`). χ² = 2.77 with 1 df, p = 0.0960: at α = 0.05 the sample does not show an association (`ch9.ind.chi2`, `.p`). In all 1,208 there is one: 9.5% of full-time and 22.5% of part-time students withdrew (`ch9.ind.pop.*`), so this test made a Type II error (Section 8.6). Two contrasts: the offer against part-time study among all 1,219, χ² = 1.32, p = 0.2501, checks the random assignment (`ch9.ind.balance.*`); joining against part-time study among the 1,600 invited, χ² = 21.39, p = 3.75 × 10⁻⁶, is a homogeneity test by its design, since the plan fixed 960 full-time and 640 part-time invitations (`ch9.ind.join.*`; Investigation 6) | Matrix [A] 2 × 2: 9, 68, 10, 33; χ²-Test: χ² = 2.7704, p = 0.0960 (`ch9.ind.chi2.screen`) | Homogeneity or independence? Decide from how the data were collected: one sample with two variables recorded (independence), or groups fixed in advance (homogeneity); the arithmetic is the same |

**Hand figures checked against the command:** (−1.0913)² = 1.19 (`ch9.hom.two.chi2`); 4.6246² = 21.39
(`ch9.ind.join.z2`).

**Chapter 9 review:**

1. *(Multiple choice; no numbers.)* Students at one school are surveyed once, and each is asked two
   questions. Which test fits? (A) goodness of fit (B) homogeneity (C) independence (D) a
   two-sample t test. Answer: (C).
2. *(Multiple choice; fictional.)* A four-section spinner gives 25, 18, 22, 15 in 80 spins. χ² for
   equal sections? (A) 2.90 (B) 0.725 (C) 58.00 (D) 11.60. Answer: (A); each expected count is 20,
   and p = 0.4073 with 3 df (`ch9.review.spin.*`; (B) divides by 80 instead of 20).
3. *(Multiple choice; no numbers.)* The degrees of freedom for a 3 × 4 table: (A) 12 (B) 11 (C) 7
   (D) 6. Answer: (D).
4. *(Multiple choice; no numbers.)* A two-way table has an expected count of 3.2. The best next
   step: (A) report the p value anyway (B) the large-counts condition fails, so do not trust the
   chi-square p value (C) use 1 df (D) drop that cell. Answer: (B).
5. *(Written; Tonmick, the sample of 100.)* In Chapter 8's sample of 100, 9 of the 51 offered and
   6 of the 49 not offered withdrew (`ch9.review.s100.*`).
   - Expected counts 7.65, 43.35, 7.35, 41.65; the smallest is 7.35, so the condition holds.
   - χ² = 0.57 with 1 df, p = 0.4495: no evidence in this sample that withdrawal depends on the
     offer. Is this homogeneity or independence? Independence: one random sample, two variables.
6. *(Written; fictional; homogeneity.)* Three high schools each survey 150 students chosen at
   random about holding a paid job: 54, 39, and 63 say yes (36.0%, 26.0%, 42.0%).
   - Expected counts 52.00 yes and 98.00 no at each school; χ² = 8.65 with 2 df, p = 0.0132
     (`ch9.review.jobs.*`).
   - At α = 0.05 the share with a job differs among the three schools.

## Chapter 10. Inference for Means

| Section | Worked example and values | On the TI-84 Plus CE | Try it (answer) |
| --- | --- | --- | --- |
| 10.1 The t Distributions | Using s for σ calls for t: symmetric, heavier tails than the normal, closer to it as df grow. t* = 2.093 for 19 df at 95%, against z* = 1.960; 1.964 for 608 df (`ch10.tstar.19`, `.608`, `ch8.zstar`) | invT(0.975,19) = 2.0930 (`ch10.tstar.19.screen`) | t* for 9 df: larger, 2.262 (`ch10.tstar.9`) |
| 10.2 A Confidence Interval for a Mean | The sample of 20 (drawn in D1 from the 1,116 with a college grade), school grades in draw order: 3.52, 3.3, 3.81, 2.37, 2.83, 3.31, 3.19, 3.25, 2.85, 2.85, 3.17, 3.14, 2.75, 3.52, 3.7, 2.1, 3.1, 2.61, 2.72, 3.03 (`ch10.s20.school`). x̄ = 3.056, Sx = 0.432 (`samples.20.entry.mean`, `ch10.s20.school.sx`). Conditions: random; 20 is under 10% of 1,116, which is 111.6 (`ch10.pop.ten_pct`); n < 30, so check the shape: five-number summary 2.1, 2.79, 3.12, 3.305, 3.81, fences 2.0175 and 4.0775, no outliers (`ch10.s20.school.five`, `.fences`, `.outliers`), and a normal probability plot that is close to straight. SE = 0.43177 ÷ √20 = 0.0965; margin 2.093 × 0.0965 = 0.202; interval 3.056 ± 0.202, (2.854, 3.258) (`ch10.s20.school.se`, `.me`, `.low`, `.high`). The 1,116's true mean, 3.016, is inside (`samples.population.college_grade.entry.mean`) | The 20 grades in a named list, SCHL. TInterval, Inpt Data, List SCHL, C-Level 0.95: (2.8539, 3.2581), x̄ = 3.056, Sx = 0.43177, n = 20 (`ch10.s20.school.*.screen`, `.sx.screen`) | Why visits, so skewed, fail the check at n = 20: the same 20 students' visits, 0, 1, 1, 2, 1, 8, 2, 1, 0, 1, 0, 1, 2, 1, 8, 1, 0, 2, 0, 1, have five-number summary 0, 0.5, 1, 2, 8 and upper fence 4.25, so the two 8s are outliers (`ch10.s20.visits*`) |
| 10.3 A Test for a Mean | A planner assumes joiners like these entered with a mean school grade of 2.90 (`ch10.test.mu0`). Parameter μ, the 1,116's mean; H0: μ = 2.90, Ha: μ ≠ 2.90; conditions as in 10.2. t = (3.056 − 2.90) ÷ 0.0965 = 1.62 with 19 df, p = 0.1226 (`ch10.test.t`, `.p`). At α = 0.05 the sample does not contradict 2.90. The true mean is 3.016, so H0 is false: a Type II error (Section 8.6) | T-Test, Inpt Data, μ0 2.90, List SCHL, μ ≠ μ0: t = 1.6158, p = 0.1226 (`ch10.test.t.screen`) | In one sentence: the data are consistent with 2.90, which is not the same as showing it; a one-sided test (Ha: μ > 2.90) gives p = 0.0613, still above 0.05 (`ch10.test.p.one`) |
| 10.4 Paired Data | The same 20 students: college grade minus school grade, in that order: 0.48, 0.34, −0.03, 0.13, −0.39, −0.78, 0.66, 0.17, 0.28, −0.13, −0.21, −0.82, 0.01, 0.48, 0.09, 0.46, −0.43, 0.48, 0.78, 0.45; 13 are positive (`ch10.pair.d`, `.positive`). Conditions on the differences: five-number summary −0.82, −0.17, 0.15, 0.47, 0.78, fences −1.13 and 1.43, no outliers (`ch10.pair.five`, `.fences`, `.outliers`). Mean 0.101, SD 0.4515, SE 0.4515 ÷ √20 = 0.1010 (`ch10.pair.mean`, `.sd4`, `.se`); t = 0.101 ÷ 0.1010 = 1.00, p = 0.3297; interval 0.101 ± 2.093 × 0.1010 = 0.101 ± 0.211, (−0.110, 0.312) (`ch10.pair.t`, `.p`, `.me`, `.low`, `.high`). For all 555 students not offered who have both grades, the mean difference is −0.048 (SD 0.460) (`ch10.pair.not_offered.*`); for all 1,116, −0.020 (`ch10.pair.all.mean`): a description of change, not an effect of anything | The college grades in COLL; COLL − SCHL → DIFF. TInterval and T-Test (μ0 0) on DIFF | Why a two-sample test on SCHL and COLL would be wrong: the two lists are the same students, not two groups. Treated as two groups, the SE is 0.1604 instead of 0.1010, t = 0.63, p = 0.5331 (`ch10.pair.wrong.*`) |
| 10.5 Comparing Two Means | Visits, offered minus not offered: 0.314 (`ch3.gap`); SE 0.1675 (`ch7.means.se`); t = 1.87 with 1197.07 df, p = 0.0611 (`ch1.ex8.*`); 95% interval (−0.015, 0.643) (`ch10.two.low`, `.high`). Conditions: a randomized experiment, and n ≥ 30 in both groups (609 and 610), so the skew does not matter. The df lies between 608 and 1,217 (`ch10.two.df.small`, `.df.sum`); by hand use 608: t* = 1.964, margin 1.964 × 0.1675 = 0.329, the same interval, and p = 0.0614 (`ch10.two.hand.*`). Pooled: t = 1.87, p = 0.0611, the same here (`ch10.two.pooled.*`) | 2-SampTInt and 2-SampTTest, Inpt Data, List1 L2, List2 L4, Pooled No; or Inpt Stats with 2.507389, 3.104596, 609 and 2.193443, 2.731310, 610 (`ch10.two.*.summary`) | The claim the evidence supports: an estimated 0.314 more visits per student, from 0.015 fewer to 0.643 more; the study cannot rule out no effect, nor nearly two-thirds of a visit more |
| 10.6 Choosing a Procedure | One table for Chapters 8 to 11 (no new numbers) | The menu path for each command | Five short descriptions to name (no new numbers) |

**Hand figures checked against the command:** 0.43177 ÷ √20 = 0.0965; 2.093 × 0.0965 = 0.202;
(3.056 − 2.90) ÷ 0.0965 = 1.62; 0.4515 ÷ √20 = 0.1010; 0.101 ÷ 0.1010 = 1.00; 2.093 × 0.1010 =
0.211; 1.964 × 0.1675 = 0.329. Use these printed inputs: 0.432 ÷ √20 gives 0.0966, and 0.451 ÷ √20
gives 0.1008.

**Chapter 10 review:**

1. *(Multiple choice; no numbers.)* Why t and not z for a mean? (A) the sample is small (B) s
   estimates σ (C) the data are skewed (D) the population is large. Answer: (B).
2. *(Multiple choice.)* t* for a 95% interval from 12 observations: (A) 2.201 (B) 1.960 (C) 2.179
   (D) 1.796. Answer: (A), 11 df (`ch10.review.tstar.11`; (C) uses 12 df, (D) is 90%).
3. *(Multiple choice; fictional; summary numbers.)* n = 16, x̄ = 52.3, s = 6.4. The 95% interval:
   (A) (48.89, 55.71) (B) (49.16, 55.44) (C) (38.66, 65.94) (D) (48.91, 55.69). Answer: (A); SE =
   6.4 ÷ 4 = 1.6, t* = 2.131, margin 3.41 (`ch10.review.ci*`; (B) uses z*, (C) uses s for SE, (D)
   uses 16 df).
4. *(Multiple choice; no numbers.)* Which is paired? (A) two classes' test scores (B) each
   student's score before and after a course (C) boys' and girls' heights (D) two random samples
   of towns. Answer: (B).
5. *(Written; Tonmick, the sample of 20.)* The same 20 students' college grades (COLL).
   - Shape: five-number summary 2.32, 2.615, 3.11, 3.71, 4, fences 0.9725 and 5.3525, no
     outliers (`ch10.review.college.five`, `.fences`).
   - x̄ = 3.157, Sx = 0.573, SE = 0.573 ÷ √20 = 0.1281, margin 2.093 × 0.1281 = 0.268, interval
     (2.889, 3.425) (`ch10.review.college.*`).
   - The 1,116's true mean college grade is 2.996 (`ch10.review.college.true`). Did the interval
     capture it? Yes.
6. *(Written; fictional; two means.)* Students randomly assigned to two study methods: n1 = 35, x̄1
   = 78.4, s1 = 8.2; n2 = 32, x̄2 = 74.1, s2 = 9.5.
   - Difference 4.3, SE 2.1775, t = 4.3 ÷ 2.1775 = 1.97 with 61.57 df, p = 0.0528 (two-sided)
     (`ch10.review.methods.*`).
   - The 95% interval, (−0.05, 8.65), just includes 0; at α = 0.05 the evidence falls short.

## Chapter 11. Regression

All of Sections 11.1 to 11.4 and 11.6 use the 555 students not offered who have a college grade,
lists L5 and L6 (`ch11.n`).

| Section | Worked example and values | On the TI-84 Plus CE | Try it (answer) |
| --- | --- | --- | --- |
| 11.1 Scatterplots and Correlation | Positive, roughly linear, moderate: r = 0.618 (`ch11.r`). Both grades stop at 4.0: 12 students entered with 4.0, and 20 have a college grade of 4.0 (`ch11.ceiling.*`) | Plot1 scatterplot of L5 and L6; LinReg shows r with STAT DIAGNOSTICS ON | With the axes swapped, r is the same, 0.618 |
| 11.2 The Least-Squares Line | Predicted college grade = 0.636 + 0.772 × (school grade); r² = 0.382, so the line accounts for about 38% of the variation in college grades (`ch11.a`, `.b`, `.r2`, `.r2.pct`). Slope = r × sy ÷ sx = 0.6184 × 0.5704 ÷ 0.4568 = 0.772 (`ch11.r4`, `.sy`, `.sx`, `.slope.hand`). The line passes through the means: 0.636 + 0.772 × 3.001 = 2.953 (`ch11.xbar`, `.ybar`, `.through`). Regression to the mean: the 79 who entered at 3.5 or more averaged 3.745, then 3.515; the 72 below 2.5 averaged 2.273, then 2.400 (`ch11.rtm.*`) | LinReg(a+bx) L5, L6, Y1 | A school grade of 3.0: Y1(3) gives 2.953; by hand, 0.636 + 0.772 × 3.0 = 2.952 (`ch11.try.y1`, `.try.hand`). The text says which it prints and that the rounded line can differ in the last digit |
| 11.3 Residuals | S1000017: school 3.54, college 3.67 (`ch11.student*`); Y1(3.54) = 3.370, or 3.369 by hand; residual 3.67 − 3.370 = 0.300, so the line underpredicts this student (`ch11.student.pred`, `.pred.hand`, `.res`). The residual plot shows no curve, a little less spread near 4.0. s = 0.449 (Going further) (`ch11.s`). Residuals run from −1.592 to 1.480 (`ch11.res.*`) | RESID from 2nd stat (list); Plot1 with Ylist RESID | Is a residual of −0.9 unusual? −0.9 ÷ 0.449 = −2.00 s; 12 of the 555 are −0.9 or lower (`ch11.try.res.*`) |
| 11.4 Prediction and Its Limits | School grades run from 1.5 to 4 (`ch11.range`); interpolation inside, extrapolation outside: 1.0 gives 1.408, by hand or by Y1 (`ch11.pred.1`). A line for prediction, not cause. The line for the 561 offered students with a college grade, from the classroom file: 0.943 + 0.691 × (school grade), r = 0.590 (`ch11.offered.*`). Who has no college grade: 55 of the 610 not offered (39 withdrew, 9 transferred, 7 withdrew consent); of the 555 with one, 54 withdrew and 13 transferred, their grade recorded when they left (`ch11.nograde.*`, `ch11.left.*`) | Y1(1.0) on the home screen (no new command) | Why the intercept means nothing here: 0.636 is the prediction for a school grade of 0, far below any student |
| 11.5 Departures from Linearity (Going further) | Withdrawal share by school grade, among the 1,208 known outcomes, in seven groups: below 2.25, 2.25 to 2.5, 2.5 to 2.75, 2.75 to 3.0, 3.0 to 3.25, 3.25 to 3.5, and 3.5 and above (each band includes its lower cut). Counts 57, 99, 207, 238, 245, 176, 186; withdrew 21, 26, 43, 33, 27, 14, 9 (`ch11.bands.n`, `.withdrew`). Mean school grade 2.033, 2.383, 2.628, 2.878, 3.116, 3.369, 3.740; share 0.368, 0.263, 0.208, 0.139, 0.110, 0.080, 0.048 (36.8% down to 4.8%) (`ch11.bands.grade`, `.share`, `.pct`). A line on the typed values: share = 0.713 − 0.187 × grade, r = −0.971 (`ch11.bands.lin.*`), yet the residuals bend: 0.036, −0.004, −0.013, −0.035, −0.019, −0.002, 0.036, positive at both ends and negative in between (`ch11.bands.lin.res`, `.signs`). The log of the share, −1.000 down to −3.037 (`ch11.bands.ln`), is close to a line: ln(share) = 1.515 − 1.204 × grade, r = −0.997, residuals with no pattern (`ch11.bands.log.*`). On that model each half grade multiplies the share by 0.55, and a school grade of 3.0 predicts a share of 0.123 (`ch11.bands.log.ratio`, `.at3`) | The seven means in GRD and the shares in WD (named lists); LinReg(a+bx) GRD, WD; RESID plot; ln(WD) → LNWD; LinReg(a+bx) GRD, LNWD | Which plot shows the better fit? The log model's: its residuals scatter without a bend, while the straight line's are positive at both ends; r alone (−0.971) would not have shown the curve |
| 11.6 Inference for a Slope (Going further) | Slope 0.772, SE 0.0417, t = 18.50 with 553 df, p < 0.0001; 95% interval 0.772 ± 1.964 × 0.0417 = 0.772 ± 0.0819, (0.690, 0.854) (`ch11.b`, `.se_b`, `.t`, `.df`, `.slope.*`, `.tstar`). Conditions from the residual plot. By hand from four and five places: 0.7722 ÷ 0.04173 = 18.50 (`ch11.b4`, `.se_b5`, `.t.hand`) | LinRegTTest (β ≠ 0) and LinRegTInt on L5, L6 | Is a slope of 1 plausible? No: 1 is outside (0.690, 0.854); t = (0.7722 − 1) ÷ 0.04173 = −5.46, p < 0.0001 (`ch11.slope1.*`) |

**Hand figures checked against the command:** 0.6184 × 0.5704 ÷ 0.4568 = 0.772; 0.636 + 0.772 ×
3.001 = 2.953; 0.636 + 0.772 × 1.0 = 1.408; 0.7722 ÷ 0.04173 = 18.50; (0.7722 − 1) ÷ 0.04173 =
−5.46. Use these printed inputs: 0.772 ÷ 0.0417 gives 18.51, and (0.772 − 1) ÷ 0.0417 gives −5.47.
Two figures differ by design and the text names both: 11.2's Try it (2.953 and 2.952) and 11.3's
prediction (3.370 and 3.369).

**Chapter 11 review:**

1. *(Multiple choice.)* For 11.1's students, r = 0.618. What share of the variation in college
   grades does the line explain? (A) 61.8% (B) 38.2% (C) 78.6% (D) 19.1%. Answer: (B) (`ch11.r2`).
2. *(Multiple choice; fictional.)* A line is ŷ = 12.5 + 3.2x. At x = 4 the observed y is 27. The
   residual: (A) 25.3 (B) −1.7 (C) 1.7 (D) 27. Answer: (C); the prediction is 25.3
   (`ch11.review.pred`, `.res`).
3. *(Multiple choice; fictional.)* r = 0.8, sy = 10, sx = 4, x̄ = 6, ȳ = 30. The line: (A) ŷ = 18.0 +
   2.0x (B) ŷ = 30 + 0.8x (C) ŷ = 25.2 + 0.8x (D) ŷ = 6 + 2.0x. Answer: (A); slope 0.8 × 10 ÷ 4 =
   2.0, intercept 30 − 2.0 × 6 = 18.0 (`ch11.review.slope`, `.intercept`).
4. *(Multiple choice; no numbers.)* Using a line far outside the data's x values is: (A) an
   outlier (B) extrapolation (C) a residual (D) regression to the mean. Answer: (B).
5. *(Written; Tonmick, lists L3 and L4.)* For the 610 students not offered, regress visits on
   school grade (`ch11.review.visits.*`).
   - The line: visits = 2.464 − 0.090 × (school grade), r = −0.015, r² = 0.000 (0.0%).
   - Predictions at 2.0 and 4.0: 2.28 and 2.10. Is the line useful? No: school grade tells almost
     nothing about visits, and the visits are strongly skewed.
6. *(Written; fictional; slope inference.)* For 25 cities, the slope of a line is 1.84 with SE 0.52.
   - t = 1.84 ÷ 0.52 = 3.54 with 23 df, p = 0.0018 (`ch11.review.slope.*`).
   - t* = 2.069; interval 1.84 ± 1.076, (0.764, 2.916): the relationship is more than chance, for
     these cities.

## Chapter 12. Eight Investigations

Each investigation's key results come from earlier chapters' values; this table names them, with
the few that are new (`ch12.*`). Titles and questions are the classroom companion's.

| Investigation | Key results and their names |
| --- | --- |
| 1. Did Chance Make the Groups Alike? | 49.3 to 50.8% offered in each college, 33 to 43 students in colleges of 65 to 86 (`ch12.inv1.share.range`, `.offered.range`, `ch3.college.min`, `.max`); school grades, offered: 1.69, 2.665, 3.02, 3.365, 4, mean 3.024, Sx 0.475, IQR 0.7; not offered: 1.5, 2.67, 2.99, 3.3, 4, mean 2.996, Sx 0.463, IQR 0.63, lower fence 1.725 with one point below it (`ch12.inv1.*`); means differ by 0.029 (`ch12.inv1.mean_gap`); part-time 234 of 609 (38.4%) and 215 of 610 (35.2%), 3.2 points (`ch4.balance.*`) |
| 2. A Year of Support Visits | Not offered: mean 2.193, Sx 2.731, 0, 0, 1, 3, 16, fence 7.5, 37 above, 199 with none (32.6%) (`ch3.L4.*`); offered: mean 2.507, Sx 3.105, 0, 0, 1, 3, 25, 49 above, 170 with none (27.9%) (`ch3.L2.*`) |
| 3. Could Chance Alone Do This? | 0.2864 = 0.1564 + 0.1300 (`ch5.shuffle.*`); within each college, 0.2843 (`ch12.inv3.within`); shuffles mostly from 75 to 99 (the middle 95%) (`ch12.inv3.middle95`); a class of 100 shuffles finds about 29, give or take 4.5 (`ch5.shuffle.of100`, `ch12.inv3.of100.sd`) |
| 4. How Big Is the Difference in Withdrawal? | (−0.0615, 0.0175), z = −1.09, p = 0.2751 (`ch8.two.*`); by hand, SE 0.02015 unpooled and 0.02016 pooled, margin 1.96 × 0.02015 = 0.0395 (`ch12.inv4.se`, `.se.pooled`, `.me`); the 11 unknowns as staying, 80 of 609 against 93 of 610: −0.0211, (−0.0603, 0.0181), p = 0.2913; as withdrawing, 84 of 609 against 100 of 610: −0.0260, (−0.0662, 0.0142), p = 0.2048 (`ch12.inv4.*`, `ch8.sens.*`) |
| 5. Did the Offer Change How Students Left? | Section 9.2's values (`ch9.hom.*`) |
| 6. Who Joined the Study? | 80.2% of 960 and 70.2% of 640 (`ch4.invited.*`); expected 731.4, 228.6, 487.6, 152.4 (`ch9.ind.join.expected`); χ² = 21.39, p = 3.75 × 10⁻⁶ (`ch9.ind.join.*`); 2-PropZTest z = 4.6246 (`ch9.ind.join.z`); 449 of 1,219 is 36.8% against 40% invited (`ch4.part_time.share_*`). The classroom companion's audit R1 read the two screens' p values as 3.7526E-6 (χ²-Test) and 3.7566E-6 (2-PropZTest); those are readings, not computed here, and the exact value is 3.75 × 10⁻⁶ |
| 7. Did the Offer Change Support Visits? | Section 10.5's values; by hand with 1197.07 df, t* = 1.962 and margin 1.962 × 0.1675 = 0.329 (`ch12.inv7.*`); per 100 students offered, 31 more visits, from 1.5 fewer to 64.3 more (`ch10.two.per100*`); variance against mean: 3.105² = 9.64 against 2.51 (3.8 times) and 2.731² = 7.46 against 2.19 (3.4 times) (`ch10.two.*.var`, `.mean2`, `.ratio`); no visits 170 (27.9%) and 199 (32.6%), above the fence 49 and 37 (`ch3.L2.*`, `ch3.L4.*`) |
| 8. Do School Grades Predict College Grades? | Chapter 11's values (`ch11.*`), with Investigation 8's pointer to Section 11.6 |

## The tables (`expected/tables.csv`)

Each row is one value, its entries separated by ", ", so the book can print a row with
`{name|cells}`.

- **Standard normal**: the area to the left of z, four places. `table.normal.neg.T.H` holds z =
  −T.H0 to −T.H9 (for example, `table.normal.neg.1.9` is z = −1.90 to −1.99: 0.0287 down to
  0.0233), and `table.normal.pos.T.H` holds T.H0 to T.H9 (1.90 to 1.99: 0.9713 to 0.9767), for
  T.H from 0.0 to 3.4: 70 rows of 10.
- **t critical values**: tail areas 0.20, 0.10, 0.05, 0.025, 0.01, 0.005, 0.001, 0.0005, with
  confidence levels 60%, 80%, 90%, 95%, 98%, 99%, 99.8%, 99.9% (`table.t.tails`, `table.t.levels`);
  rows `table.t.df.N` for N = 1 to 30, 40, 50, 60, 80, 100, and 1,000, three places, and `table.t.z`
  for z* (0.842 to 3.291). For example, 19 df at 0.025 is 2.093. For df the table skips, such as 608, the text
  points to invT( (1.964), or to the next smaller row (100 df: 1.984), which is conservative.
- **Chi-square critical values**: tail areas 0.25, 0.20, 0.10, 0.05, 0.025, 0.01, 0.005, 0.001
  (`table.chisq.tails`); rows `table.chisq.df.N` for N = 1 to 30, 40, 50, 60, 80, and 100, three
  places. For example, 2 df at 0.05 is 5.991 and 15 df is 24.996 (`ch9.hom.crit`, `ch9.gof.crit`).

One worked line for each table belongs in the back matter (C6): reading Φ(−1.96) = 0.0250, t* for
19 df at 95%, and the 5% critical value for 2 df.
