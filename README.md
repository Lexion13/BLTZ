run
    python3 app.py
    
db structure

    db name = cryptocurrency

        collection = list
            name = bitcoin
            description = bitcoin is...
            Symbol = BTC
            website = https://bitcoin.org/
            connections = 8
            algorithm = SHA-256


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
    $mongoimport -d cryptocurrency -c list --type csv --file data.csv --headerline

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



Windows env

    run Mongodb
        Open command prompt
        rm data/mongod.lock
        mongod --dbpath "C:\Users\lexio\Dropbox\BLTZ\data"
        that's only

Change from csv to json
