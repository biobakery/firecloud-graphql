
# This file holds constant variables

VERSION = {
  "commit": "abcde",
  "data_release": "Data Release 0.1 - February 18, 2019",
  "status": "OK",
  "tag": "0.1",
  "version": 0.1
}

# First value is total sum of all file sizes

ROOT_REPOS = {
  "data": {
    "viewer": {
      "cart_summary": {
        "_aggregations1TAxVJ": {
          "fs": {
            "value": 65000000000
          }
        }
      },
      "repository": {
        "cases": {
          "_aggregations2LbddX": {
            "demographic__ethnicity": {
              "buckets": [
                {
                  "doc_count": 30,
                  "key": "not hispanic or latino"
                },
                {
                  "doc_count": 15,
                  "key": "hispanic or latino"
                },
              ]
            },
            "demographic__gender": {
              "buckets": [
                {
                  "doc_count": 15,
                  "key": "female"
                },
                {
                  "doc_count": 30,
                  "key": "male"
                },
              ]
            },
            "demographic__race": {
              "buckets": [
                {
                  "doc_count": 15,
                  "key": "white"
                },
                {
                  "doc_count": 15,
                  "key": "asian"
                },
                {
                  "doc_count": 15,
                  "key": "other"
                },
              ]
            },
            "primary_site": {
              "buckets": [
                {
                  "doc_count": 45,
                  "key": "Stool"
                },
              ]
            },
            "project__program__name": {
              "buckets": [
                {
                  "doc_count": 45,
                  "key": "NHSII"
                },
              ]
            },
            "project__project_id": {
              "buckets": [
                {
                  "doc_count": 15,
                  "key": "NHSII-DemoA"
                },
                {
                  "doc_count": 15,
                  "key": "NHSII-DemoB"
                },
                {
                  "doc_count": 15,
                  "key": "NHSII-DemoC"
                },
              ]
            }
          },
          "_hits1ATaID": {
            "total": 15
          }
        },
        "files": {
          "_aggregations2LbddX": {
            "access": {
              "buckets": [
                {
                  "doc_count": 30,
                  "key": "open"
                },
                {
                  "doc_count": 15,
                  "key": "controlled"
                }
              ]
            },
            "cases__primary_site": {
              "buckets": [
                {
                  "doc_count": 45,
                  "key": "Stool"
                },
              ]
            },
            "cases__project__project_id": {
              "buckets": [
                {
                  "doc_count": 15,
                  "key": "NHSII-DemoA"
                },
                {
                  "doc_count": 15,
                  "key": "NHSII-DemoB"
                },
                {
                  "doc_count": 15,
                  "key": "NHSII-DemoC"
                },
              ]
            },
            "data_category": {
              "buckets": [
                {
                  "doc_count": 15,
                  "key": "Raw Reads"
                },
                {
                  "doc_count": 15,
                  "key": "Gene Families"
                },
                {
                  "doc_count": 15,
                  "key": "Taxonomic Profiles"
                },
              ]
            },
            "data_format": {
              "buckets": [
                {
                  "doc_count": 30,
                  "key": "TSV"
                },
                {
                  "doc_count": 15,
                  "key": "Fastq"
                },
              ]
            },
            "experimental_strategy": {
              "buckets": [
                {
                  "doc_count": 30,
                  "key": "WMGS"
                },
                {
                  "doc_count": 15,
                  "key": "16S"
                },
              ]
            }
          },
          "_hits2bK9cM": {
            "total": 45
          }
        }
      }
    }
  }
}


