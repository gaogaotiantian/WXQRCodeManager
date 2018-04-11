from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("test.html")

# pre:id        post: image
@app.route("/qrcodeget")
def qrcodeget():
    return render_template("qrcodeget.html")

# pre:image     post: send to QR reader
@app.route("/qrcodepost")
def qrcodepost():
    return render_template("qrcodepost.html")

# pre:keywords  post: all groups contain the keywords
@app.route("/groups")
def groups():
    return render_template("groups.html")
# runs on localhost
app.run(debug=True)