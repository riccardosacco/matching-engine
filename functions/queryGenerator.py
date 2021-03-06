import json

def lambda_handler(event, context):
    body = event["queryStringParameters"]

    query_title = body["query_title"]
    query_director = body["query_director"]
    query_year = body["query_year"]

    splitTitle = query_title.split(" ")
    cleanSplitTitle = query_title.split("-")
    query_director = query_director.replace(".", "")
    splitDirector = query_director.split(" ")

    output = {
        "query": {
            "nested": {
                "path": "providerData",
                "score_mode": "max",
                "query": {"bool": {"should": []}},
            },
        },
    }
    dismax_title = {"dis_max": {"queries": []}}
    dismax_director = {"dis_max": {"queries": []}}
    dismax_year = {"dis_max": {"queries": []}}

    # TITLE QUERY
    title_exactMatch = {
        "script_score": {
            "query": {"match": {"providerData.title.keyword": {"query": query_title}}},
            "script": {"source": "_score*50"},
        },
    }

    title_matchPhrase = {
        "script_score": {
            "query": {"span_near": {"clauses": [], "slop": 0, "in_order": True}},
            "script": {
                "source":
                "20*((_score/doc['providerData.title.length'].value)*doc['providerData.title.length'].value)/(((1-(_score/doc['providerData.title.length'].value))*doc['providerData.title.length'].value)+" +
                str(len(cleanSplitTitle)) +
                ")",
            },
        },
    }
    titleFuzzy1String = ""
    titleFuzzyString = ""

    for title in splitTitle:
        title_matchPhrase["script_score"]["query"]["span_near"]["clauses"].append({
            "span_multi": {"match": {"fuzzy": {"providerData.title": title}}},
        })
        titleFuzzy1String = titleFuzzy1String + title + "~1 "
        titleFuzzyString = titleFuzzyString + title + "~ "

    title_ORFuzzy1 = {
        "script_score": {
            "query": {
                "simple_query_string": {
                    "query": titleFuzzy1String,
                    "fields": ["providerData.title"],
                    "default_operator": "OR",
                },
            },
            "script": {
                "source":
                "15*((_score/doc['providerData.title.length'].value)*doc['providerData.title.length'].value)/(((1-(_score/doc['providerData.title.length'].value))*doc['providerData.title.length'].value)+" +
                str(len(cleanSplitTitle)) +
                ")",
            },
        },
    }
    title_ORFuzzy = {
        "script_score": {
            "query": {
                "simple_query_string": {
                    "query": titleFuzzyString,
                    "fields": ["providerData.title"],
                    "default_operator": "OR",
                },
            },
            "script": {
                "source":
                "10*((_score/doc['providerData.title.length'].value)*doc['providerData.title.length'].value)/(((1-(_score/doc['providerData.title.length'].value))*doc['providerData.title.length'].value)+" +
                str(len(cleanSplitTitle)) +
                ")",
            },
        },
    }

    dismax_title["dis_max"]["queries"].append(title_exactMatch)
    dismax_title["dis_max"]["queries"].append(title_matchPhrase)
    dismax_title["dis_max"]["queries"].append(title_ORFuzzy1)
    dismax_title["dis_max"]["queries"].append(title_ORFuzzy)

    # DIRECTOR QUERY

    directorFuzzy1String = ""
    directorFuzzyString = ""

    for director in splitDirector:
        directorFuzzy1String += director + "~1 "
        directorFuzzyString += director + "~ "

        initials = director[0]
        initialsDiractorFuzzyString = ""

        for director2 in splitDirector:
            if (director2 != director):
                initialsDiractorFuzzyString += director2 + "~ "
            else:
                initialsDiractorFuzzyString += initials + "* "
        director_InitialsFuzzy = {
            "script_score": {
                "query": {
                    "simple_query_string": {
                        "query": initialsDiractorFuzzyString,
                        "fields": ["providerData.director"],
                        "default_operator": "AND",
                    },
                },
                "script": {
                    "source":
                    "25*((_score/doc['providerData.director.length'].value)*doc['providerData.director.length'].value)/(((1-(_score/doc['providerData.director.length'].value))*doc['providerData.director.length'].value)+" +
                    str(len(splitDirector)) +
                    ")",
                },
            },
        }
        dismax_director["dis_max"]["queries"].append(director_InitialsFuzzy)

    director_ORFuzzy1 = {
        "script_score": {
            "query": {
                "simple_query_string": {
                    "query": directorFuzzy1String,
                    "fields": ["providerData.director"],
                    "default_operator": "OR",
                },
            },
            "script": {
                "source":
                "20*((_score/doc['providerData.director.length'].value))/(((1-(_score/doc['providerData.director.length'].value))*doc['providerData.director.length'].value)+" +
                str(len(splitDirector)) +
                ")",
            },
        },
    }
    director_ORFuzzy = {
        "script_score": {
            "query": {
                "simple_query_string": {
                    "query": directorFuzzyString,
                    "fields": ["providerData.director"],
                    "default_operator": "OR",
                },
            },
            "script": {
                "source":
                "10*((_score/doc['providerData.director.length'].value)*doc['providerData.director.length'].value)/(((1-(_score/doc['providerData.director.length'].value))*doc['providerData.director.length'].value)+" +
                str(len(splitDirector)) +
                ")",
            },
        },
    }

    dismax_director["dis_max"]["queries"].append(director_ORFuzzy1)
    dismax_director["dis_max"]["queries"].append(director_ORFuzzy)

    # YEAR QUERY
    year_range2 = {
        "script_score": {
            "query": {
                "range": {
                    "providerData.production_year": {
                        "lte": int(query_year) + 2,
                        "gte": int(query_year) - 2,
                    },
                },
            },
            "script": {
                "source":
                "decayNumericLinear(params.origin, params.scale, params.offset, params.decay, doc['providerData.production_year'].value)*25",
                "params": {"origin": int(query_year), "scale": 1, "decay": 0.6, "offset": 0},
            },
        },
    }
    year_fuzzy1 = {
        "script_score": {
            "query": {
                "simple_query_string": {
                    "query": query_year + "~1",
                    "fields": ["providerData.production_year.text"],
                },
            },
            "script": {"source": "15*(_score*1)/(((1-_score)*1)+1)"},
        },
    }

    dismax_year["dis_max"]["queries"].append(year_range2)
    dismax_year["dis_max"]["queries"].append(year_fuzzy1)

    output["query"]["nested"]["query"]["bool"]["should"].append(dismax_title)
    output["query"]["nested"]["query"]["bool"]["should"].append(dismax_year)
    output["query"]["nested"]["query"]["bool"]["should"].append(
        dismax_director)

    return {
        'statusCode': 200,
        'body': json.dumps(output)
    }
