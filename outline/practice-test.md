# The practice test: the plan and its numbers

This file is the source for the book's practice test (overlay C6b): Part 1, 40 multiple-choice
questions with four choices, about 90 minutes; Part 2, four written questions, about 90 minutes;
and the answers to both. For each question it gives the section it practices, the invented
setting, the question, the choices in order with the answer marked, the trap in each wrong
choice, and the values it prints. Every value is named as in `expected/practice.csv`;
`python/practice.py` (standard-library Python) and `r/practice.R` (base R) compute each one
independently, and `run_all.py` requires both routes to match the expected file character for
character. Values appear here as the book prints them, with a true minus sign (−) where
`expected/practice.csv` has a hyphen.

**Every setting is invented**, and so are its numbers: each question says so in a word or two.
None uses the Tonmick study, so a student practices reading an unfamiliar setting quickly.

## Conventions

- **Where the numbers come from.** A number a question states is in `practice/givens.csv`,
  chosen by hand, and both routes copy it under its own name (`pt.q19.n` is 144). A number
  computed from data reads one of the nine data sets in `practice/`, drawn once with seed 2027
  by `python/make_practice.py` before any question was written to fit them; nothing was redrawn.
- **Wrong choices are computed, not invented.** Each numerical wrong choice comes from a named
  mistake (`pt.q20.trap.ci90` is the 90% interval offered for a 95% question), so the answer's
  "the trap" sentence prints a checked number.
- **Core sections only.** No question needs a section marked *Going further* (6.3's rules for
  combining random variables, 6.5, 9.1, the typical residual s in 11.3, 11.5, 11.6).
- **Notation** is the book's, with C6a's additions: P(A ∩ B), P(A ∪ B), P(A | B), E(X), μ and σ
  for a distribution, x̄ and s (Sx) for a sample, p̂ and p.
- **Places.** p values and probabilities four places; z and t two; t* and z* three; shares
  three when they stand alone; intervals as each question says. A given that a question states
  as a percent also has a `_pct` value (`pt.q19.p_pct` is 36). Where an answer works a figure
  by hand from printed numbers, the printed inputs give the calculator's last digit: both routes
  check each such pair and stop if they differ (`same()` in the Python route). That is why
  `pt.q25.se` prints five places and `pt.q33.se` four.
- **The letters.** Each letter is the answer exactly 10 times, and no letter is the answer more
  than twice in a row.
- **The graphs.** Figures 22 to 29 (`figures/png/`, drawn by `figures/draw.py` from `practice/`)
  show the data a question asks about and nothing that gives its answer away: Figure 24 marks the
  observed difference but does not count the dots beyond it, and Figure 27 draws the line but
  does not print r.

## Part 1: 40 multiple-choice questions

The mix, close to the course's weights: Questions 1 to 10, Chapters 2 to 4; 11 to 18, Chapters 5
and 6; 19 to 27, proportions and two-way tables (7.1, Chapter 8, 9.2, 9.3); 28 to 34, means (7.2,
Chapter 10); 35 to 40, regression (11.1 to 11.4). Two questions practice writing an investigative
question (7 and 31), as Part 2's first question does.

### Chapters 2 to 4

**1 (2.2).** A bike-share's records list, for each trip, the minutes ridden, the type of bike
(classic or electric), the rider's number of trips that month, and the ZIP code of the station
where the trip began. Which variable is categorical even though its values are numbers?
(A) minutes ridden; (B) type of bike; (C) trips that month; **(D) ZIP code**. Traps: (A) and (C)
are quantitative; (B) is categorical but its values are words. No values.

**2 (3.2, 3.3; Figure 22).** Waits of 80 riders at a bus stop (`pt.q02.n`), in a histogram with
bars 4 minutes wide (`pt.fig22.bars`: 37, 19, 12, 5, 5, 1, 0, 0, 1; the longest wait 35.6,
`pt.fig22.top`). Which is most likely true? **(A) The mean is greater than the median, since the
distribution is skewed right**; (B) the mean and median are about equal, since most waits are
short; (C) the median is greater than the mean, since the long tail pulls the median up; (D) the
mean is less than the median, since a few waits are long. Answer: mean 6.43 against median 4.95
(`pt.q02.mean`, `pt.q02.median`). Trap (C): the tail pulls the mean, not the median.

