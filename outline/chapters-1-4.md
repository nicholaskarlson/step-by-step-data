# Chapters 1 to 4: the outline and its numbers

This file is the source for the book's Chapters 1 to 4. For each section it gives the worked
example, the values the text prints, and the Try It answer. For each chapter it also gives the
one-page review. Every value is named as in `expected/chapters_1_4.csv`. `python/chapters_1_4.py`
and `r/chapters_1_4.R` compute each one independently, and `run_all.py` requires both to match
the expected file character for character. Values appear here as the book prints them, except
that the book uses a true minus sign (−) where this file has a hyphen.

The data are fictional: the Tonmick study is invented for teaching.

Conventions:

- The calculator's quartiles are the medians of the two halves, with the median left out when
  n is odd.
- Sx divides by n − 1 and σx by n.
- A share "of the known" uses the 1,208 students whose first-year outcome is known. The 11 who
  withdrew consent are left out of it.

## Chapter 1. Getting Started with the TI-84 Plus CE

Sections 1.1 to 1.6 and 1.8 to 1.11 print no data values. Section 1.9's list lengths (609, 610,
and 555) are checked in `expected/data_summary.csv`.

**1.7 Ten Exercises to Try.** Exercises 1 to 3 and 10 type numbers into L1 and L2, so the
section asks readers to load the Tonmick lists afterward (Section 1.9).

| Exercise | Inputs | Screen to expect (keys) |
| --- | --- | --- |
| 1. 1-Var Stats | The first ten visits in `tonmick-offered.csv`: 9, 3, 2, 2, 2, 0, 7, 9, 9, 7 (`ch1.ex1.data`) | x̄ = 5, Σx = 50, Sx = 3.528, σx = 3.347, n = 10; minX, Q1, Med, Q3, maxX = 0, 2, 5, 9, 9 (`ch1.ex1.*`) |
| 2. A box plot | The same list | IQR 7; fences −8.5 and 19.5; no dots (`ch1.ex2.*`) |
| 3. A histogram | Xmin 0, Xmax 10, Xscl 2 | Bars of 1, 4, 0, 2, 3 (`ch1.ex3.bars`) |
| 4. Normal areas | Normal model, mean 3.010, SD 0.469 | normalcdf(3.5, 1E99, …) = 0.1481; invNorm(0.9, …) = 3.611 (`ch1.ex4.*`). Points to Section 6.6 |
| 5. Binomial | n = 10, p = 0.13 | binompdf at 2 = 0.2496; binomcdf at 2 = 0.8692 (`ch1.ex5.*`) |
| 6. Random integers | Seed 2027; randInt(1,1219,5) | No values printed: neighbors compare screens. Points to Section 4.3 |
| 7. 1-PropZInt | x = 80, n = 605 | (0.1052, 0.1592), p̂ = 0.1322 (`ch1.ex7.*`). Points to Section 8.2: these 605 are not a random sample, which is why Section 8.1 uses the sample of 100 |
| 8. 2-SampTTest, Stats | 2.507389, 3.104596, 609; 2.193443, 2.731310, 610; Pooled: No | t = 1.87, p = 0.0611, df = 1197.07 (`ch1.ex8.*`). Points to Investigation 7 |
| 9. χ²-Test, 2 × 2 | [[80, 525], [93, 510]] | χ² = 1.191, p = 0.2751, df = 1 (`ch1.ex9.*`) |
| 10. LinReg(a+bx) | The first six pairs in `tonmick-grades-not-offered.csv` (`ch1.ex10.pairs`) | a = −0.643, b = 1.198, r² = 0.774, r = 0.880 (`ch1.ex10.*`) |

## Chapter 2. Data and Variables

