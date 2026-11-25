# Route 2 for Chapters 9 to 12: every number the chapters, their Try It answers, their reviews,
# and the eight investigations print, rebuilt from the data files and the fixed samples of 20,
# 100, and 120 with base R (no add-on packages).
#
#   Rscript --vanilla r/chapters_9_12.R ROOT OUT.csv
#
# It shares no code with python/chapters_9_12.py. Values are written as the book prints them
# (name,value), with the ASCII hyphen-minus for negative numbers. As in route 1, arithmetic the
# text shows on the home screen starts from the printed, rounded numbers; lists a reader types
# in are used as printed; and quartiles are the TI-84's (the medians of the lower and upper
# halves). The distributions come from base R: pchisq, qchisq, pt, qt, pnorm, qnorm, dhyper.

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
  zero <- if (places > 0) paste0("-0.", strrep("0", places)) else "-0"
  ifelse(s == zero, substring(s, 2), s)
}
pc <- function(num, den, places = 1) fx(100 * num / den, places)
big <- function(n) formatC(as.integer(round(n)), big.mark = ",", format = "d")
rnd <- function(x, places) as.numeric(fx(x, places))
cj <- function(x) paste(x, collapse = ", ")
trim <- function(s) {
  s <- sub("0+$", "", s)
  s <- sub("\\.$", "", s)
  ifelse(s == "-0", "0", s)
}
g <- function(x) trim(sprintf("%.3f", x))
g4 <- function(x) trim(sprintf("%.4f", x))
readc <- function(path) read.csv(file.path(root, path), colClasses = "character", check.names = FALSE)

# The five-number summary as 1-Var Stats gives it: Q1 and Q3 are the medians of the lower and
# upper halves, the median left out when the count is odd.
five <- function(x) {
  s <- sort(x)
  n <- length(s)
  lower <- s[seq_len(n %/% 2)]
  upper <- s[((n + 1) %/% 2 + 1):n]
  c(s[1], median(lower), median(s), median(upper), s[n])
}
# Expected counts, each cell's part, the statistic, and the degrees of freedom of a two-way table.
chi_tab <- function(obs) {
  e <- outer(rowSums(obs), colSums(obs)) / sum(obs)
  parts <- (obs - e)^2 / e
  list(e = e, parts = parts, stat = sum(parts), df = (nrow(obs) - 1) * (ncol(obs) - 1))
}
upper_chi <- function(x, df) pchisq(x, df, lower.tail = FALSE)
two_t <- function(t, df) 2 * pt(abs(t), df, lower.tail = FALSE)
tstar <- function(tail, df) qt(tail, df, lower.tail = FALSE)
lsq <- function(x, y) {
  mx <- mean(x); my <- mean(y)
  sxx <- sum((x - mx)^2); sxy <- sum((x - mx) * (y - my)); syy <- sum((y - my)^2)
  b <- sxy / sxx
  a <- my - b * mx
  res <- y - (a + b * x)
  s <- sqrt(sum(res^2) / (length(x) - 2))
  list(a = a, b = b, r = sxy / sqrt(sxx * syy), res = res, s = s, se_b = s / sqrt(sxx))
}
welch <- function(m1, s1, n1, m2, s2, n2) {
  v1 <- s1^2 / n1; v2 <- s2^2 / n2
  list(t = (m1 - m2) / sqrt(v1 + v2), df = (v1 + v2)^2 / (v1^2 / (n1 - 1) + v2^2 / (n2 - 1)), se = sqrt(v1 + v2))
}
zpool <- function(x1, n1, x2, n2) {
  pp <- (x1 + x2) / (n1 + n2)
  (x1 / n1 - x2 / n2) / sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
}
rows2 <- function(m, places) paste(apply(m, 1, function(r) cj(fx(r, places))), collapse = "; ")

every <- readc("data/tonmick-classroom.csv")
invited <- readc("data/tonmick-invited.csv")
s20 <- readc("samples/tonmick-sample-20.csv")
s100 <- readc("samples/tonmick-sample-100.csv")
s120 <- readc("samples/tonmick-sample-120.csv")
known <- every[every$withdrew %in% c("0", "1"), ]
off <- every[every$offer == "1", ]
notoff <- every[every$offer == "0", ]

