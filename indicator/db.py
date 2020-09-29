import os
import sqlite3
import pandas as pd

from sqlite3 import Error


base_path = os.path.dirname(os.getcwd())
db_file = os.path.join(base_path, "data\\database\\database.sqlite")
def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)    
    return conn


CREATE_TS_TABLE = """CREATE TABLE TimeSeries (
    code TEXT NOT NULL,
    date TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    open INTEGER NOT NULL,
    high INTEGER NOT NULL,
    low INTEGER NOT NULL,
    close INTEGER NOT NULL,
    volume INTEGER NOT NULL,
    PRIMARY KEY(date, timeframe, code))"""


CREATE_SIGNAL_TABLE = """CREATE TABLE Signal (    
    last_updated TEXT NOT NULL,
    code TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    buy_signal INTEGER NOT NULL,
    sell_signal INTEGER NOT NULL,
    raw_data TEXT NOT NULL,
    PRIMARY KEY(last_updated, timeframe, code))"""


conn = create_connection()



def execute_query(conn, statement):    
    try:
        conn.execute(statement)
        return True
    except Error as e:
        print(e)
    return False


def insert_timeseries(conn, df, code, timeframe, last_data=False):    
    ts = ["daily", "weekly"]
    if timeframe not in ts:
        raise ValueError("value must be daily or weekly")
    
    if "Dividends" in df.columns:
        df.drop(columns=["Dividends"], inplace=True)
    
    if "Stock Splits" in df.columns:
        df.drop(columns=["Stock Splits"], inplace=True) 
    
    df.index.name = str.lower(df.index.name)
    df.index = df.index.date
    df.columns = list(map(lambda x: str.lower(x), df.columns))
    df['code'] = code
    df['timeframe'] = timeframe
    
    if last_data:
        max_date = max(df.index)
        today = df[df.index == max_date]
        today.to_sql("TimeSeries", conn, if_exists="append", index_label="date")
    else:
        df.to_sql("TimeSeries", conn, if_exists="append", index_label="date")
    return True


def get_timeseries(conn, code, timeframe='daily'):
    ts = ["daily", "weekly"]
    if timeframe not in ts:
        raise ValueError("value must be daily or weekly")
    stmt = "SELECT * FROM TimeSeries WHERE code = '{}' AND timeframe = '{}'".format(code, timeframe)
    df = pd.read_sql(stmt, con=conn)
    return df


def get_code_from_db(conn):
    cur = conn.cursor()
    stmt = "SELECT DISTINCT Code FROM TimeSeries"
    cur.execute(stmt)
    rows = cur.fetchall()
    tickers = [row[0] for row in rows]
    return tickers


def insert_signal(conn, data, raw_data):
    #check and delete if row exist    
    stmt = ''' INSERT INTO Signal(date,code,buy_signal,buy_indicator,sell_signal,sell_indicator,raw_data)
              VALUES(?,?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(stmt, (data['date'], data['code'], data['buy_signal'], data['buy_indicator'] , data['sell_signal'], data['sell_indicator'], raw_data))
    conn.commit()
    return True