# Route 2 for Chapters 5 to 8: every number the chapters, their Try It answers, and their
# reviews print, rebuilt from the data files and the fixed sample of 100 with base R (no add-on
# packages).
#
#   Rscript --vanilla r/chapters_5_8.R ROOT OUT.csv
#
# It shares no code with python/chapters_5_8.py. Values are written as the book prints them
# (name,value), with the ASCII hyphen-minus for negative numbers. As in route 1, arithmetic the
# text shows on the home screen starts from the printed, rounded numbers, and normal-model
# values use the printed parameters. Exact values come from base R's distribution functions
# (phyper, dhyper, pbinom, pnorm, qnorm); simulate() then checks three of them against R's own
# random numbers, within a stated tolerance, and writes nothing to OUT.csv.

args <- commandArgs(trailingOnly = TRUE)
root <- args[1]
out <- args[2]
vals <- list()
put <- function(name, value) {
  if (!is.null(vals[[name]])) stop(paste("duplicate name", name))
  vals[[name]] <<- as.character(value)
}
fx <- function(x, places) sprintf(paste0("%.", places, "f"), x)
pc <- function(num, den, places = 1) sprintf(paste0("%.", places, "f"), 100 * num / den)
big <- function(n) formatC(as.integer(round(n)), big.mark = ",", format = "d")
rnd <- function(x, places) as.numeric(fx(x, places))
readc <- function(path) read.csv(file.path(root, path), colClasses = "character", check.names = FALSE)
psd <- function(x) sqrt(mean((x - mean(x))^2))
z95 <- qnorm(0.975)
twoprop <- function(x1, n1, x2, n2) {
  pp <- (x1 + x2) / (n1 + n2)
  z <- (x1 / n1 - x2 / n2) / sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
  list(z = z, p = 2 * pnorm(-abs(z)), pooled = pp)
}

every <- readc("data/tonmick-classroom.csv")
s100 <- readc("samples/tonmick-sample-100.csv")
N <- nrow(every)
off <- every[every$offer == "1", ]
notoff <- every[every$offer == "0", ]
known <- every[every$withdrew %in% c("0", "1"), ]
koff <- known[known$offer == "1", ]
knot <- known[known$offer == "0", ]
popk <- nrow(known)
goodk <- sum(known$withdrew == "1")

