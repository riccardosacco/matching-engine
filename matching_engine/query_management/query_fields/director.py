import re

from query_management.build_string_score import build_string_score

def generate_director(query_directors, max_score):
    score_director_ORFuzzy = str(max_score)
    score_director_InitialsFuzzy = str(max_score * 0.8)
    score_director_Initials = str(max_score * 0.6)

    nested_director = {"nested": {"path": "providerData.directors", "score_mode": "max", "query": {"dis_max": {"queries": []}}}}

    for director in query_directors:
        single_director = director.lstrip().rstrip()
        clearDirector = re.sub(r"([a-z])([A-Z])", r"\1 \2", single_director.replace('-', ''))
        splitDirector = clearDirector.split(" ")
        director_ORFuzzy = {
            "script_score": { "query": { "match": { "providerData.directors.director": { "query": clearDirector, "fuzziness": "auto"}}},
                "script": {
                    "source": score_director_ORFuzzy + build_string_score("directors.director",str(len(splitDirector))),
                },
            },
        }
        nested_director["nested"]["query"]["dis_max"]["queries"].append(director_ORFuzzy)

        if "." not in clearDirector:
            for directorName in splitDirector:
                initials = directorName[0]
                initialsDiractorFuzzyString = ""

                for directorName2 in splitDirector:
                    if (directorName2 != directorName):
                        initialsDiractorFuzzyString += directorName2 + " "
                    else:
                        initialsDiractorFuzzyString += initials + ". "

                director_InitialsFuzzy = {
                    "script_score": { "query": { "match": { "providerData.directors.director": { "query": initialsDiractorFuzzyString.rstrip(), "fuzziness": "auto", "operator": "AND"}}},
                        "script": {
                            "source": score_director_InitialsFuzzy + build_string_score("directors.director",str(len(splitDirector))),
                        },
                    },
                }
                nested_director["nested"]["query"]["dis_max"]["queries"].append(director_InitialsFuzzy)

        if "." in clearDirector:
            director_Initials = {
                "script_score": { "query": { "simple_query_string" : { "query": clearDirector.replace('.', '*'), "fields": ["providerData.directors.director"], "default_operator": "AND"}},
                    "script": {
                        "source": score_director_Initials + build_string_score("directors.director",str(len(splitDirector))),
                    },
                },
            }
            nested_director["nested"]["query"]["dis_max"]["queries"].append(director_Initials)

    return nested_director

def generate_empty_director(max_score):
    return {"script_score": {"query": {"bool": {"must_not": [{"nested": {"path": "providerData.directors","query": {"bool": {"must": {"exists": {"field": "providerData.directors"}}}}}}]}},"script": {"source": str(max_score)}}}
