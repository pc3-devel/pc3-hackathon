from flask import Flask, request, session
from werkzeug import secure_filename
import util, os, logging, random

dataDir = "data"

app = Flask(__name__)
app.debug=True
app.secret_key = "sekret key"
util = util.Util(dataDir)

@app.route("/")
def index():
    return "hello world"

@app.route("/authenticate", methods=["POST"])
def authenticate():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if util.checkLogin(username, password):
            session["username"] = username
            return "Success!"
        else:
            return "Bad Login!"
    else:
        return "Bad Request!"

@app.route("/inform/<problem>")
def inform(problem):
    pass

@app.route("/compete/<team>/<problem>/<lang>/", methods=["POST"])
def compete(team, problem, lang):
    if "username" not in session:
        return "You must be authenticated to do that!"
    if request.method == "POST":
        file = request.files["teamCode"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(util.makeRun(team, problem), filename))
        runStatus = util.doRun(team, problem, lang, filename)
        return str(runStatus)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run()