**3 (3.4).** Temperatures in a greenhouse have mean 20.0 °C and SD 2.5 °C (`pt.q03.mean_c`,
`pt.q03.sd_c`). In Fahrenheit, F = 1.8C + 32. The mean and SD in °F? (A) 68.0 and 2.5; (B) 36.0
and 4.5; **(C) 68.0 and 4.5**; (D) 68.0 and 36.5. Values `pt.q03.mean_f`, `pt.q03.sd_f`. Traps:
(A) the SD left unchanged; (B) the 32 left out of the mean (`pt.q03.trap.mean_unshifted`); (D)
the 32 added to the SD too (`pt.q03.trap.sd_shifted`).

**4 (3.5, 3.7; Figure 23).** Battery life of 30 phones of each of two models, in parallel
modified box plots. Which statement does the graph support? (A) Model B's median is higher than
Model A's; **(B) Model A's median is higher, and Model B's battery lives are more spread out**;
(C) neither model has an outlier; (D) about half of Model A's phones lasted longer than 18.2
hours. Values: five-number summaries A 14.4, 15.8, 17.15, 18.2, 22.4 and B 11.1, 13.9, 16.2,
17.8, 23.6 (`pt.fig23.A.five`, `pt.fig23.B.five`); IQRs 2.4 and 3.9, ranges 8.0 and 12.5
(`pt.q04.*.iqr`, `.range`); Model A's outlier 22.4 (`pt.fig23.A.out`; fences 12.20 and 21.80,
`pt.q04.A.fences`). Traps: (C) misses the open dot; (D) 18.2 is Q3, so about a quarter lasted
longer.

**5 (3.6).** Ana scored 82 on a test with mean 74 and SD 5; Ben scored 88 on a test with mean 81
and SD 6 (`pt.q05.*`). Who did better relative to the others who took the same test? **(A) Ana:
her z-score, 1.60, is higher than Ben's, 1.17**; (B) Ben, since 88 is more than 82; (C) Ben,
since his test's SD is larger; (D) they did equally well, since each scored 7 or 8 points above
the mean. Values `pt.q05.z_1`, `pt.q05.z_2`.

**6 (3.5).** The numbers of books 30 students read over a summer have five-number summary 6, 14,
17, 22, 37 (`pt.q06.*`). Is the maximum an outlier by the 1.5 × IQR rule? (A) No: the upper
fence is Q3 + 2 × IQR = 38; (B) no: the maximum is part of the five-number summary, so it cannot
be an outlier; (C) yes: any value above Q3 is an outlier; **(D) yes: the upper fence is
22 + 1.5 × 8 = 34, and 37 is above it**. Values: IQR 8, fences 2 and 34 (`pt.q06.iqr`,
`.fence_lo`, `.fence_hi`); trap (A) 38 (`pt.q06.trap.two_iqr`).

**7 (4.1).** A town library wants to know whether teens who join its summer reading club read
more books over the summer than teens who do not. Which is a statistical investigative question
for that? (A) How many books did Maya read this summer? **(B) Do teens in this town who join the
club read more books over the summer, on average, than teens who do not?** (C) Is reading good
for teens? (D) What was the most books any teen in town read? Traps: (A) and (D) ask about one
value, with no variability to study; (C) names no variable to measure. No values.

**8 (4.2, 4.5).** A survey of a school's students finds that those who eat breakfast have higher
grades, on average. Which conclusion is justified? (A) Eating breakfast causes higher grades;
(B) the school should require breakfast to raise grades; **(C) the survey shows an association,
but students who eat breakfast may differ in other ways, such as sleep, that also affect grades**;
(D) a survey can show nothing about breakfast and grades. No values.

**9 (4.3).** A library has 40 shelves of books; it picks 5 shelves at random and checks every
book on them (`pt.q09.*`). What kind of sample is this? (A) a simple random sample of books;
(B) a stratified random sample; **(C) a cluster sample**; (D) a systematic sample. Trap (B):
strata are groups sampled within; here whole groups are taken.

**10 (4.6).** A gardener has 60 tomato plants, 30 in a sunny bed and 30 in a shady bed. Within
each bed, 15 plants are chosen at random for a new fertilizer and the other 15 get the old one
(`pt.q10.*`). What design is this? (A) a completely randomized design; **(B) a randomized block
design, with the beds as blocks**; (C) a matched pairs design; (D) an observational study.

### Chapters 5 and 6

**11 (5.1).** A museum's 500 visitors on one day, by age group and whether they used the audio
guide: children 40 used it and 110 did not; adults 120 and 130; seniors 55 and 45 (`pt.q11.*`;
row totals 150, 250, 100; 215 users and 285 others). What share of the audio-guide users were
adults? **(A) 0.558**; (B) 0.480; (C) 0.240; (D) 0.430. Values: 120 ÷ 215
(`pt.q11.adults_of_users`). Traps: (B) 120 ÷ 250, the share of adults who used it
(`pt.q11.trap.users_of_adults`); (C) 120 ÷ 500 (`pt.q11.trap.joint`); (D) 215 ÷ 500
(`pt.q11.trap.users`).

