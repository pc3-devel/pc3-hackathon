import os, glob

def getTeamRunNum(teamPath, problem):
    path = os.path.join(teamPath, problem, '*')
    runs = glob.glob(path)
    return len(runs)+1

def getTeamDataPath(dataDir, team):
    return os.path.join(dataDir, "teamData", team)

def makeRun(dataDir, team, problem):
    teamPath = getTeamDataPath(dataDir, team)
    runNum = getTeamRunNum(teamPath, problem)
    runPath = os.path.join(teamPath, problem, str(runNum))
    os.makedirs(runPath)
    return runPath

if __name__=="__main__":
    print getTeamRunNum(getTeamDataPath("data", "team1"), "problem1")
    makeRun("data", "team1", "problem1", None)
