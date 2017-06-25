# analysis

## Initialize Mongodb
1) use docker image 

docker run -p 27017:27017 --name mongo -d mongo

// use mongo-express or robomongo

docker container run -p 27017:27017 --name mongodb -d mongo && docker container run -it -p 8081:8081 --name mongo_express --link mongodb:mongo -d mongo-express

2) python importdata/instrument.py
3) python importdata/instrumentDailyData.py


#000001:上证指数，所有股票之和
#399300: 沪深300
#399301: 深圳成指