# ---- Chapter 5 ----
exits <- c("stayed", "withdrew", "transferred", "consent withdrawn")
for (lab in c("offered", "not_offered")) {
  grp <- if (lab == "offered") off else notoff
  cnt <- vapply(exits, function(e) sum(grp$exit == e), 0)
  for (i in seq_along(exits)) put(paste0("ch5.table.", lab, ".", strsplit(exits[i], " ")[[1]][1]), cnt[i])
  put(paste0("ch5.table.", lab, ".total"), nrow(grp))
  put(paste0("ch5.seg.", lab), paste(pc(cnt, nrow(grp)), collapse = ", "))
}
woff <- sum(off$exit == "withdrew")
wall <- sum(every$exit == "withdrew")
tall <- sum(every$exit == "transferred")
tnot <- sum(notoff$exit == "transferred")
put("ch5.joint.offered_withdrew", fx(woff / N, 4))
put("ch5.marginal.withdrew", fx(wall / N, 4))
put("ch5.cond.offered.withdrew.pct", pc(woff, nrow(koff)))
put("ch5.cond.not_offered.withdrew.pct", pc(sum(knot$withdrew == "1"), nrow(knot)))
put("ch5.try1.offered.transferred.pct", pc(sum(off$exit == "transferred"), nrow(off)))
put("ch5.try1.not_offered.transferred.pct", pc(tnot, nrow(notoff)))
put("ch5.lln.ten.none", fx(dbinom(0, 10, 0.13), 4)); put("ch5.lln.ten.expected", fx(10 * 0.13, 1))
put("ch5.lln.twenty.expected", fx(20 * 0.13, 1))
# SHUFFLE: K, the withdrawals dealt to the offered, is hypergeometric
nk <- nrow(koff)
put("ch5.shuffle.n", big(popk)); put("ch5.shuffle.withdrawals", goodk); put("ch5.shuffle.offered", nk)
put("ch5.shuffle.expected", fx(nk * goodk / popk, 1))
gapk <- function(k) 100 * (k / nk - (goodk - k) / (popk - nk))
put("ch5.shuffle.observed", woff); put("ch5.shuffle.gap", fx(gapk(woff), 1))
ks <- 0:nk
cut <- min(ks[gapk(ks) >= abs(gapk(woff))])
put("ch5.shuffle.cut_high", cut); put("ch5.shuffle.gap_cut_high", fx(gapk(cut), 1))
put("ch5.shuffle.gap_below_cut", fx(gapk(cut - 1), 1))
lo <- phyper(woff, goodk, popk - goodk, nk)
hi <- phyper(cut - 1, goodk, popk - goodk, nk, lower.tail = FALSE)
put("ch5.shuffle.low", fx(lo, 4)); put("ch5.shuffle.high", fx(hi, 4)); put("ch5.shuffle.p", fx(lo + hi, 4))
put("ch5.shuffle.of100", fx(100 * (lo + hi), 0))
pt <- sum(every$part_time == "1")
put("ch5.p.offered", fx(nrow(off) / N, 4)); put("ch5.p.part_time", fx(pt / N, 4))
put("ch5.p.full_time", fx((N - pt) / N, 4)); put("ch5.p.not_withdrew_known", fx(1 - goodk / popk, 4))
put("ch5.count.withdrew_or_transferred", wall + tall); put("ch5.p.withdrew_or_transferred", fx((wall + tall) / N, 4))
put("ch5.p.withdrew_given_offered", fx(woff / nrow(koff), 4))
put("ch5.p.offered_given_withdrew", fx(woff / wall, 4))
put("ch5.p.not_offered_given_transferred", fx(tnot / tall, 4))
kpt <- known[known$part_time == "1", ]
kft <- known[known$part_time == "0", ]
wpt <- sum(kpt$withdrew == "1"); wft <- sum(kft$withdrew == "1")
put("ch5.tree.part_time", fx(nrow(kpt) / popk, 4)); put("ch5.tree.withdrew_given_part_time", fx(wpt / nrow(kpt), 4))
put("ch5.tree.product", fx(rnd(nrow(kpt) / popk, 4) * rnd(wpt / nrow(kpt), 4), 4))
put("ch5.tree.full_time", fx(nrow(kft) / popk, 4)); put("ch5.tree.withdrew_given_full_time", fx(wft / nrow(kft), 4))
put("ch5.tree.full_time_product", fx(rnd(nrow(kft) / popk, 4) * rnd(wft / nrow(kft), 4), 4))
put("ch5.tree.total", fx(goodk / popk, 4))
ptoff <- sum(off$part_time == "1"); ptnot <- sum(notoff$part_time == "1")
put("ch5.p.part_time_given_offered", fx(ptoff / nrow(off), 4))
put("ch5.p.part_time_given_not_offered", fx(ptnot / nrow(notoff), 4))
uni <- pt + nrow(off) - ptoff
put("ch5.union.count", uni); put("ch5.union.p", fx(uni / N, 4))
# review
put("ch5.review.union", fx(0.40 + 0.30 - 0.12, 2)); put("ch5.review.product", fx(0.40 * 0.30, 2))
put("ch5.review.atleast1", fx(pbinom(0, 10, 0.13, lower.tail = FALSE), 4))
put("ch5.review.pt.withdrew", wpt); put("ch5.review.pt.stayed", nrow(kpt) - wpt); put("ch5.review.pt.total", nrow(kpt))
put("ch5.review.ft.withdrew", wft); put("ch5.review.ft.stayed", nrow(kft) - wft); put("ch5.review.ft.total", nrow(kft))
put("ch5.review.total.stayed", big(popk - goodk)); put("ch5.review.p_pt_given_withdrew", fx(wpt / goodk, 4))
put("ch5.review.freethrow", fx(pbinom(3, 5, 0.7, lower.tail = FALSE), 4))

