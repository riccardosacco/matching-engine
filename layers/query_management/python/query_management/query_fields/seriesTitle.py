import re

from query_management.build_string_score import build_string_score

def generate_seriesTitle(query_seriesTitles, max_score):
    score_title_exactMatchFuzzy = str(max_score)
    score_title_matchPhrase = str(max_score * 0.9)
    score_title_stopWords = str(max_score * 0.7)
    score_title_ANDFuzzy = str(max_score * 0.4)

    nested_title = {"nested": {"path": "providerData.seriesTitles", "score_mode": "max", "query": {"dis_max": {"queries": []}}}}

    for query_seriesTitle in query_seriesTitles:
        clearTitle = query_seriesTitle.replace('-', '')
        splitTitle = re.sub(r"([a-z])([A-Z])", r"\1 \2", clearTitle).split(" ")
        # TITLE QUERY
        title_exactMatchFuzzy = {
            "script_score": {
                "query": {"match": {"providerData.seriesTitles.seriesTitle.keyword": {"query": query_seriesTitle, "fuzziness": "auto"}}},
                "script": {"source": score_title_exactMatchFuzzy + "*(_score*1)/(((1-_score)*1)+1)"},
            },
        }
    
        title_matchPhrase = {
            "script_score": {
                "query": {"match_phrase": { "providerData.seriesTitles.seriesTitle": {"query": query_seriesTitle}}},
                "script": {
                    "source": score_title_matchPhrase + build_string_score("seriesTitles.seriesTitle",str(len(splitTitle))),
                },
            },
        }
    
        title_stopWords = {
            "script_score": {
                "query": {"match": { "providerData.seriesTitles.seriesTitle.stopped": {"query": query_seriesTitle, "fuzziness": "auto"}}},
                "script": {
                    "source": score_title_stopWords + "*(_score*1)/(((1-_score)*1)+1)",
                },
            },
        }
    
        title_ANDFuzzy = {
            "script_score": {
                "query": {"match": { "providerData.seriesTitles.seriesTitle": { "query": query_seriesTitle, "fuzziness": "auto", "operator":"AND"}}},
                "script": {
                    "source": score_title_ANDFuzzy + build_string_score("seriesTitles.seriesTitle",str(len(splitTitle))),
                },
            },
        }
    
        nested_title["nested"]["query"]["dis_max"]["queries"].append(title_exactMatchFuzzy)
        nested_title["nested"]["query"]["dis_max"]["queries"].append(title_matchPhrase)
        nested_title["nested"]["query"]["dis_max"]["queries"].append(title_stopWords)
        nested_title["nested"]["query"]["dis_max"]["queries"].append(title_ANDFuzzy)


    return nested_title