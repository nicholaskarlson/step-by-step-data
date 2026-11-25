# Route 2 for the book's practice test: every number its questions, answers, and graphs print,
# with base R (no add-on packages).
#
#   Rscript --vanilla r/practice.R ROOT OUT.csv
#
# It shares no code with python/practice.py. The plan is outline/practice-test.md. Names start
# pt.qNN (Part 1), pt.wN (Part 2), and pt.figNN (Figures 22 to 29, drawn by figures/draw.py);
# lists are separated by ", ". Every number a question states is in practice/givens.csv and is
# copied under its own name; everything else is computed from the files in practice/, wrong
# choices included, each from the mistake the plan names.

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
readp <- function(name) read.csv(file.path(root, "practice", name), colClasses = "character", check.names = FALSE)
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
fit <- function(x, y) {
  b <- sum((x - mean(x)) * (y - mean(y))) / sum((x - mean(x))^2)
  c(a = mean(y) - b * mean(x), b = b)
}
chi <- function(tab) {
  rt <- rowSums(tab); ct <- colSums(tab); n <- sum(tab)
  ex <- outer(rt, ct) / n
  stat <- sum((tab - ex)^2 / ex)
  df <- (nrow(tab) - 1) * (ncol(tab) - 1)
  list(rt = rt, ct = ct, n = n, ex = ex, stat = stat, df = df, p = pchisq(stat, df, lower.tail = FALSE))
}

giv <- readp("givens.csv")
for (i in seq_len(nrow(giv))) put(paste0("pt.", giv$item[i], ".", giv$name[i]), giv$value[i])
gs <- function(item, name) giv$value[giv$item == item & giv$name == name]
G <- function(item, name) as.numeric(gs(item, name))
z95 <- qnorm(0.975); z90 <- qnorm(0.95)

# Givens a question states as percents, printed that way too
pct <- rbind(c("q15", "p_delivery"), c("q15", "p_late_delivery"), c("q15", "p_late_pickup"), c("q19", "p"),
             c("q23", "p0"), c("q24", "p0"), c("w3", "alpha"), c("w4", "p"))
for (i in seq_len(nrow(pct))) put(paste0("pt.", pct[i, 1], ".", pct[i, 2], "_pct"), gx(100 * G(pct[i, 1], pct[i, 2])))

# Q2 (Figure 22): waits at a bus stop
w <- as.numeric(readp("practice-waits.csv")$minutes)
put("pt.q02.n", length(w)); put("pt.q02.mean", fx(mean(w), 2)); put("pt.q02.median", gx(median(w)))
put("pt.q02.sd", fx(sd(w), 2)); put("pt.q02.five", cj(gx(five(w))))
put("pt.fig22.n", length(w)); put("pt.fig22.top", gx(max(w)))
put("pt.fig22.bars", cj(sapply(0:8, function(i) sum(w >= 4 * i & w < 4 * i + 4))))

# Q3: Celsius to Fahrenheit
m <- G("q03", "mean_c"); s <- G("q03", "sd_c"); a <- G("q03", "factor"); b <- G("q03", "shift")
put("pt.q03.mean_f", fx(a * m + b, 1)); put("pt.q03.sd_f", fx(a * s, 1))
put("pt.q03.trap.sd_shifted", fx(a * s + b, 1)); put("pt.q03.trap.mean_unshifted", fx(a * m, 1))

# Q4 (Figure 23): battery life of two models
bat <- readp("practice-batteries.csv")
for (mod in c("A", "B")) {
  v <- as.numeric(bat$hours[bat$model == mod])
  s5 <- five(v); iqr <- s5[4] - s5[2]
  lo <- s5[2] - 1.5 * iqr; hi <- s5[4] + 1.5 * iqr
  outs <- sort(v[v < lo | v > hi]); inside <- v[v >= lo & v <= hi]
  p <- paste0("pt.q04.", mod, ".")
  put(paste0(p, "n"), length(v)); put(paste0(p, "iqr"), fx(iqr, 1)); put(paste0(p, "range"), fx(s5[5] - s5[1], 1))
  put(paste0(p, "fences"), cj(fx(c(lo, hi), 2))); put(paste0(p, "mean"), fx(mean(v), 2)); put(paste0(p, "sd"), fx(sd(v), 2))
  p <- paste0("pt.fig23.", mod, ".")
  put(paste0(p, "five"), cj(gx(s5))); put(paste0(p, "whiskers"), cj(gx(c(min(inside), max(inside)))))
  put(paste0(p, "out"), if (length(outs) > 0) cj(gx(outs)) else "none")
}