| Section | Worked example and values | Try it (answer) |
| --- | --- | --- |
| 2.1 What Statistics Can Learn from Data | 1,600 invited at 16 colleges; 1,219 joined; 609 offered and 610 not (`ch2.invited`, `ch2.colleges`, `ch2.joined`, `ch2.offered`, `ch2.not_offered`). The population a question is about, the sample that answers it, a census, N and n. The comparison 80 against 93 withdrawals (`ch2.offered.withdrew`, `ch2.not_offered.withdrew`) | Which is a statistical question? Answer (a): student S1000017 made 9 visits (`ch2.first_student`, `ch2.first_student_visits`) |
| 2.2 Variables | Categorical and quantitative; discrete (visits) and continuous (grades). The mean of `offer` is 609 of 1,219 = 0.4996 (`ch2.offer_mean`). Parameter and statistic: with the joiners as the population, 173 of 1,208 = 0.1432 withdrew (`ch2.withdrew_known.share`), a parameter; a sample's share is a statistic | Classify `grade_12`, `exit`, `part_time` (no numbers) |
| 2.3 Tables for One Categorical Variable | How the year ended: 992, 173, 43, 11; 81.4%, 14.2%, 3.5%, 0.9%; on the home screen, 0.8138, 0.1419, 0.0353, 0.0090 (`ch2.exit.*`) | Share withdrawn among the known: 14.3% of 1,208, against 14.2% of 1,219 (`ch2.withdrew_known.pct`, `ch2.exit.withdrew.pct`) |
| 2.4 Bar Charts and Pie Charts | Bars of 992, 173, 43, 11 | The axis from 75 to 95: the bar for 93 looks 3.6 times as tall as the bar for 80, when 93 is only 16% more (`ch2.try4.*`); fairer: shares from 0, 13.2% of 605 and 15.4% of 603 (`ch2.offered.withdrew.pct`, `ch2.not_offered.withdrew.pct`) |

**Chapter 2 review** (four multiple choice, two written; answers in the back):

1. *(Multiple choice; no numbers.)* Which Tonmick variable is quantitative and discrete? (visits).
2. *(Multiple choice; a fictional district; summary numbers only.)* District records show that
   27.4% of all 4,812 ninth graders ride a bus. A survey of 150 finds 31 bus riders, 20.7%
   (`ch2.review.bus.pct`). Which number is the parameter?
3. *(Multiple choice; summary numbers.)* Of 1,600 students invited, 1,219 joined. What share
   joined? 76.2% (`ch2.review.joined.pct`).
4. *(Multiple choice; no numbers.)* What is wrong with a bar chart whose bars touch and whose
   axis starts at 75?
5. *(Written; fictional; summary numbers.)* A cafeteria survey of 240 students: pizza 96, salad
   36, sandwiches 60, other 48. Make a table of shares (40%, 15%, 25%, 20%;
   `ch2.review.cafeteria.*`) and sketch a bar chart.
6. *(Written; Tonmick; summary numbers.)* Of the 605 offered whose outcome is known, 504
   stayed, 80 withdrew, and 21 transferred. Of the 603 not offered, the counts were 488, 93,
   and 22.
   - Give each group's shares: 83.3%, 13.2%, 3.5% against 80.9%, 15.4%, 3.6%
     (`ch2.review.offered.*`, `ch2.review.not_offered.*`).
   - Say why the comparison uses shares, not counts.

## Chapter 3. One Quantitative Variable

