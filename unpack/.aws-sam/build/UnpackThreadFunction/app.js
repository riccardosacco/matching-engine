const LambdaClient = require("aws-sdk/clients/lambda");
const allSettled = require("promise.allsettled");

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

          const body = JSON.parse(payload.body);

          resolve(body);

          console.log(`Single thread time: - ${+new Date() - start}`);
        }
      }
    );
  });
};

const chunkArray = (array, chunk_size) => {
  var results = [];

  while (array.length) {
    results.push(array.splice(0, chunk_size));
  }

  return results;
};

exports.lambdaHandler = async (event, context) => {
  const unpack_promises = [];

  const chunk_size = process.env.CHUNK_SIZE || 5;

  const reqBody = JSON.parse(event.body);

  if (Array.isArray(reqBody)) {
    // Chunk array into n subarrays
    const pmatchArray = chunkArray(reqBody, chunk_size);

    pmatchArray.forEach((item) => {
      unpack_promises.push(runThread(item));
    });
  }
  const threaded_start = +new Date();

  const unpack_results = await allSettled(unpack_promises);

  console.log("Overall thread pool time:", +new Date() - threaded_start);

  const results = [];

  unpack_results.forEach((resultArray) => {
    resultArray.value.forEach((result) => {
      results.push(result);
    });
  });

  const response = {
    statusCode: 200,
    headers: {
      "Content-type": "application/json",
    },
    body: JSON.stringify(results),
  };

  return response;
};
