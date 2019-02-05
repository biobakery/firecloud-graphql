
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
          "disease_type": {
            "buckets": [
              {
                "doc_count": 19,
                "key": "Adenomas and Adenocarcinomas"
              },
              {
                "doc_count": 12,
                "key": "Cystic, Mucinous and Serous Neoplasms"
              },
              {
                "doc_count": 8,
                "key": "Epithelial Neoplasms, NOS"
              },
            ]
          },
          "primary_site": {
            "buckets": [
              {
                "doc_count": 8,
                "key": "Kidney"
              },
              {
                "doc_count": 5,
                "key": "Bronchus and lung"
              },
              {
                "doc_count": 5,
                "key": "Colon"
              },
              {
                "doc_count": 5,
                "key": "Heart, mediastinum, and pleura"
              },
            ]
          },
          "program__name": {
            "buckets": [
              {
                "doc_count": 33,
                "key": "TCGA"
              },
              {
                "doc_count": 6,
                "key": "TARGET"
              },
              {
                "doc_count": 1,
                "key": "CTSP"
              },
            ]
          },
          "project_id": {
            "buckets": [
              {
                "doc_count": 1,
                "key": "CTSP-DLBCL1"
              },
              {
                "doc_count": 1,
                "key": "FM-AD"
              },
              {
                "doc_count": 1,
                "key": "NCICCR-DLBCL"
              },
            ]
          },
          "summary__data_categories__data_category": {
            "buckets": [
              {
                "doc_count": 41,
                "key": "Sequencing Reads"
              },
              {
                "doc_count": 40,
                "key": "Biospecimen"
              },
              {
                "doc_count": 40,
                "key": "Clinical"
              },
              {
                "doc_count": 37,
                "key": "Simple Nucleotide Variation"
              },
            ]
          },
          "summary__experimental_strategies__experimental_strategy": {
            "buckets": [
              {
                "doc_count": 38,
                "key": "WXS"
              },
              {
                "doc_count": 37,
                "key": "RNA-Seq"
              },
              {
                "doc_count": 36,
                "key": "miRNA-Seq"
              },
              {
                "doc_count": 33,
                "key": "Genotyping Array"
              },
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
            "value": 650606999096554.0
          }
        }
      },
      "repository": {
        "cases": {
          "_aggregations2LbddX": {
            "demographic__ethnicity": {
              "buckets": [
                {
                  "doc_count": 21424,
                  "key": "not reported"
                },
                {
                  "doc_count": 10436,
                  "key": "not hispanic or latino"
                },
                {
                  "doc_count": 779,
                  "key": "hispanic or latino"
                },
                {
                  "doc_count": 163,
                  "key": "Unknown"
                }
              ]
            },
            "demographic__gender": {
              "buckets": [
                {
                  "doc_count": 17700,
                  "key": "female"
                },
                {
                  "doc_count": 15087,
                  "key": "male"
                },
                {
                  "doc_count": 10,
                  "key": "unknown"
                },
                {
                  "doc_count": 5,
                  "key": "not reported"
                }
              ]
            },
            "demographic__race": {
              "buckets": [
                {
                  "doc_count": 20156,
                  "key": "not reported"
                },
                {
                  "doc_count": 10381,
                  "key": "white"
                },
                {
                  "doc_count": 1336,
                  "key": "black or african american"
                },
                {
                  "doc_count": 789,
                  "key": "asian"
                },
                {
                  "doc_count": 74,
                  "key": "other"
                },
                {
                  "doc_count": 37,
                  "key": "american indian or alaska native"
                },
                {
                  "doc_count": 29,
                  "key": "native hawaiian or other pacific islander"
                }
              ]
            },
            "diagnoses__vital_status": {
              "buckets": [
                {
                  "doc_count": 18032,
                  "key": "not reported"
                },
                {
                  "doc_count": 9967,
                  "key": "alive"
                },
                {
                  "doc_count": 4767,
                  "key": "dead"
                },
                {
                  "doc_count": 36,
                  "key": "unknown"
                }
              ]
            },
            "disease_type": {
              "buckets": [
                {
                  "doc_count": 12492,
                  "key": "Adenomas and Adenocarcinomas"
                },
                {
                  "doc_count": 3202,
                  "key": "Epithelial Neoplasms, NOS"
                },
                {
                  "doc_count": 3025,
                  "key": "Ductal and Lobular Neoplasms"
                },
                {
                  "doc_count": 2635,
                  "key": "Squamous Cell Neoplasms"
                },
              ]
            },
            "primary_site": {
              "buckets": [
                {
                  "doc_count": 4866,
                  "key": "Bronchus and lung"
                },
                {
                  "doc_count": 3682,
                  "key": "Breast"
                },
                {
                  "doc_count": 2301,
                  "key": "Colon"
                },
                {
                  "doc_count": 2091,
                  "key": "Kidney"
                },
              ]
            },
            "project__program__name": {
              "buckets": [
                {
                  "doc_count": 18004,
                  "key": "FM"
                },
                {
                  "doc_count": 11315,
                  "key": "TCGA"
                },
                {
                  "doc_count": 3236,
                  "key": "TARGET"
                },
                {
                  "doc_count": 489,
                  "key": "NCICCR"
                },
                {
                  "doc_count": 45,
                  "key": "CTSP"
                },
                {
                  "doc_count": 7,
                  "key": "VAREPOP"
                }
              ]
            },
            "project__project_id": {
              "buckets": [
                {
                  "doc_count": 18004,
                  "key": "FM-AD"
                },
                {
                  "doc_count": 1127,
                  "key": "TARGET-NBL"
                },
                {
                  "doc_count": 1098,
                  "key": "TCGA-BRCA"
                },
                {
                  "doc_count": 988,
                  "key": "TARGET-AML"
                },
                {
                  "doc_count": 652,
                  "key": "TARGET-WT"
                },
              ]
            }
          },
          "_hits1ATaID": {
            "total": 33096
          }
        },
        "files": {
          "_aggregations2LbddX": {
            "access": {
              "buckets": [
                {
                  "doc_count": 183549,
                  "key": "open"
                },
                {
                  "doc_count": 175130,
                  "key": "controlled"
                }
              ]
            },
            "cases__primary_site": {
              "buckets": [
                {
                  "doc_count": 39977,
                  "key": "Bronchus and lung"
                },
                {
                  "doc_count": 36745,
                  "key": "Breast"
                },
                {
                  "doc_count": 26803,
                  "key": "Brain"
                },
              ]
            },
            "cases__project__project_id": {
              "buckets": [
                {
                  "doc_count": 36134,
                  "key": "FM-AD"
                },
                {
                  "doc_count": 31524,
                  "key": "TCGA-BRCA"
                },
                {
                  "doc_count": 17052,
                  "key": "TCGA-LUAD"
                },
                {
                  "doc_count": 16174,
                  "key": "TCGA-UCEC"
                },
                {
                  "doc_count": 15289,
                  "key": "TCGA-HNSC"
                },
              ]
            },
            "data_category": {
              "buckets": [
                {
                  "doc_count": 127390,
                  "key": "Simple Nucleotide Variation"
                },
                {
                  "doc_count": 58047,
                  "key": "Transcriptome Profiling"
                },
                {
                  "doc_count": 55224,
                  "key": "Biospecimen"
                },
                {
                  "doc_count": 47437,
                  "key": "Sequencing Reads"
                },
                {
                  "doc_count": 45291,
                  "key": "Copy Number Variation"
                },
                {
                  "doc_count": 12496,
                  "key": "Clinical"
                },
                {
                  "doc_count": 12359,
                  "key": "DNA Methylation"
                },
                {
                  "doc_count": 435,
                  "key": "Combined Nucleotide Variation"
                }
              ]
            },
            "data_format": {
              "buckets": [
                {
                  "doc_count": 127507,
                  "key": "VCF"
                },
                {
                  "doc_count": 115697,
                  "key": "TXT"
                },
                {
                  "doc_count": 47437,
                  "key": "BAM"
                },
                {
                  "doc_count": 30072,
                  "key": "SVS"
                },
              ]
            },
            "data_type": {
              "buckets": [
                {
                  "doc_count": 63536,
                  "key": "Annotated Somatic Mutation"
                },
                {
                  "doc_count": 63536,
                  "key": "Raw Simple Somatic Mutation"
                },
                {
                  "doc_count": 47437,
                  "key": "Aligned Reads"
                },
                {
                  "doc_count": 34713,
                  "key": "Gene Expression Quantification"
                },
                {
                  "doc_count": 30072,
                  "key": "Slide Image"
                },
              ]
            },
            "experimental_strategy": {
              "buckets": [
                {
                  "doc_count": 114727,
                  "key": "WXS"
                },
                {
                  "doc_count": 46317,
                  "key": "RNA-Seq"
                },
                {
                  "doc_count": 45291,
                  "key": "Genotyping Array"
                },
                {
                  "doc_count": 36587,
                  "key": "Targeted Sequencing"
                },
              ]
            }
          },
          "_hits2bK9cM": {
            "total": 358679
          }
        }
      }
    }
  }
}

