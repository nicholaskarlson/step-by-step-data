# Route 2 for Chapters 1 to 4: every number the chapters, their Try It answers, and their
# reviews print, rebuilt from the data files with base R (no add-on packages).
#
#   Rscript --vanilla r/chapters_1_4.R ROOT OUT.csv
#
# It shares no code with python/chapters_1_4.py. Values are written as the book prints
# them (name,value), with the TI-84's quartiles (the medians of the two halves, the median
# left out when n is odd), Sx dividing by n - 1 and sigma-x by n, and the ASCII
# hyphen-minus for negative numbers. The samples are checked here, not redrawn: each row
# must be a row of data/tonmick-classroom.csv, with no repeats, and each file's MD5 is
# reported (base R has md5sum; run_all.py checks the SHA-256).

args <- commandArgs(trailingOnly = TRUE)
root <- args[1]
out <- args[2]
vals <- list()
put <- function(name, value) {
  if (!is.null(vals[[name]])) stop(paste("duplicate name", name))
  vals[[name]] <<- as.character(value)
}
fx <- function(x, places) sprintf(paste0("%.", places, "f"), x)
gx <- function(x) sprintf("%g", x)
pc <- function(num, den, places = 1) sprintf(paste0("%.", places, "f"), 100 * num / den)
big <- function(n) formatC(n, big.mark = ",", format = "d")
readc <- function(path) read.csv(file.path(root, path), colClasses = "character", check.names = FALSE)

med <- function(v) {
  v <- sort(v); n <- length(v)
  if (n %% 2 == 1) v[(n + 1) / 2] else (v[n / 2] + v[n / 2 + 1]) / 2
}
calc <- function(x) {
  v <- sort(x); n <- length(v); h <- n %/% 2
  lower <- v[seq_len(h)]
  upper <- if (n %% 2 == 1) v[(h + 2):n] else v[(h + 1):n]
  m <- sum(v) / n
  ss <- sum((v - m)^2)
  list(n = n, mean = m, sum = sum(v), sum2 = sum(v^2), ss = ss, sx = sqrt(ss / (n - 1)), sg = sqrt(ss / n),
       min = v[1], q1 = med(lower), med = med(v), q3 = med(upper), max = v[n])
}
five <- function(s) paste(gx(c(s$min, s$q1, s$med, s$q3, s$max)), collapse = ", ")
bars <- function(x, start, width, stop) {
  edges <- seq(start, stop - width, by = width)
  sapply(edges, function(lo) sum(x >= lo & x < lo + width))
}

every <- readc("data/tonmick-classroom.csv")
invited <- readc("data/tonmick-invited.csv")
N <- nrow(every)
known <- every[every$withdrew %in% c("0", "1"), ]

