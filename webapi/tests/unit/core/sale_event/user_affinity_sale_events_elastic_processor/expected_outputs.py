expected_query_output_01 = {
    "size": 50,
    "from": 0,
    "query": {
        "function_score": {
            "boost_mode": "replace",
            "query": {
                "bool": {
                    "must": [
                        {"term": {"is_top_sale_event": {"value": True}}},
                        {"range": {"score": {"gte": 0}}},
                        {"exists": {"field": "slug"}},
                    ],
                    "must_not": [],
                    "filter": [],
                }
            },
            "script_score": {
                "script": {
                    "id": "user-affinity-search",
                    "params": {
                        "items": [
                            {
                                "name": "Nike",
                                "cscore": 1.0,
                                "field": "brand_name.keyword",
                            },
                            {
                                "name": "Catch",
                                "cscore": 1.0,
                                "field": "store_name.keyword",
                            },
                            {
                                "name": "Fashion",
                                "cscore": 1.0,
                                "field": "department_name.keyword",
                            },
                            {
                                "name": "Phones, Smart Watches & Accessories",
                                "cscore": 1.0,
                                "field": "category_name.keyword",
                            },
                            {
                                "name": "Phones",
                                "cscore": 1.0,
                                "field": "subcategory_name.keyword",
                            },
                        ],
                        "gender": "",
                    },
                },
            },
        }
    },
}

expected_query_output_02 = {
    "size": 50,
    "from": 0,
    "query": {
        "function_score": {
            "boost_mode": "replace",
            "query": {
                "bool": {
                    "must": [
                        {"term": {"is_top_sale_event": {"value": True}}},
                        {"range": {"score": {"gte": 0}}},
                        {"exists": {"field": "slug"}},
                    ],
                    "must_not": [],
                    "filter": [
                        {"terms": {"store_name.keyword": ["Nike"]}},
                        {"terms": {"brand_name.keyword": ["Nikon"]}},
                        {"terms": {"department_name.keyword": ["Fashion"]}},
                        {
                            "terms": {
                                "category_name.keyword": [
                                    "Computer Accessories & Network Hardware"
                                ]
                            }
                        },
                        {"terms": {"subcategory_name.keyword": ["Computer"]}},
                    ],
                },
            },
            "script_score": {
                "script": {
                    "id": "user-affinity-search",
                    "params": {
                        "items": [],
                        "gender": "",
                    },
                }
            },
        }
    },
}

