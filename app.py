from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work
import os
import json
import requests
from urllib.parse import urlparse


'''
for connect to mongodb heroku
'''
MONGO_URL = os.environ.get('mongodb://lexion13:1211333s@ds033096.mlab.com:33096/heroku_w8gqb97v')
if MONGO_URL:
    # Get a connection
    connection = MongoClient(MONGO_URL)
    # Get the database
    db = connection[urlparse(MONGO_URL).path[1:]]
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    connection = MongoClient('localhost', 27017)
    db = connection.cryptocurrency



'''
client = MongoClient('localhost', 27017)    #Configure the connection to the database
db = client.cryptocurrency
'''
collist = db.list

app = Flask(__name__)
title = "default title"
heading = "default heading"

@app.route('/')
def route():
    currency = collist.find().limit(10)

    fsyms = []
    tsyms = "JPY"

    for fsyms_array in currency:
        fsyms_one = fsyms_array["symbol"]
        fsyms_one = str(fsyms_one)
        fsyms.append(fsyms_one)

    fsyms = ','.join(fsyms)

    basic_info_api = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={fsyms}&tsyms={tsyms}"
    basic_info_url = basic_info_api.format(fsyms=fsyms,tsyms=tsyms)
    basic_info_data = requests.get(basic_info_url)
    basic_info_json = json.loads(basic_info_data.text)
    basic_info_data = basic_info_json
    basic_info_data = basic_info_data['DISPLAY']

    price_data = {}
    for key, value in basic_info_data.items():
        price_data[key] = value['JPY']['PRICE']

    mktcap_data = {}
    for key, value in basic_info_data.items():
        mktcap_data[key] = value['JPY']['MKTCAP']

    changepct24_data = {}
    for key, value in basic_info_data.items():
        changepct24_data[key] = value['JPY']['CHANGEPCT24HOUR']

    vol24h_data = {}
    for key, value in basic_info_data.items():
        vol24h_data[key] = value['JPY']['VOLUME24HOUR']

    currency = collist.find().limit(10)

    return render_template('index.html',
            title=title,
            heading=heading,
            currency=currency,
            basic_info_data=basic_info_data,
            price_data=price_data,
            mktcap_data=mktcap_data,
            changepct24_data=changepct24_data,
            vol24h_data=vol24h_data
    )

@app.route('/list')
def lists():
    #Display the all currency
    currency = collist.find()
    return render_template('list.html', title=title, heading=heading, currency=currency)

@app.route('/<currency>')
def currency(currency):
    currency = collist.find_one({'symbol': currency})

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

if __name__ == "__main__":
#    app.run(debug=True, host="localhost", port=8080)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, use_reloader=True, port=port)
# Careful with the debug mode..


