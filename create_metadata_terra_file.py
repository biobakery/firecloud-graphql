
import sys

import subprocess

# Run this script to create two metadata files for the Terra workspace.
# Please note this was written for HPFS so some modification in file naming convention might be needed for different projects.

# $ python create_metadata_terra_file.py "gs://fc-3f2f90e2-bbca-43ba-8e36-42b4a1a89d51/"

BUCKET = sys.argv[1]

OUTFILE1="terra_participants.tsv"
OUTFILE2="terra_samples.tsv"

# Generate a file of data metadata to store in the terra workspace.
header = ["entity:sample_id","access","data_category","data_format","experimental_strategy","file_id","file_name","file_size","participant","platform","sample","type"]

file_handle = open(OUTFILE2,"w")
file_handle.write("\t".join(header)+"\n")
# Get all of the files in the bucket with their paths and sizes.

output = subprocess.check_output(["gsutil","du",BUCKET])

all_participants = set()
for line in output.split("\n"):
    if line.endswith(".gz") or line.endswith(".tsv"):
        data = line.split(" ")
        file_size = data[0]
        url = data[-1]
        file_name = url.split("/")[-1]
        file_id = url
        tokens = file_name.replace(".gz","").replace(".","_").split("_")
        sample = tokens[0]+"_"+tokens[1]
        if not "dna" in tokens[2] and not "rna" in tokens[2]:
            sample += "_"+tokens[2]
        sample_id = sample

        experimental_strategy = "wmtx"
        if "dna" in url:
          experimental_strategy = "wmgx"
          sample_id += "_dna"
        else:
          sample_id += "_rna"

        participant = tokens[0]
        if "taxon" in url:
            type = "processedFiles"
            data_format = "tsv"
            data_category = "Taxonomic Profiles"
            access = "open"
            sample_id += "_taxon"
        elif "fastq" in url:
            type = "rawFiles"
            data_format = "fastq"
            data_category = "Raw Reads"
            access = "controlled"
            sample_id += "_fastq"
            if "_1" in file_name:
                sample_id += "_1"
            else:
                sample_id += "_2"
        elif "pathway" in url:
            type = "processedFiles"
            data_format = "tsv"
            data_category = "Pathways"
            access = "open"
            sample_id += "_pathway"

        platform = "Illumina"
        all_participants.add(participant)
        file_handle.write("\t".join([sample_id, access, data_category, data_format, experimental_strategy, file_id, file_name, file_size, participant, platform, sample, type])+"\n")

file_handle.close()
file_handle = open(OUTFILE1, "w")
header = ["entity:participant_id"]

file_handle.write("\t".join(header)+"\n")

for id in all_participants:
    file_handle.write(id+"\n")

file_handle.close()