# ---- Chapter 6 ----
v <- as.numeric(every$visits)
cnt <- c(tabulate(v + 1, nbins = 8), sum(v >= 8))
put("ch6.dist.counts", paste(cnt, collapse = ", "))
put("ch6.dist.probs", paste(fx(cnt / N, 4), collapse = ", "))
put("ch6.dist.cum", paste(fx(cumsum(cnt) / N, 4), collapse = ", "))
put("ch6.p0", fx(cnt[1] / N, 4)); put("ch6.p1", fx(cnt[2] / N, 4)); put("ch6.p8plus", fx(cnt[9] / N, 4))
put("ch6.count8plus", cnt[9]); put("ch6.cum2", fx(sum(cnt[1:3]) / N, 4))
tv <- table(v)
put("ch6.freq.values", paste(names(tv), collapse = ", "))
put("ch6.freq.counts", paste(as.integer(tv), collapse = ", "))
mu <- mean(v); sg <- psd(v)
put("ch6.sum", sum(v)); put("ch6.mu", fx(mu, 3)); put("ch6.sigma", fx(sg, 3)); put("ch6.sx", fx(sd(v), 3))
m <- rnd(mu, 3); s <- rnd(sg, 3)
put("ch6.two.mean", fx(2 * m, 3)); put("ch6.two.sd", fx(sqrt(2) * s, 3))
put("ch6.three.mean", fx(3 * m, 3)); put("ch6.three.sd", fx(sqrt(3) * s, 3))
v2 <- as.numeric(off$visits); v4 <- as.numeric(notoff$visits)
put("ch6.sigma.not_offered", fx(psd(v4), 3))
put("ch6.diff.mean", fx(rnd(mean(v2), 3) - rnd(mean(v4), 3), 3))
put("ch6.diff.sd", fx(sqrt(rnd(psd(v2), 3)^2 + rnd(psd(v4), 3)^2), 3))
put("ch6.binom.comb", choose(10, 2)); put("ch6.binom.pdf2", fx(dbinom(2, 10, 0.13), 4))
put("ch6.binom.cdf2", fx(pbinom(2, 10, 0.13), 4)); put("ch6.binom.ge3", fx(pbinom(2, 10, 0.13, lower.tail = FALSE), 4))
put("ch6.binom.mean", fx(10 * 0.13, 1)); put("ch6.binom.sd", fx(sqrt(10 * 0.13 * 0.87), 3))
# R's geometric counts the failures before the first success
put("ch6.geom.p3", fx(dgeom(2, 0.13), 4)); put("ch6.geom.cdf5", fx(pgeom(4, 0.13), 4))
put("ch6.geom.mean", fx(1 / 0.13, 2)); put("ch6.geom.after10", fx(pgeom(9, 0.13, lower.tail = FALSE), 4))
eg <- as.numeric(every$entry_grade)
mn <- 3.010; sdv <- 0.469
for (k in 1:3) {
  put(paste0("ch6.normal.within", k), pc(sum(eg >= mn - k * sdv & eg <= mn + k * sdv), N))
  put(paste0("ch6.normal.rule", k), fx(100 * (pnorm(k) - pnorm(-k)), 1))
}
put("ch6.normal.model_above_3_5", fx(100 * pnorm(3.5, mn, sdv, lower.tail = FALSE), 1))
put("ch6.normal.data_above_3_5", pc(sum(eg > 3.5), N))
put("ch6.normal.z_3_5", fx((3.5 - mn) / sdv, 2))
put("ch6.normal.model_below_2_5", fx(pnorm(2.5, mn, sdv), 4)); put("ch6.normal.model_below_2_5.pct", fx(100 * pnorm(2.5, mn, sdv), 1))
put("ch6.normal.data_below_2_5", pc(sum(eg < 2.5), N))
put("ch6.cut.p90", fx(qnorm(0.9, mn, sdv), 3)); put("ch6.cut.z90", fx(qnorm(0.9), 3))
put("ch6.cut10.low", fx(qnorm(0.05, mn, sdv), 3)); put("ch6.cut10.high", fx(qnorm(0.95, mn, sdv), 3))
put("ch6.cut10.z", fx(qnorm(0.95), 3))
put("ch6.cut10.table.low", fx(mn - 1.645 * sdv, 3)); put("ch6.cut10.table.high", fx(mn + 1.645 * sdv, 3))
put("ch6.cut.top25", fx(qnorm(0.75, mn, sdv), 3))
# review
xs <- c(0, 1, 2, 3); ps <- c(0.1, 0.3, 0.4, 0.2)
rm <- sum(xs * ps)
put("ch6.review.dist.mean", fx(rm, 1)); put("ch6.review.dist.sd", fx(sqrt(sum(ps * (xs - rm)^2)), 1))
put("ch6.review.sum.mean", fx(20 + 15, 0)); put("ch6.review.sum.sd", fx(sqrt(3^2 + 4^2), 0))
put("ch6.review.height.z", fx((68 - 64) / 2.5, 1)); put("ch6.review.height.p", fx(pnorm(68, 64, 2.5, lower.tail = FALSE), 4))
put("ch6.review.height.below", fx(pnorm(68, 64, 2.5), 4))
put("ch6.review.binom20.p3", fx(dbinom(3, 20, 0.13), 4)); put("ch6.review.binom20.le2", fx(pbinom(2, 20, 0.13), 4))
put("ch6.review.binom20.mean", fx(20 * 0.13, 1)); put("ch6.review.binom20.sd", fx(sqrt(20 * 0.13 * 0.87), 3))
g12 <- as.numeric(every$grade_12[every$grade_12 != ""])
put("ch6.review.g12.n", big(length(g12)))
put("ch6.review.g12.model_above_3_5", fx(100 * pnorm(3.5, 2.996, 0.561, lower.tail = FALSE), 1))
put("ch6.review.g12.data_above_3_5", pc(sum(g12 > 3.5), length(g12)))
put("ch6.review.g12.top10", fx(qnorm(0.9, 2.996, 0.561), 3))
put("ch6.review.g12.model_above_4", fx(100 * pnorm(4.0, 2.996, 0.561, lower.tail = FALSE), 1))
put("ch6.review.g12.at_4", sum(g12 == 4.0)); put("ch6.review.g12.at_4.pct", pc(sum(g12 == 4.0), length(g12)))

