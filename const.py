
# This file holds constant variables

VERSION = {
  "commit": "abcde",
  "data_release": "Data Release 0.1 - January 17, 2019",
  "status": "OK",
  "tag": "0.1",
  "version": 0.1
}


ROOT_PROJECTS = {
  "data": {
    "viewer": {
      "projects": {
        "_aggregationsEJDan": {
          "primary_site": {
            "buckets": [
              {
                "doc_count": 45,
                "key": "Stool"
              }
            ]
          },
          "program__name": {
            "buckets": [
              {
                "doc_count": 45,
                "key": "NHSII"
              }
            ]
          },
          "project_id": {
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
          },
          "summary__data_categories__data_category": {
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
              }
            ]
          },
          "summary__experimental_strategies__experimental_strategy": {
            "buckets": [
              {
                "doc_count": 30,
                "key": "WXS"
              },
              {
                "doc_count": 15,
                "key": "16S"
              }
            ]
          }
        }
      }
    }
  }
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


# GenesAndCases
GENES_CASES = {
  "data": {
    "viewer": {
      "explore": {
        "cases": {
          "hits": {
            "total": 10202
          }
        },
        "genes": {
          "hits": {
            "edges": [
              {
                "node": {
                  "allCases": {
                    "hits": {
                      "total": 4334
                    }
                  },
                  "filteredCases": {
                    "hits": {
                      "total": 3609
                    }
                  },
                  "gene_id": "ENSG00000141510",
                  "id": "R2VuZTpFTlNHMDAwMDAxNDE1MTAjNWE0ZjJhZTRiNTg5NmFiNThiNzJiNDkxN2JmNzFjMTkj",
                  "score": 3609,
                  "symbol": "TP53"
                }
              },
              {
                "node": {
                  "allCases": {
                    "hits": {
                      "total": 2736
                    }
                  },
                  "filteredCases": {
                    "hits": {
                      "total": 1320
                    }
                  },
                  "gene_id": "ENSG00000121879",
                  "id": "R2VuZTpFTlNHMDAwMDAxMjE4NzkjNWE0ZjJhZTRiNTg5NmFiNThiNzJiNDkxN2JmNzFjMTkj",
                  "score": 1320,
                  "symbol": "PIK3CA"
                }
              },
              {
                "node": {
                  "allCases": {
                    "hits": {
                      "total": 1663
                    }
                  },
                  "filteredCases": {
                    "hits": {
                      "total": 941
                    }
                  },
                  "gene_id": "ENSG00000167548",
                  "id": "R2VuZTpFTlNHMDAwMDAxNjc1NDgjNWE0ZjJhZTRiNTg5NmFiNThiNzJiNDkxN2JmNzFjMTkj",
                  "score": 941,
                  "symbol": "KMT2D"
                }
              },
            ],
            "total": 573
          }
        }
      }
    }
  }
}

# ProjectsTable
PROJECT_TABLE = {
  "data": {
    "viewer": {
      "projects": {
        "hits": {
          "edges": [
            {
              "node": {
                "id": "UHJvamVjdDpGTS1BRA==",
                "primary_site": [
                  "Stool",
                ],
                "program": {
                  "name": "NHSII"
                },
                "project_id": "NHSII-DemoA",
                "summary": {
                  "case_count": 5,
                  "data_categories": [
                    {
                      "case_count": 5,
                      "data_category": "Raw Reads"
                    },
                    {
                      "case_count": 5,
                      "data_category": "Gene Families"
                    },
                    {
                      "case_count": 5,
                      "data_category": "Taxonomic Profiles"
                    }
                  ],
                  "file_count": 15,
                  "file_size": 100
                }
              }
            },
            {
              "node": {
                "id": "UHJvamVjdDpGTS1DDA==",
                "primary_site": [
                  "Stool",
                ],
                "program": {
                  "name": "NHSII"
                },
                "project_id": "NHSII-DemoB",
                "summary": {
                  "case_count": 5,
                  "data_categories": [
                    {
                      "case_count": 5,
                      "data_category": "Raw Reads"
                    },
                    {
                      "case_count": 5,
                      "data_category": "Gene Families"
                    },
                    {
                      "case_count": 5,
                      "data_category": "Taxonomic Profiles"
                    }
                  ],
                  "file_count": 15,
                  "file_size": 100
                }
              }
            },
            {
              "node": {
                "id": "UHJvamVjdDpGTS1CDS==",
                "primary_site": [
                  "Stool",
                ],
                "program": {
                  "name": "NHSII"
                },
                "project_id": "NHSII-DemoC",
                "summary": {
                  "case_count": 5,
                  "data_categories": [
                    {
                      "case_count": 5,
                      "data_category": "Raw Reads"
                    },
                    {
                      "case_count": 5,
                      "data_category": "Gene Families"
                    },
                    {
                      "case_count": 5,
                      "data_category": "Taxonomic Profiles"
                    }
                  ],
                  "file_count": 15,
                  "file_size": 100
                }
              }
            },
          ],
          "total": 3
        }
      }
    }
  }
}