# Q5: z-scores
put("pt.q05.z_1", fx((G("q05", "score_1") - G("q05", "mean_1")) / G("q05", "sd_1"), 2))
put("pt.q05.z_2", fx((G("q05", "score_2") - G("q05", "mean_2")) / G("q05", "sd_2"), 2))

# Q6: the 1.5 x IQR rule
q1 <- G("q06", "q1"); q3 <- G("q06", "q3")
put("pt.q06.iqr", gx(q3 - q1)); put("pt.q06.fence_lo", gx(q1 - 1.5 * (q3 - q1)))
put("pt.q06.fence_hi", gx(q3 + 1.5 * (q3 - q1))); put("pt.q06.trap.two_iqr", gx(q3 + 2 * (q3 - q1)))

# Q11: audio guide by age group
cy <- G("q11", "child_yes"); cn <- G("q11", "child_no"); ay <- G("q11", "adult_yes"); an <- G("q11", "adult_no")
sy <- G("q11", "senior_yes"); sn <- G("q11", "senior_no")
users <- cy + ay + sy; tot <- cy + cn + ay + an + sy + sn; adults <- ay + an
put("pt.q11.rows", cj(c(cy + cn, adults, sy + sn))); put("pt.q11.users", users); put("pt.q11.nonusers", tot - users)
put("pt.q11.n", tot); put("pt.q11.adults_of_users", fx(ay / users, 3)); put("pt.q11.trap.users_of_adults", fx(ay / adults, 3))
put("pt.q11.trap.joint", fx(ay / tot, 3)); put("pt.q11.trap.users", fx(users / tot, 3))

# Q12: the share of red in the first spins
put("pt.q12.pct", gx(100 * G("q12", "red") / G("q12", "spins")))

# Q13 (Figure 24): 200 reruns of the seedlings' random assignment
sim <- as.integer(readp("practice-flowering-sim.csv")$flowered_a)
na <- G("q13", "n_a"); nb <- G("q13", "n_b"); fa <- G("q13", "flowered_a"); fb <- G("q13", "flowered_b")
tf <- fa + fb; dobs <- fa / na - fb / nb
put("pt.q13.share_a", fx(fa / na, 2)); put("pt.q13.share_b", fx(fb / nb, 2)); put("pt.q13.diff", fx(dobs, 2))
put("pt.q13.flowered", tf); put("pt.q13.seedlings", na + nb)
dsim <- sim / na - (tf - sim) / nb
ge <- sum(dsim >= dobs - 1e-9)
put("pt.q13.ge", ge); put("pt.q13.share", fx(ge / length(sim), 2))
put("pt.q13.trap.per100", fx(ge / 100, 2)); put("pt.q13.trap.complement", fx(1 - ge / length(sim), 2))
put("pt.q13.exact", fx(phyper(fa - 1, tf, na + nb - tf, na, lower.tail = FALSE), 4))
ks <- min(sim):max(sim)
put("pt.fig24.reruns", length(sim)); put("pt.fig24.ge", ge)
put("pt.fig24.diffs", cj(fx(ks / na - (tf - ks) / nb, 2))); put("pt.fig24.counts", cj(sapply(ks, function(k) sum(sim == k))))

# Q14: probability rules
pa <- G("q14", "p_a"); pb <- G("q14", "p_b"); pab <- G("q14", "p_ab")
put("pt.q14.union", fx(pa + pb - pab, 2)); put("pt.q14.trap.union_no_overlap", fx(pa + pb, 2))
put("pt.q14.product", fx(pa * pb, 2)); put("pt.q14.a_given_b", fx(pab / pb, 2)); put("pt.q14.b_given_a", fx(pab / pa, 2))

