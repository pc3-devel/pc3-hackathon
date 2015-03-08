from flask import Flask, request
from werkzeug import secure_filename
import LanguageSupport, CodeRunner, util, os

app = Flask(__name__)
app.debug=True

@app.route("/")
def index():
    return "hello world"

@app.route("/inform/<problem>")
def inform(problem):
    pass

@app.route("/compete/<team>/<problem>/<lang>/", methods=["POST"])
def compete(team, problem, lang):
    if request.method == "POST":
        file = request.files["teamCode"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(util.makeRun("data", team, problem), filename))
        return "Success!"

if __name__ == "__main__":
    app.run()
