#coding=utf-8

# python built-in packages
import os

# other published packages
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# our packages
from QRCodeReader import QRCodeReader

if os.environ.get('DATABASE_URL') != None:
    DATABASE_URL = os.environ.get('DATABASE_URL')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
CORS(app)
db = SQLAlchemy(app)

class QRCodeDb(db.Model):
    __tablename__ = 'qrcode'
    id          = db.Column(db.Integer, primary_key = True)
    url         = db.Column(db.String(256))
    expire_time = db.Column(db.Float)
    tags        = db.Column(db.String(256))

db.create_all()

@app.route('/')
def index():
    return 'Hello world!'

'''
Read https://developers.weixin.qq.com/miniprogram/dev/api/network-file.html

POST:
    Upload a file from the client. 

    The server should be able to receive the image, pass it to QRCodeReader,
    get the decoded data and save it in the database.

Get:
    Download an image from the server. 
    A legit request from the client should have an arg "id" to identify which
    qrcode the client needs. Get this from "request.args.get('id')"
    This id should match the qrcode id in database
'''
@app.route('/api/v1/qrcode', methods=['GET', 'POST'])
def qrcode():
    pass
