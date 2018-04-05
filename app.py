from flask import Flask, render_template,request,redirect,url_for # For flask implementation
import os
import json
import requests
import db
import api

# import sys
# sys.path.append('/Applications/PyCharm.app/Contents/debug-eggs/pycharm-debug.egg')
# import pydevd
# pydevd.settrace('localhost', port=5000, stdoutToServer=True, stderrToServer=True)

app = Flask(__name__)

dm = db.DataModels()

title = "default title"
heading = "default heading"

@app.route('/')
def route():

    view_data = {}
    fsyms = []
    tsyms = "JPY"

    for data in dm.get_coin_list(0, 20):
        view_data[data['coin']] = {'image': data['image'], 'name': data['name']}
        fsyms.append(data['coin'])

    fsyms = ','.join(fsyms)

    coin_data = api.get_details(fsyms, tsyms)

    price_data = {}
    mktcap_data = {}
    changepct24_data = {}
    vol24h_data = {}

    for key, value in coin_data.items():
        price_data[key] = value['JPY']['PRICE']
        mktcap_data[key] = value['JPY']['MKTCAP']
        changepct24_data[key] = value['JPY']['CHANGEPCT24HOUR']
        vol24h_data[key] = value['JPY']['VOLUME24HOUR']

    return render_template('index.html',
                           title=title,
                           heading=heading,
                           currency=view_data,
                           coin_data=coin_data,
                           price_data=price_data,
                           mktcap_data=mktcap_data,
                           changepct24_data=changepct24_data,
                           vol24h_data=vol24h_data)


@app.route('/list')
def lists():
    #Display the all currency
    currency = db.get_coin_list()
    return render_template('list.html', title=title, heading=heading, currency=currency)


@app.route('/currency/<currency>')
def currency(currency):
    currency = db.get_one(currency)

    '''
    Get price histo

    '''
    histoday = []
    histo_api = "https://min-api.cryptocompare.com/data/histoday?fsym={fsym}&tsym=USD&limit={limit}&aggregate=1&e=CCCAGG"
    fsym = currency['symbol']
    limit = '365'
    histo_api_url = histo_api.format(fsym=fsym, limit=limit)
    histo_data = requests.get(histo_api_url)
    histo_data_json = json.loads(histo_data.text)
    data = histo_data_json["Data"]
    for e in data:
        ti = e["time"]*1000 #I don't know why... but this plugin says that...
        op = e["open"]
        hi = e["high"]
        lo = e["low"]
        cl = e["close"]
        vf = e["volumefrom"]
        vt = e["volumeto"]
        histoday.append([ti,op,hi,lo,cl,vt])
    histoday = json.dumps(histoday)


    '''
    Get information.
    '''
    api_id = currency['api_id']
    info_api = "https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={api_id}"
    info_url = info_api.format(api_id=api_id)
    info_data = requests.get(info_url)
    info_data_json = json.loads(info_data.text)
    info_data = info_data_json['Data']
    info_data_general = info_data["General"]

    '''
    Get compare currency with others.
    '''
    compare_api = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={fsym}&tsyms={tsyms}"
    if currency['symbol'] != "BTC":
        tsyms = "JPY,USD,EUR,BTC"
    else:
        tsyms = "JPY,USD,EUR"
    compare_url = compare_api.format(fsym=fsym,tsyms=tsyms)
    compare_data = requests.get(compare_url)
    compare_data_json = json.loads(compare_data.text)
    compare_data = compare_data_json
    compare_data_jpy = compare_data['DISPLAY'][currency['symbol']]['JPY']
    compare_data_usd = compare_data['DISPLAY'][currency['symbol']]['USD']
    compare_data_eur = compare_data['DISPLAY'][currency['symbol']]['EUR']
    if currency['symbol'] != "BTC":
        compare_data_btc = compare_data['DISPLAY'][currency['symbol']]['BTC']
    else:
        compare_data_btc = "nothing"

    return render_template('currency.html',
            fsym=fsym,
            currency=currency,
            histoday=histoday,
            info_data=info_data,
            info_data_general=info_data_general,
            compare_data=compare_data,
            compare_data_jpy=compare_data_jpy,
            compare_data_usd=compare_data_usd,
            compare_data_eur=compare_data_eur,
            compare_data_btc=compare_data_btc
            )


@app.route('/getdata')
def getdata():
    currencies = db.get_coin_list()
    symbols = []
    api_ids = []


    for currency in currencies:
        api_id = currency['api_id']
        api_ids.append(api_id)

    for api_id in api_ids:
        base_api_url = "https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={api_id}"
        api_url = base_api_url.format(api_id=api_id)
        api_data = requests.get(api_url)
        api_data = json.loads(api_data.text)
        # total coin mined * price
        totalcoinsmined = api_data['Data']['General']

    return render_template('getdata.html',
                           symbols=symbols,
                           api_ids=api_ids,
                           totalcoinsmined=totalcoinsmined)


# get data from api



# insert data into mongodb

# send or display complete message as something email or something else.

if __name__ == "__main__":
#    app.run(debug=True, host="localhost", port=8080)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, use_reloader=True, port=port)
# Careful with the debug mode..
