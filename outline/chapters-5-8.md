# Chapters 5 to 8: the outline and its numbers

This file is the source for the book's Chapters 5 to 8. For each section it gives the worked
example, the values the text prints, and the Try It answer; for each chapter, the one-page review.
Every value is named as in `expected/chapters_5_8.csv`. `python/chapters_5_8.py` and
`r/chapters_5_8.R` compute each one independently, and `run_all.py` requires both to match the
expected file character for character. Values appear here as the book prints them, except that
the book uses a true minus sign (−) where this file has a hyphen. Names from Chapters 1 to 4
(`expected/chapters_1_4.csv`) are used where a number was already printed there.

The data are fictional: the Tonmick study is invented for teaching.

Conventions, beyond those of Chapters 1 to 4:

- **Home-screen arithmetic starts from printed numbers.** Where the text shows a calculation
  (2 × 2.350, √(3.102² + 2.729²)), both routes start from the rounded values the book prints,
  so a reader who types them gets the book's digits. Values a calculator command computes from
  the data (1-PropZInt, 2-PropZTest, 1-Var Stats) start from the counts and the raw data.
- **Normal models use the printed parameters:** mean 3.010 and SD 0.469 for school grades, as
  Exercise 4 types them.
- **A random variable's SD is σx.** When X is a value drawn from a known group (a joiner chosen
  at random), its distribution is the group itself, so its SD divides by n: σx on the screen.
- **Exact values replace simulation** wherever one exists. SHUFFLE's chances and the capture
  rate of 95% intervals are hypergeometric; the skewness of means of 30 is the population's
  skewness divided by √30. Each route also checks those three against a simulation with its own
  random numbers, within a stated tolerance (about six standard errors); the simulations are
  printed by `run_all.py` but not compared between the routes.

## Settled in D2 (the outline's open items, and its corrections)

| Item | Outline (November 22) | Settled |
| --- | --- | --- |
| 5.4's exact chance | 0.286 (0.156 + 0.130) | 0.2864 = 0.1564 + 0.1300, to four places as the book prints p values (`ch5.shuffle.*`) |
| 6.1's calculator route | 1-Var Stats on augment(L2,L4) | Store augment(L2,L4) as a named list, VIS2, as Section 3.4 does with GRADE; 1-Var Stats on it gives μ and σx. The frequency table (`ch6.freq.*`) is the by-hand route |
| 6.3's SDs | √(3.105² + 2.731²) = 4.135, from Sx | √(3.102² + 2.729²) = 4.132, from σx: one student drawn from each group (`ch6.diff.sd`) |
| 6.3's totals | 4.701 and 4.137 | 4.700 and 4.138, from the printed 2.350 and 2.926, so the arithmetic shown checks (`ch6.two.*`) |
| 6.7's cutoffs | 2.238 and 3.782 | invNorm( gives 2.239 and 3.781; the table route, z = 1.645, gives 2.238 and 3.782. The book prints invNorm('s values and says the table can differ in the last digit (`ch6.cut10.*`) |
| 6.7's Try it | The top 5% (the same cutoff as the example) | The top 25%: 3.326 (`ch6.cut.top25`) |
| 7.1's share | 0.1322, the offered students' share | 0.1432, the share among the 1,208 the sample of 100 is drawn from, so Chapter 8 continues it (`ch7.p`, `ch7.sd100`) |
| 7.1's Try it | Samples of 400 (more than 10% of 1,208) | Samples of 25: SD 0.0701, and 3.6 expected withdrawals, too few for a normal model (`ch7.sd25`, `ch7.np25`) |
| 7.2's simulation | "D2 checks by simulation" | Exact: visits have skewness 2.08, so means of 30 have 2.08 ÷ √30 = 0.38, still right-skewed; a simulation agrees (`ch7.skew.*`) |
| 8.1 to 8.5's sample | To be drawn | Drawn in D1: 15 of 100 withdrew, p̂ = 0.15 (`ch8.x`) |
| 8.2's capture rate | "about 95%" | Exact: 95.5% of all samples of 100 from the 1,208 give a 95% interval that captures 0.1432 (`ch8.coverage`) |
| 8.3's guess | 0.1322 gives 490 | The sample's 0.15 gives 545; no guess, 1,068 (`ch8.n.*`) |
| 8.5's test | Numbers in D2 | z = 0.00 and p = 0.5000: the sample's share equals the goal (`ch8.test.*`) |
| 8.6's power | 0.19, normal approximation | 0.1936 for the offer, stated with its setup: true shares 80/605 and 93/603, two-sided, α = 0.05, normal approximation; about 3,978 per group would give 80% power. The goal test's power is 0.0690 (`ch8.power.*`) |
| 8.8's unknown outcomes | p = 0.29 and 0.20 | All 11 stayed: 0.2913; all withdrew: 0.2048; the two extremes: 0.4716 and 0.1090 (`ch8.sens.*`) |

