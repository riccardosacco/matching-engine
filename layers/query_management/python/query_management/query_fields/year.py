def generate_year(query_year, max_score):
    score_year_range = str(max_score)
    score_year_fuzzy1 = str(max_score * 0.6)
    nested_year = {"nested": {"path": "providerData.productionYears", "score_mode": "max", "query": {"dis_max": {"queries": []}}}}  

    year_range2 = {
        "script_score": {
            "query": {
                "range": {
                    "providerData.productionYears.productionYear": {
                        "lte": int(query_year) + 2,
                        "gte": int(query_year) - 2,
                    },
                },
            },
            "script": {
                "source":
                "decayNumericLinear(params.origin, params.scale, params.offset, params.decay, doc['providerData.productionYears.productionYear'].value)*" + score_year_range,
                "params": {"origin": int(query_year), "scale": 1, "decay": 0.6, "offset": 0},
            },
        },
    }
    year_fuzzy1 = {
        "script_score": {
            "query": {
                "simple_query_string": {
                    "query": query_year + "~1",
                    "fields": ["providerData.productionYears.productionYear.text"],
                },
            },
            "script": {"source": score_year_fuzzy1 + "*(_score*1)/(((1-_score)*1)+1)"},
        },
    }

    nested_year["nested"]["query"]["dis_max"]["queries"].append(year_range2)
    nested_year["nested"]["query"]["dis_max"]["queries"].append(year_fuzzy1)

    return nested_year

def generate_empty_year(max_score):
    return {"script_score": {"query": {"bool": {"must_not": [{"nested": {"path": "providerData.productionYears","query": {"bool": {"must": {"exists": {"field": "providerData.productionYears"}}}}}}]}},"script": {"source": str(max_score)}}}