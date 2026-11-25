# Route 2 for the book's figures: every number a figure draws or prints, with base R (no add-on
# packages).
#
#   Rscript --vanilla r/figures.R ROOT OUT.csv
#
# It shares no code with python/figures.py. Names start fig.NN, where NN is the figure's number
# in figures/README.md; lists are separated by ", ". The figures themselves are drawn by
# figures/draw.py, which stops unless what it draws equals these values. Figures 13 and 14 read
# the files in simulations/; this route does not redraw them, it summarizes them.

args <- commandArgs(trailingOnly = TRUE)
root <- args[1]
out <- args[2]
vals <- list()
put <- function(name, value) {
  if (!is.null(vals[[name]])) stop(paste("duplicate name", name))
  vals[[name]] <<- as.character(value)
}
fx <- function(x, places) {
  s <- sprintf(paste0("%.", places, "f"), x)
  ifelse(substr(s, 1, 1) == "-" & as.numeric(s) == 0, substring(s, 2), s)
}
gx <- function(x) sprintf("%g", x)
cj <- function(x) paste(x, collapse = ", ")
readc <- function(path) read.csv(file.path(root, path), colClasses = "character", check.names = FALSE)
med <- function(v) {
  v <- sort(v); n <- length(v)
  if (n %% 2 == 1) v[(n + 1) / 2] else (v[n / 2] + v[n / 2 + 1]) / 2
}
five <- function(x) {
  v <- sort(x); n <- length(v); h <- n %/% 2
  lower <- v[seq_len(h)]
  upper <- if (n %% 2 == 1) v[(h + 2):n] else v[(h + 1):n]
  c(v[1], med(lower), med(v), med(upper), v[n])
}
bins <- function(x, start, width, count) {
  sapply(0:(count - 1), function(i) { lo <- start + i * width; sum(x >= lo & x < lo + width) })
}
fit <- function(x, y) {
  b <- sum((x - mean(x)) * (y - mean(y))) / sum((x - mean(x))^2)
  a <- mean(y) - b * mean(x)
  list(a = a, b = b, res = y - (a + b * x))
}

every <- readc("data/tonmick-classroom.csv")
known <- every[every$withdrew %in% c("0", "1"), ]
L2 <- as.numeric(every$visits[every$offer == "1"])
L4 <- as.numeric(every$visits[every$offer == "0"])

# Figure 1: how the first year ended
ends <- c("stayed", "withdrew", "transferred", "consent withdrawn")
put("fig.01.counts", cj(sapply(ends, function(e) sum(every$exit == e))))
put("fig.01.n", nrow(every))

# Figure 2: the same two bars from 0 and from 75
w_off <- sum(known$withdrew == "1" & known$offer == "1")
w_not <- sum(known$withdrew == "1" & known$offer == "0")
put("fig.02.counts", cj(c(w_off, w_not))); put("fig.02.base", 75)
put("fig.02.ratio", fx(w_not / w_off, 2)); put("fig.02.ratio_cut", fx((w_not - 75) / (w_off - 75), 1))

# Figure 3: histogram of the offered students' visits, bars 2 wide
put("fig.03.bars", cj(bins(L2, 0, 2, 13))); put("fig.03.n", length(L2)); put("fig.03.top", gx(max(L2)))

# Figure 4: dotplot of the 16 colleges' joiners
joined <- table(every$college)
put("fig.04.joined", cj(sort(as.integer(joined)))); put("fig.04.colleges", length(joined))

# Figure 5: parallel modified box plots of visits
for (lab in c("offered", "not")) {
  v <- if (lab == "offered") L2 else L4
  s <- five(v)
  iqr <- s[4] - s[2]
  lo <- s[2] - 1.5 * iqr; hi <- s[4] + 1.5 * iqr
  put(paste0("fig.05.", lab, ".five"), cj(gx(s))); put(paste0("fig.05.", lab, ".fences"), cj(gx(c(lo, hi))))
  put(paste0("fig.05.", lab, ".whisker"), gx(max(v[v <= hi])))
  put(paste0("fig.05.", lab, ".outliers"), sum(v < lo | v > hi))
}

# Figure 6: segmented bar chart and mosaic plot of how the year ended, by offer
sizes <- c()
for (lab in c("offered", "not")) {
  grp <- every[every$offer == (if (lab == "offered") "1" else "0"), ]
  sizes <- c(sizes, nrow(grp))
  put(paste0("fig.06.", lab, ".pct"), cj(sapply(ends, function(e) fx(100 * sum(grp$exit == e) / nrow(grp), 1))))
}
put("fig.06.sizes", cj(sizes))

