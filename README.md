The following pipeline was part of a class project and was required to accept input data and produce output data in the form of variant calls while outputting some quality metrics along the way.

This basic script creates options that takes file names and optional BWA MEM options as input for sequence alignment and variant calling. The expected output is VCF quality scores and number of SNPs per file. However, there are limitations to using options:

1) The script's relies on the original file name(s) for naming output files so if options were passed, the same output file would be overwritten and only the last file would be outputted

2) The script has only been tested for using a single value for an option (e.g., -k 10) and is unlikely to work if given a range of values (e.g., -k for 1 to 10)


The specific data set used for this pipeline was from roryk's tiny-data-set: https://github.com/roryk/tiny-test-data
