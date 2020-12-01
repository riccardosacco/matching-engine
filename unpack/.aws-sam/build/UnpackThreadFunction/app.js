const LambdaClient = require("aws-sdk/clients/lambda");

const REGION = "eu-west-1";

const lambda_client = new LambdaClient(REGION);

const runThread = async (reqItem) => {
  const start = +new Date();

  return new Promise((resolve, reject) => {
    lambda_client.invoke(
      {
        FunctionName: "programmeMatchFunction-test-ds",
        InvocationType: "RequestResponse",
        LogType: "Tail",
        Payload: JSON.stringify(reqItem),
      },
      (err, data) => {
        if (err) reject(err);
        if (data) {
          const payload = JSON.parse(data.Payload);

          resolve(JSON.parse(payload.body));
        }
      }
    );

    console.log(
      `Single thread time: ${reqItem["title"]} - ${+new Date() - start}`
    );
  });
};

exports.lambdaHandler = async (event, context) => {
  const unpack_promises = [];

  const reqBody = JSON.parse(event.body);

  if (Array.isArray(reqBody)) {
    reqBody.forEach((item) => {
      unpack_promises.push(runThread(item));
    });
  }
  const threaded_start = +new Date();

  const unpack_results = await Promise.all(unpack_promises);

  console.log("Overall thread pool time:", +new Date() - threaded_start);

  const response = {
    statusCode: 200,
    headers: {
      "Content-type": "application/json",
    },
    body: JSON.stringify(unpack_results),
  };

  return response;
};
