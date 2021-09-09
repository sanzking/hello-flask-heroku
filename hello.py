from flask import Flask, request, render_template, make_response
import requests as req
from bs4 import BeautifulSoup as  bs
import json


app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/api/drakorstation', methods=['GET', 'POST'])
def drakorstation():
	nama = request.args['judul']
	return ds(nama)

def ds(keyword):
	url = "https://drakorstation.org/?s="
	r = req.get(url+keyword)
	soup = bs(r.content, 'html.parser')
	container = soup.find('div', attrs = {'id':'container'}).find('div', attrs = {'id':'content'}).find('div', attrs = {'id':'inner-content'}).find('div', attrs = {'id':'main'}).findAll('article')
	for i in range(len(container)):
		res = container[i]
		link = res.find('header').find('h2', class_='post-title').find('a')['href']
		s = req.get(link)
		soup1 = bs(s.content, 'html.parser')
		sinopsis = soup1.find('div', attrs = {'id':'container'}).find('div', attrs = {'id':'content'}).find('div', attrs = {'id':'inner-content'}).find('div', attrs = {'id':'main'}).find('article').find('section').findAll('p')[0].text
		judul_ = soup1.find('div', attrs = {'id':'container'}).find('div', attrs = {'id':'content'}).find('div', attrs = {'id':'inner-content'}).find('div', attrs = {'id':'main'}).find('article').find('section').findAll('h3')[0].text
		genre_ = soup1.find('div', attrs = {'id':'container'}).find('div', attrs = {'id':'content'}).find('div', attrs = {'id':'inner-content'}).find('div', attrs = {'id':'main'}).find('article').find('section').findAll('h3')[2].text
		director_ = soup1.find('div', attrs = {'id':'container'}).find('div', attrs = {'id':'content'}).find('div', attrs = {'id':'inner-content'}).find('div', attrs = {'id':'main'}).find('article').find('section').findAll('h3')[3].text
		penulis_ = soup1.find('div', attrs = {'id':'container'}).find('div', attrs = {'id':'content'}).find('div', attrs = {'id':'inner-content'}).find('div', attrs = {'id':'main'}).find('article').find('section').findAll('h3')[4].text
		episode_ = soup1.find('div', attrs = {'id':'container'}).find('div', attrs = {'id':'content'}).find('div', attrs = {'id':'inner-content'}).find('div', attrs = {'id':'main'}).find('article').find('section').findAll('h3')[5].text
		jadwal_ = soup1.find('div', attrs = {'id':'container'}).find('div', attrs = {'id':'content'}).find('div', attrs = {'id':'inner-content'}).find('div', attrs = {'id':'main'}).find('article').find('section').findAll('h3')[6].text

		judul = judul_.split(':')[1]
		genre = genre_.split(':')[1]
		director = director_.split(':')[1]
		penulis = penulis_.split(':')[1]
		episode = episode_.split(':')[1]
		jadwal = jadwal_.split(':')[1]


		data = {
		    "status":200,
		    "creator":"sanzking",
		    "result":{
		        "judul":judul,
		        "genre":genre,
		        "director":director,
		        "penulis":penulis,
		        "episode":episode,
		        "jadwal":jadwal,
		        "sinopsis":sinopsis,
		        "link":link
		    }
		}
		b = json.dumps(data, indent=4)
		response = make_response(b)
		response.headers['Content-Type'] = 'application/json; charset=utf-8'
		response.headers['mimetype'] = 'application/json'
		return response
		
if __name__ == '__main__':
    app.run(debug=True)