# ---- Chapter 9 ----
# 9.1 goodness of fit: joiners per college, against equal shares
jn <- invited[invited$joined == "1", ]
cols <- sort(unique(jn$college), method = "radix")
obs <- vapply(cols, function(c) sum(jn$college == c), 0)
put("ch9.gof.colleges", cj(cols)); put("ch9.gof.counts", cj(obs))
put("ch9.gof.k", length(cols)); put("ch9.gof.df", length(cols) - 1)
e <- sum(obs) / length(cols)
put("ch9.gof.expected", fx(e, 2)); put("ch9.gof.expected.screen", fx(e, 4))
ep <- rnd(e, 2)
put("ch9.gof.low.part", fx((min(obs) - ep)^2 / ep, 2)); put("ch9.gof.high.part", fx((max(obs) - ep)^2 / ep, 2))
st <- sum((obs - e)^2 / e)
p <- upper_chi(st, length(cols) - 1)
put("ch9.gof.chi2", fx(st, 2)); put("ch9.gof.chi2.screen", fx(st, 4))
put("ch9.gof.p", fx(p, 4)); put("ch9.gof.p.pct", fx(100 * p, 1))
put("ch9.gof.crit", fx(qchisq(0.05, length(cols) - 1, lower.tail = FALSE), 3))
# Try it: part-time joiners against the invited mix
ptj <- sum(every$part_time == "1")
share <- sum(invited$part_time == "1") / nrow(invited)
e1 <- nrow(every) * share; e2 <- nrow(every) * (1 - share)
st <- (ptj - e1)^2 / e1 + (nrow(every) - ptj - e2)^2 / e2
put("ch9.gof.try.expected.part", fx(e1, 1)); put("ch9.gof.try.expected.full", fx(e2, 1))
put("ch9.gof.try.chi2", fx(st, 2)); put("ch9.gof.try.p", fx(upper_chi(st, 1), 4))
# 9.2 homogeneity: how the year ended, by offer, among the known outcomes
ends <- c("stayed", "withdrew", "transferred")
koff <- known[known$offer == "1", ]; knot <- known[known$offer == "0", ]
tab <- rbind(vapply(ends, function(x) sum(koff$exit == x), 0), vapply(ends, function(x) sum(knot$exit == x), 0))
h <- chi_tab(tab)
labs <- c("offered", "not_offered")
for (i in 1:2) {
  put(paste0("ch9.hom.", labs[i], ".counts"), cj(tab[i, ]))
  put(paste0("ch9.hom.", labs[i], ".pct"), cj(pc(tab[i, ], sum(tab[i, ]))))
  put(paste0("ch9.hom.", labs[i], ".expected"), cj(fx(h$e[i, ], 2)))
  put(paste0("ch9.hom.", labs[i], ".parts"), cj(fx(h$parts[i, ], 2)))
}
put("ch9.hom.totals", cj(colSums(tab))); put("ch9.hom.totals.pct", cj(pc(colSums(tab), nrow(known))))
put("ch9.hom.expected.min", fx(min(h$e), 2))
put("ch9.hom.chi2", fx(h$stat, 2)); put("ch9.hom.chi2.screen", fx(h$stat, 4)); put("ch9.hom.df", h$df)
p <- upper_chi(h$stat, h$df)
put("ch9.hom.p", fx(p, 4))
put("ch9.hom.crit", fx(qchisq(0.05, h$df, lower.tail = FALSE), 3))
two <- cbind(tab[, 2], tab[, 1] + tab[, 3])
h2 <- chi_tab(two)
put("ch9.hom.two.chi2", fx(h2$stat, 2))
put("ch9.hom.two.z", fx(zpool(two[1, 1], sum(two[1, ]), two[2, 1], sum(two[2, ])), 4))
put("ch9.hom.two.p", fx(upper_chi(h2$stat, 1), 4))
# 9.3 independence: the sample of 120, part-time study by withdrawal
cnt2 <- function(d, va, a, vb, b) sum(d[[va]] == a & d[[vb]] == b)
cells <- rbind(c(cnt2(s120, "part_time", "0", "withdrew", "1"), cnt2(s120, "part_time", "0", "withdrew", "0")),
               c(cnt2(s120, "part_time", "1", "withdrew", "1"), cnt2(s120, "part_time", "1", "withdrew", "0")))
h3 <- chi_tab(cells)
labs <- c("full", "part")
for (i in 1:2) {
  put(paste0("ch9.ind.", labs[i], ".counts"), cj(cells[i, ])); put(paste0("ch9.ind.", labs[i], ".n"), sum(cells[i, ]))
  put(paste0("ch9.ind.", labs[i], ".withdrew.pct"), pc(cells[i, 1], sum(cells[i, ])))
  put(paste0("ch9.ind.", labs[i], ".expected"), cj(fx(h3$e[i, ], 2)))
}
put("ch9.ind.withdrew", sum(cells[, 1])); put("ch9.ind.stayed", sum(cells[, 2]))
put("ch9.ind.expected.min", fx(min(h3$e), 2))
put("ch9.ind.chi2", fx(h3$stat, 2)); put("ch9.ind.chi2.screen", fx(h3$stat, 4)); put("ch9.ind.df", h3$df)
p <- upper_chi(h3$stat, h3$df)
put("ch9.ind.p", fx(p, 4))
for (i in 1:2) {
  z <- as.character(i - 1)
  put(paste0("ch9.ind.pop.", labs[i], ".withdrew.pct"),
      pc(cnt2(known, "part_time", z, "withdrew", "1"), sum(known$part_time == z)))
}
bal <- rbind(c(cnt2(every, "offer", "1", "part_time", "1"), cnt2(every, "offer", "1", "part_time", "0")),
             c(cnt2(every, "offer", "0", "part_time", "1"), cnt2(every, "offer", "0", "part_time", "0")))
