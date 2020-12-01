import re

from query_management.build_string_score import build_string_score

def generate_title(query_titles, max_score):
    score_title_exactMatchFuzzy = str(max_score)
    score_title_matchPhrase = str(max_score * 0.9)
    score_title_stopWords = str(max_score * 0.7)
    score_title_ORFuzzy = str(max_score * 0.4)

    nested_title = {"nested": {"path": "providerData.titles", "score_mode": "max", "query": {"dis_max": {"queries": []}}}}

    for query_title in query_titles:
        clearTitle = query_title.replace('-', '')
        splitTitle = re.sub(r"([a-z])([A-Z])", r"\1 \2", clearTitle).split(" ")
        # TITLE QUERY
        title_exactMatchFuzzy = {
            "script_score": {
                "query": {"match": {"providerData.titles.title.keyword": {"query": query_title, "fuzziness": "auto"}}},
                "script": {"source": score_title_exactMatchFuzzy + "*(_score*1)/(((1-_score)*1)+1)"},
            },
        }
    
        title_matchPhrase = {
            "script_score": {
                "query": {"match_phrase": { "providerData.titles.title": {"query": query_title}}},
                "script": {
                    "source": score_title_matchPhrase + build_string_score("titles.title",str(len(splitTitle))),
                },
            },
        }
    
        title_stopWords = {
            "script_score": {
                "query": {"match": { "providerData.titles.title.stopped": {"query": query_title, "fuzziness": "auto"}}},
                "script": {
                    "source": score_title_stopWords + "*(_score*1)/(((1-_score)*1)+1)",
                },
            },
        }
    
        title_ORFuzzy = {
            "script_score": {
                "query": {
                    "match": {
                        "providerData.titles.title": {
                            "query": query_title,
                            "fuzziness": "auto"
                        }
                    },
                },
                "script": {
                    "source": score_title_ORFuzzy + build_string_score("titles.title",str(len(splitTitle))),
                },
            },
        }
    
        nested_title["nested"]["query"]["dis_max"]["queries"].append(title_exactMatchFuzzy)
        nested_title["nested"]["query"]["dis_max"]["queries"].append(title_matchPhrase)
        nested_title["nested"]["query"]["dis_max"]["queries"].append(title_stopWords)
        nested_title["nested"]["query"]["dis_max"]["queries"].append(title_ORFuzzy)


    return nested_title