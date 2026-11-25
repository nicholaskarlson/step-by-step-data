# Route 2 for the back matter's three tables: the standard normal table, t critical values, and
# chi-square critical values, with base R (pnorm, qnorm, qt, qchisq; no add-on packages).
#
#   Rscript --vanilla r/tables.R ROOT OUT.csv
#
# It shares no code with python/tables.py. Each table row is one value, its entries separated
# by ", ", as the book prints them. Row table.normal.neg.1.9 holds the area to the left of
# z = -1.90, -1.91, ..., -1.99; row table.normal.pos.1.9 the area to the left of 1.90 to 1.99.

args <- commandArgs(trailingOnly = TRUE)
out <- args[2]
vals <- list()
put <- function(name, value) {
  if (!is.null(vals[[name]])) stop(paste("duplicate name", name))
  vals[[name]] <<- as.character(value)
}
cj <- function(x) paste(x, collapse = ", ")
t_tails <- c("0.20", "0.10", "0.05", "0.025", "0.01", "0.005", "0.001", "0.0005")
t_levels <- c("60%", "80%", "90%", "95%", "98%", "99%", "99.8%", "99.9%")
t_df <- c(1:30, 40, 50, 60, 80, 100, 1000)
c_tails <- c("0.25", "0.20", "0.10", "0.05", "0.025", "0.01", "0.005", "0.001")
c_df <- c(1:30, 40, 50, 60, 80, 100)

for (side in c("neg", "pos")) {
  sgn <- if (side == "neg") -1 else 1
  for (tenth in 0:34) {
    z <- sgn * (tenth * 10 + 0:9) / 100
    put(sprintf("table.normal.%s.%d.%d", side, tenth %/% 10, tenth %% 10), cj(sprintf("%.4f", pnorm(z))))
  }
}
put("table.t.tails", cj(t_tails)); put("table.t.levels", cj(t_levels))
for (d in t_df) {
  put(paste0("table.t.df.", d), cj(sprintf("%.3f", qt(as.numeric(t_tails), d, lower.tail = FALSE))))
}
put("table.t.z", cj(sprintf("%.3f", qnorm(as.numeric(t_tails), lower.tail = FALSE))))
put("table.chisq.tails", cj(c_tails))
for (d in c_df) {
  put(paste0("table.chisq.df.", d), cj(sprintf("%.3f", qchisq(as.numeric(c_tails), d, lower.tail = FALSE))))
}

dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
nm <- sort(names(vals), method = "radix")
quoted <- vapply(nm, function(k) {
  x <- vals[[k]]
  if (grepl("[,\"]", x)) paste0("\"", gsub("\"", "\"\"", x), "\"") else x
}, "")
writeLines(c("name,value", paste0(nm, ",", quoted)), out)
cat(sprintf("r route: %d values in %s\n", length(nm), out))