# Q15: late orders
pd <- G("q15", "p_delivery"); ld <- G("q15", "p_late_delivery"); lp <- G("q15", "p_late_pickup")
late <- pd * ld + (1 - pd) * lp
put("pt.q15.p_pickup", fx(1 - pd, 2)); put("pt.q15.joint_delivery", fx(pd * ld, 3)); put("pt.q15.joint_pickup", fx((1 - pd) * lp, 3))
put("pt.q15.p_late", fx(late, 3)); put("pt.q15.trap.late_given_delivery", fx(ld, 3)); put("pt.q15.delivery_given_late", fx(pd * ld / late, 3))

# Q16: a probability distribution's mean and SD
xs <- as.numeric(strsplit(gs("q16", "x"), ", ")[[1]]); ps <- as.numeric(strsplit(gs("q16", "p"), ", ")[[1]])
if (abs(sum(ps) - 1) > 1e-12) stop("Q16: the probabilities do not add to 1")
mu <- sum(xs * ps); vr <- sum((xs - mu)^2 * ps)
put("pt.q16.mu", fx(mu, 1)); put("pt.q16.var", fx(vr, 2)); put("pt.q16.sigma", fx(sqrt(vr), 2))
put("pt.q16.trap.mean_values", fx(mean(xs), 1)); put("pt.q16.trap.sd_values", fx(sqrt(mean((xs - mean(xs))^2)), 2))

# Q17: binomial
pk <- dbinom(0:G("q17", "n"), G("q17", "n"), G("q17", "p"))
put("pt.q17.p0", fx(pk[1], 4)); put("pt.q17.p1", fx(pk[2], 4)); put("pt.q17.ge2", fx(1 - pk[1] - pk[2], 4))
put("pt.q17.trap.eq2", fx(pk[3], 4)); put("pt.q17.trap.le2", fx(pk[1] + pk[2] + pk[3], 4))
put("pt.q17.trap.gt2", fx(1 - pk[1] - pk[2] - pk[3], 4))

# Q18: the cutoff for the heaviest 5%
m <- G("q18", "mean"); s <- G("q18", "sd"); top <- G("q18", "top_pct") / 100
z <- qnorm(1 - top)
put("pt.q18.area", fx(1 - top, 2)); put("pt.q18.z", fx(z, 3)); put("pt.q18.cutoff", fx(m + z * s, 1))
put("pt.q18.trap.two_tailed", fx(m + qnorm(1 - top / 2) * s, 1)); put("pt.q18.trap.lower", fx(m - z * s, 1))
put("pt.q18.trap.area", fx(m + (1 - top) * s, 1))

# Q19: the sampling distribution of p-hat
p <- G("q19", "p"); n <- G("q19", "n"); cut <- G("q19", "cut")
sdp <- sqrt(p * (1 - p) / n); zz <- (cut - p) / sdp
put("pt.q19.q", fx(1 - p, 2)); put("pt.q19.np", gx(n * p)); put("pt.q19.nq", gx(n * (1 - p)))
put("pt.q19.sd", fx(sdp, 3)); put("pt.q19.z", fx(zz, 2)); put("pt.q19.prob", fx(pnorm(zz, lower.tail = FALSE), 4))
put("pt.q19.trap.lower", fx(pnorm(zz), 4)); put("pt.q19.trap.two_tails", fx(2 * pnorm(zz, lower.tail = FALSE), 4))
one <- sqrt(p * (1 - p))
put("pt.q19.trap.sd_one", fx(one, 2)); put("pt.q19.trap.one", fx(pnorm((cut - p) / one, lower.tail = FALSE), 4))

# Q20: a 95% interval for a proportion
n <- G("q20", "n"); ph <- G("q20", "x") / n; se <- sqrt(ph * (1 - ph) / n)
put("pt.q20.phat", fx(ph, 2)); put("pt.q20.se", fx(se, 4)); put("pt.q20.zstar", fx(z95, 3)); put("pt.q20.me", fx(z95 * se, 4))
put("pt.q20.ci", cj(fx(ph + c(-1, 1) * z95 * se, 3))); put("pt.q20.trap.ci90", cj(fx(ph + c(-1, 1) * z90 * se, 3)))
put("pt.q20.trap.no_root", cj(fx(ph + c(-1, 1) * z95 * se^2, 3))); put("pt.q20.trap.no_zstar", cj(fx(ph + c(-1, 1) * se, 3)))

