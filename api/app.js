'use strict';

const express = require('express');
const { getByIndex } = require('./src/codes');
const { getStockData } = require('./src/stockData/get')

const app = express();

// Routes
app.get('/stocks/codes', (req, res) => {
  let indexesFlat = req.query.index
  let indexes = indexesFlat && indexesFlat.toUpperCase().split(',')
  let result = getByIndex(indexes)
  res.send(result);
});

app.get('/stocks/data', (req, res) => {
  getStockData(req.query).then(result => {
    res.send(result)
  })
})

// Error handler
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).send('Internal Serverless Error');
});

app.listen(3000)

module.exports = app;
