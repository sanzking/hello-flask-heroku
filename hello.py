import requests
import json
from flask import Flask

url = "http://www.sanzstore.org/api/covid"
html = requests.get(url).text
raw = json.loads(html)
positif = raw["result"]["positif"]
meninggal = raw["result"]["meninggal"]
sembuh = raw["result"]["sembuh"]

data = {
    "positif":positif,
    "meninggal":meninggal,
    "sembuh":sembuh
}

app = Flask(__name__)

@app.route('/')
def hello_world():
    return data

if __name__ == '__main__':
    app.run()