# Q22: the sample size for a margin of 0.03
me <- G("q22", "margin"); pst <- G("q22", "p_star")
en <- (z95 / me)^2 * pst * (1 - pst)
put("pt.q22.exact", fx(en, 1)); put("pt.q22.n", ceiling(en)); put("pt.q22.trap.down", floor(en))
put("pt.q22.trap.n90", ceiling((z90 / me)^2 * pst * (1 - pst))); put("pt.q22.trap.no_square", ceiling(z95 * sqrt(pst * (1 - pst)) / me))

# Q23: a one-sided test for a proportion
p0 <- G("q23", "p0"); n <- G("q23", "n"); ph <- G("q23", "x") / n
sd0 <- sqrt(p0 * (1 - p0) / n); zz <- (ph - p0) / sd0
put("pt.q23.phat", fx(ph, 2)); put("pt.q23.np0", gx(n * p0)); put("pt.q23.nq0", gx(n * (1 - p0)))
put("pt.q23.sd0", fx(sd0, 3)); put("pt.q23.z", fx(zz, 2)); put("pt.q23.p", fx(pnorm(zz), 4))
put("pt.q23.trap.two_sided", fx(2 * pnorm(-abs(zz)), 4)); put("pt.q23.trap.upper", fx(pnorm(zz, lower.tail = FALSE), 4))
sep <- sqrt(ph * (1 - ph) / n)
put("pt.q23.trap.se_phat", fx(sep, 4)); put("pt.q23.trap.z_phat", fx((ph - p0) / sep, 2)); put("pt.q23.trap.p_phat", fx(pnorm((ph - p0) / sep), 4))

# Q25: two proportions from a randomized experiment
n1 <- G("q25", "n_1"); x1 <- G("q25", "x_1"); n2 <- G("q25", "n_2"); x2 <- G("q25", "x_2")
p1 <- x1 / n1; p2 <- x2 / n2; pool <- (x1 + x2) / (n1 + n2)
sep <- sqrt(pool * (1 - pool) * (1 / n1 + 1 / n2)); seu <- sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
zz <- (p1 - p2) / sep; zu <- (p1 - p2) / seu
put("pt.q25.n", gx(n1 + n2)); put("pt.q25.phat_1", fx(p1, 2)); put("pt.q25.phat_2", fx(p2, 2)); put("pt.q25.diff", fx(p1 - p2, 2))
put("pt.q25.pooled", fx(pool, 3)); put("pt.q25.se", fx(sep, 5)); put("pt.q25.z", fx(zz, 2))
put("pt.q25.p", fx(2 * pnorm(-abs(zz)), 4)); put("pt.q25.trap.one_sided", fx(pnorm(zz, lower.tail = FALSE), 4))
put("pt.q25.trap.se_unpooled", fx(seu, 4)); put("pt.q25.trap.z_unpooled", fx(zu, 2)); put("pt.q25.trap.p_unpooled", fx(2 * pnorm(-abs(zu)), 4))
se1 <- sqrt(pool * (1 - pool) / (n1 + n2))
put("pt.q25.trap.z_one_n", fx((p1 - p2) / se1, 2)); put("pt.q25.trap.p_one_n", fx(2 * pnorm(-abs((p1 - p2) / se1)), 4))
put("pt.q25.ci", cj(fx(p1 - p2 + c(-1, 1) * z95 * seu, 3)))

# Q26 (Figure 25): news source by age group, one random sample
tab <- rbind(c(G("q26", "under40_phone"), G("q26", "under40_tv"), G("q26", "under40_print")),
             c(G("q26", "over40_phone"), G("q26", "over40_tv"), G("q26", "over40_print")))
r <- chi(tab)
put("pt.q26.rows", cj(r$rt)); put("pt.q26.cols", cj(r$ct)); put("pt.q26.n", r$n)
put("pt.q26.expected", cj(fx(as.vector(t(r$ex)), 1))); put("pt.q26.chi2", fx(r$stat, 2)); put("pt.q26.df", r$df)
put("pt.q26.p", fx(r$p, 4)); put("pt.q26.trap.cells_less_one", length(tab) - 1)
put("pt.fig25.under40.pct", cj(fx(100 * tab[1, ] / r$rt[1], 1))); put("pt.fig25.over40.pct", cj(fx(100 * tab[2, ] / r$rt[2], 1)))

