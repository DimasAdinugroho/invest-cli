const masterIndexes = require('./constants/indexes')

const getByIndex = indexes => {
    let availableIndexes = Object.keys(masterIndexes)

    if (!(indexes && indexes.length) || !indexes.every(i => availableIndexes.includes(i))) {
        return {
            success: false,
            message: "Invalid index given. Available indexes: " + availableIndexes.join(', ')
        }
    }

    var result = masterIndexes[indexes[0]]
    for (let i = 1; i < indexes.length; i++) {
        result = result.filter(v => masterIndexes[indexes[i]].includes(v))
    }

    return {
        success: true,
        data: result
    }
}

module.exports = { getByIndex }