# Figure 7: the exact randomization distribution of K, the withdrawals dealt to the offered group
w_all <- sum(known$withdrew == "1"); off_all <- sum(known$offer == "1"); n_known <- nrow(known)
krange <- 64:110
put("fig.07.k_range", cj(c(64, 110)))
put("fig.07.pmf", cj(fx(dhyper(krange, w_all, n_known - w_all, off_all), 4)))
put("fig.07.mean", fx(w_all * off_all / n_known, 1))
low <- phyper(80, w_all, n_known - w_all, off_all)
high <- phyper(93, w_all, n_known - w_all, off_all, lower.tail = FALSE)
put("fig.07.low", fx(low, 4)); put("fig.07.high", fx(high, 4)); put("fig.07.p", fx(low + high, 4))
put("fig.07.outside", fx(1 - sum(dhyper(krange, w_all, n_known - w_all, off_all)), 4))

# Figure 8: probability histogram of a joiner's visits
vis <- as.integer(every$visits)
cnt <- c(sapply(0:7, function(x) sum(vis == x)), sum(vis >= 8))
put("fig.08.probs", cj(fx(cnt / nrow(every), 4)))

# Figure 9: binomial, n = 10, p = 0.13
put("fig.09.probs", cj(fx(dbinom(0:10, 10, 0.13), 4)))

# Figure 10: school grades, a histogram with the normal model, and the normal probability plot
eg <- as.numeric(every$entry_grade)
put("fig.10.bars", cj(bins(eg, 1.5, 0.25, 11))); put("fig.10.n", length(eg))
put("fig.10.mean", fx(mean(eg), 3)); put("fig.10.sd", fx(sd(eg), 3))
zs <- qnorm(((seq_along(eg)) - 0.5) / length(eg))
put("fig.10.npp_r", fx(cor(sort(eg), zs), 4))

# Figure 11: the school-grade model, the share above 3.5 and the 90th percentile
put("fig.11.above", fx(pnorm(3.5, 3.010, 0.469, lower.tail = FALSE), 4))
put("fig.11.p90", fx(qnorm(0.9, 3.010, 0.469), 3))

# Figure 12: p-hat for samples of 100 when p = 0.1432, as randBin(100,0.1432)/100 simulates it
put("fig.12.k_range", cj(c(3, 30)))
put("fig.12.pmf", cj(fx(dbinom(3:30, 100, 0.1432), 4)))
put("fig.12.sd", fx(sqrt(0.1432 * 0.8568 / 100), 4))

# Figure 13: the population of visits beside 1,000 means of 30
put("fig.13.pop.counts", cj(sapply(0:max(vis), function(k) sum(vis == k))))
mu <- mean(vis); sigma <- sqrt(sum((vis - mu)^2) / length(vis))
put("fig.13.pop.mean", fx(mu, 3)); put("fig.13.pop.sd", fx(sigma, 3))
put("fig.13.model.sd", fx(sigma / sqrt(30), 3))
sims <- readc("simulations/tonmick-sim-means-30.csv")
if (!identical(sims$rep, as.character(1:1000))) stop("simulations/tonmick-sim-means-30.csv: rep should run 1 to 1000")
tot <- as.integer(sims$visits_total)
if (any(tot < 0 | tot > 30 * max(vis))) stop("simulations/tonmick-sim-means-30.csv: a total out of range")
means <- tot / 30
put("fig.13.reps", length(means)); put("fig.13.means.bars", cj(bins(means, 1.0, 0.25, 16)))
put("fig.13.means.mean", fx(mean(means), 3)); put("fig.13.means.sd", fx(sd(means), 3))
put("fig.13.means.range", cj(fx(range(means), 3)))
nn <- length(vis)
sd_srs <- sigma / sqrt(30) * sqrt((nn - 30) / (nn - 1))
kurt <- sum((vis - mu)^4) / nn / sigma^4
se_sd <- sd_srs * sqrt((2 + (kurt - 3) / 30) / (4 * length(means)))
if (abs(mean(means) - mu) > 4 * sd_srs / sqrt(length(means)) || abs(sd(means) - sd_srs) > 4 * se_sd) {
  stop("Figure 13: the 1,000 means do not agree with the model within four standard errors")
}
cat(sprintf("r figures: 1,000 means of 30, mean %.3f against %.3f, SD %.3f against %.3f (within four standard errors)\n",
            mean(means), mu, sd(means), sd_srs))

