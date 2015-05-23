from flask import Flask, request, session
from werkzeug import secure_filename
import util, flaskUtils, os, logging, random, json, sys

#default data directory, stores the configuration and runtime data
#also stores the problem sets
dataDir = os.path.join("pc3-data", "defaultData")

app = Flask(__name__)
app.debug=True
app.secret_key = os.urandom(32)


@app.route("/")
def index():
    """return the version if this is the only thing queried"""
    return "pc3 v1.0.0"

@app.route("/api/authenticate", methods=["POST"])
def authenticate():
    """simple file based auth, insecure but workable"""
    #only work for requests of the correct type
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if util.checkLogin(username, password):
            #login cleared, therefore add to the session table
            session["username"] = username
            return json.dumps({"status": True})
        else:
            return json.dumps({"status": False, reason: "bad login"}), 401
    else:
        return json.dumps({"status": False, reason: "bad method"}), 405

@app.route("/api/info/problems/<problem>")
def info_problem(problem):
    """return the problem description"""
    return json.dumps(util.getProblemDesc(problem))

@app.route("/api/run/<problem>/<lang>", methods=["POST"])
@flaskUtils.requires_auth
def run(problem, lang, team="NOTEAM"):
    """accept submissions to be run on the problem set"""
    problem = problem.lower()
    lang = lang.lower()

    if problem not in [s.lower() for s in util.problemSet]:
        return json.dumps({"status": False, "reason": "bad problem ID"}), 400

    if lang not in [s.lower() for s in util.langs]:
        return json.dumps({"status": False, "reason": "bad language ID"}), 400

    if request.method == "POST":
        #if authenticated and POSTing, proceed
        file = request.files["teamCode"]

        #make a "safe" filename
        filename = secure_filename(file.filename)

        #store the code into the runs directory for the team
        file.save(os.path.join(util.makeRun(team, problem), filename))

        #run the code and grade it
        runCorrect, points = util.doRun(team, problem, lang, filename)
        return json.dumps({"status": True, "correct": runCorrect, "message": "Problem Solved: %s\nPoints Received: %i" % (runStatus, points)})

@app.route("/api/info/scores")
def info_scores():
    """return the scoring table"""
    return json.dumps(util.scoreboard.getRanks())
    
@app.route("/api/supervise/override/<team>/<problem>", methods=["POST"])
@flaskutils.requires_auth # Need to implement a decorator for requiring supervisor perms
def supervise_override(team, problem):
    """manually override a team's score for a problem."""
    
    # Verify the problem id.
    problem = problem.lower()
    if problem not in [s.lower() for s in util.problemSet]:
        return json.dumps({"status": False, "reason": "bad problem ID"}), 400
    
    if request.method == "POST":
        return json.dumps({"status": False, "reason": "manual override not yet implemented"}), 501
        
@app.route("/api/supervise/kill/<team>/<problem>/<run>")
@flaskutils.requires_auth # See note on supervise_override
def supervise_kill(team, problem, run):
    """kill a malfunctioning run"""
    # I have no idea how this should be implemented.
    return json.dumps({"status": False, "reason": "run management not yet implemented"}), 501

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) == 2 and os.path.isdir(sys.argv[1]): # overriding data directory
        dataDir = sys.argv[1]
    util = util.Util(dataDir)
    app.run(host='0.0.0.0')