# ---- Chapter 1: the ten exercises ----
off <- readc("data/tonmick-offered.csv")
v <- as.numeric(off$visits[1:10])
put("ch1.ex1.data", paste(gx(v), collapse = ", "))
s <- calc(v)
put("ch1.ex1.mean", gx(s$mean)); put("ch1.ex1.sum", gx(s$sum)); put("ch1.ex1.sx", fx(s$sx, 3))
put("ch1.ex1.sigma", fx(s$sg, 3)); put("ch1.ex1.n", s$n); put("ch1.ex1.five", five(s))
iqr <- s$q3 - s$q1
put("ch1.ex2.iqr", gx(iqr)); put("ch1.ex2.fence_low", gx(s$q1 - 1.5 * iqr)); put("ch1.ex2.fence_high", gx(s$q3 + 1.5 * iqr))
put("ch1.ex2.outliers", sum(v < s$q1 - 1.5 * iqr | v > s$q3 + 1.5 * iqr))
put("ch1.ex3.bars", paste(bars(v, 0, 2, 10), collapse = ", "))
put("ch1.ex4.above_3_5", fx(pnorm(3.5, 3.010, 0.469, lower.tail = FALSE), 4))
put("ch1.ex4.p90", fx(qnorm(0.9, 3.010, 0.469), 3))
put("ch1.ex5.pdf2", fx(dbinom(2, 10, 0.13), 4)); put("ch1.ex5.cdf2", fx(pbinom(2, 10, 0.13), 4))
p <- 80 / 605; se <- sqrt(p * (1 - p) / 605); z <- qnorm(0.975)
put("ch1.ex7.low", fx(p - z * se, 4)); put("ch1.ex7.high", fx(p + z * se, 4)); put("ch1.ex7.phat", fx(p, 4))
va <- 3.104596^2 / 609; vb <- 2.731310^2 / 610
tt <- (2.507389 - 2.193443) / sqrt(va + vb)
df <- (va + vb)^2 / (va^2 / 608 + vb^2 / 609)
put("ch1.ex8.t", fx(tt, 2)); put("ch1.ex8.p", fx(2 * pt(-abs(tt), df), 4)); put("ch1.ex8.df", fx(df, 2))
obs <- matrix(c(80, 93, 525, 510), nrow = 2)
expd <- outer(rowSums(obs), colSums(obs)) / sum(obs)
chi <- sum((obs - expd)^2 / expd)
put("ch1.ex9.chi2", fx(chi, 3)); put("ch1.ex9.p", fx(pchisq(chi, 1, lower.tail = FALSE), 4)); put("ch1.ex9.df", 1)
gr <- readc("data/tonmick-grades-not-offered.csv")[1:6, ]
put("ch1.ex10.pairs", paste0("(", gr$entry_grade, ", ", gr$grade_12, ")", collapse = "; "))
fit <- lm(as.numeric(gr$grade_12) ~ as.numeric(gr$entry_grade))
r <- cor(as.numeric(gr$entry_grade), as.numeric(gr$grade_12))
put("ch1.ex10.a", fx(unname(coef(fit)[1]), 3)); put("ch1.ex10.b", fx(unname(coef(fit)[2]), 3))
put("ch1.ex10.r2", fx(r^2, 3)); put("ch1.ex10.r", fx(r, 3))

# ---- Chapter 2 ----
put("ch2.invited", big(nrow(invited))); put("ch2.colleges", length(unique(every$college))); put("ch2.joined", big(N))
n1 <- sum(every$offer == "1")
put("ch2.offered", n1); put("ch2.not_offered", N - n1); put("ch2.offer_mean", fx(mean(every$offer == "1"), 4))
put("ch2.first_student", every$student_id[1]); put("ch2.first_student_visits", every$visits[1])
for (e in c("stayed", "withdrew", "transferred", "consent withdrawn")) {
  key <- strsplit(e, " ")[[1]][1]
  cnt <- sum(every$exit == e)
  put(paste0("ch2.exit.", key), cnt); put(paste0("ch2.exit.", key, ".pct"), pc(cnt, N))
  put(paste0("ch2.exit.", key, ".share"), fx(cnt / N, 4))
}
w <- sum(known$withdrew == "1")
put("ch2.known", big(nrow(known))); put("ch2.withdrew_known.pct", pc(w, nrow(known)))
put("ch2.withdrew_known.share", fx(w / nrow(known), 4))
for (z in c("1", "0")) {
  lab <- if (z == "1") "offered" else "not_offered"
  k <- known[known$offer == z, ]
  ww <- sum(k$withdrew == "1")
  put(paste0("ch2.", lab, ".withdrew"), ww); put(paste0("ch2.", lab, ".known"), nrow(k))
  put(paste0("ch2.", lab, ".withdrew.pct"), pc(ww, nrow(k)))
}
w1 <- sum(every$offer == "1" & every$withdrew == "1"); w0 <- sum(every$offer == "0" & every$withdrew == "1")
put("ch2.try4.height_ratio", fx((w0 - 75) / (w1 - 75), 1)); put("ch2.try4.more_pct", sprintf("%.0f", 100 * (w0 / w1 - 1)))
put("ch2.review.bus.pct", pc(31, 150))
put("ch2.review.joined.pct", pc(sum(invited$joined == "1"), nrow(invited)))
cafe <- c(pizza = 96, salad = 36, sandwich = 60, other = 48)
for (item in names(cafe)) put(paste0("ch2.review.cafeteria.", item, ".pct"), pc(cafe[[item]], 240, 0))
for (z in c("1", "0")) {
  lab <- if (z == "1") "offered" else "not_offered"
  k <- known[known$offer == z, ]
  for (e in c("stayed", "withdrew", "transferred")) put(paste0("ch2.review.", lab, ".", e, ".pct"), pc(sum(k$exit == e), nrow(k)))
}

