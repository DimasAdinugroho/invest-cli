const moment = require('moment')
const AWS = require('aws-sdk');
const { stockDataFromDynamoDb, groupStockData } = require('../mapper/util');
const dynamodb = new AWS.DynamoDB({
    apiVersion: '2012-08-10'
});

function getStockData({ stockCode, startDate, endDate, numDays }) {
    let start, end
    if (numDays) {
        end = moment().hours() < 18 ? moment().add(-1, 'days') : moment()
        start = moment(end).add(-parseInt(numDays), 'days')
    } else {
        start = moment(startDate)
        end = moment(endDate)
    }

    let params = {
        TableName: 'stock-table',
        KeyConditionExpression: '#stock = :stock AND #date BETWEEN :start AND :end',
        ExpressionAttributeNames: {
            '#stock': 'name',
            '#date': 'date'
        },
        ExpressionAttributeValues: {
            ':stock': { S: stockCode },
            ':start': { S: start.format('YYYY-MM-DD') },
            ':end': { S: end.format('YYYY-MM-DD') }
        }
    }
    return dynamodb.query(params).promise().then(data => {
        let result = groupStockData(data.Items.map(i => stockDataFromDynamoDb(i)))
        return {
            success: true,
            data: result
        }
    })
}

module.exports = {
    getStockData
}