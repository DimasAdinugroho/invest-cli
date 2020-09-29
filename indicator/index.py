import json
import logging
from indicator import make_signal
from utils import ( getStock, stockCode )
from db import ( create_connection, get_timeseries,
    insert_timeseries, CREATE_TS_TABLE, execute_query, insert_signal )

log = logging.getLogger("main")


if __name__ == "__main__":    
    conn = create_connection()
    succesStock = 0
    all_stock = stockCode() 
    for ticker in all_stock:
        try:
            dfticker = getStock(ticker, "1y")
            dfticker['date'] = dfticker.index.strftime('%Y-%m-%d')
            dfticker['code'] = ticker
            data = make_signal(dfticker, True)
            raw_data = json.dumps(data)
            insert_signal(conn, data, raw_data)
            succesStock += 1
            # insert_timeseries(conn, dfticker, ticker, "daily", False)
        except:
            log.error("insert {} to Signal is failed".format(ticker))
            continue

    print('success {} out of {}'.format(succesStock, len(all_stock)))    