# ---- Chapter 3 ----
L2 <- as.numeric(every$visits[every$offer == "1"])
L4 <- as.numeric(every$visits[every$offer == "0"])
put("ch3.hist2.bars", paste(bars(L2, 0, 2, 18), collapse = ", "))
put("ch3.hist2.top", gx(max(L2))); put("ch3.hist2.after18", sum(L2 >= 18))
put("ch3.L2.zero", sum(L2 == 0)); put("ch3.L2.zero.pct", pc(sum(L2 == 0), length(L2)))
s <- calc(L2)
put("ch3.L2.mean", fx(s$mean, 3)); put("ch3.L2.sx", fx(s$sx, 3)); put("ch3.L2.n", s$n); put("ch3.L2.five", five(s))
put("ch3.L2.sum", gx(s$sum)); put("ch3.L2.sum2", gx(s$sum2)); put("ch3.L2.sigma", fx(s$sg, 3))
put("ch3.L2.mean_without_max", fx((s$sum - s$max) / (s$n - 1), 3))
iqr <- s$q3 - s$q1; lo <- s$q1 - 1.5 * iqr; hi <- s$q3 + 1.5 * iqr
put("ch3.L2.iqr", gx(iqr)); put("ch3.L2.fences", paste(gx(lo), gx(hi), sep = ", "))
o <- L2[L2 > hi]
put("ch3.L2.outliers", length(o)); put("ch3.L2.outliers.range", paste(gx(min(o)), "to", gx(max(o))))
put("ch3.L2.whisker", gx(max(L2[L2 <= hi])))
two <- s$mean + 2 * s$sx
put("ch3.L2.two_sd", fx(two, 2)); put("ch3.L2.two_sd.count", sum(L2 > two)); put("ch3.L2.two_sd.from", gx(min(L2[L2 > two])))
p1 <- calc(L2 + 1)
put("ch3.units.plus1.mean", fx(p1$mean, 3)); put("ch3.units.plus1.med", gx(p1$med))
put("ch3.units.plus1.quartiles", paste(gx(p1$q1), gx(p1$q3), sep = ", ")); put("ch3.units.plus1.sx", fx(p1$sx, 3))
eg <- as.numeric(every$entry_grade)
e <- calc(eg)
put("ch3.entry.mean", fx(e$mean, 3)); put("ch3.entry.sx", fx(e$sx, 3))
t25 <- calc(25 * eg)
put("ch3.units.times25.mean", fx(t25$mean, 2)); put("ch3.units.times25.sx", fx(t25$sx, 2))
# D5c: 25 x 0.469 is 11.725, a halfway value, so the book works 25 x Sx from Sx to four places
put("ch3.entry.sx4", fx(e$sx, 4))
if (fx(25 * as.numeric(vals[["ch3.entry.sx4"]]), 2) != vals[["ch3.units.times25.sx"]])
  stop("25 x ch3.entry.sx4 does not give ch3.units.times25.sx")
