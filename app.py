#coding=utf-8

# python built-in packages
import os
import io
import json


# other published packages
from flask import Flask, request, send_file, render_template, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from PIL import Image


# our packages
from QRCodeReader import QRCodeReader as QR

DATABASE_URL = None
if os.environ.get('DATABASE_URL') != None:
    DATABASE_URL = os.environ.get('DATABASE_URL')

app = Flask(__name__, static_url_path = '/static')


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
        if id == None:
            return make_response("You need to input a valid id", 400)
        try:
            int(id)
        except:
            return make_response("You need to input a valid id", 400)

        qrInfo = QRCodeDb.query.get(id)
        if qrInfo != None:
            reader = QR.QRCodeReader()
            image = reader.generate_image(qrInfo.url)
            # Convert the image into Bytes
            file = io.BytesIO()
            image.save(file, 'jpeg')
            file.seek(0)
            return send_file(file, as_attachment=True, attachment_filename='myfile.jpg')
        else:
            return make_response("Cannot find the id in database", 200)

    if request.method == 'POST':
        file = request.files.get("img")
        if file == None:
            return make_response("Cannot find the attached file. It must be a form-data contains the key pair 'img':imgFile", 400)
        image = None
        try:
            image = Image.open(file)
        except:
            return make_response("The file is not a valid image", 400)

        if image != None:
            reader = QR.QRCodeReader()
            qrcode = reader.get_qrcode_data(image)
            if qrcode == None:
                return make_response("Cannot read QRCode from the image.", 200)
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
                return make_response("Saved successfully!", 200)
            else:
                return make_response("QRCode already exists, didn't save.", 200)

    return make_response("Invalid request method, only support GET or POST", 400)


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
'''
	keywords = request.args.get ("keywords")
	groups = []
	for elem in QRCodeDb.query.filter_by(keywords = keywords).all():
		groups.append ({"id":elem.id, "name":elem.name, "tags":elem.tags})
	return json.dump(groups)

'''
	faked_list = [ {"id" : 1234, "name" : "name00", "tags" : ["tags00", "tags01", "tags02"] }, 
		       {"id" : 1235, "name" : "name01", "tags" : ["tags01", "tags03", "tags04"] },
		       {"id" : 1236, "name" : "name02", "tags" : ["tags02", "tags04", "tags05"] } ]
	return Response( jsonify (results = faked_list), status = 200) 

@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
