# Paid API Flask Template
## Requirements
**packages:** flask

```pip install flask=2.2.2```

**python version:** tested on python 3.7.1

## Technology used:
this template have been made with **flask** and **sqlite3** as a simple database. it's not very pratical but still a good example for working with paid api. no security layers were used to stop bots from cracking it but you may add more. i would recommand requesting the balance api with 4 diffrent data from server side.

after paiment confirmed, make a post request to the server with a payload composed of these three informations:
- **confirmed email**
- **api key**
- **purchased option** *(added balance)*
- **secure key**: a secure key saved on *.env* that changes every 5 minutes.

## Actual problems with this template
as i said in the last part; this template is not pratical at all ! use *mysql* for better experience. with *sqlite3* you have to look the database everytime which will a negative point and would make the api so slow if you get multiple customers.

PS: the main reason i choosed to use sqlite3 is because the library already exists in python and i have already used it in other simple project. when i started this project i barely had any internet connection so i couldn't use any alternative libraries like *mysql-connect* or *firebase-python* for this so purpose !

## Test of template !
### on your terminal:
```
    cd C:/Pc/..../paid-api-template/
    flask --app main --debug run
```
### on your browser:
- **create new user**: go to [create account](https://127.0.0.1:5000/api/newmember/hcn1z1). this is an example of creating a user undertitled *hcn1z1*.

- **add balance to user**: go to [more balance](https://127.0.0.1:5000/api/morebalance/hcn1z1). this simple get request will add 200$ balance to *hcn1z1* account.

### on your ipython:
```
import json
from requests import post as POST
API_KEY = "get api key from terminal or from database"
url = "https://127.0.0.1:5000/api/hcn1z1/paid_function"
data = {"apikey":API_KEY,"name":"hcn1z1","number":"17602395911"}
resp = POST(url,data = json.dumps(data))

```

PS: if you don't have python use command ```pip install ipython```. to enter ipython open a new cmd window and type **ipython**.