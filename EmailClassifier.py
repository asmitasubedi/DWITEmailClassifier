from flask import Flask, render_template
import pickle

app = Flask(__name__)

allPickle = pickle.load(open("RESULT.pickle", "rb"))


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/admin')
def adminEmails():
    adminEmails = allPickle.get("adminEmails")
    return render_template("admin.html", result = adminEmails)


@app.route('/club')
def clubEmails():
    clubEmails = allPickle.get("clubEmails")
    return render_template("club.html", result = clubEmails)

@app.route('/class')
def classEmails():
    classEmails = allPickle.get("classEmails")
    return render_template("class.html", result = classEmails)

@app.route('/msc')
def msc():
    msc = allPickle.get("msc")
    return render_template("msc.html", result = msc)

if __name__ == '__main__':
    app.run(debug=True)
