const axios = require("axios");
const https = require("https");
const fs = require("fs");
const express = require("express");

const app = express();
app.use(express.json())
app.use(express.urlencoded({extended: true}))
app.use(express.static(__dirname + "/public"));

const httpsAgent = new https.Agent({
    rejectUnauthorized: false,
    cert: fs.readFileSync("./certificates/CA/localhost/localhost.crt"),
    key: fs.readFileSync("./certificates/CA/localhost/localhost.decrypted.key")
})

const axiosInstance = axios.create({httpsAgent: httpsAgent, baseURL: 'https://127.0.0.1:8001'});

app.get('/client/data', async function (request,
                                        response
) {
    axiosInstance.get('/server/data').then(r => {
        console.log(r.data)
        response.status(200).send(r.data);
    }).catch(e => {
        console.log(e.message)
        response.sendStatus(400);
    })
})

app.get('/client/:id', async function (request,
                                       response
) {
    axiosInstance.get(`/server/data/${request.params.id}`).then(r => {
        response.status(200).send(r.data);
    }).catch(e => {
        console.log(e.message)
        response.sendStatus(400);
    })
})


app.listen(4000, function () {
    console.log("Server wait connection...");
    console.log("http://localhost:4000");
});

module.exports = {app, axiosInstance};