## Chapter 5. Two Categorical Variables and Probability

| Section | Worked example and values | Try it (answer) |
| --- | --- | --- |
| 5.1 Two-Way Tables and Relative Frequencies | Offer by how the year ended: offered 504, 80, 21, 4 (609); not offered 488, 93, 22, 7 (610) (`ch5.table.*`). Joint: P(offered and withdrew) = 80/1,219 = 0.0656 (`ch5.joint.offered_withdrew`). Marginal: 173/1,219 = 0.1419 withdrew (`ch5.marginal.withdrew`). Conditional: withdrawal among the known, 13.2% of 605 against 15.4% of 603 (`ch5.cond.*`) | Transfers: 21 of 609 (3.4%) offered against 22 of 610 (3.6%) not offered (`ch5.try1.*`) |
| 5.2 Graphs for Two Categorical Variables | How the year ended within each group, as segmented bars of all its students: offered 82.8%, 13.1%, 3.4%, 0.7%; not offered 80.0%, 15.2%, 3.6%, 1.1% (`ch5.seg.*`). Side-by-side bars and a mosaic plot of the same table. Bars that differ suggest an association | Which graph also shows the group sizes? The mosaic plot (no numbers) |
| 5.3 Simulation and the Law of Large Numbers | One offered student's year, as a model: withdraws with chance 0.13. Random integers 1 to 100, with 1 to 13 meaning "withdraws"; ten trials give 1.3 withdrawals on average, and none at all with chance 0.2484 (`ch5.lln.ten.*`). Over many trials, the share settles near 0.13 | Twenty students: describe the simulation; the expected count is 2.6 (`ch5.lln.twenty.expected`) |
| 5.4 Could Chance Alone Make the Gap? | SHUFFLE deals the 173 withdrawals at random among the 1,208 known outcomes and counts K, those dealt to the 605 offered (`ch5.shuffle.n`, `.withdrawals`, `.offered`). Chance alone gives 86.6 on average (`ch5.shuffle.expected`); Tonmick had 80, a gap of −2.2 points (`ch5.shuffle.observed`, `.gap`). A gap at least as large either way means K ≤ 80 or K ≥ 94: exact chance 0.1564 + 0.1300 = 0.2864 (`ch5.shuffle.low`, `.high`, `.p`); a class of 100 shuffles should find about 29 (`ch5.shuffle.of100`) | Why does K = 94 count as extreme and 93 not? 94 gives a gap of 2.4 points, 93 only 2.1 (`ch5.shuffle.gap_cut_high`, `.gap_below_cut`) |
| 5.5 Probability and Complements | A joiner chosen at random: P(offered) = 609/1,219 = 0.4996; P(part-time) = 449/1,219 = 0.3683 (`ch5.p.offered`, `ch5.p.part_time`). Complement: P(did not withdraw) = 1 − 173/1,208 = 0.8568 among known outcomes (`ch5.p.not_withdrew_known`) | P(full-time) = 770/1,219 = 0.6317 (`ch5.p.full_time`) |
| 5.6 Mutually Exclusive Events | Withdrew and transferred cannot both happen: P(withdrew or transferred) = (173 + 43)/1,219 = 216/1,219 = 0.1772 (`ch5.count.withdrew_or_transferred`, `ch5.p.withdrew_or_transferred`) | Which pairs are not mutually exclusive? Offered and withdrew, for example (no numbers) |
| 5.7 Conditional Probability and the Multiplication Rule | P(withdrew given offered) = 80/605 = 0.1322; the other way round, P(offered given withdrew) = 80/173 = 0.4624 (`ch5.p.withdrew_given_offered`, `ch5.p.offered_given_withdrew`). Tree among the 1,208: part-time 0.3709, then withdrew 0.2254, product 0.0836; full-time 0.6291, then withdrew 0.0947, product 0.0596; total 0.1432 (`ch5.tree.*`) | P(not offered given transferred) = 22/43 = 0.5116 (`ch5.p.not_offered_given_transferred`) |
| 5.8 Independence and Unions | P(part-time) = 0.3683 against P(part-time given offered) = 234/609 = 0.3842 and given not offered 215/610 = 0.3525 (`ch5.p.part_time_given_*`): close; Chapter 9 tests the gap. P(part-time or offered) = (449 + 609 − 234)/1,219 = 824/1,219 = 0.6760 (`ch5.union.*`) | Independent if assigned by chance? Yes in the long run; a single assignment differs a little by chance (no new numbers) |

