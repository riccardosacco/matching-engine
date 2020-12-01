"use strict";

const app = require("../../app.js");
const chai = require("chai");
const expect = chai.expect;
var event, context;

event = {
  httpMethod: "POST",
  body: '{\n    "programme":{\n        "id":1\n    }\n}',
  resouce: "/itemMatch",
};

describe("Tests index", function () {
  it("verifies successful response", async () => {
    const result = await app.lambdaHandler(event, context);

    expect(result).to.be.an("object");
    expect(result.statusCode).to.equal(200);
    expect(result.body).to.be.an("string");

    let response = JSON.parse(result.body);

    expect(response).to.be.an("object");
    expect(response.httpMethod).to.be.equal("POST");
  });
});