**12 (5.3).** A fair spinner lands on red with probability 0.5. In its first 10 spins it lands on
red 7 times, 70% (`pt.q12.*`). What does the law of large numbers say about the next 1,000
spins? (A) Red is now less likely, so the share evens out; (B) the share of red will stay near
70%; (C) exactly 500 of the next 1,000 will be red; **(D) over many spins, the share of red will
tend to settle near 0.5, though a short run can stray far from it**. Trap (A): the spinner has no
memory; the early 7 are swamped, not paid back.

**13 (5.4; Figure 24).** An experiment randomly assigned 80 seedlings, 40 to fertilizer A and 40
to B; 20 of A's and 12 of B's flowered, shares 0.50 and 0.30, a difference of 0.20
(`pt.q13.*`). A computer reran the random assignment 200 times with the same 32 flowering
seedlings; Figure 24 shows each rerun's difference, with a dashed line at 0.20. In what share of
the reruns was the difference 0.20 or more? (A) 0.94; **(B) 0.06**; (C) 0.12; (D) 0.20. Values:
12 of 200 reruns (`pt.q13.ge`, `pt.q13.share`); the exact share, 0.0548 (`pt.q13.exact`), for
the answer's last sentence: chance alone gives a difference this large about 6% of the time, so
the evidence is suggestive but not convincing at the 5% level. Traps: (A) the reruns below 0.20
(`pt.q13.trap.complement`); (C) 12 read as 12 of 100 (`pt.q13.trap.per100`); (D) the observed
difference itself.

**14 (5.5 to 5.8).** For a student chosen at random, A is "plays a sport" and B is "plays an
instrument", with P(A) = 0.40, P(B) = 0.25, and P(A ∩ B) = 0.10 (`pt.q14.*`). Which is true?
(A) P(A ∪ B) = 0.65; (B) A and B are mutually exclusive; **(C) A and B are independent**;
(D) P(A | B) = 0.25. Values: 0.40 × 0.25 = 0.10 (`pt.q14.product`); P(A ∪ B) = 0.55
(`pt.q14.union`); P(A | B) = 0.40 (`pt.q14.a_given_b`). Traps: (A) the overlap counted twice
(`pt.q14.trap.union_no_overlap`); (B) P(A ∩ B) is not 0; (D) that is P(B | A)
(`pt.q14.b_given_a`).

**15 (5.7).** At a pizza shop, 30% of orders are delivered and the rest are picked up. 8% of
delivered orders and 2% of picked-up orders are late (`pt.q15.*`). An order is late; what is the
probability it was delivered? **(A) 0.632**; (B) 0.080; (C) 0.038; (D) 0.024. Values: 0.30 ×
0.08 = 0.024 and 0.70 × 0.02 = 0.014 (`pt.q15.joint_delivery`, `.joint_pickup`); P(late) =
0.038 (`pt.q15.p_late`); 0.024 ÷ 0.038 = 0.632 (`pt.q15.delivery_given_late`). Traps: (B) the
reverse condition; (C) P(late); (D) P(delivered and late).

**16 (6.1, 6.2).** X, the goals a team scores in a game, has P(0) = 0.1, P(1) = 0.3, P(2) = 0.4,
and P(3) = 0.2 (`pt.q16.x`, `.p`). Its mean and standard deviation? (A) μ = 1.5, σ = 1.12;
(B) μ = 1.7, σ = 0.81; (C) μ = 1.5, σ = 0.90; **(D) μ = 1.7, σ = 0.90**. Values
`pt.q16.mu`, `pt.q16.sigma` (variance 0.81, `pt.q16.var`). Traps: (A) and (C) average the four
values as if equally likely (`pt.q16.trap.mean_values`, `.sd_values`); (B) the variance given as
σ.

**17 (6.4).** Each of 10 customers independently orders dessert with probability 0.2
(`pt.q17.*`). P(at least 2 order dessert)? (A) 0.3020; **(B) 0.6242**; (C) 0.6778; (D) 0.3222.
Values: 1 − P(0) − P(1) = 1 − 0.1074 − 0.2684 (`pt.q17.p0`, `.p1`, `.ge2`); on the calculator,
1 − binomcdf(10,0.2,1). Traps: (A) P(X = 2); (C) P(X ≤ 2); (D) P(X > 2), which leaves out 2
(`pt.q17.trap.*`).

