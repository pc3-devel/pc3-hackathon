from flask import Flask, request, session
from werkzeug import secure_filename
import util, os, logging, random, json

#master data directory, stores the configuration and runtime data
#also stores the problem sets
dataDir = "data"

app = Flask(__name__)
app.debug=True
app.secret_key = "sekret key"
util = util.Util(dataDir)

#return the version if this is the only thing queried
@app.route("/")
def index():
    return "pc3 v1.0.0"

#simple file based auth, insecure but workable
@app.route("/authenticate", methods=["POST"])
def authenticate():
    #only work for requests of the correct type
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if util.checkLogin(username, password):
            #login cleared, therefore add to the session table
            session["username"] = username
            return "Success!"
        else:
            return "Bad Login!"
    else:
        return "Bad Request!"

#return the problem description
@app.route("/inform/<problem>")
def inform(problem):
    return util.getProblemDesc(problem)

#accept submissions to be run on the problem set
@app.route("/compete/<team>/<problem>/<lang>", methods=["POST"])
def compete(team, problem, lang):
    if "username" not in session:
        #bounce back for unauthenticated users
        return "You must be authenticated to do that!"
    if request.method == "POST":
        #if authenticated and POSTing, proceed
        file = request.files["teamCode"]

        #make a "safe" filename
        filename = secure_filename(file.filename)

        #store the code into the runs directory for the team
        file.save(os.path.join(util.makeRun(team, problem), filename))

        #run the code and grade it
        runStatus = util.doRun(team, problem, lang, filename)
        return str(runStatus)

#return the scoring table
@app.route("/scores")
def scores():
    return json.dumps(util.scoreboard.getRanks())

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0')