hb <- chi_tab(bal)
put("ch9.ind.balance.chi2", fx(hb$stat, 2)); put("ch9.ind.balance.p", fx(upper_chi(hb$stat, 1), 4))
jt <- rbind(c(cnt2(invited, "part_time", "0", "joined", "1"), cnt2(invited, "part_time", "0", "joined", "0")),
            c(cnt2(invited, "part_time", "1", "joined", "1"), cnt2(invited, "part_time", "1", "joined", "0")))
hj <- chi_tab(jt)
put("ch9.ind.join.counts", paste(apply(jt, 1, cj), collapse = "; "))
put("ch9.ind.join.expected", rows2(hj$e, 1))
put("ch9.ind.join.expected.min", fx(min(hj$e), 1))
put("ch9.ind.join.chi2", fx(hj$stat, 2))
pj <- upper_chi(hj$stat, 1)
ex <- floor(log10(pj)); mant <- pj / 10^ex
if (sprintf("%.2f", mant) == "10.00") { mant <- mant / 10; ex <- ex + 1 }
put("ch9.ind.join.p.mantissa", sprintf("%.2f", mant)); put("ch9.ind.join.p.exponent", sprintf("%d", as.integer(ex)))
zj <- zpool(jt[1, 1], sum(jt[1, ]), jt[2, 1], sum(jt[2, ]))
put("ch9.ind.join.z", fx(zj, 4)); put("ch9.ind.join.z2", fx(rnd(zj, 4)^2, 2))
# Chapter 9 review
spin <- c(25, 18, 22, 15)
es <- sum(spin) / 4
ss <- sum((spin - es)^2 / es)
put("ch9.review.spin.expected", fx(es, 0)); put("ch9.review.spin.chi2", fx(ss, 2)); put("ch9.review.spin.p", fx(upper_chi(ss, 3), 4))
put("ch9.review.spin.wrong_n", fx(sum((spin - es)^2 / sum(spin)), 3))
c100 <- rbind(c(cnt2(s100, "offer", "1", "withdrew", "1"), cnt2(s100, "offer", "1", "withdrew", "0")),
              c(cnt2(s100, "offer", "0", "withdrew", "1"), cnt2(s100, "offer", "0", "withdrew", "0")))
h4 <- chi_tab(c100)
put("ch9.review.s100.offered", cj(c100[1, ])); put("ch9.review.s100.not_offered", cj(c100[2, ]))
put("ch9.review.s100.offered.n", sum(c100[1, ])); put("ch9.review.s100.not_offered.n", sum(c100[2, ]))
put("ch9.review.s100.expected", rows2(h4$e, 2)); put("ch9.review.s100.expected.min", fx(min(h4$e), 2))
put("ch9.review.s100.chi2", fx(h4$stat, 2)); put("ch9.review.s100.p", fx(upper_chi(h4$stat, 1), 4))
jobs <- rbind(c(54, 39, 63), 150 - c(54, 39, 63))
h5 <- chi_tab(jobs)
put("ch9.review.jobs.expected", rows2(h5$e, 2))
put("ch9.review.jobs.chi2", fx(h5$stat, 2)); put("ch9.review.jobs.df", h5$df); put("ch9.review.jobs.p", fx(upper_chi(h5$stat, h5$df), 4))
put("ch9.review.jobs.pct", cj(pc(jobs[1, ], 150)))

