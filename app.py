from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work
import os
import json
import requests

client = MongoClient('localhost', 27017)    #Configure the connection to the database
db = client.cryptocurrency
collist = db.list

app = Flask(__name__)
title = "default title"
heading = "default heading"
#modify=ObjectId()

@app.route('/')
def route():
	currency = collist.find();
	return render_template('index.html', title=title, heading=heading, currency=currency)
	
@app.route('/list')
def lists():
	#Display the all currency
	currency = collist.find()
	return render_template('list.html', title=title, heading=heading, currency=currency)

@app.route('/<currency>')
def currency(currency):

	'''
	Get price histo
	
	'''
	histoday = []
	histo_api = "https://min-api.cryptocompare.com/data/histoday?fsym={fsym}&tsym=USD&limit={limit}&aggregate=3&e=CCCAGG"
	fsym = currency
	limit = '60'
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
		histoday.append([ti,op,hi,lo,cl])
	'''
	Get current price
	'''
	current_price_api = "https://min-api.cryptocompare.com/data/pricemulti?fsyms={fsym}&tsyms={tsyms}"
	fsym = currency
	tsyms = "JPY,BTC,USD,EUR"
	current_price_api_url = current_price_api.format(fsym=fsym, tsyms=tsyms)
	current_price_data = requests.get(current_price_api_url)
	current_price_data_json = json.loads(current_price_data.text)
	current_price_data_json = current_price_data_json[currency]
	current_price_JPY = current_price_data_json['JPY']
#	current_price_BTC = current_price_data_json['BTC']
	current_price_USD = current_price_data_json['USD']
	current_price_EUR = current_price_data_json['EUR']
	currency = collist.find_one({'symbol': currency})
	return render_template('currency.html',
			currency=currency,
			histoday=histoday,
			current_price_data_json=current_price_data_json,
			current_price_api_url=current_price_api_url,
			current_price_data=current_price_data,
			current_price_JPY=current_price_JPY,
#			current_price_BTC=current_price_BTC,
			current_price_USD=current_price_USD,
			current_price_EUR=current_price_EUR)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
# Careful with the debug mode..


