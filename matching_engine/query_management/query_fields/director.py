import re

from query_management.build_string_score import build_string_score

def generate_director(query_directors, max_score):
    score_director_ORFuzzy = str(max_score)
    score_director_InitialsFuzzy = str(max_score * 0.8)
    score_director_Initials = str(max_score * 0.6)

    nested_director = {"nested": {"path": "providerData.directors", "score_mode": "max", "query": {"dis_max": {"queries": []}}}}

    for director in query_directors:
        single_director = director.lstrip().rstrip()
        clearDirector = single_director.replace('-', '')
        splitDirector = re.sub(r"([a-z])([A-Z])", r"\1 \2", clearDirector).split(" ")
        directorFuzzyString = ""
        for directorName in splitDirector:
            initials = directorName[0]
            initialsDiractorFuzzyString = ""

            for directorName2 in splitDirector:
                if (directorName2 != directorName):
                    initialsDiractorFuzzyString += directorName2 + " "
                else:
                    initialsDiractorFuzzyString += initials + ". "

            director_InitialsFuzzy = {
                "script_score": {
                    "query": {
                        "match": {
                            "providerData.directors.director": {
                                "query": initialsDiractorFuzzyString,
                                "fuzziness": "auto",
                                "operator": "AND"
                            }
                        },
                    },
                    "script": {
                        "source": score_director_InitialsFuzzy +
                        build_string_score("directors.director",str(len(splitDirector))),
                    },
                },
            }
            nested_director["nested"]["query"]["dis_max"]["queries"].append(director_InitialsFuzzy)

        director_ORFuzzy = {
            "script_score": {
                "query": {
                    "match": {
                        "providerData.directors.director": {
                            "query": director,
                            "fuzziness": "auto"
                        }
                    },
                },
                "script": {
                    "source": score_director_ORFuzzy + build_string_score("directors.director",str(len(splitDirector))),
                },
            },
        }

        director_Initials = {
            "script_score": {
                "query": {
                    "simple_query_string" : {
                        "query": single_director.replace('.', '*'),
                        "fields": ["providerData.directors.director"],
                        "default_operator": "and"
                    },
                },
                "script": {
                    "source": score_director_Initials + build_string_score("directors.director",str(len(splitDirector))),
                },
            },
        }

        nested_director["nested"]["query"]["dis_max"]["queries"].append(director_ORFuzzy)
        nested_director["nested"]["query"]["dis_max"]["queries"].append(director_Initials)

    return nested_director