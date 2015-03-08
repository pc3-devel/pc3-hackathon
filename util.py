import os, glob, CodeRunner, logging, json, loader

class Util:
    def __init__(self, dataDir):
        self.logger = logging.getLogger("util")
        self.logger.debug("Data dir is: " + dataDir)
        self.problemSet = loader.Loader(dataDir).problemsDictionary
        self.logger.debug(self.problemSet)
        self.evaluator = CodeRunner.Evaluate(dataDir)
        self.dataDir = dataDir
        self.passwd = json.load(open(os.path.join(dataDir, "passwd.json")))

    def getTeamRunNum(self, teamPath, problem):
        path = os.path.join(teamPath, problem, '*')
        runs = glob.glob(path)
        return len(runs)+1

    def getTeamDataPath(self, team):
        return os.path.join(self.dataDir, "teamData", team)

    def makeRun(self, team, problem):
        teamPath = self.getTeamDataPath(team)
        runNum = self.getTeamRunNum(teamPath, problem)
        runPath = os.path.join(teamPath, problem, str(runNum))
        os.makedirs(runPath)
        return runPath

    def doRun(self, team, problem, lang, teamFile):
        problemDir=os.path.join(self.getTeamDataPath(team), problem, str(self.getTeamRunNum(self.getTeamDataPath(team), problem)-1))
        return self.evaluator.evaluate(lang, teamFile, problemDir)

    #TODO make this even remotely secure
    def checkLogin(self, username, password):
        return self.passwd[username] == password

    def getProblemDesc(self, problem):
        return self.problemSet[problem]["desc"]

if __name__=="__main__":
    u = Util("data")
    print u.getTeamRunNum(getTeamDataPath("data", "team1"), "problem1")
    u.makeRun("data", "team1", "problem1", None)
