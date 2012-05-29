# Read in an xpt file and produce a line-by-line JSON result

args <- commandArgs(trailingOnly = TRUE)

library('foreign');
library('RJSONIO');
print(' [*] Reading data...')
d <- read.xport(file=args[1])

cat(toJSON(unname(apply(d, 1, function(x) as.data.frame(t(x))))), file=args[2])
