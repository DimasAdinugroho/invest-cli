'use strict';

const express = require('express');
const { getByIndex } = require('./src/codes');

const app = express();

// Routes
app.get('/stocks/codes', (req, res) => {
  let indexesFlat = req.query.index
  let indexes = indexesFlat && indexesFlat.toUpperCase().split(',')
  let result = getByIndex(indexes)
  res.send(result);
});

// Error handler
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).send('Internal Serverless Error');
});

module.exports = app;
