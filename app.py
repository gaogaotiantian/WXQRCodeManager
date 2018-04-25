#coding=utf-8

# python built-in packages
import os
import io
import json
import time
import base64


# other published packages
from flask import Flask, request, send_file, render_template, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from PIL import Image


# our packages
from QRCodeReader import QRCodeReader as QR

DATABASE_URL = None
if os.environ.get('DATABASE_URL') != None:
    DATABASE_URL = os.environ.get('DATABASE_URL')

if os.environ.get('TESSERACT_PATH') != None:
    QR.set_tesseract_path(os.environ.get('TESSERACT_PATH'))

app = Flask(__name__, static_url_path = '/static')


app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
CORS(app)
db = SQLAlchemy(app)

class QRCodeDb(db.Model):
    __tablename__ = 'qrcode'
    id           = db.Column(db.Integer, primary_key = True)
    url          = db.Column(db.String(256))
    add_time     = db.Column(db.Float)
    expire_time  = db.Column(db.Float)
    name         = db.Column(db.String(256))
    tags         = db.Column(db.String(256))
    description  = db.Column(db.Text)
    session_id   = db.Column(db.String(32))
    session_time = db.Column(db.Float)
    search_text  = db.Column(db.Text)
    read         = db.Column(db.Integer, default = 0)

    def to_dict(self):
        ret = {}
        ret['id'] = self.id
        ret['name'] = self.name
        ret['description'] = self.description
        ret['tags'] = self.tags.strip().split()
        ret['session_id'] = self.session_id
        ret['session_time'] = self.session_time
        return ret

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
            return make_response(jsonify({"err_msg":"You need to input a valid id"}), 400)
        try:
            int(id)
        except:
            return make_response(jsonify({"err_msg":"You need to input a valid id"}), 400)

        qrInfo = QRCodeDb.query.get(id)
        if qrInfo != None:
            reader = QR.QRCodeReader()
            image = reader.generate_image(QR.QRCode(url = qrInfo.url, name = qrInfo.name, date=""))
            # Convert the image into Bytes
            file = io.BytesIO()
            image.save(file, 'jpeg')
            file.seek(0)
            return send_file(file, as_attachment=True, attachment_filename='myfile.jpg')
        else:
            return make_response(jsonify({"err_msg":"Cannot find the id in database"}), 404)

    if request.method == 'POST':
        file = request.files.get("img")
        if file == None:
            return make_response(jsonify({"err_msg":"Cannot find the attached file. It must be a form-data contains the key pair 'img':imgFile"}), 400)
        image = None
        try:
            image = Image.open(file)
        except:
            return make_response(jsonify({"err_msg":"The file is not a valid image"}), 400)

        if image != None:
            reader = QR.QRCodeReader()
            qrcode = reader.get_qrcode_data(image)
            if qrcode == None:
                return make_response(jsonify({"err_msg":"Cannot read QRCode from the image."}), 400)
            url = qrcode.url
            # Check whether url is a valid wechat group url
            if not url.startswith("https://weixin.qq.com/g/"):
                return make_response(jsonify({"err_msg":"The QRCode is not a valid WeChat group code."}), 400)
            # Generate the session_id and session_time pair
            session_id = base64.urlsafe_b64encode(os.urandom(24)).decode('utf-8')
            session_time = time.time()
            # Check same QRcode
            urlDb = QRCodeDb.query.filter_by(url=url).first()
            if urlDb == None:
                maxId = db.session.query(db.func.max(QRCodeDb.id)).scalar()
                qrInfo = QRCodeDb()
                qrInfo.id = maxId + 1 if maxId != None else 1
                qrInfo.url = url
                qrInfo.expire_time = 0.0
                qrInfo.add_time = time.time()
                qrInfo.name = qrcode.name
                qrInfo.tags = ""
                qrInfo.description = ""
                qrInfo.search_text = qrcode.name
                qrInfo.session_id = session_id
                qrInfo.session_time = session_time
                db.session.add(qrInfo)
                db.session.commit()
                return make_response(jsonify(qrInfo.to_dict()), 201)
            else:
                urlDb.session_id = session_id
                urlDb.session_time = session_time
                db.session.commit()
                return make_response(jsonify(urlDb.to_dict()), 200)

    return make_response("Invalid request method, only support GET or POST", 405)


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
@app.route('/api/v1/groups', methods=['GET', 'POST'])
def groups():
    '''
        keywords = request.args.get ("keywords")
        groups = []
        for elem in QRCodeDb.query.filter_by(keywords = keywords).all():
            groups.append ({"id":elem.id, "name":elem.name, "tags":elem.tags})
        return json.dump(groups)

    '''
    if request.method == 'GET':
        keywords_str = request.args.get("keywords")
        keywords = []
        if keywords_str != None:
            keywords = keywords_str.strip().split()

        limit = 20
        limit_str = request.args.get("limit")
        if limit_str != None:
            try:
                limit = limit_str
            except:
                pass

        q = QRCodeDb.query
        for keyword in keywords:
            q = q.filter(QRCodeDb.search_text.ilike("%"+keyword+"%"))

        q = q.limit(limit)
        ret_list = [qrcode.to_dict() for qrcode in q.all()]

        return make_response(jsonify ({'results':ret_list}), 200)

    elif request.method == 'POST':
        data = request.json
        if data == None:
            return make_response(jsonify({"err_msg":"Invalid parameter"}), 400)
        try:
            id = data['id']
            name = data['name']
            tags = data['tags']
            description = data['description']
            # WARNING: : Waiting for front end to be updated
            session_id = None
            session_time = 0.0
            try:
                session_id = data['session_id']
                session_time = data['session_time']
            except:
                print("session_id or session_time is empty")
        except:
            return make_response(jsonify({"err_msg":"Invalid parameter"}), 400)
        qrInfo = QRCodeDb.query.get(id)
        if qrInfo != None:
            # WARNING: need to be uncommented after front end is updateds.
            """
            if session_id != qrInfo.session_id:
                return make_response(jsonify({"err_msg":"Unsafe behavior"}), 400)
            if time.time() - session_time >= 100.0:
                return make_response(jsonify({"err_msg":"Operation expired"}), 400)
            """
            qrInfo.name = name
            qrInfo.tags = tags
            qrInfo.description = description
            qrInfo.search_text = " ".join([name, tags, description])
            db.session.commit()
        else:
            return make_response(jsonify({"err_msg":"Invalid parameter"}), 400)

        return make_response(jsonify({}), 201)



@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