# D5c: a list holds at most 999 values, so the calculator shows the rule on L1 alone (609 grades)
L1 <- as.numeric(every$entry_grade[every$offer == "1"])
l1 <- calc(L1); h1 <- calc(25 * L1)
put("ch3.units.L1.mean", fx(l1$mean, 6)); put("ch3.units.L1.sx", fx(l1$sx, 6))
put("ch3.units.L1x25.mean", fx(h1$mean, 4)); put("ch3.units.L1x25.sx", fx(h1$sx, 4))
for (k in c("mean", "sx")) {
  if (fx(25 * as.numeric(vals[[paste0("ch3.units.L1.", k)]]), 4) != vals[[paste0("ch3.units.L1x25.", k)]])
    stop(paste0("25 x ch3.units.L1.", k, " does not give ch3.units.L1x25.", k))
}
m25 <- calc(eg - 0.25)
put("ch3.units.minus025.mean", fx(m25$mean, 3)); put("ch3.units.minus025.med", fx(m25$med, 2))
put("ch3.units.minus025.sx", fx(m25$sx, 3)); put("ch3.units.minus025.iqr", fx(m25$q3 - m25$q1, 2))
put("ch3.entry.med", fx(e$med, 2)); put("ch3.entry.iqr", fx(e$q3 - e$q1, 2))
tab <- table(every$college)
jc <- as.numeric(tab)
cs <- calc(jc)
put("ch3.college.sorted", paste(sort(jc), collapse = ", "))
sj <- sort(jc)
stems <- sapply(split(sj %% 10, sj %/% 10), function(l) paste(l, collapse = ""))
put("ch3.college.stems", paste(paste(names(stems), "|", stems), collapse = "; "))
put("ch3.college.mean", fx(cs$mean, 2)); put("ch3.college.med", gx(cs$med)); put("ch3.college.ss", fx(cs$ss, 2))
put("ch3.college.var", fx(cs$ss / (cs$n - 1), 2)); put("ch3.college.sx", fx(cs$sx, 2))
put("ch3.college.quartiles", paste(gx(cs$q1), gx(cs$q3), sep = ", ")); put("ch3.college.range", gx(cs$max - cs$min))
put("ch3.college.min", paste0(min(jc), " (", names(tab)[which.min(jc)], ")"))
put("ch3.college.max", paste0(max(jc), " (", names(tab)[which.max(jc)], ")"))
ci <- cs$q3 - cs$q1
put("ch3.college.fences", paste(fx(cs$q1 - 1.5 * ci, 1), fx(cs$q3 + 1.5 * ci, 1), sep = ", "))
x1 <- as.numeric(every$entry_grade[1]); x2 <- as.numeric(every$grade_12[1])
g12 <- as.numeric(every$grade_12[every$grade_12 != ""])
gs <- calc(g12)
put("ch3.z.student", every$student_id[1]); put("ch3.z.entry", every$entry_grade[1]); put("ch3.z.college", every$grade_12[1])
put("ch3.z.entry.z", fx((x1 - e$mean) / e$sx, 2)); put("ch3.z.entry.z_sigma", fx((x1 - e$mean) / e$sg, 2))
put("ch3.z.entry.pctile", pc(sum(eg <= x1), length(eg)))
put("ch3.z.g12.n", big(length(g12))); put("ch3.z.g12.mean", fx(gs$mean, 3)); put("ch3.z.g12.sx", fx(gs$sx, 3))
put("ch3.z.college.z", fx((x2 - gs$mean) / gs$sx, 2)); put("ch3.z.college.z_sigma", fx((x2 - gs$mean) / gs$sg, 2))
put("ch3.z.college.pctile", pc(sum(g12 <= x2), length(g12)))
put("ch3.z.try.2_50", fx((2.50 - e$mean) / e$sx, 2))
s4 <- calc(L4)
put("ch3.L4.zero", sum(L4 == 0)); put("ch3.L4.zero.pct", pc(sum(L4 == 0), length(L4))); put("ch3.L4.five", five(s4))
put("ch3.L4.mean", fx(s4$mean, 3)); put("ch3.L4.sx", fx(s4$sx, 3)); put("ch3.gap", fx(s$mean - s4$mean, 3))
i4 <- s4$q3 - s4$q1
put("ch3.L4.fences", paste(gx(s4$q1 - 1.5 * i4), gx(s4$q3 + 1.5 * i4), sep = ", "))
put("ch3.L4.outliers", sum(L4 > s4$q3 + 1.5 * i4))
two4 <- s4$mean + 2 * s4$sx
put("ch3.L4.two_sd", fx(two4, 2)); put("ch3.L4.two_sd.count", sum(L4 > two4))
# D5c: 2.193 + 2 x 2.731 is 7.655, a halfway value, so the Try It works it from four places
put("ch3.L4.mean4", fx(s4$mean, 4)); put("ch3.L4.sx4", fx(s4$sx, 4))
if (fx(as.numeric(vals[["ch3.L4.mean4"]]) + 2 * as.numeric(vals[["ch3.L4.sx4"]]), 2) != vals[["ch3.L4.two_sd"]])
  stop("ch3.L4.mean4 + 2 x ch3.L4.sx4 does not give ch3.L4.two_sd")