# Q27: survival by watering schedule, an experiment
tab <- rbind(c(G("q27", "daily_survived"), G("q27", "daily_died")), c(G("q27", "alternate_survived"), G("q27", "alternate_died")),
             c(G("q27", "weekly_survived"), G("q27", "weekly_died")))
r <- chi(tab)
put("pt.q27.rows", cj(r$rt)); put("pt.q27.cols", cj(r$ct)); put("pt.q27.n", r$n)
put("pt.q27.expected", cj(fx(as.vector(t(r$ex)), 2))); put("pt.q27.expected_weekly_died", fx(r$ex[3, 2], 2))
put("pt.q27.trap.equal_split", fx(r$ct[2] / 3, 2)); put("pt.q27.trap.weekly_survived", fx(r$ex[3, 1], 2))
put("pt.q27.chi2", fx(r$stat, 2)); put("pt.q27.df", r$df); put("pt.q27.p", fx(r$p, 4))

# Q28: the sampling distribution of x-bar
mu <- G("q28", "mu"); sg <- G("q28", "sigma"); n <- G("q28", "n"); cut <- G("q28", "cut")
sdx <- sg / sqrt(n); zz <- (cut - mu) / sdx
put("pt.q28.sd", gx(sdx)); put("pt.q28.z", fx(zz, 2)); put("pt.q28.prob", fx(pnorm(zz, lower.tail = FALSE), 4))
put("pt.q28.trap.sigma", fx(pnorm((cut - mu) / sg, lower.tail = FALSE), 4)); put("pt.q28.trap.lower", fx(pnorm(zz), 4))
put("pt.q28.trap.two_tails", fx(2 * pnorm(zz, lower.tail = FALSE), 4))

# Q29: a t interval from summary statistics
n <- G("q29", "n"); xb <- G("q29", "mean"); s <- G("q29", "s"); df <- n - 1
ts <- qt(0.975, df); ts90 <- qt(0.95, df); se <- s / sqrt(n)
put("pt.q29.df", df); put("pt.q29.tstar", fx(ts, 3)); put("pt.q29.se", fx(se, 2)); put("pt.q29.me", fx(ts * se, 2))
put("pt.q29.ci", cj(fx(xb + c(-1, 1) * ts * se, 2))); put("pt.q29.trap.z", cj(fx(xb + c(-1, 1) * z95 * se, 2)))
put("pt.q29.trap.tstar90", fx(ts90, 3)); put("pt.q29.trap.ci90", cj(fx(xb + c(-1, 1) * ts90 * se, 2)))
put("pt.q29.trap.no_root", cj(fx(xb + c(-1, 1) * ts * s, 2)))

# Q30 (Figure 26): twelve checkout waits
cw <- as.numeric(readp("practice-checkout.csv")$minutes)
s5 <- five(cw); iqr <- s5[4] - s5[2]
put("pt.q30.n", length(cw)); put("pt.q30.values", cj(gx(cw))); put("pt.q30.five", cj(gx(s5)))
put("pt.q30.iqr", gx(iqr)); put("pt.q30.fence_hi", gx(s5[4] + 1.5 * iqr)); put("pt.q30.mean", fx(mean(cw), 2))
put("pt.q30.out", cj(gx(sort(cw[cw > s5[4] + 1.5 * iqr | cw < s5[2] - 1.5 * iqr]))))
put("pt.fig26.values", cj(gx(sort(cw))))

# Q32: ten runners in two shoes
sh <- readp("practice-shoes.csv")
sa <- as.numeric(sh$shoe_a); sb <- as.numeric(sh$shoe_b); d <- sa - sb; n <- length(d)
tt <- mean(d) / (sd(d) / sqrt(n))
put("pt.q32.n", n); put("pt.q32.diffs", cj(gx(d))); put("pt.q32.mean", fx(mean(d), 2)); put("pt.q32.sd", fx(sd(d), 3))
put("pt.q32.se", fx(sd(d) / sqrt(n), 3)); put("pt.q32.t", fx(tt, 2)); put("pt.q32.df", n - 1)
put("pt.q32.p", fx(2 * pt(-abs(tt), n - 1), 4))
put("pt.q32.trap.two_sample", fx((mean(sa) - mean(sb)) / sqrt(var(sa) / n + var(sb) / n), 2))
put("pt.q32.trap.over_n", fx(mean(d) / (sd(d) / n), 2)); put("pt.q32.trap.no_root", fx(mean(d) / sd(d), 2))