| Section | Worked example and values | Try it (answer) |
| --- | --- | --- |
| 3.1 Histograms, Dotplots, and Stemplots | L2, bars 2 wide: 317, 141, 61, 41, 26, 10, 7, 3, 2, then 1 student at 25 (`ch3.hist2.*`). Joiners by college as a dotplot and a stemplot: 65 to 86 (`ch3.college.sorted`); stems 6 \| 5; 7 \| 1122455677; 8 \| 02336 (`ch3.college.stems`) | Xscl = 1: first bar 170, 27.9% (`ch3.L2.zero`, `ch3.L2.zero.pct`) |
| 3.2 Describing a Distribution | Visits skewed right; median 1, quartiles 0 and 3, mean 2.507; 49 made 8 or more (`ch3.L2.*`). Joiners by college: roughly symmetric, one peak in the 70s, no gaps; 65 at TC25 sits a little apart (`ch3.college.min`) | Mean or median for the center? The median, 1 |
| 3.3 Summary Statistics | 1-Var Stats on L2: x̄ = 2.507, Sx = 3.105, n = 609, five-number summary 0, 0, 1, 3, 25, Σx = 1527, Σx² = 9689, σx = 3.102 (`ch3.L2.*`). By hand for the 16 college counts: mean 76.19, median 75.5, squared deviations 460.44, variance 30.70, SD 5.54, quartiles 72 and 81, range 21 (`ch3.college.*`); percentiles | Drop the 25: the median stays 1; mean (1527 − 25)/608 = 2.470 (`ch3.L2.mean_without_max`) |
| 3.4 Changing Units | Visits + 1: mean 3.507, median 2, quartiles 1 and 4, Sx still 3.105 (`ch3.units.plus1.*`). School grades × 25: mean 75.25, Sx 11.73 (`ch3.units.times25.*`), from mean 3.010 and Sx 0.469 (`ch3.entry.mean`, `ch3.entry.sx`) | Every grade − 0.25: the mean goes from 3.010 to 2.760 and the median from 3.00 to 2.75; Sx stays 0.469 and the IQR 0.67 (`ch3.units.minus025.*`, `ch3.entry.med`, `ch3.entry.iqr`) |
| 3.5 Box Plots and Outliers | IQR 3; fences −4.5 and 7.5; 49 outliers from 8 to 25; whisker to 7 (`ch3.L2.*`). The 2-SD rule: above 8.72, so 34 students, those with 9 or more (`ch3.L2.two_sd*`). College counts: fences 58.5 and 94.5, no outliers (`ch3.college.fences`) | L4: the same fences; 37 above (`ch3.L4.fences`, `ch3.L4.outliers`); its 2-SD line, 7.66, flags the same 37 (`ch3.L4.two_sd*`) |
| 3.6 Relative Position: z-Scores and Percentiles | S1000017: school grade 3.54, z = 1.13, 86.8th percentile of 1,219; college grade 3.67, z = 1.20, 87.9th percentile of 1,116, whose mean is 2.996 and Sx 0.561 (`ch3.z.*`). z uses x̄ and Sx; σx gives the same z to two decimals (`ch3.z.*.z_sigma`) | z for a school grade of 2.50: −1.09 (`ch3.z.try.2_50`) |
| 3.7 Comparing Distributions | Offered against not offered: zeros 170 (27.9%) and 199 (32.6%); five-number summaries 0, 0, 1, 3, 25 and 0, 0, 1, 3, 16; means 2.507 and 2.193, a gap of 0.314; Sx 3.105 and 2.731; 8 or more, 49 against 37 (`ch3.L2.*`, `ch3.L4.*`, `ch3.gap`). Back-to-back stemplot, the percent who withdrew at each college, among the known: offered 0, 0, 7, 9, 11, 13, 14, 14, 15, 16, 17, 17, 17, 18, 22, 24 (median 14.5); not offered 7, 7, 9, 10, 11, 14, 14, 15, 16, 19, 19, 19, 20, 22, 22, 27 (median 15.5) (`ch3.b2b.*`) | One sentence comparing the centers (no new numbers) |

**Chapter 3 review:**

1. *(Multiple choice; fictional; summary numbers only.)* A distribution has mean 12.4 and
   median 9.0. Which shape is most likely? (skewed right).
2. *(Multiple choice; fictional; summary numbers only.)* Commute times: minimum 2, Q1 10,
   median 14, Q3 18, maximum 35. The fences are −2 and 30, so 35 is an outlier
   (`ch3.review.five.fences`).
3. *(Multiple choice; fictional.)* Scores out of 50, with mean 38.6 and SD 5.2, are doubled to
   percents. The new mean is 77.2 and the new SD 10.4 (`ch3.review.scale.*`).
4. *(Multiple choice; fictional.)* Which test went relatively better: 82 when the mean was 74
   and the SD 6 (z = 1.33), or 88 when the mean was 81 and the SD 4 (z = 1.75)?
   (`ch3.review.z.*`).
5. *(Written; Tonmick.)* For L4, give the five-number summary, the mean, and Sx, and describe
   the shape. Then say how many students each outlier rule flags: 37 and 37 (`ch3.L4.*`).
6. *(Written; fictional; by hand.)* Eight students' study minutes: 5, 8, 12, 15, 15, 20, 25, 60.
   - The mean is 20.0, the median 15, Sx 17.35, the quartiles 10 and 22.5, and the upper
     fence 41.25, so 60 is an outlier.
   - Without the 60: mean 14.29, Sx 6.82, median 15 (`ch3.review.minutes.*`).
   - Which statistics resist the outlier?

## Chapter 4. Collecting Data: Samples and Experiments

