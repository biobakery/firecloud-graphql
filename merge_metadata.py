
# combine all sample and participant files in folder into two files to use to load the database

# To run:
# $ python merge_metadata.py INPUT OUTPUT
# Place all of the sample and participant files from each study in the "INPUT" folder.
# Manually change column names so those that should be shared across studies have the same
# name and case (ie age vs age_2012 vs Age).

import os
import sys

INPUT_FOLDER = sys.argv[1]
OUTPUT_FOLDER = sys.argv[2]

def merge_data(files, filetype):
    data = {}
    headers = []
    # read in all the files
    for filename in files:
        data[filename]={}
        header = None
        for line in open(filename):
            line = line.rstrip().split(",")
            if not header:
                headers += line
                header = line
            else:
                data[filename][line[0]]=dict([(x,y) for x,y in zip(header, line[1:])])
    # create a master header
    header_set=set(headers)
    header_set.remove(filetype)
    final_headers = [filetype]+list(header_set)
    final_data = []
    for filename, filedata in data.items():
        for sample, sampledata in filedata.items():
            newline = [sample]
            for item in final_headers:
                newline.append(sampledata.get(item,"NA"))
            final_data.append(newline)

    return final_headers, final_data

def write_file(header, data, filename):
    with open(filename, "w") as file_handle:
        file_handle.write(",".join(header)+"\n")
        for line in data:
            file_handle.write(",".join(line)+"\n")


samples_files = filter(lambda x: "sample" in x and os.path.isfile(x), [os.path.join(INPUT_FOLDER, file) for file in os.listdir(INPUT_FOLDER)])
participants_files = filter(lambda x: "participant" in x and os.path.isfile(x), [os.path.join(INPUT_FOLDER, file) for file in os.listdir(INPUT_FOLDER)])


# create output folder if it does not exist
if not os.path.isdir(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)

samples_header, samples_data = merge_data(samples_files,"sample")
samples_output = os.path.join(OUTPUT_FOLDER, "merged_samples.csv")
write_file(samples_header, samples_data, samples_output)


participants_header, participants_data = merge_data(participants_files,"entity_participant_id")
participants_output = os.path.join(OUTPUT_FOLDER, "merged_participants.csv")
write_file(participants_header, participants_data, participants_output)
