const moment = require('moment');

function marketDataStruct(rows) {
  return rows.map(row => {
    return {
      PutRequest: {
        Item: {
          date: {S : moment(row.Date).format("YYYY-MM-DD")},
          name: {S: row.StockCode},
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
  })
}

module.exports = {
  marketDataStruct
}