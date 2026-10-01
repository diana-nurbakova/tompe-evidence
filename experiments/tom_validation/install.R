# R dependencies for the CLMM (V3) and GLMM (V4) stages of the ToM validation.
#
# Usage:
#   Rscript experiments/tom_validation/install.R
#
# Installs any missing package from CRAN, then compares installed versions with
# the ones the committed results were checked against.
#
# Committed results: R 4.2.3, ordinal 2023.12.4, lme4 1.1.35.3.
# Re-checked 2026-10-01 with the versions below: CLMM and GLMM estimates agree
# to the third decimal; the ToM coefficient and the random-slope test are unchanged.

tested <- c(ordinal = "2026.7.26", lme4 = "2.0.6", jsonlite = "2.0.0")

missing <- setdiff(names(tested), rownames(installed.packages()))
if (length(missing) > 0) {
  install.packages(missing, repos = "https://cloud.r-project.org")
}

cat(R.version.string, "\n")
for (p in names(tested)) {
  v <- as.character(packageVersion(p))
  flag <- if (v == tested[[p]]) "" else paste0("  (tested: ", tested[[p]], ")")
  cat(sprintf("%-9s %s%s\n", p, v, flag))
}
