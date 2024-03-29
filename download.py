import json
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
from oandapyV20.contrib.factories import InstrumentsCandlesFactory
import datetime

def get_dates_excluding_weekends(period,ticker):
    exclude = ["BTC_USD","ETH_USD","LTC_USD"] #these trade 24/7
    # Get today's date
    tday = datetime.datetime.today()
    tday_str = tday.strftime("%Y-%m-%dT%H:%M:%SZ")
    # Initialize the counter and the date for 'yday'
    days_back = 0
    yday = tday
    if ticker in exclude:
        yday = yday - datetime.timedelta(days=period)
        yday_str = yday.strftime("%Y-%m-%dT%H:%M:%SZ")#T00:00:00Z")
        return tday_str, yday_str
    while days_back < period:
        # Subtract one day
        yday -= datetime.timedelta(days=1)

        # Check if the resulting day is a weekend (Saturday=5, Sunday=6)
        if yday.weekday() < 5:
            days_back += 1

    yday_str = yday.strftime("%Y-%m-%dT%H:%M:%SZ")#T00:00:00Z")

    return tday_str, yday_str


def download(ticker = "EUR_USD",period = 1):
    import os
    files = os.listdir("data")
    for file in files:
        #delete file if it exists
        if file.startswith(ticker):
            os.remove("data/"+file)

    #tday = datetime.datetime.today().strftime("%Y-%m-%dT00:00:00Z")
    #print(tday)
    #find today - period days excluding weekends
    #yday = (datetime.datetime.today() - datetime.timedelta(days=period)).strftime("%Y-%m-%dT00:00:00Z")
    tday,yday = get_dates_excluding_weekends(period,ticker)
    print(tday,yday)
    with open("OANDA_ID.txt", "r") as f:
        accountID = f.read()
    with open("OANDA_KEY.txt", "r") as f:
        access_token = f.read()
    
    client = oandapyV20.API(access_token=access_token)

    #find today and yesterdays date at midnight in the format oanda wants
    
    
    params = {
        "from": yday,
        "to" : tday,
        "granularity": "M1",
    }

    def cnv(r, h):
        # get all candles from the response and write them as a record to the filehandle h
        for candle in r.get('candles'):
            ctime = candle.get('time')[0:19]
            try:
                rec = "{time},{complete},{o},{h},{l},{c},{v}".format(
                    time=ctime,
                    complete=candle['complete'],
                    o=candle['mid']['o'],
                    h=candle['mid']['h'],
                    l=candle['mid']['l'],
                    c=candle['mid']['c'],
                    v=candle['volume'],
                )
            except Exception as e:
                print(e, r)
            else:
                h.write(rec+"\n")

    datafile = "data/{}.{}.out".format(ticker, params['granularity'])
    with open(datafile, "w") as O:
        n = 0
        for r in InstrumentsCandlesFactory(instrument=ticker, params=params):
            rv = client.request(r)
            cnt = len(r.response.get('candles'))
            print("REQUEST: {} {} {}, received: {}".format(r, r.__class__.__name__, r.params, cnt))
            n += cnt
            cnv(r.response, O)
        print("Check the datafile: {} under /tmp!, it contains {} records".format(datafile, n))

def now(ticker):
    pass

if __name__ == "__main__":
    download(period=1)