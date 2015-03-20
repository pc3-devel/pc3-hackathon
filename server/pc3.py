from flask import Flask, request, session
from werkzeug import secure_filename
import util, flaskUtils, os, logging, random, json

#master data directory, stores the configuration and runtime data
#also stores the problem sets
dataDir = "data"

app = Flask(__name__)
app.debug=True
app.secret_key = os.urandom(32)

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
            return json.dumps({"status":True, "message":"Successfully Authenticated"})
        else:
            return json.dumps({"status":False, "message":"Bad Login"})
    else:
        return json.dumps({"status":False, "message":"Incorrect Request"})

#return the problem description
@app.route("/inform/<problem>")
def inform(problem):
    return json.dumps(util.getProblemDesc(problem))

#accept submissions to be run on the problem set
@app.route("/compete/<problem>/<lang>", methods=["POST"])
@flaskUtils.requires_auth
def compete(problem, lang, team="NOTEAM"):
    problem = problem.lower()
    lang = lang.lower()

    if problem not in [s.lower() for s in util.problemSet]:
        return json.dumps({"status":False, "message":"That is not a valid problem identifier!"})

    if lang not in [s.lower() for s in util.langs]:
        return json.dumps({"status":False, "message":"That is not a valid language identifier!"})

    if request.method == "POST":
        #if authenticated and POSTing, proceed
        file = request.files["teamCode"]

        #make a "safe" filename
        filename = secure_filename(file.filename)

        #store the code into the runs directory for the team
        file.save(os.path.join(util.makeRun(team, problem), filename))

        #run the code and grade it
        runStatus = util.doRun(team, problem, lang, filename)
        return json.dumps(runStatus)

#return the scoring table
@app.route("/scores")
def scores():
    return json.dumps(util.scoreboard.getRanks())

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    util = util.Util(dataDir)
    app.run(host='0.0.0.0')
