import csv
import pymongo
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

LQ45 = ['ADHI', 'ADRO', 'AKRA', 'ANTM', 'ASII', 'BBCA', 'BBNI', 'BBRI', 'BBTN', 'BMRI', 'BRPT', 'BSDE', 'CPIN', 'ELSA', 'ERAA', 'EXCL', 'GGRM', 'HMSP', 'ICBP', 'INCO', 'INDF', 'INDY',
        'INKP', 'INTP', 'ITMG', 'JSMR', 'KLBF', 'LPPF', 'MEDC', 'MNCN', 'PGAS', 'PTBA', 'PTPP', 'PWON', 'SCMA', 'SMGR', 'SRIL', 'TKIM', 'TLKM', 'TPIA', 'UNTR', 'UNVR', 'WIKA', 'WSBP', 'WSKT']
JII30 = ['ADRO', 'AKRA', 'ANTM', 'ASII', 'BRPT', 'BSDE', 'CPIN', 'CTRA', 'EXCL', 'ICBP', 'INCO', 'INDF', 'INDY', 'INTP', 'ITMG',
         'JSMR', 'KLBF', 'LPPF', 'PGAS', 'PTBA', 'PTPP', 'SCMA', 'SMGR', 'SMRA', 'TLKM', 'TPIA', 'UNTR', 'UNVR', 'WIKA', 'WSBP', ]
JII70 = ['AALI', 'ACES', 'ADHI', 'ADRO', 'AKRA', 'ANTM', 'APLN', 'ASII', 'ASRI', 'AUTO', 'BKSL', 'BMTR', 'BRMS', 'BRPT', 'BSDE', 'BWPT', 'CPIN', 'CTRA', 'DMAS', 'ELSA', 'ERAA', 'EXCL', 'HRUM', 'ICBP', 'IIKP', 'INAF', 'INCO', 'INDF', 'INDY', 'INTP', 'ISAT', 'ITMG', 'JPFA', 'JSMR', 'KAEF',
         'KLBF', 'LINK', 'LPKR', 'LPPF', 'LSIP', 'MAPI', 'MIKA', 'MNCN', 'MYOR', 'MYRX', 'PGAS', 'PPRO', 'PTBA', 'PTPP', 'PWON', 'RALS', 'RIMO', 'SCMA', 'SIDO', 'SIMP', 'SMBR', 'SMGR', 'SMRA', 'TARA', 'TINS', 'TLKM', 'TOPS', 'TPIA', 'TRAM', 'UNTR', 'UNVR', 'VIVA', 'WIKA', 'WSBP', 'WTON', ]