**Chapter 5 review** (four multiple choice, two written; answers in the back):

1. *(Multiple choice; Tonmick; summary numbers.)* Of the 173 students who withdrew, 80 had been
   offered mentoring. What is 80 ÷ 173 = 0.4624 (`ch5.p.offered_given_withdrew`)? (A) P(offered
   given withdrew) (B) P(withdrew given offered) (C) P(offered and withdrew) (D) P(offered or
   withdrew). Answer: (A).
2. *(Multiple choice; fictional; summary numbers.)* At a school, 40% of students play a sport,
   30% are in band, and 12% do both. What share do at least one? (A) 0.70 (B) 0.58 (C) 0.12
   (D) 0.88. Answer: (B), 0.40 + 0.30 − 0.12 = 0.58 (`ch5.review.union`).
3. *(Multiple choice; the same school.)* Are playing a sport and being in band independent?
   (A) No, since 12% do both (B) Yes, since 0.40 × 0.30 = 0.12 (C) No, since 0.40 + 0.30 ≠ 1
   (D) There is not enough information. Answer: (B) (`ch5.review.product`).
4. *(Multiple choice; Tonmick model.)* Ten offered students each withdraw with chance 0.13,
   independently. P(at least one withdraws)? (A) 0.13 (B) 0.2484 (C) 0.7516 (D) 1.3. Answer: (C),
   1 − 0.87¹⁰ (`ch5.review.atleast1`, `ch5.lln.ten.none`).
5. *(Written; Tonmick.)* Among the 1,208 known outcomes, 101 of 448 part-time and 72 of 760
   full-time students withdrew.
   - Make the two-way table with totals: 101, 347, 448; 72, 688, 760; 173, 1,035, 1,208
     (`ch5.review.pt.*`, `ch5.review.ft.*`, `ch5.review.total.stayed`).
   - Find P(withdrew) = 0.1432, P(withdrew given part-time) = 0.2254, and P(part-time given
     withdrew) = 101/173 = 0.5838 (`ch5.tree.total`, `ch5.tree.withdrew_given_part_time`,
     `ch5.review.p_pt_given_withdrew`).
   - Are enrollment and withdrawal independent? No: 0.2254 is far from 0.1432.