**18 (6.7).** Bags of rice have weights that follow a normal model with mean 454 g and SD 6 g
(`pt.q18.*`). Above what weight are the heaviest 5% of bags? (A) 444.1 g; (B) 465.8 g;
**(C) 463.9 g**; (D) 459.7 g. Values: z = 1.645, 454 + 1.645 × 6 = 463.9 (`pt.q18.z`,
`.cutoff`); invNorm(0.95,454,6). Traps: (A) the lightest 5% (`pt.q18.trap.lower`); (B) z* for 5%
split between two tails, 1.960 (`pt.q18.trap.two_tailed`); (D) 0.95 used as a z-score
(`pt.q18.trap.area`).

### Proportions and two-way tables

**19 (7.1).** 36% of all trips on a city's bike-share are taken by members. For random samples
of 144 trips, what is the probability that p̂, the share by members, is 0.43 or more
(`pt.q19.*`)? **(A) 0.0401**; (B) 0.0801; (C) 0.4420; (D) 0.9599. Values: large counts 51.84 and
92.16 (`pt.q19.np`, `.nq`); SD √(0.36 × 0.64 ÷ 144) = 0.040 (`pt.q19.sd`); z = 1.75
(`pt.q19.z`); 0.0401 (`pt.q19.prob`). Traps: (B) both tails; (C) the SD of one trip, 0.48, used
for p̂ (`pt.q19.trap.sd_one`, `.one`); (D) the lower tail.

**20 (8.1).** In a random sample of 250 households in a city, 95 recycle glass (`pt.q20.*`). A
95% confidence interval for the share of all the city's households that do? (A) (0.330, 0.430);
(B) (0.349, 0.411); (C) (0.378, 0.382); **(D) (0.320, 0.440)**. Values: p̂ = 0.38, SE 0.0307,
z* = 1.960, margin 0.0602 (`pt.q20.phat`, `.se`, `.zstar`, `.me`, `.ci`). Traps: (A) z* for
90% (`pt.q20.trap.ci90`); (B) the SE used as the margin (`pt.q20.trap.no_zstar`); (C) the square
root left out (`pt.q20.trap.no_root`).

**21 (8.2).** A 95% confidence interval for the share of a town's households that compost is
(0.21, 0.29) (`pt.q21.*`). What does "95% confidence" mean? (A) 95% of the town's households
compost; (B) there is a 95% chance that another sample's share will be between 0.21 and 0.29;
**(C) the method gives intervals that capture the true share in about 95% of all possible
samples**; (D) 95% of the households in the sample compost. No computed values.

**22 (8.3).** How large a random sample gives a margin of error of at most 0.03 for a 95%
interval for a share, using p* = 0.5 (`pt.q22.*`)? (A) 33; **(B) 1,068**; (C) 1,067; (D) 752.
Values: (1.960 ÷ 0.03)² × 0.5 × 0.5 = 1,067.1, rounded up (`pt.q22.exact`, `.n`). Traps:
(A) the square left out (`pt.q22.trap.no_square`); (C) rounded down (`pt.q22.trap.down`); (D) z*
for 90% (`pt.q22.trap.n90`).

**23 (8.4, 8.5).** A library claims that 60% of its visitors find a book they want. In a random
sample of 150 visitors, 81 did, p̂ = 0.54 (`pt.q23.*`). For H0: p = 0.60 against Ha: p < 0.60,
the p value? **(A) 0.0668**; (B) 0.1336; (C) 0.0702; (D) 0.9332. Values: large counts 90 and 60
(`pt.q23.np0`, `.nq0`); SD √(0.60 × 0.40 ÷ 150) = 0.040; z = −1.50; p = 0.0668. Traps:
(B) two-sided; (C) the SE from p̂, 0.0407, as for an interval (z = −1.47); (D) the wrong tail.

**24 (8.6).** A cafeteria manager tests H0: p = 0.60 against Ha: p < 0.60, where p is the share
of the school's students who buy lunch at least three days a week (`pt.q24.p0`). Which is a
Type II error? (A) Concluding that fewer than 60% buy lunch that often, when in fact 60% do;
**(B) not concluding that fewer than 60% buy lunch that often, when in fact fewer do**;
(C) concluding that 60% buy lunch that often, when in fact more do; (D) taking a sample too small
to detect a difference. Trap (A) is a Type I error; (C) states a conclusion a test never reaches
(it never concludes H0); (D) is a cause of low power, not an error.