# ---- Chapter 10 ----
ts19 <- tstar(0.025, 19)
put("ch10.tstar.19", fx(ts19, 3)); put("ch10.tstar.608", fx(tstar(0.025, 608), 3))
put("ch10.tstar.9", fx(tstar(0.025, 9), 3)); put("ch10.tstar.19.screen", fx(ts19, 4))
sch <- as.numeric(s20$entry_grade); col <- as.numeric(s20$grade_12)
n <- length(sch)
put("ch10.s20.school", cj(s20$entry_grade)); put("ch10.s20.college", cj(s20$grade_12))
m <- mean(sch); s <- sd(sch); se <- s / sqrt(n)
put("ch10.s20.school.mean", fx(m, 3)); put("ch10.s20.school.sx", fx(s, 3)); put("ch10.s20.school.sx.screen", fx(s, 5))
put("ch10.s20.school.se", fx(se, 4)); put("ch10.s20.school.se5", fx(se, 5))
me <- ts19 * se
put("ch10.s20.school.me", fx(me, 3))
put("ch10.s20.school.se.hand", fx(rnd(s, 5) / sqrt(n), 4))
put("ch10.s20.school.me.hand", fx(rnd(ts19, 3) * rnd(se, 4), 3))
put("ch10.s20.school.low", fx(m - me, 3)); put("ch10.s20.school.high", fx(m + me, 3))
put("ch10.s20.school.low.screen", fx(m - me, 4)); put("ch10.s20.school.high.screen", fx(m + me, 4))
pop <- every[every$grade_12 != "", ]
put("ch10.pop.ten_pct", fx(nrow(pop) / 10, 1))
fv <- five(sch); iqr <- fv[4] - fv[2]
put("ch10.s20.school.five", cj(g(fv)))
put("ch10.s20.school.fences", cj(g4(c(fv[2] - 1.5 * iqr, fv[4] + 1.5 * iqr))))
put("ch10.s20.school.outliers", sum(sch < fv[2] - 1.5 * iqr | sch > fv[4] + 1.5 * iqr))
vis <- as.numeric(s20$visits)
put("ch10.s20.visits", cj(s20$visits))
fv <- five(vis); iqr <- fv[4] - fv[2]
put("ch10.s20.visits.five", cj(g(fv)))
put("ch10.s20.visits.fence", g4(fv[4] + 1.5 * iqr))
put("ch10.s20.visits.outliers", sum(vis > fv[4] + 1.5 * iqr))
# 10.3 a test for a mean, against a planner's figure of 2.90
mu0 <- 2.90
tt <- (m - mu0) / se
put("ch10.test.mu0", "2.90"); put("ch10.test.t", fx(tt, 2)); put("ch10.test.t.screen", fx(tt, 4))
put("ch10.test.p", fx(two_t(tt, 19), 4)); put("ch10.test.p.one", fx(pt(tt, 19, lower.tail = FALSE), 4))
put("ch10.test.diff", fx(rnd(m, 3) - mu0, 3))
put("ch10.test.t.hand", fx((rnd(m, 3) - mu0) / rnd(se, 4), 2))
# 10.4 paired data: college grade minus school grade, in hundredths so the differences are exact
d <- (round(100 * col) - round(100 * sch)) / 100
put("ch10.pair.d", cj(fx(d, 2)))
md <- mean(d); sdd <- sd(d); sed <- sdd / sqrt(n)
put("ch10.pair.mean", fx(md, 3)); put("ch10.pair.sd", fx(sdd, 3)); put("ch10.pair.se", fx(sed, 4))
tp <- md / sed
put("ch10.pair.t", fx(tp, 2)); put("ch10.pair.p", fx(two_t(tp, 19), 4))
put("ch10.pair.me", fx(ts19 * sed, 3))
put("ch10.pair.sd4", fx(sdd, 4)); put("ch10.pair.se.hand", fx(rnd(sdd, 4) / sqrt(n), 4))
put("ch10.pair.t.hand", fx(rnd(md, 3) / rnd(sed, 4), 2))
put("ch10.pair.me.hand", fx(rnd(ts19, 3) * rnd(sed, 4), 3))
put("ch10.pair.low", fx(md - ts19 * sed, 3)); put("ch10.pair.high", fx(md + ts19 * sed, 3))
fv <- five(d); iqr <- fv[4] - fv[2]
put("ch10.pair.five", cj(g(fv)))
put("ch10.pair.fences", cj(g4(c(fv[2] - 1.5 * iqr, fv[4] + 1.5 * iqr))))
put("ch10.pair.outliers", sum(d < fv[2] - 1.5 * iqr | d > fv[4] + 1.5 * iqr))
put("ch10.pair.positive", sum(d > 0))
w <- welch(mean(col), sd(col), n, m, s, n)
put("ch10.pair.wrong.se", fx(w$se, 4)); put("ch10.pair.wrong.t", fx(w$t, 2)); put("ch10.pair.wrong.p", fx(two_t(w$t, w$df), 4))
no <- pop[pop$offer == "0", ]
dn <- (round(100 * as.numeric(no$grade_12)) - round(100 * as.numeric(no$entry_grade))) / 100
put("ch10.pair.not_offered.n", nrow(no)); put("ch10.pair.not_offered.mean", fx(mean(dn), 3)); put("ch10.pair.not_offered.sd", fx(sd(dn), 3))
da <- (round(100 * as.numeric(pop$grade_12)) - round(100 * as.numeric(pop$entry_grade))) / 100
put("ch10.pair.all.mean", fx(mean(da), 3))
# 10.5 comparing two means: visits, offered minus not offered
v1 <- as.numeric(off$visits); v2 <- as.numeric(notoff$visits)
w <- welch(mean(v1), sd(v1), length(v1), mean(v2), sd(v2), length(v2))
diff <- mean(v1) - mean(v2)
ts <- tstar(0.025, w$df)
put("ch10.two.diff4", fx(diff, 4)); put("ch10.two.tstar", fx(ts, 3)); put("ch10.two.me", fx(ts * w$se, 3))
put("ch10.two.low", fx(diff - ts * w$se, 3)); put("ch10.two.high", fx(diff + ts * w$se, 3))
small <- min(length(v1), length(v2)) - 1
put("ch10.two.df.small", small); put("ch10.two.df.sum", big(length(v1) + length(v2) - 2))
ts608 <- tstar(0.025, small)
put("ch10.two.hand.me", fx(rnd(ts608, 3) * rnd(w$se, 4), 3))
put("ch10.two.hand.low", fx(diff - ts608 * w$se, 3)); put("ch10.two.hand.high", fx(diff + ts608 * w$se, 3))
put("ch10.two.hand.p", fx(two_t(w$t, small), 4))
sp <- sqrt(((length(v1) - 1) * sd(v1)^2 + (length(v2) - 1) * sd(v2)^2) / (length(v1) + length(v2) - 2))
tpool <- diff / (sp * sqrt(1 / length(v1) + 1 / length(v2)))
put("ch10.two.pooled.t", fx(tpool, 2)); put("ch10.two.pooled.p", fx(two_t(tpool, length(v1) + length(v2) - 2), 4))
put("ch10.two.per100", fx(100 * diff, 0)); put("ch10.two.per100.low", fx(100 * (diff - ts * w$se), 1))
put("ch10.two.per100.high", fx(100 * (diff + ts * w$se), 1))
put("ch10.two.offered.summary", cj(c(fx(mean(v1), 6), fx(sd(v1), 6))))
put("ch10.two.not_offered.summary", cj(c(fx(mean(v2), 6), fx(sd(v2), 6))))
for (lab in c("offered", "not_offered")) {
  v <- if (lab == "offered") v1 else v2
  sdp <- rnd(sd(v), 3); mp <- rnd(mean(v), 2)
  put(paste0("ch10.two.", lab, ".var"), fx(sdp^2, 2)); put(paste0("ch10.two.", lab, ".mean2"), fx(mp, 2))
  put(paste0("ch10.two.", lab, ".ratio"), fx(rnd(sdp^2, 2) / mp, 1))
}
# Chapter 10 review
put("ch10.review.tstar.11", fx(tstar(0.025, 11), 3)); put("ch10.review.tstar.12", fx(tstar(0.025, 12), 3))
put("ch10.review.tstar90.11", fx(tstar(0.05, 11), 3))
ts15 <- tstar(0.025, 15); se16 <- 6.4 / sqrt(16)
put("ch10.review.ci.se", fx(se16, 1)); put("ch10.review.ci.tstar", fx(ts15, 3))
put("ch10.review.ci.me", fx(rnd(ts15, 3) * se16, 2))
put("ch10.review.ci", cj(fx(c(52.3 - ts15 * se16, 52.3 + ts15 * se16), 2)))
z95 <- qnorm(0.975)
put("ch10.review.ci.z", cj(fx(c(52.3 - z95 * se16, 52.3 + z95 * se16), 2)))
t16 <- tstar(0.025, 16)
put("ch10.review.ci.df16", cj(fx(c(52.3 - t16 * se16, 52.3 + t16 * se16), 2)))
put("ch10.review.ci.sd", cj(fx(c(52.3 - ts15 * 6.4, 52.3 + ts15 * 6.4), 2)))
mc <- mean(col); sc <- sd(col); sec <- sc / sqrt(n)
put("ch10.review.college.mean", fx(mc, 3)); put("ch10.review.college.sx", fx(sc, 3)); put("ch10.review.college.se", fx(sec, 4))
put("ch10.review.college.me", fx(ts19 * sec, 3))
put("ch10.review.college.se.hand", fx(rnd(sc, 3) / sqrt(n), 4))
put("ch10.review.college.me.hand", fx(rnd(ts19, 3) * rnd(sec, 4), 3))
put("ch10.review.college.low", fx(mc - ts19 * sec, 3)); put("ch10.review.college.high", fx(mc + ts19 * sec, 3))
fv <- five(col); iqr <- fv[4] - fv[2]
put("ch10.review.college.five", cj(g(fv)))
put("ch10.review.college.fences", cj(g4(c(fv[2] - 1.5 * iqr, fv[4] + 1.5 * iqr))))
put("ch10.review.college.outliers", sum(col < fv[2] - 1.5 * iqr | col > fv[4] + 1.5 * iqr))
put("ch10.review.college.true", fx(mean(as.numeric(pop$grade_12)), 3))
w <- welch(78.4, 8.2, 35, 74.1, 9.5, 32)
put("ch10.review.methods.diff", fx(78.4 - 74.1, 1)); put("ch10.review.methods.se", fx(w$se, 4))
put("ch10.review.methods.t.hand", fx(4.3 / rnd(w$se, 4), 2))
put("ch10.review.methods.t", fx(w$t, 2)); put("ch10.review.methods.df", fx(w$df, 2)); put("ch10.review.methods.p", fx(two_t(w$t, w$df), 4))
tsq <- tstar(0.025, w$df)
put("ch10.review.methods.low", fx(4.3 - tsq * w$se, 2)); put("ch10.review.methods.high", fx(4.3 + tsq * w$se, 2))

