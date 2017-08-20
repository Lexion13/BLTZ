from flask import Flask, render_template,request,redirect,url_for # For flask implementation
from pymongo import MongoClient # Database connector
from bson.objectid import ObjectId # For ObjectId to work
import os

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
	name = currency['name']
	symbol = currency['symbol']
	algorithm = currency['algorithm']
	return render_template('currency.html', currency=currency, name=name, symbol=symbol, algorithm=algorithm)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
# Careful with the debug mode..