**25 (8.8).** A library randomly assigned 400 borrowers, 200 to get a reminder text and 200 not;
64 and 46 returned their books on time, 0.32 and 0.23 (`pt.q25.*`). For H0: p1 = p2 against
Ha: p1 ≠ p2, the test statistic and p value? (A) z = 4.03, p = 0.0001; (B) z = 2.02,
p = 0.0219; (C) z = 2.03, p = 0.0428; **(D) z = 2.02, p = 0.0438**. Values: pooled share 0.275,
SE 0.04465, z = 0.09 ÷ 0.04465 = 2.02, p = 0.0438 (`pt.q25.pooled`, `.se`, `.z`, `.p`); 95%
interval for p1 − p2, (0.003, 0.177) (`pt.q25.ci`). Traps: (A) the SE with all 400 as one
sample (`pt.q25.trap.z_one_n`, `.p_one_n`); (B) one-sided (`pt.q25.trap.one_sided`); (C) the
unpooled SE of the interval, 0.0444 (`pt.q25.trap.se_unpooled`, `.z_unpooled`, `.p_unpooled`).

**26 (9.3; Figure 25).** A random sample of 300 adults, by age group (under 40, 40 and over) and
main news source (phone, TV, print): 95, 40, 15 and 60, 65, 25 (`pt.q26.*`). Figure 25 is the
segmented bar chart (percents 63.3, 26.7, 10.0 and 40.0, 43.3, 16.7, `pt.fig25.*`). To ask
whether age group and news source are associated among all adults, use which test, with how many
degrees of freedom? (A) a chi-square test of homogeneity, 2 df; **(B) a chi-square test of
independence, 2 df**; (C) a chi-square test of independence, 5 df; (D) a two-sample z test for
two proportions. Values: df = (2 − 1)(3 − 1) = 2 (`pt.q26.df`); expected counts 77.5, 52.5,
20.0 in each row (`pt.q26.expected`); for the answer's last sentence, χ² = 16.36, p = 0.0003
(`pt.q26.chi2`, `.p`). Traps: (A) one sample with two variables, not separate samples from
groups; (C) cells less one (`pt.q26.trap.cells_less_one`); (D) news source has three values.

**27 (9.2).** An experiment randomly assigned 180 seedlings to three watering schedules: daily,
41 survived and 9 died; every other day, 44 and 16; weekly, 40 and 30 (`pt.q27.*`; rows 50, 60,
70; columns 125 and 55). If schedule and survival were not associated, how many weekly-watered
seedlings would be expected to die? (A) 30; (B) 18.33; **(C) 21.39**; (D) 48.61. Values:
70 × 55 ÷ 180 (`pt.q27.expected_weekly_died`); all six expected counts (`pt.q27.expected`);
χ² = 9.13, 2 df, p = 0.0104 (`pt.q27.chi2`, `.df`, `.p`). Traps: (A) the observed count;
(B) 55 split equally among three unequal groups (`pt.q27.trap.equal_split`); (D) the expected
survivors (`pt.q27.trap.weekly_survived`).

### Means

**28 (7.2).** Time customers spend in a café is skewed right with mean 48 minutes and SD 12
minutes (`pt.q28.*`). For random samples of 36 customers, P(x̄ > 52)? **(A) 0.0228**; (B) 0.0455;
(C) 0.3694; (D) 0.9772. Values: SD of x̄ 12 ÷ √36 = 2, z = 2.00 (`pt.q28.sd`, `.z`, `.prob`); the
central limit theorem makes the normal model fit though the times are skewed. Traps: (B) both
tails; (C) σ used for x̄ (`pt.q28.trap.sigma`); (D) the lower tail.

**29 (10.2).** A random sample of 16 bags of popcorn has a mean of 23.4 unpopped kernels and
s = 4.8, and a dotplot of the 16 counts shows no strong skew or outliers (`pt.q29.*`). A 95% confidence interval for the mean of all such bags? (A) (21.05,
25.75); (B) (21.30, 25.50); (C) (13.17, 33.63); **(D) (20.84, 25.96)**. Values: 15 df,
t* = 2.131, SE 1.20, margin 2.56 (`pt.q29.df`, `.tstar`, `.se`, `.me`, `.ci`). Traps: (A) z*
(`pt.q29.trap.z`); (B) t* for 90%, 1.753 (`pt.q29.trap.tstar90`, `.ci90`); (C) s used in place
of s ÷ √n (`pt.q29.trap.no_root`).

**30 (10.2, 10.3; Figure 26).** A random sample of 12 customers' waits at a store's checkout, in
minutes (`pt.q30.values`), in the dotplot of Figure 26. Is a t interval for the mean wait
appropriate? (A) Yes: the data are a random sample; (B) yes: t procedures work for any sample;
**(C) no: the sample is small, and the dotplot shows strong right skew and an outlier**; (D) no:
the population SD is unknown. Values: five-number summary 1.8, 2.45, 3.5, 5.1, 14.6; IQR 2.65;
upper fence 9.075, so 14.6 is an outlier (`pt.q30.five`, `.iqr`, `.fence_hi`, `.out`); mean 4.63
(`pt.q30.mean`). Traps: (A) randomness is one condition, not all; (D) an unknown σ is why t is
used.

