const axios = require("axios");
const fs = require("fs");

const lambdaURL = "https://fqma0mxypb.execute-api.eu-central-1.amazonaws.com";

const queryArr = [
  {
    query_title: "Spider-man",
    query_director: "James Cameroon",
    query_year: "2010",
  },
  {
    query_title: "Avatar",
    query_director: "James Cameroon",
    query_year: "2012",
  },
  {
    query_title: "2012",
    query_director: "James Cameroon",
    query_year: "2012",
  },
];

const requests = [];

const callLambda = async (query) => {
  return await axios.get(`${lambdaURL}/v1/queryGenerator`, { params: query });
};
queryArr.forEach((query) => requests.push(callLambda(query)));

axios.all(requests).then((output) => {
  const responses = [];

  output.forEach((result) => responses.push(result.data));

  fs.writeFile("responses.json", JSON.stringify(responses), (err) => {
    if (err) console.log(err);
  });
});
