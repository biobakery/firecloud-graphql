

class Project(object):
    """ Holds data for each project including name and files """

    def __init__(self, name, files):
        self.name = name
        self.files = files

    def get_name(self):
        return self.name

    def get_participants(self, ids_only=True):
        if ids_only:
            participants = list(set([file.participant.id for file in self.files]))
        else:
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

class Participant(object):
    """ Holds information on each person in each project including metadata """

    def __init__(self, id, age, gender, race, project):
        self.id = id
        self.age = age
        self.gender = gender
        self.race = race
        self.project = project

class Sample(object):
    """ Holds information about each sample including participant and type """

    def __init__(self, id, participant, type):
        self.id = id
        self.participant = participant
        self.type = type

USERNAME = "null"

PARTICIPANTS = [
    Participant("participant_A1", "24", "F", "white", "NHSII-demo_A"),
    Participant("participant_A2", "38", "M", "asian", "NHSII-demo_A"),
    Participant("participant_B1", "29", "F", "african american", "NHSII-demo_B"),
    Participant("participant_B2", "42", "M", "asian", "NHSII-demo_B"),
    Participant("participant_C1", "24", "F", "african american", "NHSII-demo_C"),
    Participant("participant_C2", "53", "M", "white", "NHSII-demo_C"),
]

PROJECTS = [
    Project(name="NHSII-demo_A",
        files=[
            File("demo_A1.fastq",PARTICIPANTS[0],"sample_A1","fastq", open_access=False),
            File("demo_A2.fastq",PARTICIPANTS[0],"sample_A2","fastq", open_access=False),
            File("demo_A3.fastq",PARTICIPANTS[1],"sample_A1","fastq", open_access=False),
            File("demo_A4.fastq",PARTICIPANTS[1],"sample_A2","fastq", open_access=False),
            File("demo_A1.tsv",PARTICIPANTS[0],"sample_A1","tsv", raw=False),
            File("demo_A2.tsv",PARTICIPANTS[0],"sample_A2","tsv", raw=False),
            File("demo_A3.tsv",PARTICIPANTS[1],"sample_A1","tsv", raw=False),
            File("demo_A4.tsv",PARTICIPANTS[1],"sample_A2","tsv", raw=False)
        ]),
    Project(name="NHSII-demo_B",
        files=[
            File("demo_B1.fastq",PARTICIPANTS[2],"sample_B1","fastq"),
            File("demo_B2.fastq",PARTICIPANTS[2],"sample_B2","fastq"),
            File("demo_B3.fastq",PARTICIPANTS[3],"sample_B1","fastq"),
            File("demo_B4.fastq",PARTICIPANTS[3],"sample_B2","fastq"),
            File("demo_B1.tsv",PARTICIPANTS[2],"sample_B1","tsv", raw=False),
            File("demo_B2.tsv",PARTICIPANTS[2],"sample_B2","tsv", raw=False),
            File("demo_B3.tsv",PARTICIPANTS[3],"sample_B1","tsv", raw=False),
            File("demo_B4.tsv",PARTICIPANTS[3],"sample_B2","tsv", raw=False)
        ]),
    Project(name="NHSII-demo_C",
        files=[
            File("demo_C1.fastq",PARTICIPANTS[4],"sample_C1","fastq"),
            File("demo_C2.fastq",PARTICIPANTS[4],"sample_C2","fastq"),
            File("demo_C3.fastq",PARTICIPANTS[5],"sample_C1","fastq"),
            File("demo_C4.fastq",PARTICIPANTS[5],"sample_C2","fastq"),
            File("demo_C1.tsv",PARTICIPANTS[4],"sample_C1","tsv", raw=False),
            File("demo_C2.tsv",PARTICIPANTS[4],"sample_C2","tsv", raw=False),
            File("demo_C3.tsv",PARTICIPANTS[5],"sample_C1","tsv", raw=False),
            File("demo_C4.tsv",PARTICIPANTS[5],"sample_C2","tsv", raw=False)
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