**31 (4.1, 10.4).** Ten runners each ran a mile in shoe A and in shoe B, in random order
(`pt.q31.runners`). Which investigative question does a paired t test of their times answer?
**(A) For runners like these, is the mean difference in mile time between the two shoes
different from 0?** (B) Is the mean mile time in shoe A different from 0? (C) Do runners who
wear shoe A run faster than different runners who wear shoe B? (D) What share of runners prefer
shoe A? Traps: (B) tests the wrong value; (C) describes two independent groups; (D) is about a
share, and nothing asked for preferences.

**32 (10.4).** The ten runners' times, shoe A minus shoe B, in seconds: 2, −3, −4, 5, −2, 4, 0,
9, −1, 6 (`pt.q32.diffs`). The test statistic for H0: μd = 0? (A) 0.16; **(B) 1.18**; (C) 3.72;
(D) 0.37. Values: mean difference 1.60, sd 4.300, SE 1.360, t = 1.18 with 9 df, p = 0.2695
(`pt.q32.mean`, `.sd`, `.se`, `.t`, `.df`, `.p`). Traps: (A) a two-sample t on the two columns,
which ignores the pairing (`pt.q32.trap.two_sample`); (C) s ÷ n in place of s ÷ √n
(`pt.q32.trap.over_n`); (D) the mean ÷ s, with no √n (`pt.q32.trap.no_root`). The data file is
`practice/practice-shoes.csv`.

**33 (10.5).** 75 students were randomly assigned to two ways of practicing for a skills test:
40 had mean 72.5 and s = 8.0; 35 had mean 68.0 and s = 10.5 (`pt.q33.*`). The two-sample t
statistic? (A) 1.48; (B) 6.36; (C) 0.34; **(D) 2.06**. Values: difference 4.5, SE
√(8.0² ÷ 40 + 10.5² ÷ 35) = 2.1794, t = 2.06 (`pt.q33.diff`, `.se`, `.t`). Traps: (A) the two
SEs added (`pt.q33.trap.add_se`); (B) the SDs not squared (`pt.q33.trap.no_square`); (C) the
sample sizes left out (`pt.q33.trap.no_n`).

**34 (10.6).** 40 students are randomly assigned, 20 each, to two vocabulary apps; after a month
each takes the same quiz (`pt.q34.*`). To estimate how much the mean scores differ, use: (A) a
one-sample t interval; (B) a paired t interval; **(C) a two-sample t interval**; (D) a
two-proportion z interval. Trap (B): no student is in both groups.

### Regression

Questions 35 to 37 and 39 share one setting: a snack stand's iced-drink sales on 25 summer days
and each day's high (`practice/practice-iced.csv`; Figure 27).

**35 (11.1; Figure 27).** Which describes the relationship between the day's high and iced drinks
sold? **(A) strong, positive, and linear**; (B) weak and positive; (C) strong and negative;
(D) curved, with no linear trend. Values: r = 0.929 (`pt.q35.r`), for the answer only; highs
from 60 to 95 °F (`pt.q35.x_range`).

**36 (11.2).** LinReg(a+bx) gives a = −210.760 and b = 5.347 (`pt.q36.a`, `.b`). Which interprets
the slope? (A) For each additional drink sold, the day's high is 5.347 degrees higher, on
average; **(B) for each additional degree, the stand sells about 5.347 more iced drinks, on
average**; (C) on a day with a high of 0 degrees, the stand sells −210.760 drinks; (D) the high
explains 5.347% of the variation in drinks sold. Traps: (A) reverses the variables; (C)
interprets the intercept, far outside the data; (D) confuses the slope with r².

**37 (11.3).** On day 8 the high was 94 °F and the stand sold 345 iced drinks (`pt.q37.day`,
`.high`, `.drinks`), the largest residual of the 25. Its residual? (A) −53.1; (B) 291.9;
(C) −157.6; **(D) 53.1**. Values: predicted −210.760 + 5.347 × 94 = 291.9, residual 345 − 291.9 =
53.1 (`pt.q37.predicted`, `.residual`). Traps: (A) predicted minus observed (`pt.q37.trap.sign`);
(B) the predicted value; (C) the intercept left out (`pt.q37.trap.no_intercept`).

