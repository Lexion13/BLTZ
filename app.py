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
	currency = collist.find_one({'symbol': currency})

	'''
	Get price histo

	'''
	histoday = []
	histo_api = "https://min-api.cryptocompare.com/data/histoday?fsym={fsym}&tsym=USD&limit={limit}&aggregate=3&e=CCCAGG"
	fsym = currency['symbol']
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
	Get information.
	'''
	api_id = currency['api_id']
	info_api = "https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id={api_id}"
	info_url = info_api.format(api_id=api_id)
	info_data = requests.get(info_url)
	info_data_json = json.loads(info_data.text)
	info_data = info_data_json['Data']
	info_data_general = info_data["General"]

	return render_template('currency.html',
			currency=currency,
			histoday=histoday,
			info_data=info_data,
			info_data_general=info_data_general
			)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
# Careful with the debug mode..