ISSI = ['AALI','ABBA','ACES','ACST','ADES','ADHI','ADMG','ADRO','AGII','AKKU','AKPI','AKRA','AKSI','ALDO','ALKA','AMFG','AMIN','ANJT','ANTM','APII','APLI','APLN','ARII','ARMY','ARNA','ARTA','ARTI','ASGR','ASII','ASRI','ATIC','ATPK','AUTO','BAPA','BATA','BAYU','BCIP','BEEF','BELL','BEST','BIPP','BIRD','BISI','BKDP','BKSL','BLTZ','BMSR','BMTR','BOGA','BOLT','BOSS','BRAM','BRIS','BRMS','BRNA','BRPT','BSDE','BSSR','BTEK','BTON','BTPS','BUDI','BUKK','BULL','BUVA','BWPT','BYAN','CAKK','CAMP','CANI','CASS','CEKA','CENT','CINT','CKRA','CLEO','CLPI','CMNP','CMPP','CPIN','CPRI','CSAP','CSIS','CTBN','CTRA','CTTH','DART','DAYA','DEWA','DGIK','DIGI','DILD','DKFT','DMAS','DPNS','DPUM','DSFI','DSSA','DUCK','DUTI','DVLA','DWGL','DYAN','ECII','EKAD','ELSA','EMDE','EMTK','EPMT','ERAA','EXCL','FAST','FASW','FILM','FIRE','FISH','FMII','FOOD','FORZ','FPNI','FREN','GAMA','GDST','GDYR','GEMA','GEMS','GHON','GIAA','GJTL','GMFI','GMTD','GOLD','GOOD','GPRA','GTBO','GWSA','GZCO','HADE','HEAL','HERO','HEXA','HITS','HKMU','HOKI','HOME','HRME','HRTA','HRUM','IATA','IBST','ICBP','ICON','IDPR','IGAR','IIKP','IKBI','IMPC','INAF','INCI','INCO','INDF','INDR','INDS','INDX','INDY','INPP','INTD','INTP','IPCC','IPCM','IPOL','ISAT','ISSP','ITMA','ITMG','JECC','JGLE','JIHD','JKON','JKSW','JMAS','JPFA','JPRS','JRPT','JSKY','JSMR','JSPT','JTPE','KAEF','KARW','KBLI','KBLM','KBLV','KDSI','KIAS','KICI','KIJA','KINO','KIOS','KKGI','KLBF','KOBX','KOIN','KOPI','KPIG','LAND','LAPD','LCGP','LCKM','LINK','LION','LMPI','LMSH','LPCK','LPIN','LPKR','LPLI','LPPF','LRNA','LSIP','LTLS','LUCK','MAGP','MAIN','MAMI','MAPA','MAPB','MAPI','MARK','MASA','MBAP','MBSS','MBTO','MCAS','MDKA','MDKI','MDLN','MERK','META','MFMI','MGRO','MICE','MIKA','MINA','MIRA','MITI','MKPI','MLIA','MLPL','MLPT','MMLP','MNCN','MPMX','MPPA','MRAT','MSIN','MTDL','MTLA','MTPS','MTRA','MTSM','MYOH','MYOR','MYRX','NASA','NATO','NELY','NFCX','NIKL','NIPS','NRCA','OASA','OMRE','PALM','PANI','PANR','PBID','PBSA','PCAR','PDES','PEHA','PGAS','PGLI','PICO','PJAA','PKPK','PNBS','PNSE','POLI','POLL','PORT','POWR','PPRE','PPRO','PRDA','PRIM','PSAB','PSKT','PSSI','PTBA','PTIS','PTPP','PTRO','PTSN','PTSP','PUDP','PWON','PYFA','PZZA','RAJA','RALS','RANC','RBMS','RICY','RIGS','RIMO','RISE','RODA','ROTI','RUIS','SAME','SCBD','SCCO','SCMA','SDPC','SHID','SHIP','SIDO','SILO','SIMP','SIPD','SKBM','SKLT','SKRN','SKYB','SMBR','SMDM','SMDR','SMGR','SMMT','SMRA','SMRU','SMSM','SONA','SOSS','SOTS','SPMA','SPTO','SQMI','SRAJ','SRSN','SRTG','SSIA','SSTM','STAR','STTP','SUGI','SWAT','TARA','TBMS','TCID','TCPI','TDPM','TFCO','TGKA','TGRA','TINS','TIRA','TLKM','TMPO','TNCA','TOBA','TOPS','TOTL','TOTO','TPIA','TPMA','TRAM','TRIL','TRIS','TRST','TRUK','TSPC','TURI','ULTJ','UNIC','UNIT','UNTR','UNVR','URBN','VIVA','VOKS','WAPO','WEGE','WEHA','WICO','WIKA','WINS','WOOD','WSBP','WTON','YELO','ZBRA','ZINC','ZONE']
INDICES = ['IHSG', 'LQ45', 'JII', 'ISSI', 'MINING', 'MANUFACTURING', 'MISCINDUSTRY', 'INFRASTRUCTURE', 'FINANCE', 'TRADE', 'PROPERTY', 'CONSTRUCTION', 'BASICINDUSTRY', 'AGRICULTURE']
LQ45_JII70 = list(set(LQ45+JII70))
LQ45_JII70.sort()

MONGO_CLIENT = pymongo.MongoClient('mongodb://localhost:27017/')
DB = MONGO_CLIENT['stock']