# ---- Chapter 11 ----
no <- every[every$offer == "0" & every$grade_12 != "", ]
x <- as.numeric(no$entry_grade); y <- as.numeric(no$grade_12)
L <- lsq(x, y)
a <- L$a; b <- L$b; r <- L$r
put("ch11.n", length(x)); put("ch11.a", fx(a, 3)); put("ch11.b", fx(b, 3)); put("ch11.r", fx(r, 3)); put("ch11.r2", fx(r^2, 3))
put("ch11.r4", fx(r, 4)); put("ch11.r2.pct", fx(100 * r^2, 0)); put("ch11.unexplained.pct", fx(100 - 100 * r^2, 0))
put("ch11.sx", fx(sd(x), 4)); put("ch11.sy", fx(sd(y), 4)); put("ch11.xbar", fx(mean(x), 3)); put("ch11.ybar", fx(mean(y), 3))
put("ch11.slope.hand", fx(rnd(r, 4) * rnd(sd(y), 4) / rnd(sd(x), 4), 3))
ar <- rnd(a, 3); br <- rnd(b, 3)
put("ch11.through", fx(ar + br * rnd(mean(x), 3), 3))
put("ch11.ceiling.school", sum(x == 4)); put("ch11.ceiling.college", sum(y == 4))
put("ch11.range", cj(g(c(min(x), max(x)))))
put("ch11.try.hand", fx(ar + br * 3.0, 3)); put("ch11.try.y1", fx(a + b * 3.0, 3))
xf <- as.numeric(no$entry_grade[1]); yf <- as.numeric(no$grade_12[1])
put("ch11.student", no$student_id[1]); put("ch11.student.x", no$entry_grade[1]); put("ch11.student.y", no$grade_12[1])
put("ch11.student.pred", fx(a + b * xf, 3)); put("ch11.student.pred.hand", fx(ar + br * xf, 3))
put("ch11.student.res", fx(yf - (a + b * xf), 3))
put("ch11.s", fx(L$s, 3))
put("ch11.try.res.sds", fx(-0.9 / rnd(L$s, 3), 2))
put("ch11.try.res.below", sum(L$res <= -0.9)); put("ch11.res.min", fx(min(L$res), 3)); put("ch11.res.max", fx(max(L$res), 3))
put("ch11.pred.1", fx(a + b * 1.0, 3)); put("ch11.pred.1.hand", fx(ar + br * 1.0, 3))
og <- every[every$offer == "1" & every$grade_12 != "", ]
Lo <- lsq(as.numeric(og$entry_grade), as.numeric(og$grade_12))
put("ch11.offered.n", nrow(og)); put("ch11.offered.a", fx(Lo$a, 3)); put("ch11.offered.b", fx(Lo$b, 3)); put("ch11.offered.r", fx(Lo$r, 3))
nog <- every[every$offer == "0" & every$grade_12 == "", ]
put("ch11.nograde", nrow(nog))
for (e in c("withdrew", "transferred", "consent withdrawn")) {
  k <- strsplit(e, " ")[[1]][1]
  put(paste0("ch11.nograde.", k), sum(nog$exit == e))
  put(paste0("ch11.left.", k), sum(no$exit == e))
}
for (lab in c("high", "low")) {
  keep <- if (lab == "high") x >= 3.5 else x < 2.5
  put(paste0("ch11.rtm.", lab, ".n"), sum(keep))
  put(paste0("ch11.rtm.", lab, ".school"), fx(mean(x[keep]), 3)); put(paste0("ch11.rtm.", lab, ".college"), fx(mean(y[keep]), 3))
}
# 11.5 departures from linearity: withdrawal share by school grade, in bands
gh <- round(100 * as.numeric(known$entry_grade))
cuts <- c(225, 250, 275, 300, 325, 350)
band <- vapply(gh, function(v) sum(v >= cuts), 0)
bn <- integer(0); bw <- integer(0); gm <- character(0); sh <- character(0)
for (k in 0:length(cuts)) {
  sel <- known[band == k, ]
  wk <- sum(sel$withdrew == "1")
  bn <- c(bn, nrow(sel)); bw <- c(bw, wk)
  gm <- c(gm, fx(mean(as.numeric(sel$entry_grade)), 3)); sh <- c(sh, fx(wk / nrow(sel), 3))
}
put("ch11.bands.n", cj(bn)); put("ch11.bands.withdrew", cj(bw)); put("ch11.bands.k", length(bn))
put("ch11.bands.grade", cj(gm)); put("ch11.bands.share", cj(sh))
put("ch11.bands.pct", cj(fx(100 * as.numeric(sh), 1)))
gx <- as.numeric(gm); sy <- as.numeric(sh)
L1 <- lsq(gx, sy)
put("ch11.bands.lin.a", fx(L1$a, 3)); put("ch11.bands.lin.b", fx(L1$b, 3)); put("ch11.bands.lin.r", fx(L1$r, 3))
put("ch11.bands.lin.r2", fx(L1$r^2, 3)); put("ch11.bands.lin.res", cj(fx(L1$res, 3)))
put("ch11.bands.lin.signs", cj(ifelse(L1$res > 0, "+", "-")))
ly <- log(sy)
put("ch11.bands.ln", cj(fx(ly, 3)))
L2 <- lsq(gx, ly)
put("ch11.bands.log.a", fx(L2$a, 3)); put("ch11.bands.log.b", fx(L2$b, 3)); put("ch11.bands.log.r", fx(L2$r, 3))
put("ch11.bands.log.r2", fx(L2$r^2, 3)); put("ch11.bands.log.res", cj(fx(L2$res, 3)))
put("ch11.bands.log.at3", fx(exp(L2$a + L2$b * 3.0), 3)); put("ch11.bands.log.ratio", fx(exp(L2$b * 0.5), 2))
# 11.6 inference for a slope
df <- length(x) - 2
ts <- tstar(0.025, df)
put("ch11.b4", fx(b, 4)); put("ch11.se_b5", fx(L$se_b, 5))
put("ch11.t.hand", fx(rnd(b, 4) / rnd(L$se_b, 5), 2))
put("ch11.slope1.hand", fx((rnd(b, 4) - 1) / rnd(L$se_b, 5), 2))
put("ch11.df", df); put("ch11.se_b", fx(L$se_b, 4)); put("ch11.t", fx(b / L$se_b, 2)); put("ch11.tstar", fx(ts, 3))
put("ch11.slope.low", fx(b - ts * L$se_b, 3)); put("ch11.slope.high", fx(b + ts * L$se_b, 3))
put("ch11.slope.me", fx(rnd(ts, 3) * rnd(L$se_b, 4), 4))
put("ch11.slope.p.below", if (two_t(b / L$se_b, df) < 0.0001) "0.0001" else "no")
t1 <- (b - 1) / L$se_b
put("ch11.slope1.t", fx(t1, 2)); put("ch11.slope1.p.below", if (two_t(t1, df) < 0.0001) "0.0001" else fx(two_t(t1, df), 4))
# Chapter 11 review
put("ch11.review.pred", fx(12.5 + 3.2 * 4, 1)); put("ch11.review.res", fx(27 - (12.5 + 3.2 * 4), 1))
put("ch11.review.slope", fx(0.8 * 10 / 4, 1)); put("ch11.review.intercept", fx(30 - 2.0 * 6, 1))
L3 <- lsq(as.numeric(notoff$entry_grade), as.numeric(notoff$visits))
put("ch11.review.visits.n", nrow(notoff)); put("ch11.review.visits.a", fx(L3$a, 3)); put("ch11.review.visits.b", fx(L3$b, 3))
put("ch11.review.visits.r", fx(L3$r, 3)); put("ch11.review.visits.r2", fx(L3$r^2, 3)); put("ch11.review.visits.r2.pct", fx(100 * L3$r^2, 1))
put("ch11.review.visits.at2", fx(L3$a + L3$b * 2.0, 2)); put("ch11.review.visits.at4", fx(L3$a + L3$b * 4.0, 2))
put("ch11.review.visits.at2.hand", fx(rnd(L3$a, 3) + rnd(L3$b, 3) * 2.0, 2))
put("ch11.review.visits.at4.hand", fx(rnd(L3$a, 3) + rnd(L3$b, 3) * 4.0, 2))
tq <- 1.84 / 0.52; ts23 <- tstar(0.025, 23)
put("ch11.review.slope.t", fx(tq, 2)); put("ch11.review.slope.p", fx(two_t(tq, 23), 4)); put("ch11.review.slope.tstar", fx(ts23, 3))
put("ch11.review.slope.me", fx(rnd(ts23, 3) * 0.52, 3))
put("ch11.review.slope.low", fx(1.84 - rnd(ts23, 3) * 0.52, 3)); put("ch11.review.slope.high", fx(1.84 + rnd(ts23, 3) * 0.52, 3))

