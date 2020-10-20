const AWS = require("aws-sdk");
const fs = require("fs");

const lambda = new AWS.Lambda({
  region: "eu-central-1",
});

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

const generateLambda = (query) => {
  const params = {
    FunctionName: "queryGenerator",
    InvocationType: "RequestResponse",
    Payload: JSON.stringify({ queryStringParameters: query }),
  };

  requests.push(lambda.invoke(params).promise());
};

queryArr.forEach((query) => {
  generateLambda(query);
});

Promise.all(requests).then((responses) => {
  const output = [];

  responses.forEach((response) => {
    output.push(JSON.parse(JSON.parse(response.Payload).body));
  });

  fs.writeFile("responses_invoke.json", JSON.stringify(output), (err) => {
    if (err) console.log(err);
  });
});