expected_query_output_03 = {
    "size": 50,
    "from": 0,
    "query": {
        "function_score": {
            "boost_mode": "replace",
            "query": {
                "bool": {
                    "minimum_should_match": 1,
                    "must": [
                        {"term": {"is_top_sale_event": {"value": True}}},
                        {"range": {"score": {"gte": 0}}},
                        {"exists": {"field": "slug"}},
                    ],
                    "must_not": [],
                    "filter": [],
                    "should": [
                        {"term": {"category_gender_affinity": {"value": "M"}}},
                        {
                            "nested": {
                                "path": "object_properties",
                                "query": {
                                    "term": {
                                        "object_properties.category_gender_affinity": {
                                            "value": "M"
                                        }
                                    }
                                },
                            }
                        },
                        {
                            "bool": {
                                "must": [
                                    {
                                        "bool": {
                                            "must_not": [
                                                {
                                                    "exists": {
                                                        "field": "category_gender_affinity"
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        "bool": {
                                            "must_not": [
                                                {
                                                    "nested": {
                                                        "path": "object_properties",
                                                        "query": {
                                                            "exists": {
                                                                "field": "object_properties.category_gender_affinity"
                                                            }
                                                        },
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                ]
                            }
                        },
                    ],
                }
            },
            "script_score": {
                "script": {
                    "id": "user-affinity-search",
                    "params": {
                        "items": [],
                        "gender": "",
                    },
                },
            },
        }
    },
}
expected_query_output_04 = {
    "size": 50,
    "from": 0,
    "query": {
        "function_score": {
            "boost_mode": "replace",
            "query": {
                "bool": {
                    "minimum_should_match": 1,
                    "must": [
                        {"term": {"is_top_sale_event": {"value": True}}},
                        {"range": {"score": {"gte": 0}}},
                        {"exists": {"field": "slug"}},
                    ],
                    "must_not": [],
                    "filter": [],
                    "should": [
                        {"term": {"category_gender_affinity": {"value": "F"}}},
                        {
                            "nested": {
                                "path": "object_properties",
                                "query": {
                                    "term": {
                                        "object_properties.category_gender_affinity": {
                                            "value": "F"
                                        }
                                    }
                                },
                            }
                        },
                        {
                            "bool": {
                                "must": [
                                    {
                                        "bool": {
                                            "must_not": [
                                                {
                                                    "exists": {
                                                        "field": "category_gender_affinity"
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        "bool": {
                                            "must_not": [
                                                {
                                                    "nested": {
                                                        "path": "object_properties",
                                                        "query": {
                                                            "exists": {
                                                                "field": "object_properties.category_gender_affinity"
                                                            }
                                                        },
                                                    }
                                                }
                                            ]
                                        }
                                    },
                                ]
                            }
                        },
                    ],
                }
            },
            "script_score": {
                "script": {
                    "id": "user-affinity-search",
                    "params": {
                        "items": [],
                        "gender": "",
                    },
                },
            },
        }
    },
}

expected_parse_response_output_01 = []

expected_parse_response_output_02 = [
    {
        "archived_at": "1970-01-01T10:00:00+10:00",
        "brand_name": None,
        "category_name": "Women's Clothing",
        "department_name": "Fashion",
        "expire_at": "2024-03-02T23:50:00+11:00",
        "fixed_global_score": "1128",
        "id": "296414",
        "impressions_count": "93",
        "name": "30% off women's dresses",
        "offer_text": "30% off",
        "published_at": "2024-02-29T08:03:50.440000+11:00",
        "sale_event_image": "https://assets.littlebirdie.com.au/uploads/sale_event/sale_event_image/296414/Copy_of_myer_dresses.jpg",
        "slug": "30-off-womens-dresses-1709154230",
        "start_at": "2024-02-29T02:00:00+11:00",
        "store_logo": "https://media.littlebirdie.com.au/store/2_2023-06-15141715.204.jpg",
        "store_name": "Myer",
        "type": None,
        "url": "https://myer.sjv.io/c/2561188/1279730/15706?u=https%3A//www.myer.com.au/c/myer-one/myer-one-sale-women/women-clothing-myer-one/women-dresses-myer-one",
    },
    {
        "archived_at": "1970-01-01T10:00:00+10:00",
        "brand_name": None,
        "category_name": "Audio & Headphones",
        "department_name": "Electronics",
        "expire_at": "2024-03-01T23:50:00+11:00",
        "fixed_global_score": "1027",
        "id": "296276",
        "impressions_count": "22",
        "name": "15% off huge range of audio",
        "offer_text": "15% off",
        "published_at": "2024-02-28T08:24:29.731000+11:00",
        "sale_event_image": "https://assets.littlebirdie.com.au/uploads/sale_event/sale_event_image/296276/Copy_of_Master_Template-Black__46_.png",
        "slug": "15-off-huge-range-of-audio-1709069069",
        "start_at": "2024-02-28T02:00:00+11:00",
        "store_logo": "https://media.littlebirdie.com.au/store/7_2022-12-02175011.073.jpg",
        "store_name": "The Good Guys",
        "type": None,
        "url": "https://prf.hn/click/camref:1011ljkyT/destination:https%3A//www.thegoodguys.com.au/buy/headphone-and-soundbar-sale%23facet%3A5750149533280114111109111116105111110484850",
    },
    {
        "archived_at": "1970-01-01T10:00:00+10:00",
        "brand_name": None,
        "category_name": "Women's Activewear",
        "department_name": "Fashion",
        "expire_at": "2024-03-05T23:50:00+11:00",
        "fixed_global_score": "1017",
        "id": "296412",
        "impressions_count": "13",
        "name": "20% off sports top picks",
        "offer_text": "20% off",
        "published_at": "2024-02-29T08:01:35.909000+11:00",
        "sale_event_image": "https://assets.littlebirdie.com.au/uploads/sale_event/sale_event_image/296412/Copy_of_Master_Template-Black__47_.png",
        "slug": "20-off-sports-top-picks-1709154095",
        "start_at": "2024-02-29T02:00:00+11:00",
        "store_logo": "https://media.littlebirdie.com.au/store/17_2022-12-02114929.814.jpg",
        "store_name": "The Iconic",
        "type": None,
        "url": "https://prf.hn/click/camref:1011lfQEb/destination:https%3A//www.theiconic.com.au/womens-sports-all/%3Fcampaign%3Dlp-wmksbh-30-top-picks-0924-v2%26page%3D1%26sort%3Dpopularity",
    },
]

expected_parse_response_output_03 = [
    {
        "archived_at": "1970-01-01T10:00:00+10:00",
        "brand_name": None,
        "category_name": "Women's Clothing",
        "department_name": "Fashion",
        "expire_at": "2024-03-02T23:50:00+11:00",
        "fixed_global_score": "1128",
        "id": "296414",
        "impressions_count": "93",
        "name": "30% off women's dresses",
        "offer_text": "30% off",
        "published_at": "2024-02-29T08:03:50.440000+11:00",
        "sale_event_image": "https://assets.littlebirdie.com.au/uploads/sale_event/sale_event_image/296414/Copy_of_myer_dresses.jpg",
        "slug": "30-off-womens-dresses-1709154230",
        "start_at": "2024-02-29T02:00:00+11:00",
        "store_logo": "https://media.littlebirdie.com.au/store/2_2023-06-15141715.204.jpg",
        "store_name": "Myer",
        "type": None,
        "url": "https://myer.sjv.io/c/2561188/1279730/15706?u=https%3A//www.myer.com.au/c/myer-one/myer-one-sale-women/women-clothing-myer-one/women-dresses-myer-one",
    },
    {
        "archived_at": "1970-01-01T10:00:00+10:00",
        "brand_name": None,
        "category_name": "Audio & Headphones",
        "department_name": "Electronics",
        "expire_at": "2024-03-01T23:50:00+11:00",
        "fixed_global_score": "1027",
        "id": "296276",
        "impressions_count": "22",
        "name": "15% off huge range of audio",
        "offer_text": "15% off",
        "published_at": "2024-02-28T08:24:29.731000+11:00",
        "sale_event_image": "https://assets.littlebirdie.com.au/uploads/sale_event/sale_event_image/296276/Copy_of_Master_Template-Black__46_.png",
        "slug": "15-off-huge-range-of-audio-1709069069",
        "start_at": "2024-02-28T02:00:00+11:00",
        "store_logo": "https://media.littlebirdie.com.au/store/7_2022-12-02175011.073.jpg",
        "store_name": "The Good Guys",
        "type": None,
        "url": "https://prf.hn/click/camref:1011ljkyT/destination:https%3A//www.thegoodguys.com.au/buy/headphone-and-soundbar-sale%23facet%3A5750149533280114111109111116105111110484850",
    },
    {
        "archived_at": "1970-01-01T10:00:00+10:00",
        "brand_name": None,
        "category_name": "Bedding",
        "department_name": "Home & Kitchen",
        "expire_at": "2024-03-02T23:50:00+11:00",
        "fixed_global_score": "1026",
        "id": "296411",
        "impressions_count": "20",
        "name": "50% off great range of homewares",
        "offer_text": "50% off",
        "published_at": "2024-02-29T07:58:41.878000+11:00",
        "sale_event_image": "https://assets.littlebirdie.com.au/uploads/sale_event/sale_event_image/296411/Copy_of_Master_Template-Black__48_.png",
        "slug": "50-off-great-range-of-homewares-1709153921",
        "start_at": "2024-02-29T02:00:00+11:00",
        "store_logo": "https://media.littlebirdie.com.au/store/2_2023-06-15141715.204.jpg",
        "store_name": "Myer",
        "type": None,
        "url": "https://myer.sjv.io/c/2561188/1279730/15706?u=https%3A//www.myer.com.au/c/myer-one/myer-one-sale-home%3Ffacets%3Dmv--sale_type--502520off%26pageNumber%3D1%26promo_position%3DHomepage%257C3%257C2%257Ctile-master%26promo_id%3D2512f9cd-cd25-42fc-a8bd-cfaca512888c%26promo_creative%3DMaster__03__1x1.jpg%26promo_name%3D2024-02-23%257CAW24-HP-CONTENT%257CNon%2520promo%23filter-buttons",
    },
]
