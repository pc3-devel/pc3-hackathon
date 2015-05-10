import os, glob, CodeRunner, logging, json, loader, scoring

#general purpose class to keep all the stuff that isn't in the
#web routing module

class Util:
    def __init__(self, dataDir):
        """init the internal instances of stuff"""
        self.dataDir = dataDir
        self.logger = logging.getLogger("util")
        self.logger.debug("Data dir is: " + dataDir)
        self.problemSet = loader.Loader(dataDir).problemsDictionary
        self.evaluator = CodeRunner.Evaluate(dataDir)
        self.langs = self.evaluator.getLangs()
        self.logger.info("Supporting the following languages: " + str(self.langs))
        self.passwd = json.load(open(os.path.join(dataDir, "passwd.json")))
        self.scoreboard = scoring.ScoreBoard(dataDir)

    def getTeamRunNum(self, teamPath, problem):
        """figure out what run number this one is"""
        path = os.path.join(teamPath, problem, '*')
        runs = glob.glob(path)
        #plus one because we want to create the current run directory
        return len(runs)+1

    def getTeamDataPath(self, team):
        """convenience function to build the team path"""
        return os.path.join(self.dataDir, "teamData", team)

    def makeRun(self, team, problem):
        """generate the paths, numbers, and run context"""
        teamPath = self.getTeamDataPath(team)
        runNum = self.getTeamRunNum(teamPath, problem)
        runPath = os.path.join(teamPath, problem, str(runNum))
        os.makedirs(runPath)
        return runPath

    def doRun(self, team, problem, lang, teamFile):
        """actually run the code"""
        problemDir=os.path.join(self.getTeamDataPath(team), problem, str(self.getTeamRunNum(self.getTeamDataPath(team), problem)-1))

        #evaluate the status of the run
        runStatus, teamOutput, goodOutput, lazyOn = self.evaluator.evaluate(lang, teamFile, problemDir, self.problemSet[problem])

        #check status and manage scoreboard
        if runStatus:
            points = self.problemSet[problem]["meta"]["points"]
            self.scoreboard.solve(team, problem, points) 
        else:
            points = 0
        with open(os.path.join(problemDir, "result.json"), "w") as f:
            json.dump({"solved":runStatus, "teamOutput":teamOutput, "expectedOutput":goodOutput, "lazyMode":lazyOn}, f)
        return (runStatus, points)

    #TODO make this even remotely secure
    def checkLogin(self, username, password):
        return self.passwd[username] == password

    def getProblemDesc(self, problem):
        """convenience function to get the description from the problem"""
        return self.problemSet[problem]["desc"]

if __name__=="__main__":
    u = Util("data")
    print u.getTeamRunNum(getTeamDataPath("data", "team1"), "problem1")
    u.makeRun("data", "team1", "problem1", None)