6. *(Written; fictional; simulation.)* A player makes 70% of free throws. Design a simulation
   with randInt( to estimate P(at least 4 of 5 made), and say what many runs should give: about
   0.5282, the exact binomial value (`ch5.review.freethrow`).

## Chapter 6. Random Variables

| Section | Worked example and values | Try it (answer) |
| --- | --- | --- |
| 6.1 Probability Distributions | X = visits of a joiner chosen at random from all 1,219. Counts for 0 to 7 and 8 or more: 369, 274, 176, 120, 75, 54, 38, 27, 86; probabilities 0.3027, 0.2248, 0.1444, 0.0984, 0.0615, 0.0443, 0.0312, 0.0221, 0.0705; cumulative 0.3027, 0.5275, 0.6719, …, 1.0000 (`ch6.dist.*`, `ch6.p0`, `ch6.p1`, `ch6.p8plus`) | P(X ≤ 2) = 0.6719 (`ch6.cum2`) |
| 6.2 Mean and Standard Deviation | μ = 2.350 visits, σ = 2.926 (`ch6.mu`, `ch6.sigma`): σx on the screen, since the 1,219 are the whole distribution (Sx would be 2.927, `ch6.sx`). Σx = 2865 (`ch6.sum`). By hand from the frequency table: values 0 to 16 and 25 with counts 369, 274, … (`ch6.freq.*`) | Why σx here and Sx in Chapter 3? (no numbers) |
| 6.3 Combining Random Variables (Going further) | Two joiners chosen at random, independently: total visits mean 2 × 2.350 = 4.700, SD √2 × 2.926 = 4.138 (`ch6.two.*`). One offered student minus one not offered: mean 2.507 − 2.193 = 0.314, SD √(3.102² + 2.729²) = 4.132 (`ch6.diff.*`, `ch3.L2.sigma`, `ch6.sigma.not_offered`). Variances add; SDs do not | Three students: mean 7.050, SD 5.068 (`ch6.three.*`) |
| 6.4 The Binomial Distribution | Ten offered students, each withdrawing with chance 0.13. Conditions: two outcomes, fixed n, independent trials, the same chance. C(10, 2) = 45; 45 × 0.13² × 0.87⁸ = 0.2496 = P(X = 2); P(X ≤ 2) = 0.8692; mean 1.3, SD 1.063 (`ch6.binom.*`) | P(X ≥ 3) = 1 − 0.8692 = 0.1308 (`ch6.binom.ge3`) |
| 6.5 The Geometric Distribution (Going further) | Offered students checked one at a time: the first withdrawal is the 3rd with chance 0.87² × 0.13 = 0.0984; within the first 5 with chance 1 − 0.87⁵ = 0.5016; on average the 7.69th student (`ch6.geom.p3`, `.cdf5`, `.mean`) | After the 10th: 0.87¹⁰ = 0.2484 (`ch6.geom.after10`) |
| 6.6 The Normal Distribution and the Empirical Rule | School grades at entry, model mean 3.010 and SD 0.469. Within 1, 2, and 3 SDs: the data 68.0%, 94.8%, 99.9%; the rule 68.3%, 95.4%, 99.7% (`ch6.normal.within*`, `.rule*`). Above 3.5: z = 1.04, the model 14.8%, the data 15.1% (`ch6.normal.z_3_5`, `.model_above_3_5`, `.data_above_3_5`) | Below 2.5: the model 0.1384 (13.8%), the data 13.0% (`ch6.normal.model_below_2_5*`, `.data_below_2_5`) |
| 6.7 Cutoffs and Percentiles from a Normal Model | The 90th percentile, z = 1.282: 3.611 (`ch6.cut.z90`, `ch6.cut.p90`, `ch1.ex4.p90`). The most extreme 10%, split between the tails, z = ±1.645: below 2.239 and above 3.781 by invNorm(, or 2.238 and 3.782 from the table's z (`ch6.cut10.*`) | The top 25%: 3.326 (`ch6.cut.top25`) |

**Chapter 6 review:**

1. *(Multiple choice; fictional; summary numbers.)* X takes 0, 1, 2, 3 with chances 0.1, 0.3,
   0.4, 0.2. Its mean? (A) 1.5 (B) 1.7 (C) 2.0 (D) 0.25. Answer: (B) (`ch6.review.dist.mean`;
   its SD is 0.9, `ch6.review.dist.sd`).
2. *(Multiple choice; fictional.)* X has mean 20 and SD 3; Y, independent of X, has mean 15 and
   SD 4. The SD of X + Y? (A) 7 (B) 5 (C) 1 (D) 25. Answer: (B), √(9 + 16) (`ch6.review.sum.*`).
3. *(Multiple choice; no numbers.)* Which count is binomial? (A) Students checked until the first
   withdrawal (B) Withdrawals among 10 students chosen independently (C) Visits by one student
   (D) Students who joined at a college. Answer: (B).
4. *(Multiple choice; fictional; summary numbers.)* Heights follow a normal model with mean 64
   and SD 2.5 inches. P(taller than 68)? (A) 0.9452 (B) 0.0548 (C) 0.1096 (D) 0.4452. Answer:
   (B), z = 1.6 (`ch6.review.height.*`).
5. *(Written; Tonmick model.)* Twenty offered students, each withdrawing with chance 0.13.
   - Check the binomial conditions.
   - P(exactly 3) = 0.2347; P(at most 2) = 0.5080 (`ch6.review.binom20.p3`, `.le2`).
   - Mean 2.6 and SD 1.504 (`ch6.review.binom20.mean`, `.sd`).
6. *(Written; Tonmick.)* College grades of the 1,116 with a grade: model mean 2.996, SD 0.561
   (`ch3.z.g12.*`).
   - The model's share above 3.5 is 18.4%; the data's, 19.2% (`ch6.review.g12.model_above_3_5`,
     `.data_above_3_5`).
   - The cutoff for the top 10%: 3.715 (`ch6.review.g12.top10`).
   - The model puts 3.7% above 4.0, the top of the scale, where 44 students (3.9%) sit
     (`ch6.review.g12.model_above_4`, `.at_4`, `.at_4.pct`). Does the model fit?

## Chapter 7. Sampling Distributions

| Section | Worked example and values | Try it (answer) |
| --- | --- | --- |
| 7.1 Estimators and Sample Shares | Among the 1,208 known outcomes, p = 0.1432. Samples of 100: p̂ centers on 0.1432 with SD √(0.1432 × 0.8568 ÷ 100) = 0.0350; 14.3 and 85.7 expected, both at least 10; 100 is under 10% of 1,208 (120.8) (`ch7.p`, `ch7.sd100`, `ch7.np100`, `ch7.nq100`, `ch7.ten_pct`). The sample of 100 drawn for Chapter 8 gave 0.15, 0.19 SDs above p (`ch7.sample100.*`) | Samples of 25: SD 0.0701, and only 3.6 expected withdrawals, so no normal model (`ch7.sd25`, `ch7.np25`) |
| 7.2 Sample Means and the Central Limit Theorem | Visits: μ = 2.350, σ = 2.926, skewed (skewness 2.08). Means of 30 drawn at random: SD 2.926 ÷ √30 = 0.534, skewness 2.08 ÷ √30 = 0.38, closer to normal but still right-skewed (`ch7.sd30`, `ch7.skew.*`). 30 is under 10% of 1,219 (121.9) (`ch7.ten_pct.joiners`) | Means of 120: SD 0.267 (`ch7.sd120`) |
| 7.3 The Gap Between Two Shares | With no effect, the chance assignment gives the gap in withdrawal shares an SD of √(0.1432 × 0.8568 × (1/605 + 1/603)) = 0.0202; Tonmick's gap, −0.0220, is −1.09 SDs from 0 (`ch7.gap.*`) | A gap of 0.04: 1.98 SDs (`ch7.gap.try`) |
| 7.4 The Gap Between Two Means | Visits: SE = √(3.105²/609 + 2.731²/610) = 0.1675; the gap, 0.314, is 1.87 SEs from 0 (`ch7.means.se`, `ch7.means.z`) | Both groups four times as large: 0.0838, half (`ch7.means.se4`) |

**Chapter 7 review:**

1. *(Multiple choice; no numbers.)* What does a sampling distribution describe? (A) The values in
   one sample (B) A statistic's values over many samples (C) The population (D) The data's
   outliers. Answer: (B).
2. *(Multiple choice; fictional; summary numbers.)* p = 0.30 and n = 50. The SD of p̂? (A) 0.0648
   (B) 0.0042 (C) 0.2100 (D) 0.4583. Answer: (A) (`ch7.review.sd_phat`).
3. *(Multiple choice; fictional; summary numbers.)* A population has mean 50 and SD 12. The SD of
   means of 36? (A) 12 (B) 2 (C) 0.33 (D) 50. Answer: (B) (`ch7.review.sd_xbar`).
4. *(Multiple choice; fictional.)* p = 0.04 and n = 150. Why is a normal model for p̂ a poor
   choice? (A) n is too large (B) only 6 expected successes (C) p is too large (D) the 10%
   condition fails. Answer: (B) (`ch7.review.np`, `ch7.review.nq`).
5. *(Written; Tonmick.)* Samples of 100 from the 1,208, p = 0.1432.
   - The mean and SD of p̂: 0.1432 and 0.0350; check the conditions.
   - With a normal model, P(p̂ ≥ 0.20): z = 1.62, about 0.0526 (`ch7.review.z20`,
     `ch7.review.p20`). The exact chance is 0.0655 (`ch7.review.exact20`): the model is rough in
     the tail.
   - Was the sample's 0.15 unusual? No: z = 0.19 (`ch7.sample100.z`).
6. *(Written; Tonmick.)* Means of 50 visits, drawn at random from all 1,219.
   - SD 0.414 (`ch7.review.sd50`), and 50 is under 121.9.
   - P(x̄ > 3): z = 1.57, about 0.0582 (`ch7.review.z3`, `ch7.review.p3`).
   - Why might the normal model still be rough here? The skewness, 2.08.

## Chapter 8. Inference for Proportions

The one-sample sections use `samples/tonmick-sample-100.csv`: a simple random sample of 100 of the
1,208 joiners with a known outcome, drawn once in D1 with seed 2027. With the 1,208 as the
population, the true share is known, 0.1432 (`ch8.true`).

| Section | Worked example and values | Try it (answer) |
| --- | --- | --- |
| 8.1 A Confidence Interval for a Proportion | 15 of 100 withdrew: p̂ = 0.15 (`ch8.x`, `ch8.phat`). Conditions: random; 100 ≤ 120.8; 15 and 85 at least 10 (`ch8.failures`). SE = √(0.15 × 0.85 ÷ 100) = 0.0357; z* = 1.960; margin 0.0700; interval (0.0800, 0.2200) (`ch8.se`, `ch8.zstar`, `ch8.me`, `ch8.ci.*`) | 90%: z* = 1.645, (0.0913, 0.2087), narrower (`ch8.zstar90`, `ch8.ci90.*`) |
| 8.2 What Confidence Means | The truth, 0.1432, is inside (0.0800, 0.2200). Of all samples of 100 from the 1,208, 95.5% give an interval that captures it (`ch8.coverage`); a class's intervals should capture it about 95% of the time. With n = 400 the margin would be about 0.0350, half (`ch8.me400`). The interval for the 605 offered, (0.1052, 0.1592), describes no sampled population (`ch1.ex7.*`) | Rewrite an overreaching claim (no numbers) |
| 8.3 Choosing a Sample Size | A new survey of a large population, margin 0.03 at 95%: n = (1.960 ÷ 0.03)² × 0.15 × 0.85, rounded up, 545 with the guess 0.15; 1,068 with no guess (0.5) (`ch8.n.guess`, `ch8.n.half`) | Margin 0.02, no guess: 2,401 (`ch8.n.try`) |
| 8.4 Setting Up a Test for a Proportion | A stated, hypothetical goal: fewer than 15% withdraw. H0: p = 0.15; Ha: p < 0.15. Conditions: random, 10%, 100 × 0.15 = 15 and 100 × 0.85 = 85 (`ch8.null`, `ch8.null.expected`, `ch8.null.expected_fail`) | The two-sided version, and when it fits (no numbers) |
| 8.5 Carrying Out the Test: p-Values and Conclusions | z = (0.15 − 0.15) ÷ 0.0357 = 0.00; p = 0.5000 (`ch8.test.z`, `ch8.test.p`): no evidence that fewer than 15% withdraw. A simulated p value from the null model, as in Section 5.4 | Two-sided p value: 1.0000 (`ch8.test.p2`) |
| 8.6 Errors and Power | The truth, 0.1432, is below 0.15, so 8.5's failure to reject is a Type II error. The goal test rejects only when p̂ < 0.0913, which happens 6.9% of the time when p = 0.1432: power 0.0690, a Type II error 93.1% of the time (`ch8.power.goal*`). For the offer, setup stated: true shares 0.1322 and 0.1542, 605 and 603 students, two-sided, α = 0.05, normal approximation: power 0.1936, about 19.4%; about 3,978 per group for 80% (`ch8.power.*`) | What raises power? (no numbers) |
| 8.7 A Confidence Interval for Two Proportions | Offered minus not offered: −0.0220, SE 0.0201, 95% interval (−0.0615, 0.0175) (`ch8.two.diff`, `ch8.two.se`, `ch8.two.ci.*`). Random assignment is the condition; no 10% condition | Contains 0 (no new numbers) |
| 8.8 A Test for Two Proportions | Pooled share 0.1432; expected withdrawals 86.6 and 86.4, at least 10; z = −1.09, p = 0.2751 (`ch8.pooled*`, `ch8.two.z`, `ch8.two.p`). The 11 unknown outcomes (4 and 7): all stayed, p = 0.2913; all withdrew, p = 0.2048; the extremes, 0.4716 and 0.1090: no case reaches 0.05 (`ch8.unknown.*`, `ch8.sens.*`) | The conclusion in context (no new numbers) |
| 8.9 Writing Up an Inference Procedure | Section 8.8's test in four parts (no new numbers) | Section 8.7's interval the same way (no new numbers) |

**Chapter 8 review:**

1. *(Multiple choice; no numbers.)* What does "95% confident" mean? (A) 95% of the data lie in
   the interval (B) The method captures the true value in 95% of samples (C) p is in this interval
   with chance 0.95 (D) 95% of samples give this interval. Answer: (B).
2. *(Multiple choice; fictional; summary numbers.)* A poll finds 312 of 600 in favor. The 95%
   interval? (A) (0.4800, 0.5600) (B) (0.5000, 0.5400) (C) (0.4600, 0.5800) (D) (0.4800, 0.5200).
   Answer: (A), 0.52 ± 0.0400 (`ch8.review.poll.*`).
3. *(Multiple choice; no numbers.)* In 8.4's test, a Type I error would be: (A) concluding fewer
   than 15% withdraw when they do not (B) failing to conclude it when they do (C) a sampling
   error (D) a wrong p value. Answer: (A).
4. *(Multiple choice; summary numbers.)* The sample size for a margin of 0.04 at 95% with no
   guess? (A) 600 (B) 601 (C) 25 (D) 1,201. Answer: (B) (`ch8.review.n`).
5. *(Written; Tonmick, the sample of 100.)* 33 of the 100 studied part-time (`ch8.review.pt.x`).
   - Check the conditions (33 and 67).
   - The 95% interval: 0.33 ± 0.0922, (0.2378, 0.4222) (`ch8.review.pt.*`).
   - The true share among the 1,208 is 0.3709 (`ch8.review.pt.true`). Did the interval capture
     it?
6. *(Written; fictional; a write-up.)* A school sends a reminder text to 200 families chosen at
   random from 400; 52 of those 200 return a form, against 38 of the other 200.
   - Write up a one-sided two-proportion z test in four parts: p̂ = 0.26 and 0.19, pooled 0.225,
     SE 0.0418, z = 1.68, p = 0.0468 (`ch8.review.remind.*`).
   - Conclude at α = 0.05: the reminder raised returns, for these families. The two-sided p
     value would be 0.0937 (`ch8.review.remind.p_two`).