# ---- Chapter 12: what the investigations print that earlier chapters do not ----
cl <- unique(every$college)
offc <- vapply(cl, function(c) sum(every$college == c & every$offer == "1"), 0)
allc <- vapply(cl, function(c) sum(every$college == c), 0)
put("ch12.inv1.offered.range", paste(min(offc), "to", max(offc)))
put("ch12.inv1.share.range", paste(fx(min(100 * offc / allc), 1), "to", fx(max(100 * offc / allc), 1)))
for (lab in c("offered", "not_offered")) {
  xg <- as.numeric((if (lab == "offered") off else notoff)$entry_grade)
  fv <- five(xg); iqr <- fv[4] - fv[2]
  put(paste0("ch12.inv1.", lab, ".five"), cj(g(fv)))
  put(paste0("ch12.inv1.", lab, ".mean"), fx(mean(xg), 3)); put(paste0("ch12.inv1.", lab, ".sx"), fx(sd(xg), 3))
  put(paste0("ch12.inv1.", lab, ".iqr"), g(iqr))
  put(paste0("ch12.inv1.", lab, ".low_fence"), g4(fv[2] - 1.5 * iqr))
  put(paste0("ch12.inv1.", lab, ".below_fence"), sum(xg < fv[2] - 1.5 * iqr))
}
put("ch12.inv1.mean_gap", fx(mean(as.numeric(off$entry_grade)) - mean(as.numeric(notoff$entry_grade)), 3))
# Investigation 3: SHUFFLE's exact chance, both sides, and a shuffle within each college
popk <- nrow(known); goodk <- sum(known$withdrew == "1"); nk <- sum(known$offer == "1")
obsk <- sum(known$offer == "1" & known$withdrew == "1")
ks <- 0:goodk
pmf <- dhyper(ks, nk, popk - nk, goodk)
gapk <- function(k) 100 * (k / nk - (goodk - k) / (popk - nk))
cut <- min(ks[gapk(ks) >= abs(gapk(obsk))])
lo <- sum(pmf[ks <= obsk]); hi <- sum(pmf[ks >= cut])
put("ch12.inv3.of100.sd", fx(sqrt(100 * (lo + hi) * (1 - lo - hi)), 1))
cdf <- cumsum(pmf)
put("ch12.inv3.middle95", paste(min(ks[cdf >= 0.025]), "to", min(ks[cdf >= 0.975])))
dist <- 1
for (cc in sort(unique(known$college), method = "radix")) {
  kc <- known[known$college == cc, ]
  wc <- sum(kc$withdrew == "1"); oc <- sum(kc$offer == "1")
  pc_ <- dhyper(0:wc, oc, nrow(kc) - oc, wc)
  new <- numeric(length(dist) + length(pc_) - 1)
  for (i in seq_along(dist)) new[i:(i + length(pc_) - 1)] <- new[i:(i + length(pc_) - 1)] + dist[i] * pc_
  dist <- new
}
kk <- seq_along(dist) - 1
put("ch12.inv3.within", fx(sum(dist[kk <= obsk]) + sum(dist[kk >= cut]), 4))
# Investigation 4: the 11 unknown outcomes counted two ways, and the standard errors by hand
x1 <- sum(koff$withdrew == "1"); n1 <- nrow(koff); x2 <- sum(knot$withdrew == "1"); n2 <- nrow(knot)
seu <- sqrt(x1 / n1 * (1 - x1 / n1) / n1 + x2 / n2 * (1 - x2 / n2) / n2)
pp <- (x1 + x2) / (n1 + n2)
sep <- sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
put("ch12.inv4.se", fx(seu, 5)); put("ch12.inv4.se.pooled", fx(sep, 5)); put("ch12.inv4.me", fx(1.96 * rnd(seu, 5), 4))
u1 <- sum(off$withdrew == ""); u2 <- sum(notoff$withdrew == "")
for (lab in c("stayed", "withdrew")) {
  y1 <- x1 + if (lab == "withdrew") u1 else 0
  y2 <- x2 + if (lab == "withdrew") u2 else 0
  m1 <- nrow(off); m2 <- nrow(notoff)
  p1 <- y1 / m1; p2 <- y2 / m2
  se_ <- sqrt(p1 * (1 - p1) / m1 + p2 * (1 - p2) / m2)
  put(paste0("ch12.inv4.", lab, ".counts"), paste(y1, "of", m1, "against", y2, "of", m2))
  put(paste0("ch12.inv4.", lab, ".diff"), fx(p1 - p2, 4))
  put(paste0("ch12.inv4.", lab, ".ci"), cj(fx(c(p1 - p2 - z95 * se_, p1 - p2 + z95 * se_), 4)))
}
# Investigation 7: by hand with Welch's degrees of freedom
w <- welch(mean(v1), sd(v1), length(v1), mean(v2), sd(v2), length(v2))
ts <- tstar(0.025, w$df)
put("ch12.inv7.tstar", fx(ts, 3)); put("ch12.inv7.me", fx(rnd(ts, 3) * rnd(w$se, 4), 3))
put("ch12.inv7.diff", fx(mean(v1) - mean(v2), 4))