def import_to_db(stock, period):
    with open(stock + '.' + period + '.csv', 'r') as csv_file:
        rows = list(csv.reader(csv_file, delimiter=','))
        coll = get_collection(stock, period)
        for row in rows[1:]:
            if 'null' in row:
                continue
        #     if not int(row[6]): //volume
        #         continue
            row_data = process_raw_row(row)
            coll.insert_one(row_data)


def create_db_index(stock, period):
    coll = get_collection(stock, period)
    coll.create_index([('time', pymongo.ASCENDING)])

def tick(price):
    if price < 200:
        return 1
    if price < 500:
        return 2
    if price < 2000:
        return 5
    if price < 5000:
        return 10
    return 25


def ara(price):
    if price < 200:
        return 1.35*price
    if price < 5000:
        return 1.25*price
    return 1.2*price


def arb(price):
    if price < 200:
        return 0.65*price
    if price < 5000:
        return 0.75*price
    return 0.8*price


def calculate_sma_in_db(stock, period, sma_period):
    coll = get_collection(stock, period)
    df = pd.DataFrame(list(coll.find().sort('date')))
    col_name = calculate_sma_in_df(df, sma_period)
    for idx, row in df.iterrows():
        coll.update_one({'time': row['time']}, {
                        '$set': {col_name: row[col_name]}})


def calculate_rsi_in_db(stock, period, rsi_period):
    coll = get_collection(stock, period)
    df = pd.DataFrame(list(coll.find().sort('date')))
    col_name = calculate_rsi_in_df(df, rsi_period)
    for idx, row in df.iterrows():
        coll.update_one({'time': row['time']}, {
                        '$set': {col_name: row[col_name]}})


def calculate_ppsr_in_db(stock, period):
    coll = get_collection(stock, period)
    df = pd.DataFrame(list(coll.find().sort('date')))
    col_names = calculate_ppsr_in_df(df)
    for idx, row in df.iterrows():
        coll.update_one({'time': row['time']}, {
                        '$set': {col_name: row[col_name] for col_name in col_names}})


def calculate_lowest_low_in_db(stock, period, ll_period):
    coll = get_collection(stock, period)
    df = pd.DataFrame(list(coll.find().sort('date')))
    col_name = calculate_lowest_low_in_df(df, ll_period)
    for idx, row in df.iterrows():
        coll.update_one({'time': row['time']}, {
                        '$set': {col_name: row[col_name]}})


def calculate_stochastic_in_db(stock, period, sto_period, k_smoothing, d_smoothing):
    coll = get_collection(stock, period)
    df = pd.DataFrame(list(coll.find().sort('date')))
    col_names = calculate_stochastic_in_df(df, sto_period, k_smoothing, d_smoothing)
    for idx, row in df.iterrows():
        coll.update_one({'time': row['time']}, {
                        '$set': {col_name: row[col_name] for col_name in col_names}})


def calculate_bb_in_db(stock, period, bb_period, bb_mul):
    coll = get_collection(stock, period)
    df = pd.DataFrame(list(coll.find().sort('date')))
    col_names = calculate_bb_in_df(df, bb_period, bb_mul)
    for idx, row in df.iterrows():
        coll.update_one({'time': row['time']}, {
                        '$set': {col_name: row[col_name] for col_name in col_names}})


def calculate_macd_in_db(stock, period, fast, slow, smoothing):
    coll = get_collection(stock, period)
    df = pd.DataFrame(list(coll.find().sort('date')))
    col_names = calculate_macd_in_df(df, fast, slow, smoothing)
    for idx, row in df.iterrows():
        coll.update_one({'time': row['time']}, {
                        '$set': {col_name: row[col_name] for col_name in col_names}})


def calculate_sma_in_df(df, period):
    col_name = 'sma(%d)' % period
    df[col_name] = df['close'].rolling(period).mean()
    return col_name


def calculate_rsi_in_df(df, period):
    col_name = 'rsi(%d)' % period
    delta = df['close'].diff()
    gain, loss = delta.copy(), delta.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    avg_gain = pd.Series(np.nan, df.index)
    avg_gain[period-1] = gain[:period-1].mean()
    avg_loss = pd.Series(np.nan, df.index)
    avg_loss[period-1] = abs(loss[:period-1].mean())
    for i in df.index[period:]:
        avg_gain.iloc[i] = (avg_gain.iloc[i-1] *
                            (period-1) + gain.iloc[i]) / period
        avg_loss.iloc[i] = (avg_loss.iloc[i-1]*(period-1) +
                            abs(loss.iloc[i])) / period
    rs = avg_gain/avg_loss
    rsi = 100 - (100/(1+rs))
    df[col_name] = rsi
    return col_name