PROJECTS = {
  "data": {
    "viewer": {
      "explore": {
        "genes": {
          "hits": {
            "total": "200"
          }
        },
        "ssms": {
          "hits": {
            "total": "300"
          }
        }
      },
      "projects": {
        "aggregations": {
          "primary_site": {
            "buckets": [
              {
                "key": "Kidney"
              },
              {
                "key": "Bronchus and lung"
              },
            ]
          }
        },
        "hits": {
          "total": "40"
        }
      },
      "repository": {
        "cases": {
          "hits": {
            "total": "100"
          }
        },
        "files": {
          "hits": {
            "total": "500"
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
                "disease_type": [
                  "Germ Cell Neoplasms",
                  "Acinar Cell Neoplasms",
                ],
                "id": "UHJvamVjdDpGTS1BRA==",
                "primary_site": [
                  "Testis",
                  "Gallbladder",
                  "Unknown",
                ],
                "program": {
                  "name": "FM"
                },
                "project_id": "FM-AD",
                "summary": {
                  "case_count": 18004.0,
                  "data_categories": [
                    {
                      "case_count": 18004.0,
                      "data_category": "Simple Nucleotide Variation"
                    },
                    {
                      "case_count": 18004.0,
                      "data_category": "Clinical"
                    },
                    {
                      "case_count": 18004.0,
                      "data_category": "Biospecimen"
                    }
                  ],
                  "file_count": 36134.0,
                  "file_size": 188564761.0
                }
              }
            },
            {
              "node": {
                "disease_type": [
                  "Neuroblastoma"
                ],
                "id": "UHJvamVjdDpUQVJHRVQtTkJM",
                "primary_site": [
                  "Nervous System"
                ],
                "program": {
                  "name": "TARGET"
                },
                "project_id": "TARGET-NBL",
                "summary": {
                  "case_count": 1127.0,
                  "data_categories": [
                    {
                      "case_count": 216.0,
                      "data_category": "Simple Nucleotide Variation"
                    },
                    {
                      "case_count": 277.0,
                      "data_category": "Sequencing Reads"
                    },
                    {
                      "case_count": 152.0,
                      "data_category": "Transcriptome Profiling"
                    },
                  ],
                  "file_count": 2809.0,
                  "file_size": 11301459288767.0
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
                "disease_type": [
                  "Germ Cell Neoplasms",
                  "Acinar Cell Neoplasms",
                  "Miscellaneous Tumors",
                  "Thymic Epithelial Neoplasms",
                  "Gliomas",
                ],
                "id": "UHJvamVjdDpGTS1BRA==",
                "name": "Foundation Medicine Adult Cancer Clinical Dataset (FM-AD)",
                "primary_site": [
                  "Testis",
                  "Gallbladder",
                  "Unknown",
                  "Other and unspecified parts of biliary tract",
                  "Adrenal gland",
                  "Thyroid gland",
                ],
                "program": {
                  "name": "FM"
                },
                "project_id": "FM-AD",
                "summary": {
                  "case_count": 18004.0,
                  "data_categories": [
                    {
                      "case_count": 18004.0,
                      "data_category": "Simple Nucleotide Variation"
                    },
                    {
                      "case_count": 18004.0,
                      "data_category": "Clinical"
                    },
                    {
                      "case_count": 18004.0,
                      "data_category": "Biospecimen"
                    }
                  ],
                  "file_count": 36134.0
                }
              }
            },
            {
              "node": {
                "disease_type": [
                  "Neuroblastoma"
                ],
                "id": "UHJvamVjdDpUQVJHRVQtTkJM",
                "name": "Neuroblastoma",
                "primary_site": [
                  "Nervous System"
                ],
                "program": {
                  "name": "TARGET"
                },
                "project_id": "TARGET-NBL",
                "summary": {
                  "case_count": 1127.0,
                  "data_categories": [
                    {
                      "case_count": 216.0,
                      "data_category": "Simple Nucleotide Variation"
                    },
                    {
                      "case_count": 277.0,
                      "data_category": "Sequencing Reads"
                    },
                    {
                      "case_count": 152.0,
                      "data_category": "Transcriptome Profiling"
                    },
                    {
                      "case_count": 1127.0,
                      "data_category": "Biospecimen"
                    },
                    {
                      "case_count": 1127.0,
                      "data_category": "Clinical"
                    }
                  ],
                  "file_count": 2809.0
                }
              }
            },
            {
              "node": {
                "disease_type": [
                  "Adnexal and Skin Appendage Neoplasms",
                  "Basal Cell Neoplasms",
                  "Adenomas and Adenocarcinomas",
                  "Cystic, Mucinous and Serous Neoplasms",
                  "Epithelial Neoplasms, NOS",
                  "Squamous Cell Neoplasms",
                  "Fibroepithelial Neoplasms",
                  "Ductal and Lobular Neoplasms",
                  "Complex Epithelial Neoplasms"
                ],
                "id": "UHJvamVjdDpUQ0dBLUJSQ0E=",
                "name": "Breast Invasive Carcinoma",
                "primary_site": [
                  "Breast"
                ],
                "program": {
                  "name": "TCGA"
                },
                "project_id": "TCGA-BRCA",
                "summary": {
                  "case_count": 1098.0,
                  "data_categories": [
                    {
                      "case_count": 1097.0,
                      "data_category": "Transcriptome Profiling"
                    },
                    {
                      "case_count": 1098.0,
                      "data_category": "Copy Number Variation"
                    },
                    {
                      "case_count": 1044.0,
                      "data_category": "Simple Nucleotide Variation"
                    },
                    {
                      "case_count": 1095.0,
                      "data_category": "DNA Methylation"
                    },
                    {
                      "case_count": 1098.0,
                      "data_category": "Clinical"
                    },
                    {
                      "case_count": 1098.0,
                      "data_category": "Sequencing Reads"
                    },
                    {
                      "case_count": 1098.0,
                      "data_category": "Biospecimen"
                    }
                  ],
                  "file_count": 31524.0
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
                  "doc_count": 21424,
                  "key": "not reported"
                },
                {
                  "doc_count": 10436,
                  "key": "not hispanic or latino"
                },
                {
                  "doc_count": 779,
                  "key": "hispanic or latino"
                },
                {
                  "doc_count": 163,
                  "key": "Unknown"
                }
              ]
            },
            "demographic__gender": {
              "buckets": [
                {
                  "doc_count": 17700,
                  "key": "female"
                },
                {
                  "doc_count": 15087,
                  "key": "male"
                },
                {
                  "doc_count": 10,
                  "key": "unknown"
                },
                {
                  "doc_count": 5,
                  "key": "not reported"
                }
              ]
            },
            "demographic__race": {
              "buckets": [
                {
                  "doc_count": 10381,
                  "key": "white"
                },
                {
                  "doc_count": 1336,
                  "key": "black or african american"
                },
                {
                  "doc_count": 789,
                  "key": "asian"
                },
                {
                  "doc_count": 74,
                  "key": "other"
                },
                {
                  "doc_count": 37,
                  "key": "american indian or alaska native"
                },
                {
                  "doc_count": 29,
                  "key": "native hawaiian or other pacific islander"
                }
              ]
            },
            "diagnoses__age_at_diagnosis": {
              "stats": {
                "count": 32677,
                "max": 32872.0,
                "min": 0.0
              }
            },
            "diagnoses__days_to_death": {
              "stats": {
                "count": 4198,
                "max": 10870.0,
                "min": 0.0
              }
            },
            "diagnoses__vital_status": {
              "buckets": [
                {
                  "doc_count": 18032,
                  "key": "not reported"
                },
                {
                  "doc_count": 9967,
                  "key": "alive"
                },
                {
                  "doc_count": 4767,
                  "key": "dead"
                },
                {
                  "doc_count": 36,
                  "key": "unknown"
                }
              ]
            },
            "disease_type": {
              "buckets": [
                {
                  "doc_count": 12492,
                  "key": "Adenomas and Adenocarcinomas"
                },
                {
                  "doc_count": 3202,
                  "key": "Epithelial Neoplasms, NOS"
                },
                {
                  "doc_count": 3025,
                  "key": "Ductal and Lobular Neoplasms"
                },
                {
                  "doc_count": 2635,
                  "key": "Squamous Cell Neoplasms"
                }
              ]
            },
            "primary_site": {
              "buckets": [
                {
                  "doc_count": 4866,
                  "key": "Bronchus and lung"
                },
                {
                  "doc_count": 3682,
                  "key": "Breast"
                },
                {
                  "doc_count": 2301,
                  "key": "Colon"
                },
                {
                  "doc_count": 2091,
                  "key": "Kidney"
                }
              ]
            },
            "project__program__name": {
              "buckets": [
                {
                  "doc_count": 18004,
                  "key": "FM"
                },
                {
                  "doc_count": 11315,
                  "key": "TCGA"
                },
                {
                  "doc_count": 3236,
                  "key": "TARGET"
                },
                {
                  "doc_count": 489,
                  "key": "NCICCR"
                },
                {
                  "doc_count": 45,
                  "key": "CTSP"
                },
                {
                  "doc_count": 7,
                  "key": "VAREPOP"
                }
              ]
            },
            "project__project_id": {
              "buckets": [
                {
                  "doc_count": 18004,
                  "key": "FM-AD"
                },
                {
                  "doc_count": 1127,
                  "key": "TARGET-NBL"
                },
                {
                  "doc_count": 1098,
                  "key": "TCGA-BRCA"
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
                  "doc_count": 183549,
                  "key": "open"
                },
                {
                  "doc_count": 175130,
                  "key": "controlled"
                }
              ]
            },
            "analysis__workflow_type": {
              "buckets": [
                {
                  "doc_count": 45258,
                  "key": "DNAcopy"
                },
                {
                  "doc_count": 23334,
                  "key": "BCGSC miRNA Profiling"
                },
                {
                  "doc_count": 22871,
                  "key": "BWA with Mark Duplicates and Cocleaning"
                },
                {
                  "doc_count": 18004,
                  "key": "FM Simple Somatic Mutation"
                }
              ]
            },
            "data_category": {
              "buckets": [
                {
                  "doc_count": 127390,
                  "key": "Simple Nucleotide Variation"
                },
                {
                  "doc_count": 58047,
                  "key": "Transcriptome Profiling"
                },
                {
                  "doc_count": 55224,
                  "key": "Biospecimen"
                },
                {
                  "doc_count": 47437,
                  "key": "Sequencing Reads"
                },
                {
                  "doc_count": 45291,
                  "key": "Copy Number Variation"
                },
                {
                  "doc_count": 12496,
                  "key": "Clinical"
                },
                {
                  "doc_count": 12359,
                  "key": "DNA Methylation"
                },
                {
                  "doc_count": 435,
                  "key": "Combined Nucleotide Variation"
                }
              ]
            },
            "data_format": {
              "buckets": [
                {
                  "doc_count": 127507,
                  "key": "VCF"
                },
                {
                  "doc_count": 115697,
                  "key": "TXT"
                },
                {
                  "doc_count": 47437,
                  "key": "BAM"
                },
                {
                  "doc_count": 30072,
                  "key": "SVS"
                }
              ]
            },
            "data_type": {
              "buckets": [
                {
                  "doc_count": 63536,
                  "key": "Annotated Somatic Mutation"
                },
                {
                  "doc_count": 63536,
                  "key": "Raw Simple Somatic Mutation"
                },
                {
                  "doc_count": 47437,
                  "key": "Aligned Reads"
                }
              ]
            },
            "experimental_strategy": {
              "buckets": [
                {
                  "doc_count": 114727,
                  "key": "WXS"
                },
                {
                  "doc_count": 46317,
                  "key": "RNA-Seq"
                },
                {
                  "doc_count": 45291,
                  "key": "Genotyping Array"
                }
              ]
            },
            "platform": {
              "buckets": [
                {
                  "doc_count": 47437,
                  "key": "Illumina"
                },
                {
                  "doc_count": 45291,
                  "key": "Affymetrix SNP 6.0"
                },
                {
                  "doc_count": 9756,
                  "key": "Illumina Human Methylation 450"
                },
                {
                  "doc_count": 2603,
                  "key": "Illumina Human Methylation 27"
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

FILE_TABLE = {
  "data": {
    "viewer": {
      "repository": {
        "files": {
          "hits": {
            "edges": [
              {
                "node": {
                  "access": "open",
                  "acl": [
                    "open"
                  ],
                  "annotations": {
                    "hits": {
                      "total": 0
                    }
                  },
                  "cases": {
                    "hits": {
                      "edges": [
                        {
                          "node": {
                            "case_id": "34f545ab-d420-4dd2-8db4-3159896efd23",
                            "id": "RmlsZUNhc2U6NDQwZTllYzUtOGU2MS00Zjc1LWIxZDEtNjE2OTQxZDk0NTZkOjM0ZjU0NWFiLWQ0MjAtNGRkMi04ZGI0LTMxNTk4OTZlZmQyMw==",
                            "project": {
                              "id": "UHJvamVjdDo0NDBlOWVjNS04ZTYxLTRmNzUtYjFkMS02MTY5NDFkOTQ1NmQ6MzRmNTQ1YWItZDQyMC00ZGQyLThkYjQtMzE1OTg5NmVmZDIzOl8=",
                              "project_id": "TCGA-OV"
                            }
                          }
                        }
                      ],
                      "total": 1
                    }
                  },
                  "data_category": "Copy Number Variation",
                  "data_format": "TXT",
                  "data_type": "Masked Copy Number Segment",
                  "experimental_strategy": "Genotyping Array",
                  "file_id": "440e9ec5-8e61-4f75-b1d1-616941d9456d",
                  "file_name": "THETA_p_TCGA_Batch14_SNP_N_GenomeWideSNP_6_C03_455318.nocnv_grch38.seg.v2.txt",
                  "file_size": 27158.0,
                  "id": "RmlsZTo0NDBlOWVjNS04ZTYxLTRmNzUtYjFkMS02MTY5NDFkOTQ1NmQ=",
                  "platform": "Affymetrix SNP 6.0",
                  "state": "released"
                }
              },
              {
                "node": {
                  "access": "controlled",
                  "acl": [
                    "phs000178"
                  ],
                  "annotations": {
                    "hits": {
                      "total": 0
                    }
                  },
                  "cases": {
                    "hits": {
                      "edges": [
                        {
                          "node": {
                            "case_id": "e5a329ec-e50e-4786-901d-b58474f8ea65",
                            "id": "RmlsZUNhc2U6OTc4ZDEyNGQtYWUzOS00ZmJiLTk3OTYtNThiYWJjOTQ4YWNiOmU1YTMyOWVjLWU1MGUtNDc4Ni05MDFkLWI1ODQ3NGY4ZWE2NQ==",
                            "project": {
                              "id": "UHJvamVjdDo5NzhkMTI0ZC1hZTM5LTRmYmItOTc5Ni01OGJhYmM5NDhhY2I6ZTVhMzI5ZWMtZTUwZS00Nzg2LTkwMWQtYjU4NDc0ZjhlYTY1Ol8=",
                              "project_id": "TCGA-OV"
                            }
                          }
                        }
                      ],
                      "total": 1
                    }
                  },
                  "data_category": "Simple Nucleotide Variation",
                  "data_format": "VCF",
                  "data_type": "Annotated Somatic Mutation",
                  "experimental_strategy": "WXS",
                  "file_id": "978d124d-ae39-4fbb-9796-58babc948acb",
                  "file_name": "978d124d-ae39-4fbb-9796-58babc948acb.vep.vcf.gz",
                  "file_size": 115844.0,
                  "id": "RmlsZTo5NzhkMTI0ZC1hZTM5LTRmYmItOTc5Ni01OGJhYmM5NDhhY2I=",
                  "platform": "Illumina",
                  "state": "released"
                }
              },
              {
                "node": {
                  "access": "controlled",
                  "acl": [
                    "phs000178"
                  ],
                  "annotations": {
                    "hits": {
                      "total": 0
                    }
                  },
                  "cases": {
                    "hits": {
                      "edges": [
                        {
                          "node": {
                            "case_id": "0ba7b6cc-e5f5-47d7-859a-24e31aa336ab",
                            "id": "RmlsZUNhc2U6M2IxM2IwMjMtMDMyNS00ZDZjLTg1MGYtMGY1NTM0ZjdkNDJiOjBiYTdiNmNjLWU1ZjUtNDdkNy04NTlhLTI0ZTMxYWEzMzZhYg==",
                            "project": {
                              "id": "UHJvamVjdDozYjEzYjAyMy0wMzI1LTRkNmMtODUwZi0wZjU1MzRmN2Q0MmI6MGJhN2I2Y2MtZTVmNS00N2Q3LTg1OWEtMjRlMzFhYTMzNmFiOl8=",
                              "project_id": "TCGA-OV"
                            }
                          }
                        }
                      ],
                      "total": 1
                    }
                  },
                  "data_category": "Sequencing Reads",
                  "data_format": "BAM",
                  "data_type": "Aligned Reads",
                  "experimental_strategy": "WXS",
                  "file_id": "3b13b023-0325-4d6c-850f-0f5534f7d42b",
                  "file_name": "C239.TCGA-13-0908-10A-01W.7_gdc_realn.bam",
                  "file_size": 44297789827.0,
                  "id": "RmlsZTozYjEzYjAyMy0wMzI1LTRkNmMtODUwZi0wZjU1MzRmN2Q0MmI=",
                  "platform": "Illumina",
                  "state": "released"
                }
              },
              {
                "node": {
                  "access": "open",
                  "acl": [
                    "open"
                  ],
                  "annotations": {
                    "hits": {
                      "total": 0
                    }
                  },
                  "cases": {
                    "hits": {
                      "edges": [
                        {
                          "node": {
                            "case_id": "47681e4b-01e8-4779-b966-ce57aff4b712",
                            "id": "RmlsZUNhc2U6MjI4ZjYwMWMtYjY1Ny00NzliLWJjZjQtZjI1YmIyYzgyM2U0OjQ3NjgxZTRiLTAxZTgtNDc3OS1iOTY2LWNlNTdhZmY0YjcxMg==",
                            "project": {
                              "id": "UHJvamVjdDoyMjhmNjAxYy1iNjU3LTQ3OWItYmNmNC1mMjViYjJjODIzZTQ6NDc2ODFlNGItMDFlOC00Nzc5LWI5NjYtY2U1N2FmZjRiNzEyOl8=",
                              "project_id": "TCGA-OV"
                            }
                          }
                        }
                      ],
                      "total": 1
                    }
                  },
                  "data_category": "Transcriptome Profiling",
                  "data_format": "TXT",
                  "data_type": "Gene Expression Quantification",
                  "experimental_strategy": "RNA-Seq",
                  "file_id": "228f601c-b657-479b-bcf4-f25bb2c823e4",
                  "file_name": "16417d82-1ae0-4097-85c1-5e2df313fd35.htseq.counts.gz",
                  "file_size": 251840.0,
                  "id": "RmlsZToyMjhmNjAxYy1iNjU3LTQ3OWItYmNmNC1mMjViYjJjODIzZTQ=",
                  "platform": "Illumina",
                  "state": "released"
                }
              },
              {
                "node": {
                  "access": "controlled",
                  "acl": [
                    "phs000178"
                  ],
                  "annotations": {
                    "hits": {
                      "total": 0
                    }
                  },
                  "cases": {
                    "hits": {
                      "edges": [
                        {
                          "node": {
                            "case_id": "565d06a1-3640-4274-8fb3-8cad7e578876",
                            "id": "RmlsZUNhc2U6YjI0NWJkYWItYTU4NS00YTU1LThmYjMtZDkyZTFkMTJmYjZiOjU2NWQwNmExLTM2NDAtNDI3NC04ZmIzLThjYWQ3ZTU3ODg3Ng==",
                            "project": {
                              "id": "UHJvamVjdDpiMjQ1YmRhYi1hNTg1LTRhNTUtOGZiMy1kOTJlMWQxMmZiNmI6NTY1ZDA2YTEtMzY0MC00Mjc0LThmYjMtOGNhZDdlNTc4ODc2Ol8=",
                              "project_id": "TCGA-OV"
                            }
                          }
                        }
                      ],
                      "total": 1
                    }
                  },
                  "data_category": "Simple Nucleotide Variation",
                  "data_format": "VCF",
                  "data_type": "Raw Simple Somatic Mutation",
                  "experimental_strategy": "WXS",
                  "file_id": "b245bdab-a585-4a55-8fb3-d92e1d12fb6b",
                  "file_name": "b245bdab-a585-4a55-8fb3-d92e1d12fb6b.vcf.gz",
                  "file_size": 92669.0,
                  "id": "RmlsZTpiMjQ1YmRhYi1hNTg1LTRhNTUtOGZiMy1kOTJlMWQxMmZiNmI=",
                  "platform": "Illumina",
                  "state": "released"
                }
              }
            ],
            "total": 5
          }
        }
      }
    }
  }
}

# TopCasesCountByGenes
TOP_CASES_GENES = {
  "data": {
    "analysisViewer": {
      "analysis": {
        "top_cases_count_by_genes": {
          "data": "{\"hits\": {\"hits\": [], \"total\": 7203, \"max_score\": 0.0}, \"_shards\": {\"successful\": 12, \"failed\": 0, \"total\": 12}, \"took\": 109, \"aggregations\": {\"projects\": {\"buckets\": [{\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 324}, {\"key\": \"ENSG00000121879\", \"doc_count\": 321}, {\"key\": \"ENSG00000055609\", \"doc_count\": 91}, {\"key\": \"ENSG00000171862\", \"doc_count\": 55}, {\"key\": \"ENSG00000117713\", \"doc_count\": 39}, {\"key\": \"ENSG00000196712\", \"doc_count\": 34}, {\"key\": \"ENSG00000167548\", \"doc_count\": 33}, {\"key\": \"ENSG00000083857\", \"doc_count\": 31}, {\"key\": \"ENSG00000127914\", \"doc_count\": 30}, {\"key\": \"ENSG00000085224\", \"doc_count\": 26}, {\"key\": \"ENSG00000173821\", \"doc_count\": 25}, {\"key\": \"ENSG00000149311\", \"doc_count\": 22}, {\"key\": \"ENSG00000196159\", \"doc_count\": 21}, {\"key\": \"ENSG00000183454\", \"doc_count\": 20}, {\"key\": \"ENSG00000140836\", \"doc_count\": 19}, {\"key\": \"ENSG00000196367\", \"doc_count\": 16}, {\"key\": \"ENSG00000134982\", \"doc_count\": 14}, {\"key\": \"ENSG00000157764\", \"doc_count\": 8}, {\"key\": \"ENSG00000133703\", \"doc_count\": 6}, {\"key\": \"ENSG00000138413\", \"doc_count\": 6}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 1141}, \"doc_count\": 1624872}, \"key\": \"TCGA-BRCA\", \"doc_count\": 705}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000171862\", \"doc_count\": 331}, {\"key\": \"ENSG00000121879\", \"doc_count\": 256}, {\"key\": \"ENSG00000117713\", \"doc_count\": 237}, {\"key\": \"ENSG00000141510\", \"doc_count\": 193}, {\"key\": \"ENSG00000167548\", \"doc_count\": 146}, {\"key\": \"ENSG00000140836\", \"doc_count\": 132}, {\"key\": \"ENSG00000196159\", \"doc_count\": 115}, {\"key\": \"ENSG00000083857\", \"doc_count\": 107}, {\"key\": \"ENSG00000133703\", \"doc_count\": 105}, {\"key\": \"ENSG00000149311\", \"doc_count\": 98}, {\"key\": \"ENSG00000055609\", \"doc_count\": 95}, {\"key\": \"ENSG00000127914\", \"doc_count\": 87}, {\"key\": \"ENSG00000173821\", \"doc_count\": 82}, {\"key\": \"ENSG00000196367\", \"doc_count\": 82}, {\"key\": \"ENSG00000085224\", \"doc_count\": 81}, {\"key\": \"ENSG00000134982\", \"doc_count\": 79}, {\"key\": \"ENSG00000196712\", \"doc_count\": 71}, {\"key\": \"ENSG00000183454\", \"doc_count\": 60}, {\"key\": \"ENSG00000157764\", \"doc_count\": 34}, {\"key\": \"ENSG00000138413\", \"doc_count\": 20}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 2411}, \"doc_count\": 1281903}, \"key\": \"TCGA-UCEC\", \"doc_count\": 516}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 271}, {\"key\": \"ENSG00000133703\", \"doc_count\": 158}, {\"key\": \"ENSG00000196159\", \"doc_count\": 91}, {\"key\": \"ENSG00000083857\", \"doc_count\": 63}, {\"key\": \"ENSG00000055609\", \"doc_count\": 56}, {\"key\": \"ENSG00000183454\", \"doc_count\": 52}, {\"key\": \"ENSG00000196712\", \"doc_count\": 52}, {\"key\": \"ENSG00000149311\", \"doc_count\": 45}, {\"key\": \"ENSG00000157764\", \"doc_count\": 39}, {\"key\": \"ENSG00000196367\", \"doc_count\": 39}, {\"key\": \"ENSG00000167548\", \"doc_count\": 38}, {\"key\": \"ENSG00000117713\", \"doc_count\": 36}, {\"key\": \"ENSG00000085224\", \"doc_count\": 34}, {\"key\": \"ENSG00000127914\", \"doc_count\": 33}, {\"key\": \"ENSG00000134982\", \"doc_count\": 28}, {\"key\": \"ENSG00000121879\", \"doc_count\": 26}, {\"key\": \"ENSG00000140836\", \"doc_count\": 25}, {\"key\": \"ENSG00000173821\", \"doc_count\": 25}, {\"key\": \"ENSG00000171862\", \"doc_count\": 10}, {\"key\": \"ENSG00000138413\", \"doc_count\": 5}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 1126}, \"doc_count\": 916226}, \"key\": \"TCGA-LUAD\", \"doc_count\": 481}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 377}, {\"key\": \"ENSG00000167548\", \"doc_count\": 110}, {\"key\": \"ENSG00000083857\", \"doc_count\": 65}, {\"key\": \"ENSG00000196159\", \"doc_count\": 62}, {\"key\": \"ENSG00000121879\", \"doc_count\": 58}, {\"key\": \"ENSG00000055609\", \"doc_count\": 56}, {\"key\": \"ENSG00000171862\", \"doc_count\": 50}, {\"key\": \"ENSG00000196712\", \"doc_count\": 49}, {\"key\": \"ENSG00000183454\", \"doc_count\": 47}, {\"key\": \"ENSG00000140836\", \"doc_count\": 39}, {\"key\": \"ENSG00000127914\", \"doc_count\": 36}, {\"key\": \"ENSG00000173821\", \"doc_count\": 35}, {\"key\": \"ENSG00000117713\", \"doc_count\": 33}, {\"key\": \"ENSG00000196367\", \"doc_count\": 28}, {\"key\": \"ENSG00000149311\", \"doc_count\": 26}, {\"key\": \"ENSG00000134982\", \"doc_count\": 25}, {\"key\": \"ENSG00000085224\", \"doc_count\": 22}, {\"key\": \"ENSG00000157764\", \"doc_count\": 13}, {\"key\": \"ENSG00000133703\", \"doc_count\": 9}, {\"key\": \"ENSG00000138413\", \"doc_count\": 3}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 1143}, \"doc_count\": 1145759}, \"key\": \"TCGA-LUSC\", \"doc_count\": 457}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000138413\", \"doc_count\": 394}, {\"key\": \"ENSG00000141510\", \"doc_count\": 233}, {\"key\": \"ENSG00000085224\", \"doc_count\": 186}, {\"key\": \"ENSG00000121879\", \"doc_count\": 38}, {\"key\": \"ENSG00000196712\", \"doc_count\": 27}, {\"key\": \"ENSG00000171862\", \"doc_count\": 25}, {\"key\": \"ENSG00000117713\", \"doc_count\": 24}, {\"key\": \"ENSG00000167548\", \"doc_count\": 9}, {\"key\": \"ENSG00000196159\", \"doc_count\": 9}, {\"key\": \"ENSG00000055609\", \"doc_count\": 7}, {\"key\": \"ENSG00000083857\", \"doc_count\": 7}, {\"key\": \"ENSG00000196367\", \"doc_count\": 7}, {\"key\": \"ENSG00000127914\", \"doc_count\": 5}, {\"key\": \"ENSG00000183454\", \"doc_count\": 5}, {\"key\": \"ENSG00000157764\", \"doc_count\": 4}, {\"key\": \"ENSG00000134982\", \"doc_count\": 3}, {\"key\": \"ENSG00000140836\", \"doc_count\": 3}, {\"key\": \"ENSG00000173821\", \"doc_count\": 3}, {\"key\": \"ENSG00000133703\", \"doc_count\": 2}, {\"key\": \"ENSG00000149311\", \"doc_count\": 2}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 993}, \"doc_count\": 282284}, \"key\": \"TCGA-LGG\", \"doc_count\": 453}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 338}, {\"key\": \"ENSG00000083857\", \"doc_count\": 116}, {\"key\": \"ENSG00000121879\", \"doc_count\": 90}, {\"key\": \"ENSG00000167548\", \"doc_count\": 75}, {\"key\": \"ENSG00000196159\", \"doc_count\": 43}, {\"key\": \"ENSG00000055609\", \"doc_count\": 33}, {\"key\": \"ENSG00000127914\", \"doc_count\": 29}, {\"key\": \"ENSG00000173821\", \"doc_count\": 27}, {\"key\": \"ENSG00000085224\", \"doc_count\": 22}, {\"key\": \"ENSG00000134982\", \"doc_count\": 22}, {\"key\": \"ENSG00000183454\", \"doc_count\": 20}, {\"key\": \"ENSG00000196367\", \"doc_count\": 20}, {\"key\": \"ENSG00000117713\", \"doc_count\": 19}, {\"key\": \"ENSG00000140836\", \"doc_count\": 15}, {\"key\": \"ENSG00000149311\", \"doc_count\": 14}, {\"key\": \"ENSG00000171862\", \"doc_count\": 13}, {\"key\": \"ENSG00000196712\", \"doc_count\": 11}, {\"key\": \"ENSG00000157764\", \"doc_count\": 9}, {\"key\": \"ENSG00000138413\", \"doc_count\": 4}, {\"key\": \"ENSG00000133703\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 921}, \"doc_count\": 664023}, \"key\": \"TCGA-HNSC\", \"doc_count\": 433}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000157764\", \"doc_count\": 240}, {\"key\": \"ENSG00000196159\", \"doc_count\": 152}, {\"key\": \"ENSG00000183454\", \"doc_count\": 114}, {\"key\": \"ENSG00000141510\", \"doc_count\": 65}, {\"key\": \"ENSG00000167548\", \"doc_count\": 65}, {\"key\": \"ENSG00000196712\", \"doc_count\": 64}, {\"key\": \"ENSG00000196367\", \"doc_count\": 63}, {\"key\": \"ENSG00000055609\", \"doc_count\": 57}, {\"key\": \"ENSG00000140836\", \"doc_count\": 55}, {\"key\": \"ENSG00000127914\", \"doc_count\": 47}, {\"key\": \"ENSG00000083857\", \"doc_count\": 46}, {\"key\": \"ENSG00000171862\", \"doc_count\": 44}, {\"key\": \"ENSG00000134982\", \"doc_count\": 41}, {\"key\": \"ENSG00000173821\", \"doc_count\": 37}, {\"key\": \"ENSG00000085224\", \"doc_count\": 29}, {\"key\": \"ENSG00000149311\", \"doc_count\": 25}, {\"key\": \"ENSG00000117713\", \"doc_count\": 23}, {\"key\": \"ENSG00000138413\", \"doc_count\": 22}, {\"key\": \"ENSG00000121879\", \"doc_count\": 12}, {\"key\": \"ENSG00000133703\", \"doc_count\": 11}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 1212}, \"doc_count\": 776839}, \"key\": \"TCGA-SKCM\", \"doc_count\": 399}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000134982\", \"doc_count\": 304}, {\"key\": \"ENSG00000141510\", \"doc_count\": 217}, {\"key\": \"ENSG00000133703\", \"doc_count\": 172}, {\"key\": \"ENSG00000121879\", \"doc_count\": 117}, {\"key\": \"ENSG00000196159\", \"doc_count\": 105}, {\"key\": \"ENSG00000167548\", \"doc_count\": 63}, {\"key\": \"ENSG00000140836\", \"doc_count\": 59}, {\"key\": \"ENSG00000157764\", \"doc_count\": 59}, {\"key\": \"ENSG00000149311\", \"doc_count\": 58}, {\"key\": \"ENSG00000083857\", \"doc_count\": 56}, {\"key\": \"ENSG00000117713\", \"doc_count\": 55}, {\"key\": \"ENSG00000055609\", \"doc_count\": 52}, {\"key\": \"ENSG00000173821\", \"doc_count\": 46}, {\"key\": \"ENSG00000196367\", \"doc_count\": 46}, {\"key\": \"ENSG00000127914\", \"doc_count\": 41}, {\"key\": \"ENSG00000183454\", \"doc_count\": 37}, {\"key\": \"ENSG00000085224\", \"doc_count\": 34}, {\"key\": \"ENSG00000171862\", \"doc_count\": 28}, {\"key\": \"ENSG00000196712\", \"doc_count\": 25}, {\"key\": \"ENSG00000138413\", \"doc_count\": 7}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 1581}, \"doc_count\": 531541}, \"key\": \"TCGA-COAD\", \"doc_count\": 396}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 351}, {\"key\": \"ENSG00000055609\", \"doc_count\": 33}, {\"key\": \"ENSG00000173821\", \"doc_count\": 31}, {\"key\": \"ENSG00000196712\", \"doc_count\": 29}, {\"key\": \"ENSG00000196367\", \"doc_count\": 28}, {\"key\": \"ENSG00000140836\", \"doc_count\": 22}, {\"key\": \"ENSG00000196159\", \"doc_count\": 22}, {\"key\": \"ENSG00000134982\", \"doc_count\": 17}, {\"key\": \"ENSG00000083857\", \"doc_count\": 15}, {\"key\": \"ENSG00000085224\", \"doc_count\": 14}, {\"key\": \"ENSG00000127914\", \"doc_count\": 14}, {\"key\": \"ENSG00000167548\", \"doc_count\": 14}, {\"key\": \"ENSG00000183454\", \"doc_count\": 14}, {\"key\": \"ENSG00000149311\", \"doc_count\": 13}, {\"key\": \"ENSG00000117713\", \"doc_count\": 10}, {\"key\": \"ENSG00000121879\", \"doc_count\": 10}, {\"key\": \"ENSG00000133703\", \"doc_count\": 6}, {\"key\": \"ENSG00000171862\", \"doc_count\": 4}, {\"key\": \"ENSG00000157764\", \"doc_count\": 2}, {\"key\": \"ENSG00000138413\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 650}, \"doc_count\": 1912199}, \"key\": \"TCGA-OV\", \"doc_count\": 389}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 198}, {\"key\": \"ENSG00000167548\", \"doc_count\": 117}, {\"key\": \"ENSG00000117713\", \"doc_count\": 101}, {\"key\": \"ENSG00000121879\", \"doc_count\": 91}, {\"key\": \"ENSG00000055609\", \"doc_count\": 76}, {\"key\": \"ENSG00000196159\", \"doc_count\": 62}, {\"key\": \"ENSG00000149311\", \"doc_count\": 48}, {\"key\": \"ENSG00000083857\", \"doc_count\": 46}, {\"key\": \"ENSG00000127914\", \"doc_count\": 46}, {\"key\": \"ENSG00000173821\", \"doc_count\": 39}, {\"key\": \"ENSG00000196367\", \"doc_count\": 35}, {\"key\": \"ENSG00000196712\", \"doc_count\": 26}, {\"key\": \"ENSG00000134982\", \"doc_count\": 24}, {\"key\": \"ENSG00000085224\", \"doc_count\": 23}, {\"key\": \"ENSG00000140836\", \"doc_count\": 21}, {\"key\": \"ENSG00000133703\", \"doc_count\": 17}, {\"key\": \"ENSG00000171862\", \"doc_count\": 14}, {\"key\": \"ENSG00000183454\", \"doc_count\": 14}, {\"key\": \"ENSG00000157764\", \"doc_count\": 11}, {\"key\": \"ENSG00000138413\", \"doc_count\": 9}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 1018}, \"doc_count\": 844656}, \"key\": \"TCGA-BLCA\", \"doc_count\": 363}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 191}, {\"key\": \"ENSG00000117713\", \"doc_count\": 111}, {\"key\": \"ENSG00000196159\", \"doc_count\": 95}, {\"key\": \"ENSG00000167548\", \"doc_count\": 75}, {\"key\": \"ENSG00000121879\", \"doc_count\": 70}, {\"key\": \"ENSG00000055609\", \"doc_count\": 55}, {\"key\": \"ENSG00000173821\", \"doc_count\": 53}, {\"key\": \"ENSG00000196367\", \"doc_count\": 51}, {\"key\": \"ENSG00000127914\", \"doc_count\": 50}, {\"key\": \"ENSG00000134982\", \"doc_count\": 50}, {\"key\": \"ENSG00000140836\", \"doc_count\": 45}, {\"key\": \"ENSG00000133703\", \"doc_count\": 40}, {\"key\": \"ENSG00000149311\", \"doc_count\": 40}, {\"key\": \"ENSG00000083857\", \"doc_count\": 36}, {\"key\": \"ENSG00000171862\", \"doc_count\": 34}, {\"key\": \"ENSG00000196712\", \"doc_count\": 30}, {\"key\": \"ENSG00000183454\", \"doc_count\": 27}, {\"key\": \"ENSG00000085224\", \"doc_count\": 24}, {\"key\": \"ENSG00000157764\", \"doc_count\": 21}, {\"key\": \"ENSG00000138413\", \"doc_count\": 4}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 1102}, \"doc_count\": 764078}, \"key\": \"TCGA-STAD\", \"doc_count\": 361}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000157764\", \"doc_count\": 290}, {\"key\": \"ENSG00000140836\", \"doc_count\": 6}, {\"key\": \"ENSG00000149311\", \"doc_count\": 6}, {\"key\": \"ENSG00000055609\", \"doc_count\": 5}, {\"key\": \"ENSG00000127914\", \"doc_count\": 4}, {\"key\": \"ENSG00000133703\", \"doc_count\": 4}, {\"key\": \"ENSG00000085224\", \"doc_count\": 3}, {\"key\": \"ENSG00000134982\", \"doc_count\": 3}, {\"key\": \"ENSG00000141510\", \"doc_count\": 3}, {\"key\": \"ENSG00000121879\", \"doc_count\": 2}, {\"key\": \"ENSG00000167548\", \"doc_count\": 2}, {\"key\": \"ENSG00000171862\", \"doc_count\": 2}, {\"key\": \"ENSG00000183454\", \"doc_count\": 2}, {\"key\": \"ENSG00000083857\", \"doc_count\": 1}, {\"key\": \"ENSG00000196367\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 334}, \"doc_count\": 14028}, \"key\": \"TCGA-THCA\", \"doc_count\": 304}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000171862\", \"doc_count\": 121}, {\"key\": \"ENSG00000141510\", \"doc_count\": 113}, {\"key\": \"ENSG00000196712\", \"doc_count\": 45}, {\"key\": \"ENSG00000085224\", \"doc_count\": 39}, {\"key\": \"ENSG00000121879\", \"doc_count\": 35}, {\"key\": \"ENSG00000055609\", \"doc_count\": 28}, {\"key\": \"ENSG00000138413\", \"doc_count\": 26}, {\"key\": \"ENSG00000196367\", \"doc_count\": 23}, {\"key\": \"ENSG00000140836\", \"doc_count\": 21}, {\"key\": \"ENSG00000196159\", \"doc_count\": 21}, {\"key\": \"ENSG00000183454\", \"doc_count\": 20}, {\"key\": \"ENSG00000173821\", \"doc_count\": 19}, {\"key\": \"ENSG00000134982\", \"doc_count\": 16}, {\"key\": \"ENSG00000157764\", \"doc_count\": 9}, {\"key\": \"ENSG00000167548\", \"doc_count\": 9}, {\"key\": \"ENSG00000149311\", \"doc_count\": 8}, {\"key\": \"ENSG00000127914\", \"doc_count\": 7}, {\"key\": \"ENSG00000117713\", \"doc_count\": 6}, {\"key\": \"ENSG00000083857\", \"doc_count\": 5}, {\"key\": \"ENSG00000133703\", \"doc_count\": 2}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 573}, \"doc_count\": 254773}, \"key\": \"TCGA-GBM\", \"doc_count\": 270}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 100}, {\"key\": \"ENSG00000117713\", \"doc_count\": 28}, {\"key\": \"ENSG00000167548\", \"doc_count\": 18}, {\"key\": \"ENSG00000196159\", \"doc_count\": 14}, {\"key\": \"ENSG00000055609\", \"doc_count\": 13}, {\"key\": \"ENSG00000121879\", \"doc_count\": 13}, {\"key\": \"ENSG00000134982\", \"doc_count\": 12}, {\"key\": \"ENSG00000149311\", \"doc_count\": 10}, {\"key\": \"ENSG00000196712\", \"doc_count\": 10}, {\"key\": \"ENSG00000140836\", \"doc_count\": 8}, {\"key\": \"ENSG00000173821\", \"doc_count\": 8}, {\"key\": \"ENSG00000083857\", \"doc_count\": 7}, {\"key\": \"ENSG00000138413\", \"doc_count\": 7}, {\"key\": \"ENSG00000133703\", \"doc_count\": 6}, {\"key\": \"ENSG00000171862\", \"doc_count\": 6}, {\"key\": \"ENSG00000085224\", \"doc_count\": 5}, {\"key\": \"ENSG00000127914\", \"doc_count\": 5}, {\"key\": \"ENSG00000196367\", \"doc_count\": 5}, {\"key\": \"ENSG00000183454\", \"doc_count\": 3}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 278}, \"doc_count\": 330999}, \"key\": \"TCGA-LIHC\", \"doc_count\": 206}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000121879\", \"doc_count\": 84}, {\"key\": \"ENSG00000055609\", \"doc_count\": 59}, {\"key\": \"ENSG00000167548\", \"doc_count\": 43}, {\"key\": \"ENSG00000083857\", \"doc_count\": 25}, {\"key\": \"ENSG00000141510\", \"doc_count\": 23}, {\"key\": \"ENSG00000117713\", \"doc_count\": 19}, {\"key\": \"ENSG00000171862\", \"doc_count\": 19}, {\"key\": \"ENSG00000085224\", \"doc_count\": 17}, {\"key\": \"ENSG00000196367\", \"doc_count\": 17}, {\"key\": \"ENSG00000133703\", \"doc_count\": 16}, {\"key\": \"ENSG00000196159\", \"doc_count\": 16}, {\"key\": \"ENSG00000140836\", \"doc_count\": 15}, {\"key\": \"ENSG00000196712\", \"doc_count\": 15}, {\"key\": \"ENSG00000173821\", \"doc_count\": 14}, {\"key\": \"ENSG00000149311\", \"doc_count\": 12}, {\"key\": \"ENSG00000127914\", \"doc_count\": 9}, {\"key\": \"ENSG00000134982\", \"doc_count\": 9}, {\"key\": \"ENSG00000183454\", \"doc_count\": 8}, {\"key\": \"ENSG00000157764\", \"doc_count\": 3}, {\"key\": \"ENSG00000138413\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 424}, \"doc_count\": 328133}, \"key\": \"TCGA-CESC\", \"doc_count\": 197}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 54}, {\"key\": \"ENSG00000167548\", \"doc_count\": 27}, {\"key\": \"ENSG00000055609\", \"doc_count\": 24}, {\"key\": \"ENSG00000149311\", \"doc_count\": 19}, {\"key\": \"ENSG00000171862\", \"doc_count\": 14}, {\"key\": \"ENSG00000140836\", \"doc_count\": 13}, {\"key\": \"ENSG00000121879\", \"doc_count\": 11}, {\"key\": \"ENSG00000134982\", \"doc_count\": 11}, {\"key\": \"ENSG00000183454\", \"doc_count\": 9}, {\"key\": \"ENSG00000196159\", \"doc_count\": 9}, {\"key\": \"ENSG00000127914\", \"doc_count\": 7}, {\"key\": \"ENSG00000173821\", \"doc_count\": 7}, {\"key\": \"ENSG00000157764\", \"doc_count\": 6}, {\"key\": \"ENSG00000117713\", \"doc_count\": 5}, {\"key\": \"ENSG00000138413\", \"doc_count\": 5}, {\"key\": \"ENSG00000085224\", \"doc_count\": 4}, {\"key\": \"ENSG00000196367\", \"doc_count\": 4}, {\"key\": \"ENSG00000083857\", \"doc_count\": 3}, {\"key\": \"ENSG00000133703\", \"doc_count\": 2}, {\"key\": \"ENSG00000196712\", \"doc_count\": 2}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 236}, \"doc_count\": 184562}, \"key\": \"TCGA-PRAD\", \"doc_count\": 171}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 140}, {\"key\": \"ENSG00000167548\", \"doc_count\": 23}, {\"key\": \"ENSG00000117713\", \"doc_count\": 17}, {\"key\": \"ENSG00000121879\", \"doc_count\": 17}, {\"key\": \"ENSG00000055609\", \"doc_count\": 13}, {\"key\": \"ENSG00000196159\", \"doc_count\": 13}, {\"key\": \"ENSG00000196367\", \"doc_count\": 12}, {\"key\": \"ENSG00000127914\", \"doc_count\": 10}, {\"key\": \"ENSG00000134982\", \"doc_count\": 8}, {\"key\": \"ENSG00000173821\", \"doc_count\": 8}, {\"key\": \"ENSG00000149311\", \"doc_count\": 7}, {\"key\": \"ENSG00000171862\", \"doc_count\": 6}, {\"key\": \"ENSG00000083857\", \"doc_count\": 5}, {\"key\": \"ENSG00000140836\", \"doc_count\": 5}, {\"key\": \"ENSG00000196712\", \"doc_count\": 5}, {\"key\": \"ENSG00000133703\", \"doc_count\": 2}, {\"key\": \"ENSG00000157764\", \"doc_count\": 2}, {\"key\": \"ENSG00000183454\", \"doc_count\": 2}, {\"key\": \"ENSG00000085224\", \"doc_count\": 1}, {\"key\": \"ENSG00000138413\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 297}, \"doc_count\": 413220}, \"key\": \"TCGA-ESCA\", \"doc_count\": 167}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000133703\", \"doc_count\": 137}, {\"key\": \"ENSG00000141510\", \"doc_count\": 110}, {\"key\": \"ENSG00000117713\", \"doc_count\": 10}, {\"key\": \"ENSG00000173821\", \"doc_count\": 8}, {\"key\": \"ENSG00000055609\", \"doc_count\": 6}, {\"key\": \"ENSG00000149311\", \"doc_count\": 6}, {\"key\": \"ENSG00000167548\", \"doc_count\": 6}, {\"key\": \"ENSG00000196159\", \"doc_count\": 6}, {\"key\": \"ENSG00000121879\", \"doc_count\": 5}, {\"key\": \"ENSG00000083857\", \"doc_count\": 4}, {\"key\": \"ENSG00000134982\", \"doc_count\": 4}, {\"key\": \"ENSG00000140836\", \"doc_count\": 4}, {\"key\": \"ENSG00000085224\", \"doc_count\": 2}, {\"key\": \"ENSG00000127914\", \"doc_count\": 2}, {\"key\": \"ENSG00000196712\", \"doc_count\": 2}, {\"key\": \"ENSG00000138413\", \"doc_count\": 1}, {\"key\": \"ENSG00000157764\", \"doc_count\": 1}, {\"key\": \"ENSG00000183454\", \"doc_count\": 1}, {\"key\": \"ENSG00000196367\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 316}, \"doc_count\": 134537}, \"key\": \"TCGA-PAAD\", \"doc_count\": 151}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000134982\", \"doc_count\": 121}, {\"key\": \"ENSG00000141510\", \"doc_count\": 107}, {\"key\": \"ENSG00000133703\", \"doc_count\": 56}, {\"key\": \"ENSG00000196159\", \"doc_count\": 29}, {\"key\": \"ENSG00000121879\", \"doc_count\": 21}, {\"key\": \"ENSG00000149311\", \"doc_count\": 15}, {\"key\": \"ENSG00000127914\", \"doc_count\": 11}, {\"key\": \"ENSG00000173821\", \"doc_count\": 11}, {\"key\": \"ENSG00000083857\", \"doc_count\": 10}, {\"key\": \"ENSG00000183454\", \"doc_count\": 10}, {\"key\": \"ENSG00000085224\", \"doc_count\": 9}, {\"key\": \"ENSG00000117713\", \"doc_count\": 9}, {\"key\": \"ENSG00000196367\", \"doc_count\": 9}, {\"key\": \"ENSG00000171862\", \"doc_count\": 8}, {\"key\": \"ENSG00000196712\", \"doc_count\": 8}, {\"key\": \"ENSG00000055609\", \"doc_count\": 7}, {\"key\": \"ENSG00000140836\", \"doc_count\": 7}, {\"key\": \"ENSG00000167548\", \"doc_count\": 7}, {\"key\": \"ENSG00000157764\", \"doc_count\": 4}, {\"key\": \"ENSG00000138413\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 460}, \"doc_count\": 177123}, \"key\": \"TCGA-READ\", \"doc_count\": 136}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 72}, {\"key\": \"ENSG00000085224\", \"doc_count\": 36}, {\"key\": \"ENSG00000196712\", \"doc_count\": 11}, {\"key\": \"ENSG00000055609\", \"doc_count\": 7}, {\"key\": \"ENSG00000083857\", \"doc_count\": 7}, {\"key\": \"ENSG00000121879\", \"doc_count\": 7}, {\"key\": \"ENSG00000134982\", \"doc_count\": 7}, {\"key\": \"ENSG00000167548\", \"doc_count\": 7}, {\"key\": \"ENSG00000173821\", \"doc_count\": 7}, {\"key\": \"ENSG00000149311\", \"doc_count\": 6}, {\"key\": \"ENSG00000171862\", \"doc_count\": 6}, {\"key\": \"ENSG00000117713\", \"doc_count\": 4}, {\"key\": \"ENSG00000127914\", \"doc_count\": 4}, {\"key\": \"ENSG00000140836\", \"doc_count\": 4}, {\"key\": \"ENSG00000196367\", \"doc_count\": 4}, {\"key\": \"ENSG00000196159\", \"doc_count\": 3}, {\"key\": \"ENSG00000133703\", \"doc_count\": 2}, {\"key\": \"ENSG00000138413\", \"doc_count\": 2}, {\"key\": \"ENSG00000183454\", \"doc_count\": 2}, {\"key\": \"ENSG00000157764\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 199}, \"doc_count\": 367887}, \"key\": \"TCGA-SARC\", \"doc_count\": 128}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000055609\", \"doc_count\": 15}, {\"key\": \"ENSG00000117713\", \"doc_count\": 15}, {\"key\": \"ENSG00000149311\", \"doc_count\": 15}, {\"key\": \"ENSG00000171862\", \"doc_count\": 13}, {\"key\": \"ENSG00000127914\", \"doc_count\": 11}, {\"key\": \"ENSG00000085224\", \"doc_count\": 10}, {\"key\": \"ENSG00000083857\", \"doc_count\": 8}, {\"key\": \"ENSG00000167548\", \"doc_count\": 8}, {\"key\": \"ENSG00000196159\", \"doc_count\": 8}, {\"key\": \"ENSG00000134982\", \"doc_count\": 7}, {\"key\": \"ENSG00000183454\", \"doc_count\": 7}, {\"key\": \"ENSG00000141510\", \"doc_count\": 6}, {\"key\": \"ENSG00000196712\", \"doc_count\": 6}, {\"key\": \"ENSG00000121879\", \"doc_count\": 5}, {\"key\": \"ENSG00000173821\", \"doc_count\": 5}, {\"key\": \"ENSG00000140836\", \"doc_count\": 4}, {\"key\": \"ENSG00000196367\", \"doc_count\": 3}, {\"key\": \"ENSG00000133703\", \"doc_count\": 1}, {\"key\": \"ENSG00000138413\", \"doc_count\": 1}, {\"key\": \"ENSG00000157764\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 149}, \"doc_count\": 59671}, \"key\": \"TCGA-KIRC\", \"doc_count\": 111}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000055609\", \"doc_count\": 20}, {\"key\": \"ENSG00000083857\", \"doc_count\": 15}, {\"key\": \"ENSG00000167548\", \"doc_count\": 13}, {\"key\": \"ENSG00000117713\", \"doc_count\": 11}, {\"key\": \"ENSG00000171862\", \"doc_count\": 8}, {\"key\": \"ENSG00000133703\", \"doc_count\": 5}, {\"key\": \"ENSG00000141510\", \"doc_count\": 5}, {\"key\": \"ENSG00000196712\", \"doc_count\": 5}, {\"key\": \"ENSG00000134982\", \"doc_count\": 4}, {\"key\": \"ENSG00000140836\", \"doc_count\": 4}, {\"key\": \"ENSG00000157764\", \"doc_count\": 4}, {\"key\": \"ENSG00000183454\", \"doc_count\": 4}, {\"key\": \"ENSG00000196159\", \"doc_count\": 4}, {\"key\": \"ENSG00000121879\", \"doc_count\": 3}, {\"key\": \"ENSG00000127914\", \"doc_count\": 3}, {\"key\": \"ENSG00000173821\", \"doc_count\": 3}, {\"key\": \"ENSG00000149311\", \"doc_count\": 2}, {\"key\": \"ENSG00000196367\", \"doc_count\": 2}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 115}, \"doc_count\": 35808}, \"key\": \"TCGA-KIRP\", \"doc_count\": 95}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 49}, {\"key\": \"ENSG00000121879\", \"doc_count\": 20}, {\"key\": \"ENSG00000171862\", \"doc_count\": 11}, {\"key\": \"ENSG00000117713\", \"doc_count\": 7}, {\"key\": \"ENSG00000133703\", \"doc_count\": 7}, {\"key\": \"ENSG00000167548\", \"doc_count\": 6}, {\"key\": \"ENSG00000055609\", \"doc_count\": 4}, {\"key\": \"ENSG00000140836\", \"doc_count\": 4}, {\"key\": \"ENSG00000196712\", \"doc_count\": 4}, {\"key\": \"ENSG00000085224\", \"doc_count\": 2}, {\"key\": \"ENSG00000149311\", \"doc_count\": 2}, {\"key\": \"ENSG00000173821\", \"doc_count\": 2}, {\"key\": \"ENSG00000183454\", \"doc_count\": 2}, {\"key\": \"ENSG00000196159\", \"doc_count\": 2}, {\"key\": \"ENSG00000196367\", \"doc_count\": 2}, {\"key\": \"ENSG00000083857\", \"doc_count\": 1}, {\"key\": \"ENSG00000127914\", \"doc_count\": 1}, {\"key\": \"ENSG00000134982\", \"doc_count\": 1}, {\"key\": \"ENSG00000157764\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 128}, \"doc_count\": 182144}, \"key\": \"TCGA-UCS\", \"doc_count\": 55}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000138413\", \"doc_count\": 13}, {\"key\": \"ENSG00000141510\", \"doc_count\": 12}, {\"key\": \"ENSG00000133703\", \"doc_count\": 7}, {\"key\": \"ENSG00000196712\", \"doc_count\": 7}, {\"key\": \"ENSG00000083857\", \"doc_count\": 5}, {\"key\": \"ENSG00000167548\", \"doc_count\": 5}, {\"key\": \"ENSG00000196159\", \"doc_count\": 5}, {\"key\": \"ENSG00000117713\", \"doc_count\": 3}, {\"key\": \"ENSG00000134982\", \"doc_count\": 3}, {\"key\": \"ENSG00000140836\", \"doc_count\": 3}, {\"key\": \"ENSG00000173821\", \"doc_count\": 3}, {\"key\": \"ENSG00000055609\", \"doc_count\": 2}, {\"key\": \"ENSG00000085224\", \"doc_count\": 2}, {\"key\": \"ENSG00000149311\", \"doc_count\": 2}, {\"key\": \"ENSG00000196367\", \"doc_count\": 2}, {\"key\": \"ENSG00000127914\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 75}, \"doc_count\": 21858}, \"key\": \"TCGA-LAML\", \"doc_count\": 44}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 14}, {\"key\": \"ENSG00000196712\", \"doc_count\": 7}, {\"key\": \"ENSG00000196159\", \"doc_count\": 6}, {\"key\": \"ENSG00000085224\", \"doc_count\": 5}, {\"key\": \"ENSG00000055609\", \"doc_count\": 4}, {\"key\": \"ENSG00000083857\", \"doc_count\": 4}, {\"key\": \"ENSG00000134982\", \"doc_count\": 4}, {\"key\": \"ENSG00000149311\", \"doc_count\": 4}, {\"key\": \"ENSG00000167548\", \"doc_count\": 4}, {\"key\": \"ENSG00000140836\", \"doc_count\": 3}, {\"key\": \"ENSG00000127914\", \"doc_count\": 2}, {\"key\": \"ENSG00000117713\", \"doc_count\": 1}, {\"key\": \"ENSG00000121879\", \"doc_count\": 1}, {\"key\": \"ENSG00000157764\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 60}, \"doc_count\": 44120}, \"key\": \"TCGA-ACC\", \"doc_count\": 30}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000196712\", \"doc_count\": 15}, {\"key\": \"ENSG00000085224\", \"doc_count\": 5}, {\"key\": \"ENSG00000083857\", \"doc_count\": 2}, {\"key\": \"ENSG00000055609\", \"doc_count\": 1}, {\"key\": \"ENSG00000134982\", \"doc_count\": 1}, {\"key\": \"ENSG00000138413\", \"doc_count\": 1}, {\"key\": \"ENSG00000140836\", \"doc_count\": 1}, {\"key\": \"ENSG00000141510\", \"doc_count\": 1}, {\"key\": \"ENSG00000157764\", \"doc_count\": 1}, {\"key\": \"ENSG00000173821\", \"doc_count\": 1}, {\"key\": \"ENSG00000196159\", \"doc_count\": 1}, {\"key\": \"ENSG00000196367\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 31}, \"doc_count\": 18895}, \"key\": \"TCGA-PCPG\", \"doc_count\": 29}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000133703\", \"doc_count\": 13}, {\"key\": \"ENSG00000121879\", \"doc_count\": 3}, {\"key\": \"ENSG00000055609\", \"doc_count\": 2}, {\"key\": \"ENSG00000196159\", \"doc_count\": 2}, {\"key\": \"ENSG00000196712\", \"doc_count\": 2}, {\"key\": \"ENSG00000083857\", \"doc_count\": 1}, {\"key\": \"ENSG00000117713\", \"doc_count\": 1}, {\"key\": \"ENSG00000127914\", \"doc_count\": 1}, {\"key\": \"ENSG00000140836\", \"doc_count\": 1}, {\"key\": \"ENSG00000141510\", \"doc_count\": 1}, {\"key\": \"ENSG00000149311\", \"doc_count\": 1}, {\"key\": \"ENSG00000167548\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 29}, \"doc_count\": 22162}, \"key\": \"TCGA-TGCT\", \"doc_count\": 28}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000117713\", \"doc_count\": 8}, {\"key\": \"ENSG00000138413\", \"doc_count\": 6}, {\"key\": \"ENSG00000141510\", \"doc_count\": 5}, {\"key\": \"ENSG00000055609\", \"doc_count\": 3}, {\"key\": \"ENSG00000121879\", \"doc_count\": 3}, {\"key\": \"ENSG00000133703\", \"doc_count\": 2}, {\"key\": \"ENSG00000140836\", \"doc_count\": 2}, {\"key\": \"ENSG00000149311\", \"doc_count\": 2}, {\"key\": \"ENSG00000167548\", \"doc_count\": 2}, {\"key\": \"ENSG00000173821\", \"doc_count\": 2}, {\"key\": \"ENSG00000196712\", \"doc_count\": 2}, {\"key\": \"ENSG00000083857\", \"doc_count\": 1}, {\"key\": \"ENSG00000134982\", \"doc_count\": 1}, {\"key\": \"ENSG00000157764\", \"doc_count\": 1}, {\"key\": \"ENSG00000171862\", \"doc_count\": 1}, {\"key\": \"ENSG00000183454\", \"doc_count\": 1}, {\"key\": \"ENSG00000196367\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 43}, \"doc_count\": 30033}, \"key\": \"TCGA-CHOL\", \"doc_count\": 27}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000167548\", \"doc_count\": 12}, {\"key\": \"ENSG00000196159\", \"doc_count\": 8}, {\"key\": \"ENSG00000083857\", \"doc_count\": 4}, {\"key\": \"ENSG00000117713\", \"doc_count\": 4}, {\"key\": \"ENSG00000141510\", \"doc_count\": 4}, {\"key\": \"ENSG00000127914\", \"doc_count\": 2}, {\"key\": \"ENSG00000133703\", \"doc_count\": 2}, {\"key\": \"ENSG00000183454\", \"doc_count\": 2}, {\"key\": \"ENSG00000196712\", \"doc_count\": 2}, {\"key\": \"ENSG00000055609\", \"doc_count\": 1}, {\"key\": \"ENSG00000085224\", \"doc_count\": 1}, {\"key\": \"ENSG00000134982\", \"doc_count\": 1}, {\"key\": \"ENSG00000140836\", \"doc_count\": 1}, {\"key\": \"ENSG00000149311\", \"doc_count\": 1}, {\"key\": \"ENSG00000157764\", \"doc_count\": 1}, {\"key\": \"ENSG00000171862\", \"doc_count\": 1}, {\"key\": \"ENSG00000173821\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 48}, \"doc_count\": 39050}, \"key\": \"TCGA-DLBC\", \"doc_count\": 27}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 12}, {\"key\": \"ENSG00000196159\", \"doc_count\": 4}, {\"key\": \"ENSG00000171862\", \"doc_count\": 2}, {\"key\": \"ENSG00000055609\", \"doc_count\": 1}, {\"key\": \"ENSG00000083857\", \"doc_count\": 1}, {\"key\": \"ENSG00000085224\", \"doc_count\": 1}, {\"key\": \"ENSG00000117713\", \"doc_count\": 1}, {\"key\": \"ENSG00000121879\", \"doc_count\": 1}, {\"key\": \"ENSG00000133703\", \"doc_count\": 1}, {\"key\": \"ENSG00000140836\", \"doc_count\": 1}, {\"key\": \"ENSG00000149311\", \"doc_count\": 1}, {\"key\": \"ENSG00000157764\", \"doc_count\": 1}, {\"key\": \"ENSG00000173821\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 28}, \"doc_count\": 29803}, \"key\": \"TCGA-MESO\", \"doc_count\": 26}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 16}, {\"key\": \"ENSG00000171862\", \"doc_count\": 5}, {\"key\": \"ENSG00000149311\", \"doc_count\": 2}, {\"key\": \"ENSG00000167548\", \"doc_count\": 2}, {\"key\": \"ENSG00000196159\", \"doc_count\": 2}, {\"key\": \"ENSG00000196367\", \"doc_count\": 2}, {\"key\": \"ENSG00000055609\", \"doc_count\": 1}, {\"key\": \"ENSG00000083857\", \"doc_count\": 1}, {\"key\": \"ENSG00000085224\", \"doc_count\": 1}, {\"key\": \"ENSG00000127914\", \"doc_count\": 1}, {\"key\": \"ENSG00000196712\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 34}, \"doc_count\": 8825}, \"key\": \"TCGA-KICH\", \"doc_count\": 24}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000141510\", \"doc_count\": 4}, {\"key\": \"ENSG00000196712\", \"doc_count\": 3}, {\"key\": \"ENSG00000055609\", \"doc_count\": 2}, {\"key\": \"ENSG00000140836\", \"doc_count\": 2}, {\"key\": \"ENSG00000173821\", \"doc_count\": 2}, {\"key\": \"ENSG00000196159\", \"doc_count\": 2}, {\"key\": \"ENSG00000133703\", \"doc_count\": 1}, {\"key\": \"ENSG00000138413\", \"doc_count\": 1}, {\"key\": \"ENSG00000157764\", \"doc_count\": 1}, {\"key\": \"ENSG00000183454\", \"doc_count\": 1}, {\"key\": \"ENSG00000196367\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 20}, \"doc_count\": 5378}, \"key\": \"TCGA-THYM\", \"doc_count\": 15}, {\"genes\": {\"my_genes\": {\"gene_id\": {\"buckets\": [{\"key\": \"ENSG00000083857\", \"doc_count\": 2}, {\"key\": \"ENSG00000134982\", \"doc_count\": 2}, {\"key\": \"ENSG00000117713\", \"doc_count\": 1}, {\"key\": \"ENSG00000127914\", \"doc_count\": 1}, {\"key\": \"ENSG00000167548\", \"doc_count\": 1}, {\"key\": \"ENSG00000183454\", \"doc_count\": 1}, {\"key\": \"ENSG00000196159\", \"doc_count\": 1}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}, \"doc_count\": 9}, \"doc_count\": 1666}, \"key\": \"TCGA-UVM\", \"doc_count\": 9}], \"sum_other_doc_count\": 0, \"doc_count_error_upper_bound\": 0}}, \"timed_out\": false}"
        }
      }
    }
  }
}