# ---- Chapter 7 ----
p <- rnd(goodk / popk, 4)
put("ch7.p", fx(p, 4)); put("ch7.ten_pct", fx(popk / 10, 1))
sd100 <- rnd(sqrt(p * (1 - p) / 100), 4)
put("ch7.sd100", fx(sd100, 4)); put("ch7.np100", fx(100 * p, 1)); put("ch7.nq100", fx(100 * (1 - p), 1))
ph <- sum(s100$withdrew == "1") / nrow(s100)
put("ch7.sample100.phat", fx(ph, 2)); put("ch7.sample100.z", fx((ph - p) / sd100, 2))
put("ch7.sd25", fx(sqrt(p * (1 - p) / 25), 4)); put("ch7.np25", fx(25 * p, 1))
m2 <- mean((v - mu)^2); m3 <- mean((v - mu)^3)
skew <- m3 / m2^1.5
s <- rnd(sqrt(m2), 3)
put("ch7.sd30", fx(s / sqrt(30), 3)); put("ch7.sd120", fx(s / sqrt(120), 3))
put("ch7.skew.pop", fx(skew, 2)); put("ch7.skew.mean30", fx(skew / sqrt(30), 2))
# D5c: the calculator's simulation draws from L2 (609 visits), since a list holds at most 999
# values; its sigma-x, 3.102 as printed in Section 3.3, over the square root of 30
s2 <- rnd(psd(v2), 3)
put("ch7.L2.sd30", fx(s2 / sqrt(30), 3))
if (fx(psd(v2) / sqrt(30), 3) != vals[["ch7.L2.sd30"]]) stop("ch7.L2.sd30 differs when worked from the unrounded sigma-x")
put("ch7.ten_pct.joiners", fx(N / 10, 1))
gap <- rnd(sum(koff$withdrew == "1") / nrow(koff) - sum(knot$withdrew == "1") / nrow(knot), 4)
sdg <- rnd(sqrt(p * (1 - p) * (1 / nrow(koff) + 1 / nrow(knot))), 4)
put("ch7.gap", fx(gap, 4)); put("ch7.gap.sd", fx(sdg, 4)); put("ch7.gap.z", fx(gap / sdg, 2))
put("ch7.gap.try", fx(0.04 / sdg, 2))
se <- rnd(sqrt(3.105^2 / nrow(off) + 2.731^2 / nrow(notoff)), 4)
put("ch7.means.se", fx(se, 4)); put("ch7.means.z", fx(0.314 / se, 2))
put("ch7.means.se4", fx(sqrt(3.105^2 / (4 * nrow(off)) + 2.731^2 / (4 * nrow(notoff))), 4))
# review
put("ch7.review.sd_phat", fx(sqrt(0.30 * 0.70 / 50), 4)); put("ch7.review.sd_xbar", fx(12 / sqrt(36), 0))
put("ch7.review.np", fx(0.04 * 150, 0)); put("ch7.review.nq", fx(0.96 * 150, 0))
z20 <- (0.20 - p) / sd100
put("ch7.review.z20", fx(z20, 2)); put("ch7.review.p20", fx(pnorm(rnd(z20, 2), lower.tail = FALSE), 4))
put("ch7.review.exact20", fx(phyper(19, goodk, popk - goodk, 100, lower.tail = FALSE), 4))
sd50 <- rnd(s / sqrt(50), 3)
z3 <- (3 - rnd(mu, 3)) / sd50
put("ch7.review.sd50", fx(sd50, 3)); put("ch7.review.z3", fx(z3, 2))
put("ch7.review.p3", fx(pnorm(rnd(z3, 2), lower.tail = FALSE), 4))