**38 (11.3; Figure 28).** Twelve braking trials at 20 to 75 miles per hour (`practice/
practice-stopping.csv`): the line for stopping distance has r = 0.990 (`pt.q38.r`), and Figure
28 is its residual plot (`pt.fig28.res`). What does the plot show? (A) The line fits well, since
r = 0.990; (B) the line overpredicts at every speed; **(C) a curved model would fit better: the
residuals are positive at low and high speeds and negative in between**; (D) the residuals are
small, so their pattern does not matter. Traps: (A) a high r does not show a line is the right
shape; (B) four of the twelve residuals are positive.

**39 (11.2).** For the 25 days, r² = 0.862 (`pt.q39.r2`). Which interprets it? **(A) 86.2% of
the variation in drinks sold is accounted for by the linear relationship with the day's high**;
(B) 86.2% of the line's predictions are correct; (C) the slope is 0.862 drinks per degree;
(D) 86.2% of the days were hot. Value `pt.q39.r2_pct`.

**40 (11.2).** For a set of data, r = 0.60, x̄ = 20, sx = 5, ȳ = 50, and sy = 12 (`pt.q40.*`).
The least-squares line? (A) ŷ = 45.0 + 0.25x; (B) ŷ = 2.0 + 2.40x; (C) ŷ = −52.0 + 1.44x;
**(D) ŷ = 21.2 + 1.44x**. Values: b = 0.60 × 12 ÷ 5 = 1.44, a = 50 − 1.44 × 20 = 21.2
(`pt.q40.b`, `.a`); at x = 25, ŷ = 57.2 (`pt.q40.predicted`). Traps: (A) sx ÷ sy
(`pt.q40.trap.flipped_b`, `.flipped_a`); (B) r left out (`pt.q40.trap.no_r_b`, `.no_r_a`);
(C) x̄ and ȳ swapped in the intercept (`pt.q40.trap.swapped_a`).

### The letters

| Letter | Questions | Count |
| --- | --- | --- |
| A | 2, 5, 11, 15, 19, 23, 28, 31, 35, 39 | 10 |
| B | 4, 7, 10, 13, 17, 22, 24, 26, 32, 36 | 10 |
| C | 3, 8, 9, 14, 18, 21, 27, 30, 34, 38 | 10 |
| D | 1, 6, 12, 16, 20, 25, 29, 33, 37, 40 | 10 |

## Part 2: four written questions

Each answer gives a model answer and a "complete answer includes" list in the book's own words.

**W1. Designing a study (4.1, 4.5, 4.6).** A school cafeteria wonders whether putting fruit at
the start of the lunch line, instead of at the end, increases the number of fruit cups students
take. It has 30 school days for a study (`pt.w1.days`).

- (a) Write a statistical investigative question the study can answer.
- (b) Describe how to randomly assign the 30 days, 15 to each placement (`pt.w1.per_group`), so
  that someone else could carry it out.
- (c) Name one variable, other than placement, that could affect fruit taken, and say how
  random assignment deals with it.
- (d) Say what the results can be generalized to, and what they cannot.

Complete answer includes: (a) a question about the mean (or total) number of fruit cups taken
per day, comparing the two placements, for this cafeteria; (b) a chance method that gives every
set of 15 days the same chance (numbered slips, or randInt with repeats skipped), and the other
15 days get the other placement; (c) a named variable such as the day's menu or weather, and that
random assignment spreads such variables across both placements, so a difference can be credited
to placement; (d) days like these in this cafeteria, not other schools or other times of year.

**W2. Describing and comparing (3.2 to 3.7; Figure 29).** One-way commutes of 25 students who
bike and 25 who ride the bus (`practice/practice-commute.csv`), in parallel dotplots.

| Value | Bike | Bus |
| --- | --- | --- |
| Five-number summary | 9, 15, 17, 19, 24 | 12, 15.5, 19, 24, 48 |
| IQR | 4 | 8.5 |
| Fences | 9 and 25 | 2.75 and 36.75 |
| Outliers | none (9 is on the fence) | 48 |
| Mean, SD | 16.84, 3.80 | 20.60, 7.32 |

(`pt.w2.bike.*`, `pt.w2.bus.*`.)

- (a) Compare the two distributions in context: shape, center, spread, and unusual values.
- (b) Use the 1.5 × IQR rule to decide whether either group has outliers; show the fences.
- (c) Which measure of center better describes the bus commutes, and why?
- (d) A bus rider's commute is 30 minutes. Find and interpret its z-score among the bus commutes.

