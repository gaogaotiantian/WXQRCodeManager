from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import unittest
import requests

DATABASE_URL = None
if os.environ.get('DATABASE_URL') != None:
    DATABASE_URL = os.environ.get('DATABASE_URL')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
CORS(app)
db = SQLAlchemy(app)
app.testing = True
app = app.test_client()

url = 'http://127.0.0.1:5000'

class qrcode_get(unittest.TestCase):

    def test_run(self):
        assert requests.get(url+'/')

    def test_get_id1(self):
        r = requests.get(url + '/api/v1/qrcode?id=1')
        #print(requests.get(url + '/api/v1/qrcode?id=1').text)
        assert r
        assert r.status_code == 200

    def test_get_id10000(self):
        r = requests.get(url + '/api/v1/qrcode?id=10000')
        assert r.text == "Cannot find the id in database"
        assert r.status_code == 200

    def test_get_invald_id(self):
        r = requests.get(url + '/api/v1/qrcode?id=stub')
        assert r.text == "You need to input a valid id"
        assert r.status_code == 400

    def test_get_noId(self):
        r = requests.get(url + '/api/v1/qrcode')
        assert r.text == "You need to input a valid id"
        assert r.status_code == 400

    def test_get_random_argument(self):
        r = requests.get(url + '/api/v1/qrcode?stub=stub')
        assert r.text == "You need to input a valid id"
        assert r.status_code == 400

if __name__ == "__main__":
    unittest.main()