put("ch3.L2.eight_plus", sum(L2 >= 8)); put("ch3.L4.eight_plus", sum(L4 >= 8))
for (z in c("1", "0")) {
  lab <- if (z == "1") "offered" else "not_offered"
  k <- known[known$offer == z, ]
  ratio <- 100 * tapply(k$withdrew == "1", k$college, sum) / as.numeric(table(k$college))
  if (any(abs(ratio - floor(ratio) - 0.5) < 1e-9)) stop("a tie at .5 in the stemplot percents")
  pcts <- sort(round(ratio))
  put(paste0("ch3.b2b.", lab), paste(pcts, collapse = ", ")); put(paste0("ch3.b2b.", lab, ".median"), gx(med(pcts)))
}
mins <- c(5, 8, 12, 15, 15, 20, 25, 60)
m <- calc(mins)
put("ch3.review.minutes.mean", fx(m$mean, 1)); put("ch3.review.minutes.med", gx(m$med)); put("ch3.review.minutes.sx", fx(m$sx, 2))
put("ch3.review.minutes.quartiles", paste(gx(m$q1), gx(m$q3), sep = ", "))
put("ch3.review.minutes.upper_fence", fx(m$q3 + 1.5 * (m$q3 - m$q1), 2))
w60 <- calc(mins[-length(mins)])
put("ch3.review.minutes.without60.mean", fx(w60$mean, 2)); put("ch3.review.minutes.without60.sx", fx(w60$sx, 2))
put("ch3.review.minutes.without60.med", gx(w60$med))
put("ch3.review.five.fences", paste(gx(10 - 1.5 * (18 - 10)), gx(18 + 1.5 * (18 - 10)), sep = ", "))
put("ch3.review.scale.mean", fx(38.6 * 2, 1)); put("ch3.review.scale.sd", fx(5.2 * 2, 1))
put("ch3.review.z.first", fx((82 - 74) / 6, 2)); put("ch3.review.z.second", fx((88 - 81) / 4, 2))

