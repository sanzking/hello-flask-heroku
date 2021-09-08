from bs4 import BeautifulSoup as bs
import requests as req
import json as js
from flask import Flask

url = "http://www.sanzstore.org/api/covid"
html = req.get(url).text
json = js.loads(html)
positif = json["result"]["positif"]
meninggal = json["result"]["meninggal"]
sembuh = json["result"]["sembuh"]
print(positif)
print(meninggal)
print(sembuh)

json_data = {
    "positif":positif,
    "meninggal":meninggal,
    "sembuh":sembuh
}

app = Flask(__name__)


@app.route('/')
def hello_world():
    return json_data

if __name__ == '__main__':
    app.run()