# ---- Chapter 8 ----
n <- nrow(s100)
x <- sum(s100$withdrew == "1")
ph <- x / n
se <- sqrt(ph * (1 - ph) / n)
put("ch8.x", x); put("ch8.n", n); put("ch8.failures", n - x); put("ch8.phat", fx(ph, 2))
put("ch8.se", fx(se, 4)); put("ch8.zstar", fx(z95, 3)); put("ch8.me", fx(z95 * se, 4))
put("ch8.ci.low", fx(ph - z95 * se, 4)); put("ch8.ci.high", fx(ph + z95 * se, 4))
z90 <- qnorm(0.95)
put("ch8.zstar90", fx(z90, 3)); put("ch8.ci90.low", fx(ph - z90 * se, 4)); put("ch8.ci90.high", fx(ph + z90 * se, 4))
truth <- goodk / popk
put("ch8.true", fx(truth, 4))
kk <- 0:n
phk <- kk / n
mek <- z95 * sqrt(phk * (1 - phk) / n)
hit <- (phk - mek <= truth) & (truth <= phk + mek)
put("ch8.coverage", fx(100 * sum(dhyper(kk[hit], goodk, popk - goodk, n)), 1))
put("ch8.me400", fx(z95 * sqrt(ph * (1 - ph) / 400), 4))
put("ch8.n.guess", big(ceiling((z95 / 0.03)^2 * ph * (1 - ph))))
put("ch8.n.half", big(ceiling((z95 / 0.03)^2 * 0.25)))
put("ch8.n.try", big(ceiling((z95 / 0.02)^2 * 0.25)))
p0 <- 0.15
put("ch8.null", fx(p0, 2)); put("ch8.null.expected", fx(n * p0, 0)); put("ch8.null.expected_fail", fx(n * (1 - p0), 0))
zt <- (ph - p0) / sqrt(p0 * (1 - p0) / n)
put("ch8.test.z", fx(zt + 0, 2)); put("ch8.test.p", fx(pnorm(zt), 4)); put("ch8.test.p2", fx(2 * pnorm(-abs(zt)), 4))
cutg <- p0 - qnorm(0.95) * sqrt(p0 * (1 - p0) / n)
pw <- pnorm((cutg - truth) / sqrt(truth * (1 - truth) / n))
put("ch8.power.goal.cut", fx(cutg, 4)); put("ch8.power.goal", fx(pw, 4)); put("ch8.power.goal.pct", fx(100 * pw, 1))
put("ch8.power.goal.type2.pct", fx(100 * (1 - pw), 1))
x1 <- sum(koff$withdrew == "1"); n1 <- nrow(koff)
x2 <- sum(knot$withdrew == "1"); n2 <- nrow(knot)
p1 <- x1 / n1; p2 <- x2 / n2
d <- abs(p1 - p2); pp <- (x1 + x2) / (n1 + n2)
se0 <- sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2)); se1 <- sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
pw2 <- pnorm((d - z95 * se0) / se1) + pnorm((-d - z95 * se0) / se1)
put("ch8.power.two", fx(pw2, 4)); put("ch8.power.two.pct", fx(100 * pw2, 1))
put("ch8.power.p1", fx(p1, 4)); put("ch8.power.p2", fx(p2, 4))
put("ch8.power.n80", big(ceiling((z95 + qnorm(0.8))^2 * (p1 * (1 - p1) + p2 * (1 - p2)) / d^2)))
put("ch8.two.diff", fx(p1 - p2, 4)); put("ch8.two.se", fx(se1, 4))
put("ch8.two.ci.low", fx(p1 - p2 - z95 * se1, 4)); put("ch8.two.ci.high", fx(p1 - p2 + z95 * se1, 4))
tp <- twoprop(x1, n1, x2, n2)
put("ch8.pooled", fx(tp$pooled, 4)); put("ch8.two.z", fx(tp$z, 2)); put("ch8.two.p", fx(tp$p, 4))
put("ch8.pooled.expected.offered", fx(n1 * tp$pooled, 1)); put("ch8.pooled.expected.not_offered", fx(n2 * tp$pooled, 1))
u1 <- sum(off$withdrew == ""); u2 <- sum(notoff$withdrew == "")
put("ch8.unknown.offered", u1); put("ch8.unknown.not_offered", u2)
put("ch8.sens.stayed.p", fx(twoprop(x1, nrow(off), x2, nrow(notoff))$p, 4))
put("ch8.sens.withdrew.p", fx(twoprop(x1 + u1, nrow(off), x2 + u2, nrow(notoff))$p, 4))
put("ch8.sens.against.p", fx(twoprop(x1 + u1, nrow(off), x2, nrow(notoff))$p, 4))
put("ch8.sens.for.p", fx(twoprop(x1, nrow(off), x2 + u2, nrow(notoff))$p, 4))
# review
pr <- 312 / 600; mer <- z95 * sqrt(pr * (1 - pr) / 600)
put("ch8.review.poll.phat", fx(pr, 2)); put("ch8.review.poll.me", fx(mer, 4))
put("ch8.review.poll.low", fx(pr - mer, 4)); put("ch8.review.poll.high", fx(pr + mer, 4))
put("ch8.review.n", ceiling((z95 / 0.04)^2 * 0.25))
xpt <- sum(s100$part_time == "1")
ppt <- xpt / n; sept <- sqrt(ppt * (1 - ppt) / n)
put("ch8.review.pt.x", xpt); put("ch8.review.pt.fail", n - xpt); put("ch8.review.pt.phat", fx(ppt, 2))
put("ch8.review.pt.se", fx(sept, 4)); put("ch8.review.pt.me", fx(z95 * sept, 4))
put("ch8.review.pt.low", fx(ppt - z95 * sept, 4)); put("ch8.review.pt.high", fx(ppt + z95 * sept, 4))
put("ch8.review.pt.true", fx(sum(known$part_time == "1") / popk, 4))
rr <- twoprop(52, 200, 38, 200)
put("ch8.review.remind.phat1", fx(52 / 200, 2)); put("ch8.review.remind.phat2", fx(38 / 200, 2))
put("ch8.review.remind.pooled", fx(rr$pooled, 3))
put("ch8.review.remind.se", fx(sqrt(rr$pooled * (1 - rr$pooled) * (2 / 200)), 4))
put("ch8.review.remind.z", fx(rr$z, 2)); put("ch8.review.remind.p", fx(pnorm(rr$z, lower.tail = FALSE), 4))
put("ch8.review.remind.p_two", fx(rr$p, 4))

