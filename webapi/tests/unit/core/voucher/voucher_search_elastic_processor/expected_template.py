ExpectedTemplate1 = {
    "query": "Test Case 1",
    "size": 48,
    "from": 0,
    "sort": [],
    "filter": {"filter": []},
}
ExpectedTemplate2 = {
    "query": "Test Case 2",
    "size": 48,
    "from": 49,
    "sort": [],
    "filter": {"filter": []},
}
ExpectedTemplate3 = {
    "query": "Test Case 3",
    "size": 48,
    "from": 0,
    "sort": [],
    "filter": {
        "filter": [
            {
                "nested": {
                    "path": "brands",
                    "query": {"terms": {"brands.brand_name.keyword": ["Some brand"]}},
                }
            }
        ]
    },
}
ExpectedTemplate4 = {
    "query": "Test Case 4",
    "size": 48,
    "from": 0,
    "sort": [],
    "filter": {
        "filter": [
            {
                "nested": {
                    "path": "object_properties",
                    "query": {
                        "terms": {
                            "object_properties.category_name.keyword": ["Some Category"]
                        }
                    },
                }
            }
        ]
    },
}
ExpectedTemplate5 = {
    "query": "Test Case 5",
    "size": 48,
    "from": 0,
    "sort": [],
    "filter": {
        "filter": [
            {
                "nested": {
                    "path": "object_properties",
                    "query": {
                        "terms": {
                            "object_properties.department_name.keyword": [
                                "Some Department"
                            ]
                        }
                    },
                }
            }
        ]
    },
}
ExpectedTemplate6 = {
    "query": "Test Case 6",
    "size": 48,
    "from": 0,
    "sort": [],
    "filter": {"filter": []},
}
