const masterIndexes = require('./constants/indexes')

const getByIndex = indexes => {
    if (!indexes || !indexes.length) {
        return {
            success: true,
            data: []
        }
    }

    var result = masterIndexes[indexes[0]] ? masterIndexes[indexes[0]] : []
    for (let i = 1; i < indexes.length; i++) {
        result = result.filter(v => (masterIndexes[indexes[i]] ? masterIndexes[indexes[i]] : []).includes(v))
    }

    return {
        success: true,
        data: result
    }
}

module.exports = { getByIndex }