CASE_AGGREGATIONS = {
  "data": {
    "viewer": {
      "repository": {
        "cases": {
          "aggregations": {
            "demographic__ethnicity": {
              "buckets": [
                {
                  "doc_count": 30,
                  "key": "not hispanic or latino"
                },
                {
                  "doc_count": 15,
                  "key": "hispanic or latino"
                },
              ]
            },
            "demographic__gender": {
              "buckets": [
                {
                  "doc_count": 15,
                  "key": "female"
                },
                {
                  "doc_count": 30,
                  "key": "male"
                },
              ]
            },
            "demographic__race": {
              "buckets": [
                {
                  "doc_count": 15,
                  "key": "white"
                },
                {
                  "doc_count": 15,
                  "key": "asian"
                },
                {
                  "doc_count": 15,
                  "key": "other"
                },
              ]
            },
            "primary_site": {
              "buckets": [
                {
                  "doc_count": 45,
                  "key": "Stool"
                },
              ]
            },
            "project__program__name": {
              "buckets": [
                {
                  "doc_count": 45,
                  "key": "NHSII"
                },
              ]
            },
            "project__project_id": {
              "buckets": [
                {
                  "doc_count": 15,
                  "key": "NHSII-DemoA"
                },
                {
                  "doc_count": 15,
                  "key": "NHSII-DemoB"
                },
                {
                  "doc_count": 15,
                  "key": "NHSII-DemoC"
                }
              ]
            }
          },
          "facets": 'null'
        }
      }
    }
  }
}

FILE_AGGREGATIONS = {
  "data": {
    "viewer": {
      "repository": {
        "files": {
          "aggregations": {
            "access": {
              "buckets": [
                {
                  "doc_count": 30,
                  "key": "open"
                },
                {
                  "doc_count": 15,
                  "key": "controlled"
                }
              ]
            },
            "data_category": {
              "buckets": [
                {
                  "doc_count": 15,
                  "key": "Raw Reads"
                },
                {
                  "doc_count": 15,
                  "key": "Gene Families"
                },
                {
                  "doc_count": 15,
                  "key": "Taxonomic Profiles"
                },
              ]
            },
            "data_format": {
              "buckets": [
                {
                  "doc_count": 15,
                  "key": "Fastq"
                },
                {
                  "doc_count": 30,
                  "key": "TSV"
                },
              ]
            },
            "experimental_strategy": {
              "buckets": [
                {
                  "doc_count": 30,
                  "key": "WXS"
                },
                {
                  "doc_count": 15,
                  "key": "16S"
                },
              ]
            },
            "platform": {
              "buckets": [
                {
                  "doc_count": 30,
                  "key": "Illumina HiSeq"
                },
                {
                  "doc_count": 15,
                  "key": "Illumina MiSeq"
                },
              ]
            }
          },
          "facets": 'null'
        }
      }
    }
  }
}

from string import Template
import ast

TEMP_CASE_TEMPLATE = """{
                "node": {
                  "annotations": { "hits": { "edges": [ { "node": { "annotation_id": "$id", "id": "$id" } } ],
                   "total": 1
                    }
                  },
                  "case_id": "$case",
                  "demographic": { "ethnicity": "not hispanic or latino", "gender": "$gender", "race": "white" },
                  "id": "$case",
                  "primary_site": "Stool",
                  "project": { "id": "$projectid", "program": { "name": "NHSII" }, "project_id": "$project" },
                  "submitter_id": "$case",
                  "summary": {
                    "data_categories": [ { "data_category": "Raw Reads", "file_count": 1 },
                                         { "data_category": "Gene Families", "file_count": 1 },
                                         { "data_category": "Taxonomic Profile", "file_count": 1 }
                                       ],
                    "file_count": 3
                  }
                }
              }, """


temp_cases = Template(TEMP_CASE_TEMPLATE)

FILL_CASES = ""

case = 1
for i in range(1, 16):
    if i > 5 and i <= 10:
        project = "NHSII-DemoB"
        project_id = 2
        gender = "male"
    elif i > 10:
        project = "NHSII-DemoC"
        project_id = 3
        gender = "female"
    else:
        project = "NHSII-DemoA"
        project_id = 1
        gender = "male"

    if case > 5:
        case = 1

    FILL_CASES += temp_cases.substitute(id=str(i), project=project, case="Case"+str(case)+project[-1], projectid=project_id, gender=gender)

    case +=1


import ast

CASES_LIT = ast.literal_eval(FILL_CASES)

CASES_TABLE = {
  "data": {
    "viewer": {
      "repository": {
        "cases": {
          "hits": {
            "edges": CASES_LIT ,
            "total": 15
          }
        }
      }
    }
  }
}



