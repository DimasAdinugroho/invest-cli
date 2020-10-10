const moment = require('moment');
const _ = require('lodash');

function stockDataToDynamoDb(item) {
  return {
    PutRequest: {
      Item: {
        date: { S: moment(row.Date).format("YYYY-MM-DD") },
        name: { S: row.StockCode },
        previous: { N: row.Previous.toString() },
        high: { N: row.High.toString() },
        low: { N: row.Low.toString() },
        close: { N: row.Close.toString() },
        vol: { N: row.Volume.toString() },
        val: { N: row.Value.toString() },
        chg: { N: row.Change.toString() },
        freq: { N: row.Frequency.toString() },
        foreignSell: { N: row.ForeignSell.toString() },
        foreignBuy: { N: row.ForeignBuy.toString() },
        foreignTot: { N: (parseFloat(row.ForeignBuy) - parseFloat(row.ForeignSell)).toString() },
        percentage: { S: (parseFloat(row.Change) / parseFloat(row.Previous) * 100).toFixed(2) }
      }
    }

  }
}

function stockDataFromDynamoDb(item) {
  return {
    date: item.date.S,
    stockCode: item.name.S,
    previous: item.previous.S,
    high: parseInt(item.high.N),
    low: parseInt(item.low.N),
    close: parseInt(item.close.N),
    volume: parseInt(item.vol.N),
    value: parseInt(item.val.N),
    change: parseInt(item.chg.N),
    frequency: parseInt(item.freq.N),
    foreignSell: parseInt(item.foreignSell.N),
    foreignBuy: parseInt(item.foreignBuy.N),
    foreignTot: parseInt(item.foreignTot.N),
    percentage: parseFloat(item.percentage.S)
  }
}

function groupStockData(data) {
  let stockGrouped = _.groupBy(data, x => x.stockCode)
  for (let stockCode in stockGrouped) {
    let content = stockGrouped[stockCode]
    let dateGroup = {}
    content.map(item => dateGroup[item.date] = item)
    stockGrouped[stockCode] = dateGroup
  }
  return stockGrouped
}

module.exports = {
  stockDataToDynamoDb,
  stockDataFromDynamoDb,
  groupStockData
}