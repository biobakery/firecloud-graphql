# Utility script to download files from NCBI SRA using accession numbers, rename to sample names, and then upload to Terra google bucket.
# To get a list of accession numbers for an SRA project see the SRA document (https://www.ncbi.nlm.nih.gov/sra/docs/sradownload/).

# Requires google cloud SDK installed (installable with pip), anadama2, and sra-toolkit (https://github.com/ncbi/sra-tools/wiki/02.-Installing-SRA-Toolkit).

# To run: $ python download_sra_rename_upload.py --input-file sra_names.txt --output output folder --local-jobs 10

# The input file should be a tab-delimited list of accession (column 1) and sample name (column 2).
# Add the option "--output-bucket" to specify the terra workspace bucket. 
# Make sure to set up google cloud config before running this script.
# 1. $ gcloud auth activate-service-account --key-file ~/key/biom-mass-123abc.json
# 2. $ gcloud auth list (to confirm correct auth acount active)

# Also make sure to add the email of the service account to the Terra workspace.


import os

from anadama2 import Workflow

workflow = Workflow(remove_options=["input"])

workflow.add_argument("input-file", desc="the list of sra accesions and new names", required=True)
workflow.add_argument("output-bucket", desc="the bucket to write the output files", default="gs://fc-3f2f90e2-bbca-43ba-8e36-42b4a1a89d51/fastq/")

args = workflow.parse_args()

downloaded_fastq = []
for line in open(args.input_file):
    sra_access, new_name = line.rstrip().split("\t")
    downloads=[os.path.join(args.output,new_name+"_1.fastq.gz"),os.path.join(args.output,new_name+"_2.fastq.gz")]
    workflow.add_task(
        """prefetch [args[0]] -O [args[1]] && \
           fastq-dump [args[2]] --split-files --gzip --outdir [args[1]] && \
           mv [args[1]]/[args[4]]_1.fastq.gz [args[5]] && \
           mv [args[1]]/[args[4]]_2.fastq.gz [args[6]] && \
           gsutil cp [args[5]] [args[7]] && \
           gsutil cp [args[6]] [args[7]] && \
           rm [args[5]] && \
           rm [args[6]] && \
           rm -r [args[3]] && \
           echo 'done' > [targets[0]]""",
        targets=[os.path.join(args.output,new_name+".txt")],
        args=[sra_access,args.output,os.path.join(args.output,sra_access,sra_access+".sra"), os.path.join(args.output,sra_access), sra_access]+downloads+[args.output_bucket])

workflow.go()
