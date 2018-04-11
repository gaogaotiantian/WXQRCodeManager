#coding=utf-8

# python built-in packages
import os
import io
from tempfile import NamedTemporaryFile
from shutil import copyfileobj

# other published packages
from flask import Flask, request, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from PIL import Image


# our packages
from QRCodeReader import QRCodeReader as QR

DATABASE_URL = None
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
    name        = db.Column(db.String(256))
    tags        = db.Column(db.String(256))

db.create_all()

@app.route('/')
def index():
    return 'Hello world!'


'''
Read https://developers.weixin.qq.com/miniprogram/dev/api/network-file.html

POST:
    Upload an image from the client.

    The server should be able to receive the image, pass it to QRCodeReader,
    get the decoded data and save it in the database.

GET:
    arg:
        'id': id for the image

    Download an image from the server.
    A legit request from the client should have an arg "id" to identify which
    qrcode the client needs. Get this from "request.args.get('id')"
    This id should match the qrcode id in database
'''
@app.route('/api/v1/qrcode', methods=['GET', 'POST'])
def qrcode():
    if request.method == 'GET':
        id = request.args.get('id')
        qrInfo = QRCodeDb.query.get(id)
        if qrInfo != None:
            reader = QR.QRCodeReader()
            image = reader.generate_image(qrInfo.url)
            # Convert the image into Bytes
            image.save("/tmp/img{}.jpeg".format(qrInfo.id), "JPEG")
            tempFileObj = NamedTemporaryFile(mode='w+b',suffix='jpg')
            tempImg = open("/tmp/img{}.jpeg".format(qrInfo.id),'rb')
            copyfileobj(tempImg,tempFileObj)
            tempImg.close()
            os.remove("/tmp/img{}.jpeg".format(qrInfo.id))
            tempFileObj.seek(0,0)
            return send_file(tempFileObj, as_attachment=True, attachment_filename='myfile.jpg')
        else:
            return "Request id is not found in "

    if request.method == 'POST':
        image = Image.open(request.files.get("Image"))
        if image != None:
            reader = QR.QRCodeReader()
            qrcode = reader.get_qrcode_data(image)
            if qrcode == None:
                return "Invalid QRCode picture"
            url = qrcode.url
            # DEBUG: Need to add QRCode checker
            # Check same QRcode
            urlDb = QRCodeDb.query.filter_by(url=url).first()
            if urlDb == None:
                maxId = db.session.query(db.func.max(QRCodeDb.id)).scalar()
                qrInfo = QRCodeDb()
                qrInfo.id = maxId + 1 if maxId != None else 1
                qrInfo.url = url
                qrInfo.expire_time = 0.0
                qrInfo.name = "None"
                qrInfo.tags = "Test"
                db.session.add(qrInfo)
                db.session.commit()
                return "Successful!"
            else:
                return "QRCode already exists!"

    return "Invalid request method"


'''
GET:
    arg:
        'keywords': a string of key words
    return:
        'groups':
            'id': id of the group
            'name': name of the group
            'tags': tags of the group

    Get a list of groups that match the key words.
'''
@app.route('/api/v1/groups', methods=['GET'])
def groups():
    pass

if __name__ == "__main__":
    app.run(debug = True)
