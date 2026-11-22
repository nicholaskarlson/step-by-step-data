# Route 2 (base R): summarize the data files, as data_summary.py does in standard-library Python.
#
#   Rscript --vanilla r/data_summary.R ROOT OUT.csv
#
# Writes OUT.csv with two columns, name and value, each value formatted as the Python route
# formats it (whole numbers as they are; other numbers to six decimals; 1 or 0 for a check).
# No add-on packages. Every column is read as text, so nothing is converted until a number
# is needed, and an empty cell stays empty.

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2) stop("usage: Rscript --vanilla r/data_summary.R ROOT OUT.csv")
root <- args[1]
out <- args[2]
res <- character(0)

rd <- function(name, header = TRUE) {
  utils::read.csv(file.path(root, "data", name), header = header, colClasses = "character",
                  na.strings = character(0), stringsAsFactors = FALSE, check.names = FALSE,
                  fileEncoding = "UTF-8", strip.white = FALSE)
}
put_int <- function(name, x) res[name] <<- sprintf("%d", as.integer(x))
put_num <- function(name, x) res[name] <<- sprintf("%.6f", x)
put_chk <- function(name, cond) res[name] <<- if (isTRUE(cond)) "1" else "0"
mean_sd <- function(x) {
  m <- sum(x) / length(x)
  c(m, sqrt(sum((x - m)^2) / (length(x) - 1)))
}
# A TI-84 list from the lists file: the entries before the first empty cell.
leading <- function(v) {
  k <- which(v == "")
  if (length(k) == 0) v else v[seq_len(k[1] - 1)]
}

cls <- rd("tonmick-classroom.csv")
off <- rd("tonmick-offered.csv")
noff <- rd("tonmick-not-offered.csv")
grd <- rd("tonmick-grades-not-offered.csv")
inv <- rd("tonmick-invited.csv")
dic <- rd("tonmick-classroom-dictionary.csv")
lst <- rd("tonmick-lists.csv", header = FALSE)

put_int("files.classroom.rows", nrow(cls))
put_int("files.offered.rows", nrow(off))
put_int("files.not_offered.rows", nrow(noff))
put_int("files.grades_not_offered.rows", nrow(grd))
put_int("files.invited.rows", nrow(inv))
put_int("files.dictionary.rows", nrow(dic))
put_int("files.lists.rows", nrow(lst))

L <- vector("list", 6)
for (i in 1:6) {
  col <- if (i <= ncol(lst)) lst[[i]] else rep("", nrow(lst))
  L[[i]] <- leading(col)
  n <- length(L[[i]])
  rest <- if (n < length(col)) col[(n + 1):length(col)] else character(0)
  put_int(sprintf("lists.L%d.n", i), n)
  put_chk(sprintf("lists.L%d.no_gaps", i), all(rest == ""))
}

o <- cls[cls$offer == "1", ]
n0 <- cls[cls$offer == "0", ]
g <- n0[n0$grade_12 != "", ]
put_chk("check.offered_file_is_classroom", identical(o$entry_grade, off$entry_grade) && identical(o$visits, off$visits))
put_chk("check.not_offered_file_is_classroom", identical(n0$entry_grade, noff$entry_grade) && identical(n0$visits, noff$visits))
put_chk("check.grades_file_is_classroom", identical(g$entry_grade, grd$entry_grade) && identical(g$grade_12, grd$grade_12))
put_chk("check.L1_L2_are_offered", identical(L[[1]], off$entry_grade) && identical(L[[2]], off$visits))
put_chk("check.L3_L4_are_not_offered", identical(L[[3]], noff$entry_grade) && identical(L[[4]], noff$visits))
put_chk("check.L5_L6_are_grades", identical(L[[5]], grd$entry_grade) && identical(L[[6]], grd$grade_12))
joined <- inv[inv$joined == "1", ]
put_chk("check.joined_are_classroom", identical(sort(joined$student_id), sort(cls$student_id)))

put_int("classroom.offered", nrow(o))
put_int("classroom.not_offered", nrow(n0))
put_int("classroom.colleges", length(unique(cls$college)))
put_int("classroom.part_time", sum(cls$part_time == "1"))
put_int("invited.joined", nrow(joined))
put_int("invited.part_time", sum(inv$part_time == "1"))
put_int("invited.part_time_joined", sum(joined$part_time == "1"))
put_int("exit.stayed", sum(cls$exit == "stayed"))
put_int("exit.withdrew", sum(cls$exit == "withdrew"))
put_int("exit.transferred", sum(cls$exit == "transferred"))
put_int("exit.consent_withdrawn", sum(cls$exit == "consent withdrawn"))
for (label in c("offered", "not_offered")) {
  grp <- if (label == "offered") o else n0
  put_int(paste0("withdrew.", label), sum(grp$withdrew == "1"))
  put_int(paste0("known.", label), sum(grp$withdrew %in% c("0", "1")))
  v <- as.integer(grp$visits)
  put_int(paste0("visits.", label, ".sum"), sum(v))
  ms <- mean_sd(as.numeric(v))
  put_num(paste0("visits.", label, ".mean"), ms[1])
  put_num(paste0("visits.", label, ".sd"), ms[2])
  put_int(paste0("grade_12.", label, ".n"), sum(grp$grade_12 != ""))
}
ms <- mean_sd(as.numeric(cls$entry_grade))
put_num("entry_grade.all.mean", ms[1])
put_num("entry_grade.all.sd", ms[2])
ms <- mean_sd(as.numeric(g$grade_12))
put_num("grade_12.not_offered.mean", ms[1])
put_num("grade_12.not_offered.sd", ms[2])

dir.create(dirname(out), recursive = TRUE, showWarnings = FALSE)
writeLines(c("name,value", paste(names(res), res, sep = ",")), out)
cat(sprintf("r route: %d values in %s\n", length(res), out))