# ProjectsCharts
PROJECT_CHARTS = {
  "data": {
    "projectsViewer": {
      "projects": {
        "hits": {
          "edges": [
            {
              "node": {
                "id": "1",
                "name": "NHSII-DemoA",
                "program": {
                  "name": "NHSII"
                },
                "project_id": "NHSII-DemoA",
                "summary": {
                  "case_count": 5,
                  "file_count": 15
                }
              }
            },
            {
              "node": {
                "id": "2",
                "name": "NHSII-DemoB",
                "program": {
                  "name": "NHSII"
                },
                "project_id": "NHSII-DemoB",
                "summary": {
                  "case_count": 5,
                  "file_count": 15
                }
              }
            },
            {
              "node": {
                "id": "3",
                "name": "NHSII-DemoC",
                "program": {
                  "name": "NHSII"
                },
                "project_id": "NHSII-DemoC",
                "summary": {
                  "case_count": 5,
                  "file_count": 15
                }
              }
            },
          ],
          "total": 3
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

# generate temp files list

FILE_NODE_TEMPLATE = """{
                "node": {
                  "access": "$access",
                  "cases": {
                    "hits": {
                      "edges": [ { "node": $project ],
                      "total": 1
                    }
                  },
                  "data_category": "$cat",
                  "data_format": "$format",
                  "experimental_strategy": "$exp",
                  "file_id": "$id",
                  "file_name": "$name",
                  "file_size": $size,
                  "id": "$id",
                  "platform": "$plat",
                }
              },"""

FILES = ""

from string import Template

temp = Template(FILE_NODE_TEMPLATE)

sample = 1
sample_names = [1,1,1,2,2,2,3,3,3,4,4,4,5,5,5]
for i in range(1, 46):
    if i > 15 and i <= 30:
        demo = "demoB"
        project = """{ "case_id": "2", "id": "2", "project": { "id": "2", "project_id": "NHSII-DemoB" } } }"""
        exp = "WMGX"
        platform = "Illumina MiSeq"
    elif i > 30:
        demo = "demoC"
        project = """{ "case_id": "3", "id": "3", "project": { "id": "3", "project_id": "NHSII-DemoC" } } }"""
        exp = "WMGX"
        platform = "Illumina HiSeq"
    else:
        demo = "demoA"
        project = """{ "case_id": "1", "id": "1", "project": { "id": "1", "project_id": "NHSII-DemoA" } } }"""
        exp = "WMGX"
        platform = "Illumina HiSeq"
  
    if sample > 15:
        sample = 1

    if sample in [1,4,7,10,13]:
       FILES+= temp.substitute(cat="Gene Families", format="TSV", exp=exp, project=project, access="open",
           id=str(i), name=demo+"_sample"+str(sample_names[sample-1])+"_gene_families.tsv", size="300000000", plat=platform)
    elif sample in [2,5,8,11,14]:
       FILES+= temp.substitute(cat="Taxonomic Profile", format="TSV", exp=exp, project=project, access="open",
           id=str(i), name=demo+"_sample"+str(sample_names[sample-1])+"_taxonomic_profile.tsv", size="200000000", plat=platform)
    else:
       FILES+= temp.substitute(cat="Raw Reads", format="Fastq", exp=exp, project=project, access="controlled",
           id=str(i), name=demo+"_sample"+str(sample_names[sample-1])+"_raw_reads.fastq.gz", size="5000000000", plat=platform)

    sample +=1


import ast

FILES_LIT = ast.literal_eval(FILES)

FILE_TABLE = {
  "data": {
    "viewer": {
      "repository": {
        "files": {
          "hits": {
            "edges":  FILES_LIT ,
             "total" : "45"
             }
           }
         }
       }
    }
 }

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