Values for (d): z = (30 − 20.60) ÷ 7.32 = 1.28 (`pt.w2.bus.z30`). Complete answer includes:
(a) bus commutes skewed right with a high outlier, bike commutes roughly symmetric; bus median 19
above bike median 17; bus spread larger (IQR 8.5 against 4); all in minutes and in context;
(b) both groups' fences, and 48 above 36.75 is an outlier while 9 is not below 9; (c) the median,
19, because skew and the outlier pull the mean up to 20.60; (d) 1.28 SDs above the bus mean.

**W3. A complete inference procedure (8.9, 10.3, 10.2).** A drink machine is set to fill cups with
12 ounces (`pt.w3.target`). An inspector measures 20 cups chosen at random from a day's output
(`pt.w3.values`). Is there convincing evidence, at α = 0.05 (`pt.w3.alpha`), that the machine
underfills on average?

- (a) Carry out the test in the four parts of Section 8.9.
- (b) Give a 95% confidence interval for the mean fill, and say whether it agrees with (a).

Values: x̄ = 11.922, s = 0.1564, SE 0.0350, t = −2.23 with 19 df, p = 0.0190 (`pt.w3.mean`,
`.sd`, `.se`, `.t`, `.df`, `.p`); conditions: random; 20 is far less than 10% of a day's cups;
the sample is small, so the data are checked: five-number summary 11.59, 11.825, 11.945, 12.04,
12.18, fences 11.5025 and 12.3625, no outliers (`pt.w3.five`, `.fences`, `.out`), no strong skew.
Interval: t* = 2.093, margin 0.073, (11.849, 11.995) (`pt.w3.tstar`, `.me`, `.ci`). Complete
answer includes: H0: μ = 12 and Ha: μ < 12 with μ defined in context; all three conditions,
with the normal shape checked from the data; t, df, and p; a conclusion in context that rejects
H0 because 0.0190 < 0.05; for (b), the interval, with the note that 12 is not in it, which
agrees with rejecting a two-sided test at 0.05 and so with the one-sided result.

**W4. Probability, sampling, and inference together (6.4, 7.1, 8.4, 8.5).** A factory's parts
are defective with probability 0.08, independently (`pt.w4.p`).

- (a) In a box of 10 parts (`pt.w4.n_small`), what is the probability that at least one is
  defective?
- (b) For random samples of 200 parts (`pt.w4.n`), describe the sampling distribution of p̂, and
  find P(p̂ ≥ 0.125).
- (c) After a machine is repaired, 25 of a random sample of 200 parts are defective
  (`pt.w4.x`). Is there convincing evidence that the defect rate is now above 0.08? Say how (b)
  answers this.

Values: (a) 1 − 0.92¹⁰ = 1 − 0.4344 = 0.5656 (`pt.w4.p_none`, `.p_some`); (b) mean 0.08,
SD √(0.08 × 0.92 ÷ 200) = 0.01918, large counts 16 and 184, so approximately normal; z = 2.35,
P = 0.0095 (`pt.w4.sd`, `.np`, `.nq`, `.z`, `.prob`); (c) p̂ = 0.125 (`pt.w4.phat`), the same z
and p value, 0.0095 < 0.05, so convincing evidence; the exact binomial share,
1 − binomcdf(200,0.08,24) = 0.0178 (`pt.w4.exact`), also below 0.05, for an optional remark.
Complete answer includes: (a) the complement rule; (b) center, spread, and shape, with the large
counts checked; (c) hypotheses, the p value read as the probability in (b), and a conclusion in
context.

## The investigative-question parts in Chapters 8 to 10

C6b adds one part to one written review question in each of Chapters 8, 9, and 10, asking the
student to write the statistical investigative question the procedure answers. They use the
chapters' own Tonmick numbers and need no new values.

## The figures

| Figure | File | Question | Shows | Values |
| --- | --- | --- | --- | --- |
| 22 | `fig22.png` | 2 | Histogram of 80 waits, bars 4 minutes wide | `pt.fig22.*` |
| 23 | `fig23.png` | 4 | Parallel modified box plots, Models A and B | `pt.fig23.*` |
| 24 | `fig24.png` | 13 | Dotplot of 200 reruns' differences, observed 0.20 marked | `pt.fig24.*` |
| 25 | `fig25.png` | 26 | Segmented bar chart of news source by age group | `pt.fig25.*` |
| 26 | `fig26.png` | 30 | Dotplot of 12 checkout waits | `pt.fig26.values` |
| 27 | `fig27.png` | 35 to 37, 39 | Scatterplot of drinks against the day's high, with the line | `pt.fig27.*` |
| 28 | `fig28.png` | 38 | Residual plot for stopping distance against speed | `pt.fig28.*` |
| 29 | `fig29.png` | W2 | Parallel dotplots of bike and bus commutes | `pt.fig29.*` |
