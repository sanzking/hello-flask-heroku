from api import covid
from flask import Flask



app = Flask(__name__)

@app.route('/api/covid')
def hai():
	return covid

if __name__ == "__main__":
    app.run()
