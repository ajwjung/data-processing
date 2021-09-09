
#!/usr/bin/python
# Basic Variant Calling Pipeline
import os
import sys
import argparse
import subprocess

"""
This script creates options that takes file names and optional BWA MEM options as input for sequence alignment and variant calling.
Expected output is VCF quality scores and number of SNPs per file.
"""

def main():
    """Parses args, then aligns sequences and calls variants"""
    args = parse_args()
    bwa_ref="../tiny-test-data/genomes/Hsapiens/hg19/bwa/hg19.fa"
    sam_ref="../tiny-test-data/genomes/Hsapiens/hg19/seq/hg19.fa"

    try:
        # Extracting file names without extensions
        file_1, file_2 = args.input_file_name
        file_name = os.path.splitext(args.input_file_name[0])[0]
        # Provided options for BWA MEM
        if args.options_list:
            options = " ".join(args.options_list)
            cmd1 = "bwa mem %s %s %s %s > %s.sam" % (options, bwa_ref, file_1, file_2, file_name)
        else:
            cmd1 = "bwa mem %s %s %s > %s.sam" % (bwa_ref, file_1, file_2, file_name)
        # Alignment and variant calling (filtered quality score)
        cmd2 = "samtools sort %s.sam > %s.bam" % (file_name, file_name)
        cmd3 = "bcftools mpileup -Ou -f {0} {1}.bam | bcftools call -vmO z -o {2}.vcf".format(sam_ref, file_name, file_name)
        cmd4 = "bcftools filter -i 'QUAL>30' {0}.vcf | bcftools stats | grep 'QUAL\s' | cut -f 3-4".format(file_name)
        p1 = subprocess.check_output(cmd1, stderr=subprocess.PIPE, shell=True)
        p2 = subprocess.check_output(cmd2, stderr=subprocess.PIPE, shell=True)
        p3 = subprocess.check_output(cmd3, stderr=subprocess.PIPE, shell=True)
        p4 = subprocess.check_output(cmd4, stderr=subprocess.PIPE, shell=True)
        print(f"""{file_name}\n{p4.decode('utf-8')}""")
    except IOError as err:
        print("Could not find files using the provided base name: " + args.input_file_name)
        print(err)


def parse_args():
    """ Standard argument parsing """
    parser = argparse.ArgumentParser(description="Variant Calling from BAM Files")
    
    parser.add_argument('-i', '--input_file_name', type=str, nargs=2,
                        required=True, help='Sample file name')
    parser.add_argument('-f', '--input_bam_name', type=str, nargs='+',
                        required=False, help='Sample BAM file')
    parser.add_argument('-l', '--options_list', type=str, required=False, nargs="*",
                        help='Options for BWA MEM')


    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
