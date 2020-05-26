
# This script will download SRA files, convert them to fastq, and then rename them to sample names (from SRA accessions).

# To install:
# $ pip install anadama2
# Also install sra-toolkit which includes the executable fastq-dump: https://ncbi.github.io/sra-tools/install_config.html

# To run:
# $ python download_sra_rename.py --input-file hpfs_sra_with_names.txt --output sra_downloads --local-jobs 8
# The input file contains a tab-delimited list of the sra accessions and the sample names.
# The output folder is where the downloads and final fastq renamed files will be placed.
# Local jobs are the total number of downloads at once (to be modified based on the compute environment with the default set to 1).

import os

from anadama2 import Workflow

workflow = Workflow(remove_options=["input"])

workflow.add_argument("input-file", desc="the list of sra accesions and new names", required=True)

args = workflow.parse_args()

downloaded_fastq = []
for line in open(args.input_file):
    sra_access, new_name = line.rstrip().split("\t")
    downloads=[new_name+"_1.fastq.gz",new_name+"_2.fastq.gz"]
    workflow.add_task(
        """fastq-dump [args[1]] --split-files --gzip --outdir [args[0]] && \
           cd [args[0]] && \
           mv [args[1]]_1.fastq.gz [args[2]] && \
           if [ -f [args[1]]_2.fastq.gz ]; then mv [args[1]]_2.fastq.gz [args[3]]; fi && \
           echo 'done' > [targets[0]]""",
        targets=[os.path.join(args.output,new_name+".txt")],
        args=[args.output,sra_access]+downloads)

workflow.go()
