exports.handler = async (event) => {
  var { query_title, query_director, query_year } = event.queryStringParameters;

  var splitTitle = query_title.split(" ");
  var cleanSplitTitle = query_title.split("-");
  query_director = query_director.replace(".", "");
  var splitDirector = query_director.split(" ");

  var json = {
    query: {
      nested: {
        path: "providerData",
        score_mode: "max",
        query: { bool: { should: [] } },
      },
    },
  };
  var dismax_title = { dis_max: { queries: [] } };
  var dismax_director = { dis_max: { queries: [] } };
  var dismax_year = { dis_max: { queries: [] } };

  /******* TITLE QUERY *******/

  var title_exactMatch = {
    script_score: {
      query: {
        match: { "providerData.title.keyword": { query: query_title } },
      },
      script: { source: "_score*50" },
    },
  };

  var title_matchPhrase = {
    script_score: {
      query: { span_near: { clauses: [], slop: 0, in_order: true } },
      script: {
        source:
          "20*((_score/doc['providerData.title.length'].value)*doc['providerData.title.length'].value)/(((1-(_score/doc['providerData.title.length'].value))*doc['providerData.title.length'].value)+" +
          cleanSplitTitle.length +
          ")",
      },
    },
  };
  var titleFuzzy1String = "",
    titleFuzzyString = "";
  for (const title of splitTitle) {
    title_matchPhrase.script_score.query.span_near.clauses.push({
      span_multi: { match: { fuzzy: { "providerData.title": title } } },
    });
    titleFuzzy1String = titleFuzzy1String + title + "~1 ";
    titleFuzzyString = titleFuzzyString + title + "~ ";
  }

  var title_ORFuzzy1 = {
    script_score: {
      query: {
        simple_query_string: {
          query: titleFuzzy1String,
          fields: ["providerData.title"],
          default_operator: "OR",
        },
      },
      script: {
        source:
          "15*((_score/doc['providerData.title.length'].value)*doc['providerData.title.length'].value)/(((1-(_score/doc['providerData.title.length'].value))*doc['providerData.title.length'].value)+" +
          cleanSplitTitle.length +
          ")",
      },
    },
  };
  var title_ORFuzzy = {
    script_score: {
      query: {
        simple_query_string: {
          query: titleFuzzyString,
          fields: ["providerData.title"],
          default_operator: "OR",
        },
      },
      script: {
        source:
          "10*((_score/doc['providerData.title.length'].value)*doc['providerData.title.length'].value)/(((1-(_score/doc['providerData.title.length'].value))*doc['providerData.title.length'].value)+" +
          cleanSplitTitle.length +
          ")",
      },
    },
  };

  dismax_title.dis_max.queries.push(title_exactMatch);
  dismax_title.dis_max.queries.push(title_matchPhrase);
  dismax_title.dis_max.queries.push(title_ORFuzzy1);
  dismax_title.dis_max.queries.push(title_ORFuzzy);

  /******* DIRECTOR QUERY *******/

  var directorFuzzy1String = "",
    directorFuzzyString = "";

  for (const director of splitDirector) {
    directorFuzzy1String = directorFuzzy1String + director + "~1 ";
    directorFuzzyString = directorFuzzyString + director + "~ ";

    var initials = director.charAt(0);
    var initialsDiractorFuzzyString = "";

    for (const director2 of splitDirector) {
      if (director2 != director)
        initialsDiractorFuzzyString =
          initialsDiractorFuzzyString + director2 + "~ ";
      else
        initialsDiractorFuzzyString =
          initialsDiractorFuzzyString + initials + "* ";
    }
    var director_InitialsFuzzy = {
      script_score: {
        query: {
          simple_query_string: {
            query: initialsDiractorFuzzyString,
            fields: ["providerData.director"],
            default_operator: "AND",
          },
        },
        script: {
          source:
            "25*((_score/doc['providerData.director.length'].value)*doc['providerData.director.length'].value)/(((1-(_score/doc['providerData.director.length'].value))*doc['providerData.director.length'].value)+" +
            splitDirector.length +
            ")",
        },
      },
    };
    dismax_director.dis_max.queries.push(director_InitialsFuzzy);
  }
  var director_ORFuzzy1 = {
    script_score: {
      query: {
        simple_query_string: {
          query: directorFuzzy1String,
          fields: ["providerData.director"],
          default_operator: "OR",
        },
      },
      script: {
        source:
          "20*((_score/doc['providerData.director.length'].value))/(((1-(_score/doc['providerData.director.length'].value))*doc['providerData.director.length'].value)+" +
          splitDirector.length +
          ")",
      },
    },
  };
  var director_ORFuzzy = {
    script_score: {
      query: {
        simple_query_string: {
          query: directorFuzzyString,
          fields: ["providerData.director"],
          default_operator: "OR",
        },
      },
      script: {
        source:
          "10*((_score/doc['providerData.director.length'].value)*doc['providerData.director.length'].value)/(((1-(_score/doc['providerData.director.length'].value))*doc['providerData.director.length'].value)+" +
          splitDirector.length +
          ")",
      },
    },
  };

  dismax_director.dis_max.queries.push(director_ORFuzzy1);
  dismax_director.dis_max.queries.push(director_ORFuzzy);

  /******* YEAR QUERY *******/

  //var year_exactMatch =  {script_score: {query: {match:{"providerData.production_year":{query: +query_year}}},"script": {"source": "25"}}}
  //var year_range1 =  {script_score: {query: {range:{"providerData.production_year":{lte: +query_year+1, gte: query_year-1}}},"script": {"source": "15"}}}
  //var year_range2 =  {script_score: {query: {range:{"providerData.production_year":{lte: +query_year+2, gte: query_year-2}}},"script": {"source": "10"}}}
  var year_range2 = {
    script_score: {
      query: {
        range: {
          "providerData.production_year": {
            lte: +query_year + 2,
            gte: query_year - 2,
          },
        },
      },
      script: {
        source:
          "decayNumericLinear(params.origin, params.scale, params.offset, params.decay, doc['providerData.production_year'].value)*25",
        params: { origin: +query_year, scale: 1, decay: 0.6, offset: 0 },
      },
    },
  };
  var year_fuzzy1 = {
    script_score: {
      query: {
        simple_query_string: {
          query: query_year + "~1",
          fields: ["providerData.production_year.text"],
        },
      },
      script: { source: "15*(_score*1)/(((1-_score)*1)+1)" },
    },
  };

  //dismax_year.dis_max.queries.push(year_exactMatch);
  //dismax_year.dis_max.queries.push(year_range1);
  dismax_year.dis_max.queries.push(year_range2);
  dismax_year.dis_max.queries.push(year_fuzzy1);

  json.query.nested.query.bool.should.push(dismax_title);
  json.query.nested.query.bool.should.push(dismax_year);
  json.query.nested.query.bool.should.push(dismax_director);

  const response = {
    statusCode: 200,
    body: JSON.stringify(json),
  };
  return response;
};