# Q33: two means from summary statistics
n1 <- G("q33", "n_1"); m1 <- G("q33", "mean_1"); s1 <- G("q33", "s_1")
n2 <- G("q33", "n_2"); m2 <- G("q33", "mean_2"); s2 <- G("q33", "s_2")
se <- sqrt(s1^2 / n1 + s2^2 / n2)
put("pt.q33.diff", fx(m1 - m2, 1)); put("pt.q33.se", fx(se, 4)); put("pt.q33.t", fx((m1 - m2) / se, 2))
put("pt.q33.trap.add_se", fx((m1 - m2) / (s1 / sqrt(n1) + s2 / sqrt(n2)), 2))
put("pt.q33.trap.no_square", fx((m1 - m2) / sqrt(s1 / n1 + s2 / n2), 2)); put("pt.q33.trap.no_n", fx((m1 - m2) / sqrt(s1^2 + s2^2), 2))

# Q35 to Q37 and Q39 (Figure 27): iced drinks and the day's high
ic <- readp("practice-iced.csv")
x <- as.numeric(ic$high_f); y <- as.numeric(ic$drinks); cf <- fit(x, y); a <- cf[["a"]]; b <- cf[["b"]]; rr <- cor(x, y)
put("pt.q35.n", length(x)); put("pt.q35.r", fx(rr, 3)); put("pt.q35.x_range", cj(gx(range(x))))
put("pt.q36.a", fx(a, 3)); put("pt.q36.b", fx(b, 3)); put("pt.q39.r2", fx(rr^2, 3)); put("pt.q39.r2_pct", fx(100 * rr^2, 1))
res <- y - (a + b * x); k <- which.max(abs(res)); xk <- x[k]; yk <- y[k]
put("pt.q37.day", ic$day[k]); put("pt.q37.high", gx(xk)); put("pt.q37.drinks", gx(yk))
put("pt.q37.predicted", fx(a + b * xk, 1)); put("pt.q37.residual", fx(yk - (a + b * xk), 1))
put("pt.q37.trap.sign", fx((a + b * xk) - yk, 1)); put("pt.q37.trap.no_intercept", fx(yk - b * xk, 1))
put("pt.fig27.n", length(x)); put("pt.fig27.line", cj(fx(c(a, b), 3))); put("pt.fig27.x_range", cj(gx(range(x))))

# Q38 (Figure 28): stopping distance and speed
sp <- readp("practice-stopping.csv")
x <- as.numeric(sp$speed_mph); y <- as.numeric(sp$distance_ft); cf <- fit(x, y)
put("pt.q38.n", length(x)); put("pt.q38.r", fx(cor(x, y), 3)); put("pt.q38.line", cj(fx(cf, 3)))
put("pt.fig28.speeds", cj(gx(x))); put("pt.fig28.res", cj(fx(y - (cf[["a"]] + cf[["b"]] * x), 1)))

# Q40: the line from summary statistics
rq <- G("q40", "r"); mx <- G("q40", "mean_x"); sx <- G("q40", "sd_x"); my <- G("q40", "mean_y"); sy <- G("q40", "sd_y"); xn <- G("q40", "x_new")
b <- rq * sy / sx; a <- my - b * mx
put("pt.q40.b", fx(b, 2)); put("pt.q40.a", fx(a, 1)); put("pt.q40.predicted", fx(a + b * xn, 1))
put("pt.q40.trap.flipped_b", fx(rq * sx / sy, 2)); put("pt.q40.trap.flipped_a", fx(my - rq * sx / sy * mx, 1))
put("pt.q40.trap.no_r_b", fx(sy / sx, 2)); put("pt.q40.trap.no_r_a", fx(my - sy / sx * mx, 1)); put("pt.q40.trap.swapped_a", fx(mx - b * my, 1))

