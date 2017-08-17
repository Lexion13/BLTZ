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


db seed 
    $mongo
    >use cryptocurrency;
    >db.list.insert({
        name: 'bitcoin',
        description: 'bitcoin is ...',
        symbol: 'BTC',
        website: 'https://bitcoin.org',
        algorithm: 'SHA-256'
    });
    
