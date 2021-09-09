from flask import Flask, request, render_template, make_response
import requests as req
from bs4 import BeautifulSoup as  bs
import json


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/filmapik/new_movie')
def filmapik():
    url = "https://filmapik.world/"
    r = req.get(url)
    soup = bs(r.content, 'html.parser')
    container = soup.find('div', attrs = {'id':'main'}).find('div', class_='container').find('div', class_='main-content').find('div', class_='movies-list-wrap').find('div', class_='tab-content').find('div', class_='movies-list').findAll('div', class_='ml-item')
    for i in range(len(container)):
        res = container[i]
        link = res.find('a')['href']
        resolusi = res.find('a').find('span', class_='mli-quality').text
        tumbnail = res.find('a').find('img')['data-original']
        rating = res.find('a').find('span', class_='mli-rating').text
        judul = res.find('a').find('span', class_='mli-info').find('h2').text
        data = {
            "status":200,
            "creator":"sanzking",
            "result":{
                "judul":judul,
                "tumbnail":tumbnail,
                "resolusi":resolusi,
                "rating":rating,
                "link":link
            }
        }
        b = json.dumps(data, indent=4)
        drakorst = make_response(b)
        drakorst.headers['Content-Type'] = 'application/json; charset=utf-8'
        drakorst.headers['mimetype'] = 'application/json'
        return drakorst

@app.route('/api/dramaindo', methods=['GET', 'POST'])
def dramaindo():
    nama_dramaindo = request.args['judul']
    return di(nama_dramaindo)

def di(keyword):
    url = "https://163.172.111.222/?s="
    r = req.get(url+keyword)
    soup = bs(r.content, 'html.parser')
    container = soup.find('div', class_='container').find('div', class_='wrapper').find('div', class_='post-wrapper').find('div', class_='post').findAll('article')
    for i in range(len(container)):
        res = container[i]
        link = res.find('div', class_='thumb').find('a')['href']
        s = req.get(link)
        soup1 = bs(s.content, 'html.parser')
        sinopsis = soup1.find('div', class_='container').find('div', class_='wrapper').find('div', class_='post-wrapper').find('div', class_='sinopsis').find('div', class_='content').findAll('p')[0].text
        judul_ = soup1.find('div', class_='container').find('div', class_='wrapper').find('div', class_='post-wrapper').find('div', class_='info_single').find('div', class_='info_2').find('ul').findAll('li')[0].text
        genre_ = soup1.find('div', class_='container').find('div', class_='wrapper').find('div', class_='post-wrapper').find('div', class_='info_single').find('div', class_='info_2').find('ul').findAll('li')[2].text
        cast_ = soup1.find('div', class_='container').find('div', class_='wrapper').find('div', class_='post-wrapper').find('div', class_='info_single').find('div', class_='info_2').find('ul').findAll('li')[3].text
        year_ = soup1.find('div', class_='container').find('div', class_='wrapper').find('div', class_='post-wrapper').find('div', class_='info_single').find('div', class_='info_2').find('ul').findAll('li')[4].text
        episode_ = soup1.find('div', class_='container').find('div', class_='wrapper').find('div', class_='post-wrapper').find('div', class_='info_single').find('div', class_='info_2').find('ul').findAll('li')[5].text
        duration_ = soup1.find('div', class_='container').find('div', class_='wrapper').find('div', class_='post-wrapper').find('div', class_='info_single').find('div', class_='info_2').find('ul').findAll('li')[7].text

        judul = judul_.split(':')[1]
        genre = genre_.split(':')[1]
        cast = cast_.split(':')[1]
        year = year_.split(':')[1]
        episode = episode_.split(':')[1]
        duration = duration_.split(':')[1]


        data = {
            "status":200,
            "creator":"sanzking",
            "result":{
                "judul":judul,
                "genre":genre,
                "pemain":cast,
                "tahun":year,
                "episode":episode,
                "durasi":duration,
                "sinopsis":sinopsis,
                "link":link
            }
        }
        b = json.dumps(data, indent=4)
        response = make_response(b)
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        response.headers['mimetype'] = 'application/json'
        return response

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
        drakorst = make_response(b)
        drakorst.headers['Content-Type'] = 'application/json; charset=utf-8'
        drakorst.headers['mimetype'] = 'application/json'
        return drakorst

@app.route('/api/covid')
def covid():
    url = "http://www.sanzstore.org/api/covid"
    html = req.get(url).text
    js = json.loads(html)
    positif = js["result"]["positif"]
    meninggal = js["result"]["meninggal"]
    sembuh = js["result"]["sembuh"]

    data_covid = {
        "creator":"sanzking",
        "status":200,
        "result":{
            "positif":positif,
         "meninggal":meninggal,
            "sembuh":sembuh
     }
    }

    cv = json.dumps(data_covid, indent=4)
    cvd = make_response(cv)
    cvd.headers['Content-Type'] = 'application/json; charset=utf-8'
    cvd.headers['mimetype'] = 'application/json'
    return cvd
    
if __name__ == '__main__':
    app.run(debug=True)
