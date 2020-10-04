const moment = require('moment');

function marketDataStruct(rows) {
  return rows.map(row => {
    return {
      Date: moment(row.Date).format("YYYY-MM-DD"),
      Code: row.StockCode,
      Name: row.StockName,
      Previous: row.Previous,
      High: row.High,
      Low: row.Low,
      Close: row.Close,
      Volume: row.Volume,
      Value: row.Value,
      Change: row.Change,
      Frequency: row.Frequency, 
      Offer: row.Offer, 
      OfferVolume: row.OfferVolume, 
      Bid: row.Bid, 
      BidVolume: row.BidVolume, 
      ListedShares: row.ListedShares, 
      ForeignSell: row.ForeignSell, 
      ForeignBuy: row.ForeignBuy,
      TotalForeign: parseFloat(row.ForeignBuy) - parseFloat(row.ForeignSell),
      Percentage: (parseFloat(row.Change) / parseFloat(row.Previous) * 100).toFixed(2)
    }
  })
}

module.exports = {
  marketDataStruct
}