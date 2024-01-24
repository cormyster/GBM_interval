import json
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
from oandapyV20.contrib.factories import InstrumentsCandlesFactory

def download(instrument = "EUR_USD"):
    with open("OANDA_ID.txt", "r") as f:
        accountID = f.read()
    with open("OANDA_KEY.txt", "r") as f:
        access_token = f.read()
    client = oandapyV20.API(access_token=access_token)

    #find today and yesterdays date at midnight in the format oanda wants
    import datetime
    today = datetime.datetime.today().strftime("%Y-%m-%dT00:00:00Z")
    yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%dT00:00:00Z")
    params = {
        "from": yesterday,
        "to" : today,
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

    datafile = "data/{}.{}.out".format(instrument, params['granularity'])
    with open(datafile, "w") as O:
        n = 0
        for r in InstrumentsCandlesFactory(instrument=instrument, params=params):
            rv = client.request(r)
            cnt = len(r.response.get('candles'))
            print("REQUEST: {} {} {}, received: {}".format(r, r.__class__.__name__, r.params, cnt))
            n += cnt
            cnv(r.response, O)
        print("Check the datafile: {} under /tmp!, it contains {} records".format(datafile, n))