# Figure 14: fifty 95% intervals from samples of 100
sims <- readc("simulations/tonmick-sim-samples-100.csv")
if (!identical(sims$rep, as.character(1:50))) stop("simulations/tonmick-sim-samples-100.csv: rep should run 1 to 50")
cnt14 <- as.integer(sims$withdrew)
if (any(cnt14 < 0 | cnt14 > 100)) stop("simulations/tonmick-sim-samples-100.csv: a count out of range")
p_true <- w_all / n_known
ph <- cnt14 / 100
m14 <- qnorm(0.975) * sqrt(ph * (1 - ph) / 100)
hit <- ph - m14 <= p_true & p_true <= ph + m14
put("fig.14.counts", cj(cnt14)); put("fig.14.captured", sum(hit)); put("fig.14.missed", cj(which(!hit)))
put("fig.14.p", fx(p_true, 4)); put("fig.14.reps", length(cnt14))

# Figure 15: the goal test's p value (H0: p = 0.15, p-hat = 0.15, n = 100, Ha: p < 0.15)
z15 <- (0.15 - 0.15) / sqrt(0.15 * 0.85 / 100)
put("fig.15.z", fx(z15, 2)); put("fig.15.p", fx(pnorm(z15), 4))

# Figure 16: power of the goal test when p = 173/1,208
sd0 <- sqrt(0.15 * 0.85 / 100); sd1 <- sqrt(p_true * (1 - p_true) / 100)
cut <- 0.15 - qnorm(0.95) * sd0
put("fig.16.sd0", fx(sd0, 4)); put("fig.16.sd1", fx(sd1, 4)); put("fig.16.cut", fx(cut, 4))
put("fig.16.alpha", fx(pnorm((cut - 0.15) / sd0), 4)); put("fig.16.power", fx(pnorm((cut - p_true) / sd1), 4))

# Figure 17: chi-square curves; the 5% critical value for 2 degrees of freedom
put("fig.17.dfs", cj(c(2, 5, 10)))
put("fig.17.crit", fx(qchisq(0.05, 2, lower.tail = FALSE), 3))

# Figure 18: t curves for 2 and 19 degrees of freedom, and the standard normal
put("fig.18.dfs", cj(c(2, 19)))
put("fig.18.crit", cj(c(fx(qt(0.975, 2), 3), fx(qt(0.975, 19), 3), fx(qnorm(0.975), 3))))

# Figures 19 and 20: the 555 students not offered with a college grade
gr <- readc("data/tonmick-grades-not-offered.csv")
x <- as.numeric(gr$entry_grade); y <- as.numeric(gr$grade_12)
L <- fit(x, y)
put("fig.19.n", length(x)); put("fig.19.a", fx(L$a, 3)); put("fig.19.b", fx(L$b, 3)); put("fig.19.r", fx(cor(x, y), 3))
put("fig.20.res_range", cj(fx(range(L$res), 3)))

# Figure 21: withdrawal by school-grade band, the line's residuals and the log line's
cuts <- c(225, 250, 275, 300, 325, 350)
band <- sapply(round(100 * as.numeric(known$entry_grade)), function(h) sum(h >= cuts)) + 1
gm <- sapply(1:7, function(i) fx(mean(as.numeric(known$entry_grade[band == i])), 3))
sh <- sapply(1:7, function(i) fx(sum(known$withdrew[band == i] == "1") / sum(band == i), 3))
gnum <- as.numeric(gm); snum <- as.numeric(sh)
put("fig.21.grade", cj(gm)); put("fig.21.share", cj(sh))
put("fig.21.lin.res", cj(fx(fit(gnum, snum)$res, 3)))
put("fig.21.log.res", cj(fx(fit(gnum, log(snum))$res, 3)))

dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
nm <- sort(names(vals), method = "radix")
quoted <- vapply(nm, function(k) {
  x <- vals[[k]]
  if (grepl("[,\"]", x)) paste0("\"", gsub("\"", "\"\"", x), "\"") else x
}, "")
writeLines(c("name,value", paste0(nm, ",", quoted)), out)
cat(sprintf("r route: %d values in %s\n", length(nm), out))