| Section | Worked example and values | Try it (answer) |
| --- | --- | --- |
| 4.1 The Investigative Question | Its three parts: the variables (the offer; withdrawal within the first year); the analysis (the difference in withdrawal shares, tested against 0 or estimated); the conclusion (a claim about cause, for students like these 1,219) | An investigative question about visits, in three parts (no numbers) |
| 4.2 Kinds of Studies | Census, sample survey, observational study (prospective or retrospective), experiment. Visits and withdrawal, among the known: those who withdrew averaged 1.43 visits, the others 2.51 (`ch4.visits.withdrew.mean`, `ch4.visits.stayed_or_transferred.mean`). They had fewer months to visit. Part-time students visited less (1.89 against 2.62; `ch4.visits.*_time.mean`) and withdrew more (22.5% against 9.5%; `ch4.*_time.withdrew.pct`), so part-time study confounds the link. Consent: 11 withdrew it (`ch4.consent_withdrawn`) | Prospective or retrospective: a study that pulls last year's records (retrospective) |
| 4.3 Random Sampling | A simple random sample of 30 of the 1,219, without replacement. Stratified: 30 × 449 ÷ 1,219 = 11.1, so 11 part-time and 19 full-time (`ch4.srs30.*`), because part-time students withdraw more. A cluster sample of 2 colleges. Systematic: every 40th row from a random start between 1 and 40 gives 30 or 31 students, 31 when the start is 19 or less (`ch4.systematic.*`) | Stratified sample of 40: 14.7, so 15 and 25 (`ch4.try40.*`) |
| 4.4 Problems with Sampling | 381 of 1,600 (23.8%) did not join; 770 of 960 full-time (80.2%) and 449 of 640 part-time (70.2%) joined; part-time 40% of invited, 36.8% of joiners; withdrawn among the known, 101 of 448 (22.5%) part-time against 72 of 760 (9.5%) full-time (`ch4.not_joined*`, `ch4.invited.*`, `ch4.part_time.*`, `ch4.full_time.*`). Voluntary response, convenience, undercoverage, and response bias, each with a short case | "1,219 is a big sample": 80.2% against 70.2% joined, and a bigger group that joins the same way is tilted the same way |
| 4.5 Principles of Experiments | 609 and 610 by chance; part-time 234 of 609 (38.4%) against 215 of 610 (35.2%), a gap of 3.2 points by chance (`ch4.balance.*`); not blind | Could the study have been blind? What would a placebo be? (no numbers) |
| 4.6 Experimental Designs | Completely randomized, randomized block (16 colleges; 49.3% to 50.8% offered in each; `ch4.blocks.offered.range`), and matched pairs | Why randomize within each college? (no numbers) |

**Chapter 4 review:**

1. *(Multiple choice; fictional.)* A principal numbers 1,200 students and takes every 25th from
   a random start between 1 and 25. Systematic, 48 students (`ch4.review.systematic.size`).
2. *(Multiple choice; fictional; no numbers.)* A poll on a school website: voluntary response.
3. *(Multiple choice; Tonmick; no numbers.)* Visits and withdrawal: an observational
   comparison, with part-time study as a confounder.
4. *(Multiple choice; fictional; no numbers.)* Pairs matched on school grade, with one of each
   pair assigned at random: matched pairs.
5. *(Written; fictional.)* A gym wants to know whether a text reminder raises weekly visits.
   - Write the investigative question in three parts.
   - Design a completely randomized experiment for 200 members, with randInt( and the repeats
     skipped.
   - Say whom the result describes.
6. *(Written; Tonmick; summary numbers.)* A stratified sample of 60 joiners by enrollment:
   60 × 449 ÷ 1,219 = 22.10, so 22 part-time and 38 full-time (`ch4.review60.*`). Explain why
   stratifying by enrollment helps here.

## The three fixed samples

`python/make_samples.py` drew these once, with seed 2027, fixed before any draw (see
`data/SOURCE.md`). They are never redrawn. With the joiners as the population, the true values
are known, so a reader can see whether an interval captured them.

| File | Drawn from | Values (keys) | Used in |
| --- | --- | --- | --- |
| `samples/tonmick-sample-100.csv` | The 1,208 with a known outcome; 0.1432 of them withdrew (`samples.population.*`) | 15 withdrew; 33 part-time; 51 offered (`samples.100.*`) | Sections 8.1 to 8.6 (D2) |
| `samples/tonmick-sample-120.csv` | The same 1,208 (a separate draw) | 19 withdrew; 43 part-time (`samples.120.*`) | Section 9.3 (D3) |
| `samples/tonmick-sample-20.csv` | The 1,116 with a college grade; their mean school grade 3.016 and college grade 2.996 | mean school grade 3.056, college grade 3.157 (`samples.20.*`) | Sections 10.1 to 10.4 (D3) |

A note for D2: the sample of 100's share, 15 of 100 = 0.15, equals Section 8.4's planned goal
of 15%. The test of that goal gives z = 0 and a p value of 0.5. The true share, 0.1432, is
below the goal, so failing to reject is a Type II error, as Section 8.6 says. The sample stays
as drawn.
