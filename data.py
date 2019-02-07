

class Project(object):
    """ Holds data for each project including name and files """

    def __init__(self, name, files):
        self.name = name
        self.files = files

    def get_name(self):
        return self.name

    def get_participants(self):
        participants = list(set([file.participant for file in self.files]))
        return participants

    def get_samples(self):
        samples = list(set([file.sample for file in self.files]))
        return samples

class File(object):
    """ Holds information on each file including type, participant, 
        sample, raw/processed, and access 
    """

    def __init__(self, name, participant, sample, file_type, raw=True, open_access=True):
        self.name = name
        self.participant = participant
        self.sample = sample
        self.type = file_type
        self.raw = raw
        self.open_access = open_access

USERNAME = "null"

PROJECTS = [
    Project(name="NHSII-demo_A",
        files=[
            File("demo_A1.fastq","participant_A1","sample_A1","fastq", open_access=False),
            File("demo_A2.fastq","participant_A1","sample_A2","fastq", open_access=False),
            File("demo_A3.fastq","participant_A2","sample_A1","fastq", open_access=False),
            File("demo_A4.fastq","participant_A2","sample_A2","fastq", open_access=False),
            File("demo_A1.tsv","participant_A1","sample_A1","tsv", raw=False),
            File("demo_A2.tsv","participant_A1","sample_A2","tsv", raw=False),
            File("demo_A3.tsv","participant_A2","sample_A1","tsv", raw=False),
            File("demo_A4.tsv","participant_A2","sample_A2","tsv", raw=False)
        ]),
    Project(name="NHSII-demo_B",
        files=[
            File("demo_B1.fastq","participant_B1","sample_B1","fastq"),
            File("demo_B2.fastq","participant_AB","sample_B2","fastq"),
            File("demo_B3.fastq","participant_AB","sample_B1","fastq"),
            File("demo_B4.fastq","participant_AB","sample_B2","fastq"),
            File("demo_B1.tsv","participant_B1","sample_B1","tsv", raw=False),
            File("demo_B2.tsv","participant_B1","sample_B2","tsv", raw=False),
            File("demo_B3.tsv","participant_B2","sample_B1","tsv", raw=False),
            File("demo_B4.tsv","participant_B2","sample_B2","tsv", raw=False)
        ]),
    Project(name="NHSII-demo_C",
        files=[
            File("demo_C1.fastq","participant_C1","sample_C1","fastq"),
            File("demo_C2.fastq","participant_C1","sample_C2","fastq"),
            File("demo_C3.fastq","participant_C2","sample_C1","fastq"),
            File("demo_C4.fastq","participant_C2","sample_C2","fastq"),
            File("demo_C1.tsv","participant_C1","sample_C1","tsv", raw=False),
            File("demo_C2.tsv","participant_C1","sample_C2","tsv", raw=False),
            File("demo_C3.tsv","participant_C2","sample_C1","tsv", raw=False),
            File("demo_C4.tsv","participant_C2","sample_C2","tsv", raw=False)
        ])
]


def get_username():
    return USERNAME

def get_all_participants(Projects):
    participants = set()
    for project in Projects:
        participants.update(project.get_participants())
    return list(participants)

def get_all_samples(Projects):
    samples = set()
    for project in Projects:
        samples.update(project.get_samples())
    return list(samples)

def get_all_dataFormats(Projects):
    types = set()
    for project in Projects:
        for file in project.files:
            types.add(file.type)
    return list(types)

def get_all_rawFiles(Projects):
    rawFiles = []
    for project in Projects:
        for file in project.files:
            if file.raw:
                rawFiles.append(file)
    return rawFiles
    
def get_all_processedFiles(Projects):
    processedFiles = []
    for project in Projects:
        for file in project.files:
            if not file.raw:
                processedFiles.append(file)
    return processedFiles

def get_count(type, Projects=PROJECTS):
    count = 0
    if type == "projects":
        count = len(Projects)
    elif type == "participants":
        count = len(get_all_participants(Projects))
    elif type == "samples":
        count = len(get_all_samples(Projects))
    elif type == "dataFormats":
        count = len(get_all_dataFormats(Projects))
    elif type == "rawFiles":
        count = len(get_all_rawFiles(Projects))
    elif type == "processedFiles":
        count = len(get_all_processedFiles(Projects))

    return str(count)
