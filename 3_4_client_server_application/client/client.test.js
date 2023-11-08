const chai = require('chai');
const chaiHttp = require('chai-http');
const {app, axiosInstance} = require('./client');
const axios = require("axios");

chai.use(chaiHttp);
const expect = chai.expect;

describe('Express App', () => {
    it('should respond with "Server data!" on /client/data', (done) => {
        chai.request(app)
            .get('/client/data')
            .end((err, res) => {
                expect(axiosInstance.defaults.httpsAgent.options).to.have.property("cert");
                expect(axiosInstance.defaults.httpsAgent.options).to.have.property("key");

                expect(res).to.have.status(200);
                expect(res.body).to.be.an('object');
                expect(res.body).to.have.property('message');
                expect(res.body.message).to.equal("Server data!");
                done();
            });
    });

    it('should respond with a 404 status on a non-existing route', (done) => {
        chai.request(app)
            .get('/non-existing-route')
            .end((err, res) => {
                expect(res).to.have.status(404);
                done();
            });
    });
});
