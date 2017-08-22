run
    python3 test.py
    
db structure

    db name = cryptocurrency

        collection = list
            name = bitcoin
            description = bitcoin is...
            Symbol = BTC
            website = https://bitcoin.org/
            connections = 8
            algorithm = SHA-256

        collection = bitcoin
            date = 20170101
            open = 1000
            hight = 1100
            low = 900
            close = 1050

mongodb run

    if nothing data directory
    $mkdir data
    $echo 'mongod --bind_ip=$IP --dbpath=data --nojournal --rest "$@"' > mongod
    $chmod a+x mongod
    $./mongod


mongodb export as csv

    examples
    $mongoexport --db fd --csv --collection port --out export.csv --fields _id,symbol,name,algorithm
    if you wanna export cryptocurrency list collections.
    $mongoexport --db cryptocurrency --csv --collection list --out export.csv --fields _id,symbol,name,algorithm
    if you wanna import cryptocurrency list collections.
    $mongoimport -d cryptocurrency -c list --type csv --file import.csv --headerline

(kinda)db seed 

    $mongo
    >use cryptocurrency;
    >db.list.insert({
        name: 'bitcoin',
        description: 'bitcoin is ...',
        symbol: 'BTC',
        website: 'https://bitcoin.org',
        algorithm: 'SHA-256'
    });
    

pick up data from mongodb with app.py

    #this is import pymongo driver
    from pymongo import MongoClient # Database connector
    #select mongodb location
    client = MongoClient('localhost', 27017)    #Configure the connection to the database

    #select db
    db = client.cryptocurrency

    #select collection
    collist = db.list

    this is how to pick up data from mongodb
    @app.route('/<currency>')
    def currency(currency):
    	currency = collist.find_one({'name': currency})
    	name = currency['name']
    	symbol = currency['symbol']
    	return render_template('currency.html', currency=currency, name=name, symbol=symbol)