# ---- Simulations: each against its exact value, within a stated tolerance ----
simulate <- function() {
  set.seed(2027)
  res <- list()
  share <- mean(runif(10000) < 0.13)
  res[[1]] <- c("law of large numbers, share of 10,000", share, 0.13, 0.02)
  means <- replicate(4000, mean(sample(v, 30, replace = TRUE)))
  res[[2]] <- c("means of 30, their mean", mean(means), mu, 0.05)
  res[[3]] <- c("means of 30, their SD", psd(means), sg / sqrt(30), 0.03)
  kw <- known$withdrew == "1"
  hits <- replicate(4000, {
    k <- mean(sample(kw, 100))
    m <- z95 * sqrt(k * (1 - k) / 100)
    (k - m <= truth) & (truth <= k + m)
  })
  res[[4]] <- c("capture rate of 95% intervals, samples of 100", mean(hits), as.numeric(vals[["ch8.coverage"]]) / 100, 0.02)
  bad <- 0
  for (r in res) {
    got <- as.numeric(r[2]); want <- as.numeric(r[3]); tol <- as.numeric(r[4])
    cat(sprintf("simulation (r): %s %.4f, exact %.4f, tolerance %s\n", r[1], got, want, r[4]))
    if (abs(got - want) > tol) bad <- bad + 1
  }
  if (bad > 0) stop("a simulation is outside its tolerance")
}
simulate()

dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
nm <- sort(names(vals), method = "radix")
quoted <- vapply(nm, function(k) {
  x <- vals[[k]]
  if (grepl("[,\"]", x)) paste0("\"", gsub("\"", "\"\"", x), "\"") else x
}, "")
writeLines(c("name,value", paste0(nm, ",", quoted)), out)
cat(sprintf("r route: %d values in %s\n", length(nm), out))
