const AWS = require("aws-sdk");

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

queryArr.forEach((query) => {});

Promise.all(requests).then((responses) => console.log(responses));
