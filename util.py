import os, glob, CodeRunner, logging

class Util:
    def __init__(self, dataDir):
        self.logger = logging.getLogger("util")
        self.logger.debug("Data dir is: " + dataDir)
        self.evaluator = CodeRunner.Evaluate(dataDir)

    def getTeamRunNum(self, teamPath, problem):
        path = os.path.join(teamPath, problem, '*')
        runs = glob.glob(path)
        return len(runs)+1

    def getTeamDataPath(self, dataDir, team):
        return os.path.join(dataDir, "teamData", team)

    def makeRun(self, dataDir, team, problem):
        teamPath = self.getTeamDataPath(dataDir, team)
        runNum = self.getTeamRunNum(teamPath, problem)
        runPath = os.path.join(teamPath, problem, str(runNum))
        os.makedirs(runPath)
        return runPath

    def doRun(self, team, problem):
        pass

if __name__=="__main__":
    u = Util("data")
    print u.getTeamRunNum(getTeamDataPath("data", "team1"), "problem1")
    u.makeRun("data", "team1", "problem1", None)
