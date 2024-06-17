# This response was frankensteined from three query responses. `coffee` and `nik` and `fashion`
MockElasticSearchResponse01 = {
    "took": 6,
    "responses": [
        {
            "took": 4,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 3, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "preemptive_category_suggestion": {
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0,
                    "buckets": [
                        {"key": "Coffee & Beverage Machines", "doc_count": 2},
                        {"key": "Audio & Headphones", "doc_count": 1},
                    ],
                },
                "preemptive_subcategory_suggestion": {
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0,
                    "buckets": [
                        {"key": "Coffee Machines", "doc_count": 2},
                        {"key": "Audio Docks & Mini Speakers", "doc_count": 1},
                    ],
                },
            },
        },
        {
            "took": 0,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 0, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "store_main": {
                    "doc_count": 78,
                    "store_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "Nike AU",
                                "doc_count": 78,
                                "store_details": {
                                    "hits": {
                                        "total": {"value": 78, "relation": "eq"},
                                        "max_score": 17.957478,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "949097957",
                                                "_score": 17.957478,
                                                "_source": {
                                                    "store_logo": "https://media.littlebirdie.com.au/store/410_new_2022-12-09092325.615.jpg",
                                                    "store_name": "Nike AU",
                                                    "store_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                        ],
                    },
                },
                "brand_main": {
                    "doc_count": 645,
                    "brand_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "Nike",
                                "doc_count": 475,
                                "brand_details": {
                                    "hits": {
                                        "total": {"value": 475, "relation": "eq"},
                                        "max_score": 17.957478,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "949097957",
                                                "_score": 17.957478,
                                                "_source": {
                                                    "brand_slug": None,
                                                    "brand_name": "Nike",
                                                    "brand_logo": "https://media.littlebirdie.com.au/brand/144104325_2021-10-15051127.438.jpg",
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "took": 1,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 4, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "category_main": {
                    "doc_count": 315,
                    "category_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "coffee & beverage machines",
                                "doc_count": 292,
                                "category_details": {
                                    "hits": {
                                        "total": {"value": 292, "relation": "eq"},
                                        "max_score": 7.1797476,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "1106933473",
                                                "_score": 7.1797476,
                                                "_source": {
                                                    "category_name": "Coffee & Beverage Machines",
                                                    "category_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                            {
                                "key": "tea & coffee",
                                "doc_count": 23,
                                "category_details": {
                                    "hits": {
                                        "total": {"value": 23, "relation": "eq"},
                                        "max_score": 7.4819403,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "1091758586",
                                                "_score": 7.4819403,
                                                "_source": {
                                                    "category_name": "Tea & Coffee",
                                                    "category_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                        ],
                    },
                },
                "department_main": {
                    "doc_count": 2737,
                    "department_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "fashion",
                                "doc_count": 2737,
                                "department_details": {
                                    "hits": {
                                        "total": {"value": 2737, "relation": "eq"},
                                        "max_score": 10.095774,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "1166376976",
                                                "_score": 10.095774,
                                                "_source": {
                                                    "department_name": "Fashion",
                                                    "department_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            }
                        ],
                    },
                },
                "subcategory_main": {
                    "doc_count": 313,
                    "subcategory_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "coffee machines",
                                "doc_count": 290,
                                "subcategory_details": {
                                    "hits": {
                                        "total": {"value": 290, "relation": "eq"},
                                        "max_score": 7.1797476,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "1106933473",
                                                "_score": 7.1797476,
                                                "_source": {
                                                    "subcategory_name": "Coffee Machines",
                                                    "subcategory_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                            {
                                "key": "coffee",
                                "doc_count": 23,
                                "subcategory_details": {
                                    "hits": {
                                        "total": {"value": 23, "relation": "eq"},
                                        "max_score": 7.4819403,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "1091758586",
                                                "_score": 7.4819403,
                                                "_source": {
                                                    "subcategory_name": "Coffee",
                                                    "subcategory_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "took": 5,
            "timed_out": False,
            "_shards": {"total": 2, "successful": 2, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 279, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "product_suggestion": {
                    "doc_count_error_upper_bound": -1,
                    "sum_other_doc_count": 223,
                    "buckets": [
                        {
                            "key": "Breville the Barista Touch™ Coffee Machine (Black Truffle)",
                            "doc_count": 2,
                            "total_page_view": {"value": 278},
                        },
                        {
                            "key": "Baccarat Barista Brillante 6 Cup Stovetop Espresso Coffee Maker",
                            "doc_count": 1,
                            "total_page_view": {"value": 248},
                        },
                        {
                            "key": "Breville The Barista Express Coffee Machine - Stainless Steel",
                            "doc_count": 1,
                            "total_page_view": {"value": 194},
                        },
                        {
                            "key": "DeLonghi La Specialista Arte Manual Pump Coffee Machine",
                            "doc_count": 3,
                            "total_page_view": {"value": 140},
                        },
                    ],
                }
            },
        },
        {
            "took": 0,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 1, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "pagecontext_suggest": {
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0,
                    "buckets": [{"key": "Electronics", "doc_count": 1}],
                }
            },
        },
    ],
}

MockElasticSearchResponse02 = {
    "took": 6,
    "responses": [
        {
            "took": 4,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 3, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "preemptive_category_suggestion": {
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0,
                    "buckets": [],
                },
                "preemptive_subcategory_suggestion": {
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0,
                    "buckets": [],
                },
            },
        },
        {
            "took": 0,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 0, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "store_main": {
                    "doc_count": 78,
                    "store_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [],
                    },
                },
                "brand_main": {
                    "doc_count": 645,
                    "brand_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [],
                    },
                },
            },
        },
        {
            "took": 1,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 4, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "category_main": {
                    "doc_count": 315,
                    "category_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [],
                    },
                },
                "department_main": {
                    "doc_count": 2737,
                    "department_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [],
                    },
                },
                "subcategory_main": {
                    "doc_count": 313,
                    "subcategory_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [],
                    },
                },
            },
        },
        {
            "took": 0,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 1, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "pagecontext_suggest": {
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0,
                    "buckets": [],
                }
            },
        },
    ],
}

# Same response as MockElasticSearchResponse01 but without pagecontext_suggest
MockElasticSearchResponse03 = {
    "took": 6,
    "responses": [
        {
            "took": 4,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 3, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "preemptive_category_suggestion": {
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0,
                    "buckets": [
                        {"key": "Coffee & Beverage Machines", "doc_count": 2},
                        {"key": "Audio & Headphones", "doc_count": 1},
                    ],
                },
                "preemptive_subcategory_suggestion": {
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0,
                    "buckets": [
                        {"key": "Coffee Machines", "doc_count": 2},
                        {"key": "Audio Docks & Mini Speakers", "doc_count": 1},
                    ],
                },
            },
        },
        {
            "took": 0,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 0, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "store_main": {
                    "doc_count": 78,
                    "store_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "Nike AU",
                                "doc_count": 78,
                                "store_details": {
                                    "hits": {
                                        "total": {"value": 78, "relation": "eq"},
                                        "max_score": 17.957478,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "949097957",
                                                "_score": 17.957478,
                                                "_source": {
                                                    "store_logo": "https://media.littlebirdie.com.au/store/410_new_2022-12-09092325.615.jpg",
                                                    "store_name": "Nike AU",
                                                    "store_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                        ],
                    },
                },
                "brand_main": {
                    "doc_count": 645,
                    "brand_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "Nike",
                                "doc_count": 475,
                                "brand_details": {
                                    "hits": {
                                        "total": {"value": 475, "relation": "eq"},
                                        "max_score": 17.957478,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "949097957",
                                                "_score": 17.957478,
                                                "_source": {
                                                    "brand_slug": None,
                                                    "brand_name": "Nike",
                                                    "brand_logo": "https://media.littlebirdie.com.au/brand/144104325_2021-10-15051127.438.jpg",
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "took": 1,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 4, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "category_main": {
                    "doc_count": 315,
                    "category_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "coffee & beverage machines",
                                "doc_count": 292,
                                "category_details": {
                                    "hits": {
                                        "total": {"value": 292, "relation": "eq"},
                                        "max_score": 7.1797476,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "1106933473",
                                                "_score": 7.1797476,
                                                "_source": {
                                                    "category_name": "Coffee & Beverage Machines",
                                                    "category_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                            {
                                "key": "tea & coffee",
                                "doc_count": 23,
                                "category_details": {
                                    "hits": {
                                        "total": {"value": 23, "relation": "eq"},
                                        "max_score": 7.4819403,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "1091758586",
                                                "_score": 7.4819403,
                                                "_source": {
                                                    "category_name": "Tea & Coffee",
                                                    "category_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                        ],
                    },
                },
                "department_main": {
                    "doc_count": 2737,
                    "department_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "fashion",
                                "doc_count": 2737,
                                "department_details": {
                                    "hits": {
                                        "total": {"value": 2737, "relation": "eq"},
                                        "max_score": 10.095774,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "1166376976",
                                                "_score": 10.095774,
                                                "_source": {
                                                    "department_name": "Fashion",
                                                    "department_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            }
                        ],
                    },
                },
                "subcategory_main": {
                    "doc_count": 313,
                    "subcategory_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "coffee machines",
                                "doc_count": 290,
                                "subcategory_details": {
                                    "hits": {
                                        "total": {"value": 290, "relation": "eq"},
                                        "max_score": 7.1797476,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "1106933473",
                                                "_score": 7.1797476,
                                                "_source": {
                                                    "subcategory_name": "Coffee Machines",
                                                    "subcategory_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                            {
                                "key": "coffee",
                                "doc_count": 23,
                                "subcategory_details": {
                                    "hits": {
                                        "total": {"value": 23, "relation": "eq"},
                                        "max_score": 7.4819403,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "1091758586",
                                                "_score": 7.4819403,
                                                "_source": {
                                                    "subcategory_name": "Coffee",
                                                    "subcategory_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "took": 5,
            "timed_out": False,
            "_shards": {"total": 2, "successful": 2, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 279, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "product_suggestion": {
                    "doc_count_error_upper_bound": -1,
                    "sum_other_doc_count": 223,
                    "buckets": [
                        {
                            "key": "Breville the Barista Touch™ Coffee Machine (Black Truffle)",
                            "doc_count": 2,
                            "total_page_view": {"value": 278},
                        },
                        {
                            "key": "Baccarat Barista Brillante 6 Cup Stovetop Espresso Coffee Maker",
                            "doc_count": 1,
                            "total_page_view": {"value": 248},
                        },
                        {
                            "key": "Breville The Barista Express Coffee Machine - Stainless Steel",
                            "doc_count": 1,
                            "total_page_view": {"value": 194},
                        },
                        {
                            "key": "DeLonghi La Specialista Arte Manual Pump Coffee Machine",
                            "doc_count": 3,
                            "total_page_view": {"value": 140},
                        },
                    ],
                }
            },
        },
    ],
}

MockElasticSearchResponse04 = {
    "took": 6,
    "responses": [
        {"error": {}},
        {
            "took": 0,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 0, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "store_main": {
                    "doc_count": 78,
                    "store_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "Nike AU",
                                "doc_count": 78,
                                "store_details": {
                                    "hits": {
                                        "total": {"value": 78, "relation": "eq"},
                                        "max_score": 17.957478,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "949097957",
                                                "_score": 17.957478,
                                                "_source": {
                                                    "store_logo": "https://media.littlebirdie.com.au/store/410_new_2022-12-09092325.615.jpg",
                                                    "store_name": "Nike AU",
                                                    "store_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                        ],
                    },
                },
                "brand_main": {
                    "doc_count": 645,
                    "brand_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "Nike",
                                "doc_count": 475,
                                "brand_details": {
                                    "hits": {
                                        "total": {"value": 475, "relation": "eq"},
                                        "max_score": 17.957478,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "949097957",
                                                "_score": 17.957478,
                                                "_source": {
                                                    "brand_slug": None,
                                                    "brand_name": "Nike",
                                                    "brand_logo": "https://media.littlebirdie.com.au/brand/144104325_2021-10-15051127.438.jpg",
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "took": 1,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 4, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "category_main": {
                    "doc_count": 315,
                    "category_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "coffee & beverage machines",
                                "doc_count": 292,
                                "category_details": {
                                    "hits": {
                                        "total": {"value": 292, "relation": "eq"},
                                        "max_score": 7.1797476,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "1106933473",
                                                "_score": 7.1797476,
                                                "_source": {
                                                    "category_name": "Coffee & Beverage Machines",
                                                    "category_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                            {
                                "key": "tea & coffee",
                                "doc_count": 23,
                                "category_details": {
                                    "hits": {
                                        "total": {"value": 23, "relation": "eq"},
                                        "max_score": 7.4819403,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "1091758586",
                                                "_score": 7.4819403,
                                                "_source": {
                                                    "category_name": "Tea & Coffee",
                                                    "category_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                        ],
                    },
                },
                "department_main": {
                    "doc_count": 2737,
                    "department_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "fashion",
                                "doc_count": 2737,
                                "department_details": {
                                    "hits": {
                                        "total": {"value": 2737, "relation": "eq"},
                                        "max_score": 10.095774,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "1166376976",
                                                "_score": 10.095774,
                                                "_source": {
                                                    "department_name": "Fashion",
                                                    "department_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            }
                        ],
                    },
                },
                "subcategory_main": {
                    "doc_count": 313,
                    "subcategory_suggestion": {
                        "doc_count_error_upper_bound": 0,
                        "sum_other_doc_count": 0,
                        "buckets": [
                            {
                                "key": "coffee machines",
                                "doc_count": 290,
                                "subcategory_details": {
                                    "hits": {
                                        "total": {"value": 290, "relation": "eq"},
                                        "max_score": 7.1797476,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "1106933473",
                                                "_score": 7.1797476,
                                                "_source": {
                                                    "subcategory_name": "Coffee Machines",
                                                    "subcategory_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                            {
                                "key": "coffee",
                                "doc_count": 23,
                                "subcategory_details": {
                                    "hits": {
                                        "total": {"value": 23, "relation": "eq"},
                                        "max_score": 7.4819403,
                                        "hits": [
                                            {
                                                "_index": "e_deals_autocomplete_20240219",
                                                "_id": "1091758586",
                                                "_score": 7.4819403,
                                                "_source": {
                                                    "subcategory_name": "Coffee",
                                                    "subcategory_slug": None,
                                                },
                                            }
                                        ],
                                    }
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "took": 0,
            "timed_out": False,
            "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
            "hits": {
                "total": {"value": 1, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
            "aggregations": {
                "pagecontext_suggest": {
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0,
                    "buckets": [{"key": "Electronics", "doc_count": 1}],
                }
            },
        },
    ],
}