# Each figure the text works by hand, from printed numbers, must give what the calculator shows.
same <- list(c("ch10.s20.school.se.hand", "ch10.s20.school.se"), c("ch10.s20.school.me.hand", "ch10.s20.school.me"),
             c("ch10.test.t.hand", "ch10.test.t"), c("ch10.pair.se.hand", "ch10.pair.se"), c("ch10.pair.t.hand", "ch10.pair.t"),
             c("ch10.pair.me.hand", "ch10.pair.me"), c("ch10.review.college.se.hand", "ch10.review.college.se"),
             c("ch10.review.college.me.hand", "ch10.review.college.me"), c("ch10.review.methods.t.hand", "ch10.review.methods.t"),
             c("ch10.two.hand.me", "ch10.two.me"), c("ch11.t.hand", "ch11.t"), c("ch11.slope1.hand", "ch11.slope1.t"),
             c("ch11.slope.hand", "ch11.b"), c("ch11.through", "ch11.ybar"), c("ch11.pred.1.hand", "ch11.pred.1"),
             c("ch11.review.visits.at2.hand", "ch11.review.visits.at2"), c("ch11.review.visits.at4.hand", "ch11.review.visits.at4"),
             c("ch9.hom.two.p", "ch9.hom.two.p"), c("ch9.ind.join.z2", "ch9.ind.join.chi2"), c("ch12.inv7.me", "ch10.two.me"))
for (pr in same) {
  if (vals[[pr[1]]] != vals[[pr[2]]]) stop(paste(pr[1], "is", vals[[pr[1]]], "but", pr[2], "is", vals[[pr[2]]]))
}

dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
nm <- sort(names(vals), method = "radix")
quoted <- vapply(nm, function(k) {
  x <- vals[[k]]
  if (grepl("[,\"]", x)) paste0("\"", gsub("\"", "\"\"", x), "\"") else x
}, "")
writeLines(c("name,value", paste0(nm, ",", quoted)), out)
cat(sprintf("r route: %d values in %s\n", length(nm), out))