# W2 (Figure 29): commutes by bike and by bus
cm <- readp("practice-commute.csv")
for (mode in c("bike", "bus")) {
  v <- as.numeric(cm$minutes[cm$mode == mode])
  s5 <- five(v); iqr <- s5[4] - s5[2]; lo <- s5[2] - 1.5 * iqr; hi <- s5[4] + 1.5 * iqr
  p <- paste0("pt.w2.", mode, ".")
  put(paste0(p, "n"), length(v)); put(paste0(p, "five"), cj(gx(s5))); put(paste0(p, "iqr"), gx(iqr))
  put(paste0(p, "fences"), cj(gx(c(lo, hi)))); put(paste0(p, "mean"), fx(mean(v), 2)); put(paste0(p, "sd"), fx(sd(v), 2))
  outs <- sort(v[v < lo | v > hi])
  put(paste0(p, "out"), if (length(outs) > 0) cj(gx(outs)) else "none")
  put(paste0("pt.fig29.", mode), cj(gx(sort(v))))
}
bus <- as.numeric(cm$minutes[cm$mode == "bus"])
put("pt.w2.bus.z30", fx((30 - mean(bus)) / sd(bus), 2))

# W3: twenty cups from a machine set for 12 ounces
fl <- as.numeric(readp("practice-fill.csv")$ounces)
n <- length(fl); mu0 <- G("w3", "target"); xb <- mean(fl); s <- sd(fl); se <- s / sqrt(n); tt <- (xb - mu0) / se; ts <- qt(0.975, n - 1)
put("pt.w3.n", n); put("pt.w3.values", cj(fx(fl, 2))); put("pt.w3.mean", fx(xb, 3)); put("pt.w3.sd", fx(s, 4))
put("pt.w3.se", fx(se, 4)); put("pt.w3.t", fx(tt, 2)); put("pt.w3.df", n - 1); put("pt.w3.p", fx(pt(tt, n - 1), 4))
put("pt.w3.tstar", fx(ts, 3)); put("pt.w3.me", fx(ts * se, 3)); put("pt.w3.ci", cj(fx(xb + c(-1, 1) * ts * se, 3)))
put("pt.w3.median", gx(median(fl))); put("pt.w3.range", cj(fx(range(fl), 2)))
s5 <- five(fl); iqr <- s5[4] - s5[2]; lo <- s5[2] - 1.5 * iqr; hi <- s5[4] + 1.5 * iqr
put("pt.w3.five", cj(gx(s5))); put("pt.w3.iqr", gx(iqr)); put("pt.w3.fences", cj(gx(c(lo, hi))))
outs <- sort(fl[fl < lo | fl > hi])
put("pt.w3.out", if (length(outs) > 0) cj(fx(outs, 2)) else "none")

# W4: defective parts
p <- G("w4", "p"); ns <- G("w4", "n_small"); n <- G("w4", "n"); x <- G("w4", "x")
put("pt.w4.p_none", fx((1 - p)^ns, 4)); put("pt.w4.p_some", fx(1 - (1 - p)^ns, 4))
sdp <- sqrt(p * (1 - p) / n); ph <- x / n; zz <- (ph - p) / sdp
put("pt.w4.q", fx(1 - p, 2)); put("pt.w4.np", gx(n * p)); put("pt.w4.nq", gx(n * (1 - p))); put("pt.w4.sd", fx(sdp, 5)); put("pt.w4.phat", fx(ph, 3))
put("pt.w4.z", fx(zz, 2)); put("pt.w4.prob", fx(pnorm(zz, lower.tail = FALSE), 4))
put("pt.w4.exact", fx(pbinom(x - 1, n, p, lower.tail = FALSE), 4))

dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
nm <- sort(names(vals), method = "radix")
quoted <- vapply(nm, function(k) {
  x <- vals[[k]]
  if (grepl("[,\"]", x)) paste0("\"", gsub("\"", "\"\"", x), "\"") else x
}, "")
writeLines(c("name,value", paste0(nm, ",", quoted)), out)
cat(sprintf("r route: %d values in %s\n", length(nm), out))