def calculate_ppsr_in_df(df):
    pp, s1, s2, r1, r2 = 'pp', 'pp:s1', 'pp:s2', 'pp:r1', 'pp:r2'
    df[pp] = (df['high'] + df['low'] + df['close']) / 3
    df[s1] = df[pp]*2 - df['high']
    df[s2] = df[pp] - (df['high'] - df['low'])
    df[r1] = df[pp]*2 - df['low']
    df[r2] = df[pp] + (df['high'] - df['low'])
    return pp, s1, s2, r1, r2


def calculate_lowest_low_in_df(df, period):
    col_name = 'lowest_low(%d)' % period
    ll = df['low'].rolling(period).min()
    df[col_name] = ll
    return col_name


def calculate_stochastic_in_df(df, period, k_smoothing, d_smoothing):
    k_name = 'stochastic(%d,%d,%d):%%K' % (period, k_smoothing, d_smoothing)
    d_name = 'stochastic(%d,%d,%d):%%D' % (period, k_smoothing, d_smoothing)
    l = df['low'].rolling(period).min()
    h = df['high'].rolling(period).max()
    fast_k = 100 * (df['close'] - l) / (h - l)
    k = fast_k.rolling(k_smoothing).mean()
    d = k.rolling(d_smoothing).mean()
    df[k_name] = k
    df[d_name] = d
    return k_name, d_name


def calculate_bb_in_df(df, period, mul):
    mid_name = 'bb(%d,%d):middle' % (period, mul*10)
    upp_name = 'bb(%d,%d):upper' % (period, mul*10)
    low_name = 'bb(%d,%d):lower' % (period, mul*10)
    pct_b_name = 'bb(%d,%d):%%b' % (period, mul*10)
    bw_name = 'bb(%d,%d):bw' % (period, mul*10)
    mid = df['close'].rolling(period).mean()
    upp = mid + mul*df['close'].rolling(period).std()
    low = mid - mul*df['close'].rolling(period).std()
    pct_b = (df['close'] - low) / (upp - low)
    bw = (upp - low) / mid
    df[mid_name] = mid
    df[upp_name] = upp
    df[low_name] = low
    df[pct_b_name] = pct_b
    df[bw_name] = bw
    return mid_name, upp_name, low_name, pct_b_name, bw_name


def calculate_macd_in_df(df, fast, slow, smoothing):
    macd_name = 'macd(%d,%d,%d):macd' % (fast, slow, smoothing)
    signal_name = 'macd(%d,%d,%d):signal' % (fast, slow, smoothing)
    f_alpha = 2 / (fast + 1)
    s_alpha = 2 / (slow + 1)
    signal_alpha = 2 / (smoothing + 1)
    f = pd.Series(np.nan, index=df.index)
    s = pd.Series(np.nan, index=df.index)
    f[fast-1] = df['close'][:fast].mean()
    s[slow-1] = df['close'][:slow].mean()
    for i in df.index[fast:]:
        f[i] = (df['close'][i]-f[i-1])*f_alpha+f[i-1]
    for i in df.index[slow:]:
        s[i] = (df['close'][i]-s[i-1])*s_alpha+s[i-1]
    macd = f - s
    signal = macd.rolling(smoothing).mean()
    df[macd_name] = macd
    df[signal_name] = signal
    return macd_name, signal_name


def process_raw_row(row):
    data = {
        'time': datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S') + timedelta(hours=7),
        'open': float(row[1]),
        'high': float(row[2]),
        'low': float(row[3]),
        'close': float(row[4]),
        # 'adj_close': float(row[5]),
        'volume': int(float(row[5])),
    }
    return data


def get_collection(stock, period):
    return DB[stock + '.' + period]
