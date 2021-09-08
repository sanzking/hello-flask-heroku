import requests as req
import json as js

url = "http://www.sanzstore.org/api/covid"
html = req.get(url).text
json = js.loads(html)
positif = json["result"]["positif"]
meninggal = json["result"]["meninggal"]
sembuh = json["result"]["sembuh"]

json_data = {
	"creator":"sanzking",
	"status":200,
	"result":{
    	"positif":positif,
   	 "meninggal":meninggal,
    	"sembuh":sembuh
    }
}

print(json_data)