# ---- Chapter 4 ----
for (z in c("1", "0")) {
  lab <- if (z == "1") "withdrew" else "stayed_or_transferred"
  put(paste0("ch4.visits.", lab, ".mean"), fx(mean(as.numeric(known$visits[known$withdrew == z])), 2))
}
for (z in c("1", "0")) {
  lab <- if (z == "1") "part_time" else "full_time"
  # D5c: among the known, as the withdrawal shares beside them are (2.63, not 2.62 on all 1,219)
  put(paste0("ch4.visits.", lab, ".mean"), fx(mean(as.numeric(known$visits[known$part_time == z])), 2))
  k <- known[known$part_time == z, ]
  ww <- sum(k$withdrew == "1")
  put(paste0("ch4.", lab, ".withdrew"), ww); put(paste0("ch4.", lab, ".known"), nrow(k))
  put(paste0("ch4.", lab, ".withdrew.pct"), pc(ww, nrow(k)))
}
put("ch4.consent_withdrawn", sum(every$exit == "consent withdrawn"))
pt <- sum(every$part_time == "1")
put("ch4.part_time", pt); put("ch4.full_time", N - pt)
for (spec in list(list(30, "srs30", 1), list(40, "try40", 1), list(60, "review60", 2))) {
  n <- spec[[1]]; key <- spec[[2]]; share <- n * pt / N
  put(paste0("ch4.", key, ".part_time_exact"), fx(share, spec[[3]]))
  put(paste0("ch4.", key, ".split"), paste(round(share), "and", n - round(share)))
}
put("ch4.systematic.k", 40)
sizes <- sapply(1:40, function(st) length(seq(st, N, by = 40)))
put("ch4.systematic.sizes", paste(sort(unique(sizes)), collapse = " or "))
put("ch4.systematic.31_if_start_at_most", max(which(sizes == 31)))
put("ch4.review.systematic.size", 1200 %/% 25)
nj <- sum(invited$joined == "0")
put("ch4.not_joined", nj); put("ch4.not_joined.pct", pc(nj, nrow(invited)))
for (z in c("0", "1")) {
  lab <- if (z == "1") "part_time" else "full_time"
  inv <- invited[invited$part_time == z, ]
  j <- sum(inv$joined == "1")
  put(paste0("ch4.invited.", lab), nrow(inv)); put(paste0("ch4.invited.", lab, ".joined"), j)
  put(paste0("ch4.invited.", lab, ".joined.pct"), pc(j, nrow(inv)))
}
put("ch4.part_time.share_invited.pct", pc(sum(invited$part_time == "1"), nrow(invited), 0))
put("ch4.part_time.share_joined.pct", pc(pt, N))
shares <- 100 * tapply(every$offer == "1", every$college, mean)
put("ch4.blocks.offered.range", paste(fx(min(shares), 1), "to", fx(max(shares), 1)))
pp <- c()
for (z in c("1", "0")) {
  lab <- if (z == "1") "offered" else "not_offered"
  grp <- every[every$offer == z, ]
  put(paste0("ch4.balance.", lab, ".part_time"), sum(grp$part_time == "1"))
  put(paste0("ch4.balance.", lab, ".part_time.pct"), pc(sum(grp$part_time == "1"), nrow(grp)))
  pp <- c(pp, 100 * mean(grp$part_time == "1"))
}
put("ch4.balance.gap_points", fx(pp[1] - pp[2], 1))

# ---- the three fixed samples: checked, never redrawn ----
key_of <- function(d) apply(d[, names(every)], 1, paste, collapse = "\t")
pop_keys <- key_of(every)
for (n in c("100", "120", "20")) {
  path <- file.path(root, "samples", paste0("tonmick-sample-", n, ".csv"))
  sm <- read.csv(path, colClasses = "character", check.names = FALSE)
  put(paste0("samples.", n, ".size"), nrow(sm))
  put(paste0("samples.", n, ".distinct"), length(unique(sm$student_id)))
  ok <- all(key_of(sm) %in% pop_keys) && identical(sm$draw, as.character(seq_len(nrow(sm))))
  ok <- ok && if (n == "20") all(sm$grade_12 != "") else all(sm$withdrew %in% c("0", "1"))
  put(paste0("samples.", n, ".rows_match_population"), if (ok) "yes" else "no")
  put(paste0("samples.", n, ".md5"), unname(tools::md5sum(path)))
  put(paste0("samples.", n, ".withdrew"), sum(sm$withdrew == "1"))
  put(paste0("samples.", n, ".part_time"), sum(sm$part_time == "1"))
  put(paste0("samples.", n, ".offered"), sum(sm$offer == "1"))
  put(paste0("samples.", n, ".entry.mean"), fx(mean(as.numeric(sm$entry_grade)), 3))
  if (n == "20") put("samples.20.g12.mean", fx(mean(as.numeric(sm$grade_12)), 3))
}
put("samples.population.known", big(nrow(known)))
put("samples.population.withdrew.share", fx(mean(known$withdrew == "1"), 4))
gpop <- every[every$grade_12 != "", ]
put("samples.population.college_grade", big(nrow(gpop)))
put("samples.population.college_grade.entry.mean", fx(mean(as.numeric(gpop$entry_grade)), 3))
put("samples.population.college_grade.g12.mean", fx(mean(as.numeric(gpop$grade_12)), 3))

dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
nm <- sort(names(vals), method = "radix")
quoted <- vapply(nm, function(k) {
  x <- vals[[k]]
  if (grepl("[,\"]", x)) paste0("\"", gsub("\"", "\"\"", x), "\"") else x
}, "")
writeLines(c("name,value", paste0(nm, ",", quoted)), out)
cat(sprintf("r route: %d values in %s\n", length(nm), out))
