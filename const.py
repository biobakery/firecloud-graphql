
# This file holds constant variables

# Values from the const data structures (to be replaced by local database values next)

VERSION = {
  "commit": "abcde",
  "data_release": "Data Release 0.1 - February 18, 2019",
  "status": "OK",
  "tag": "0.1",
  "version": 0.1
}

class DB(object):
    def __init__(self):
        import schema
    

        self.CURRENT_FILE_SIZE = schema.FileSize(65000000000) # this is the total amount of files in repo table shown
        self.CURRENT_PROGRAMS = [schema.Program(name="NHSII")]

        self.DATA_CATEGORIES = [schema.DataCategories(case_count=2, data_category="Raw Reads"),
                               schema.DataCategories(case_count=2, data_category="Gene Families"),
                               schema.DataCategories(case_count=2, data_category="Taxonomic Profiles")]

        self.DATA_CATEGORIES_SINGLE_CASE = [schema.DataCategories(file_count=1, data_category="Raw Reads"),
                                           schema.DataCategories(file_count=1, data_category="Gene Families"),
                                           schema.DataCategories(file_count=1, data_category="Taxonomic Profiles")]

        self.EXPERIMENTAL_STRATEGIES = [schema.ExperimentalStrategies(file_count=6, experimental_strategy="WMGX"),
                                       schema.ExperimentalStrategies(file_count=6, experimental_strategy="16S")]

        self.CURRENT_PROJECTS = {
            "1":schema.Project(id="1", project_id="NHSII-DemoA", name="NHSII-DemoA", 
                               program=self.CURRENT_PROGRAMS[0], summary=schema.Summary(case_count=2, file_count=6, 
                               data_categories=self.DATA_CATEGORIES, experimental_strategies=[self.EXPERIMENTAL_STRATEGIES[0]], file_size=15), 
                               primary_site=["Stool"]),
            "2":schema.Project(id="2", project_id="NHSII-DemoB", name="NHSII-DemoB", 
                               program=self.CURRENT_PROGRAMS[0], summary=schema.Summary(case_count=2, file_count=6, 
                               data_categories=self.DATA_CATEGORIES, experimental_strategies=[self.EXPERIMENTAL_STRATEGIES[1]], file_size=15), 
                               primary_site=["Stool"]),
        } 

        self.CURRENT_FILE_CASES = {
            "1":schema.FileCase(1,"Case1",self.CURRENT_PROJECTS["1"],
                                schema.Demographic("not hispanic or latino","male","white"), "Stool"),
            "2":schema.FileCase(2,"Case2",self.CURRENT_PROJECTS["1"],
                                schema.Demographic("not hispanic or latino","male","white"), "Stool"),
            "3":schema.FileCase(3,"Case3",self.CURRENT_PROJECTS["2"],
                                schema.Demographic("not hispanic or latino","female","white"), "Stool"),
            "4":schema.FileCase(4,"Case4",self.CURRENT_PROJECTS["2"],
                                schema.Demographic("hispanic or latino","female","white"), "Stool")
        }

        self.CASE_FILES = {
        "1": schema.CaseFile(1,experimental_strategy="WMGX",
                             data_category="Raw Reads",data_format="Fastq",
                             platform="Illumina MiSeq",access="controlled"),
        "2": schema.CaseFile(2,experimental_strategy="WMGX",
                             data_category="Taxonomic Profile",data_format="TSV",
                             platform="Illumina MiSeq",access="open"),
        "3": schema.CaseFile(3,experimental_strategy="WMGX",
                             data_category="Gene Families",data_format="TSV",
                             platform="Illumina MiSeq",access="open"),
        "4": schema.CaseFile(4,experimental_strategy="WMGX",
                             data_category="Raw Reads",data_format="Fastq",
                             platform="Illumina MiSeq",access="controlled"),
        "5": schema.CaseFile(5,experimental_strategy="WMGX",
                             data_category="Taxonomic Profile",data_format="TSV",
                             platform="Illumina MiSeq",access="open"),
        "6": schema.CaseFile(6,experimental_strategy="WMGX",
                             data_category="Gene Families",data_format="TSV",
                             platform="Illumina MiSeq",access="open"),
        "7": schema.CaseFile(7,experimental_strategy="16S",
                             data_category="Raw Reads",data_format="Fastq",
                             platform="Illumina HiSeq",access="controlled"),
        "8": schema.CaseFile(8,experimental_strategy="16S",
                             data_category="Taxonomic Profile",data_format="TSV",
                             platform="Illumina HiSeq",access="open"),
        "9": schema.CaseFile(9,experimental_strategy="16S",
                             data_category="Gene Families",data_format="TSV",
                             platform="Illumina HiSeq",access="open"),
        "10": schema.CaseFile(10,experimental_strategy="16S",
                             data_category="Raw Reads",data_format="Fastq",
                             platform="Illumina HiSeq",access="controlled"),
        "11": schema.CaseFile(11,experimental_strategy="16S",
                             data_category="Taxonomic Profile",data_format="TSV",
                             platform="Illumina HiSeq",access="open"),
        "12": schema.CaseFile(12,experimental_strategy="16S",
                             data_category="Gene Families",data_format="TSV",
                             platform="Illumina HiSeq",access="open"),
        }

        self.FILE_SIZES = { "gene": 300000000, "raw": 5000000000, "taxa": 200000000 }

        self.TEST_FILES = {
        "1": schema.File(1, "demoA_sample1_raw_reads.fastq","case1","sample1", "controlled", 
                        self.FILE_SIZES["raw"], "Raw Reads", "Fastq", "Illumina MiSeq", "WMGX", 
                        "demoA_sample1_raw_reads.fastq", schema.FileCases(hits=[self.CURRENT_FILE_CASES["1"]])),
        "2": schema.File(2, "demoA_sample1_taxonomic_profile.tsv","case1","sample1", "open", 
                        self.FILE_SIZES["taxa"], "Taxonomic Profile", "TSV", "Illumina MiSeq", "WMGX", 
                        "demoA_sample1_taxonomic_profile.tsv", schema.FileCases(hits=[self.CURRENT_FILE_CASES["1"]])),
        "3": schema.File(3, "demoA_sample1_gene_families.tsv","case1","sample1", "open", 
                        self.FILE_SIZES["gene"], "Gene Families", "TSV", "Illumina MiSeq", "WMGX", 
                        "demoA_sample1_gene_families.tsv", schema.FileCases(hits=[self.CURRENT_FILE_CASES["1"]])),
        "4": schema.File(4, "demoA_sample2_raw_reads.fastq","case2","sample2", "controlled", 
                        self.FILE_SIZES["raw"], "Raw Reads", "Fastq", "Illumina MiSeq", "WMGX", 
                        "demoA_sample2_raw_reads.fastq", schema.FileCases(hits=[self.CURRENT_FILE_CASES["2"]])),
        "5": schema.File(5, "demoA_sample2_taxonomic_profile.tsv","case2","sample2", "open", 
                        self.FILE_SIZES["taxa"], "Taxonomic Profile", "TSV", "Illumina MiSeq", "WMGX", 
                        "demoA_sample2_taxonomic_profile.tsv", schema.FileCases(hits=[self.CURRENT_FILE_CASES["2"]])),
        "6": schema.File(6, "demoA_sample2_gene_families.tsv","case2","sample2", "open", 
                        self.FILE_SIZES["gene"], "Gene Families", "TSV", "Illumina MiSeq", "WMGX", 
                        "demoA_sample2_gene_families.tsv", schema.FileCases(hits=[self.CURRENT_FILE_CASES["2"]])),
        "7": schema.File(7, "demoB_sample3_raw_reads.fastq","case3","sample3", "controlled", 
                        self.FILE_SIZES["raw"], "Raw Reads", "Fastq", "Illumina HiSeq", "16S", 
                        "demoB_sample3_raw_reads.fastq", schema.FileCases(hits=[self.CURRENT_FILE_CASES["3"]])),
        "8": schema.File(8, "demoB_sample3_taxonomic_profile.tsv","case3","sample3", "open", 
                        self.FILE_SIZES["taxa"], "Taxonomic Profile", "TSV", "Illumina HiSeq","16S", 
                        "demoB_sample3_taxonomic_profile.tsv", schema.FileCases(hits=[self.CURRENT_FILE_CASES["3"]])),
        "9": schema.File(9, "demoB_sample3_gene_families.tsv","case3","sample3", "open",
                        self.FILE_SIZES["gene"], "Gene Families", "TSV", "Illumina HiSeq", "16S", 
                        "demoB_sample3_gene_families.tsv", schema.FileCases(hits=[self.CURRENT_FILE_CASES["3"]])),
        "10": schema.File(10, "demoB_sample4_raw_reads.fastq","case4","sample4", "controlled", 
                        self.FILE_SIZES["raw"], "Raw Reads", "Fastq", "Illumina HiSeq", "16S", 
                        "demoB_sample4_raw_reads.fastq", schema.FileCases(hits=[self.CURRENT_FILE_CASES["4"]])),
        "11": schema.File(11, "demoB_sample4_taxonomic_profile.tsv","case4","sample4", "open", 
                        self.FILE_SIZES["taxa"], "Taxonomic Profile", "TSV", "Illumina HiSeq", "16S", 
                        "demoB_sample4_taxonomic_profile.tsv", schema.FileCases(hits=[self.CURRENT_FILE_CASES["4"]])),
        "12": schema.File(12, "demoB_sample4_gene_families.tsv","case4","sample4", "open", 
                        self.FILE_SIZES["gene"], "Gene Families", "TSV", "Illumina HiSeq", "16S", 
                        "demoB_sample4_gene_families.tsv", schema.FileCases(hits=[self.CURRENT_FILE_CASES["4"]])),
        }

        self.CURRENT_COUNTS = schema.Count(
            projects="2",
            participants="4",
            samples="4",
            dataFormats="3",
            rawFiles="4",
            processedFiles="8"
        )

        self.TEST_CASES={"1":schema.Case(1,case_id="Case1",primary_site="Stool",
                    demographic=schema.Demographic("not hispanic or latino","male","white"),
                    project=self.CURRENT_PROJECTS["1"],
                    summary=schema.Summary(case_count=1,file_count=1,file_size=1,
                        data_categories=self.DATA_CATEGORIES_SINGLE_CASE),
                    files=schema.CaseFiles(hits=[self.CASE_FILES["1"],self.CASE_FILES["2"],self.CASE_FILES["3"]])), 
                "2":schema.Case(2,case_id="Case2",primary_site="Stool",
                    demographic=schema.Demographic("not hispanic or latino","male","white"),
                    project=self.CURRENT_PROJECTS["1"],
                    summary=schema.Summary(case_count=1,file_count=1,file_size=1,
                        data_categories=self.DATA_CATEGORIES_SINGLE_CASE),
                    files=schema.CaseFiles(hits=[self.CASE_FILES["4"],self.CASE_FILES["5"],self.CASE_FILES["6"]])), 
                "3":schema.Case(3,case_id="Case3",primary_site="Stool",
                    demographic=schema.Demographic("not hispanic or latino","female","white"),
                    project=self.CURRENT_PROJECTS["2"],
                    summary=schema.Summary(case_count=1,file_count=1,file_size=1,
                        data_categories=self.DATA_CATEGORIES_SINGLE_CASE),
                    files=schema.CaseFiles(hits=[self.CASE_FILES["7"],self.CASE_FILES["8"],self.CASE_FILES["9"]])), 
                "4":schema.Case(4,case_id="Case4",primary_site="Stool",
                    demographic=schema.Demographic("hispanic or latino","female","white"),
                    project=self.CURRENT_PROJECTS["2"],
                    summary=schema.Summary(case_count=1,file_count=1,file_size=1,
                        data_categories=self.DATA_CATEGORIES_SINGLE_CASE),
                    files=schema.CaseFiles(hits=[self.CASE_FILES["10"],self.CASE_FILES["11"],self.CASE_FILES["12"]]))
        }

        self.CURRENT_FILES = schema.Files(hits=self.TEST_FILES.keys())
        self.CURRENT_CASES = schema.RepositoryCases(hits=self.TEST_CASES.keys())

