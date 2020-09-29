import os
import json
import yfinance as yf
from functools import wraps

BASE_PATH = os.path.dirname(os.getcwd())
stocklist = json.loads(open(os.path.join(BASE_PATH, "data\\stocklist.json")).read())

indexes = ["IHSG", "LQ45", "IDXBUMN20", "KOMPAS100", "AGRI", "MINING", "BASICIND", "MISCIND", "CONSUMER", "PROPERTY", "INFRASTRUCTURE", "FINANCE", "TRADE", "MANUFACTUR"]
YFIndex = {
    "IHSG": "^JKSE",
    "LQ45": "^JKLQ45", 
    "KOMPAS100": "KOMPAS100.JK",  
    "JII": "^JKII",
    "AGRI": "^JKAGRI",
    "FINANCE": "^JKFINA",
    "MINING": "JKMING",
    "MISCIND": "^JKMISC",
    "CONSUMER": "^JKCONS",
    "PROPERTY": "^JKPROP",
    "INFRASTRUCTURE": "^JK",
    "BASICIND": "^JKBIND",
    "TRADE": "^JKTRAD",
    "MANUFACTUR": "^JKMNFG",
}



# "data\\indicator_parameter.json"
def read_json_data(relativepath):
    ''' Read data from .json
    args:
        relativepath: jsonfile path relative to the file
    '''
    BASE_PATH = os.path.dirname(os.getcwd())
    filepath = os.path.join(BASE_PATH, relativepath)
    param_file = open(filepath).read()
    return json.loads(param_file)

param_file = read_json_data("data\\indicator_parameter.json")
def param(indicator, parameter, def_value):    
    if parameter in param_file[indicator].keys():
        return param_file[indicator][parameter] 
    return def_value


class StockNotFoundError(Exception):
    """Exception raised for unknown Index Code.

    Attributes:        
        message -- explanation of the error
    """
    def __init__(self, message):    
        self.message = message


# period available:  1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
def getStock(ticker, period='1mo'):            
    if ticker not in indexes:
        name = '{}.JK'.format(str.upper(ticker))
    else:
        name = YFIndex[ticker]
    try:
        return yf.Ticker(name).history(period=period)
    except:
        raise StockNotFoundError("Tidak ada kode saham {}".format(name))



def getIndex():
    return indexes


def stockCode(index=None):
    if index == None:
        return [i['code'] for i in stocklist] 

    if isinstance(index, str):
        index  = [index]
    
    if isinstance(index, list):
        result = []
        for idx in index:
            if idx not in indexes:  
                raise StockNotFoundError("Index is not found")

        for ticker in stocklist:
            indexExist = list(set(ticker['index']) & set(index))
            if len(indexExist) >= len(index):                   
                result.append(ticker['code'])
            return result