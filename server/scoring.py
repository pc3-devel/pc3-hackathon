import logging, json, os

class ScoreBoard:
    def __init__(self, dataDir):
        self.logger = logging.getLogger(__name__)
        self.dataDir = dataDir

        #attempt to get the JSON file, or create one if not found
        try:
            with open(os.path.join(dataDir, "scores.json"), 'r+') as f:
                self.scores = json.load(f)
        except:
            with open(os.path.join(dataDir, "scores.json"), 'w+') as f:
                self.scores = {}

    def sync(self):
        #sync the copy in RAM back to the disk as needed
        self.logger.debug("Syncing database")
        with open(os.path.join(self.dataDir, "scores.json"), 'w') as f:
            json.dump(self.scores, f, sort_keys=True, indent=2, separators=(',',':'))

    def solve(self, team, problem, points):
        #allow for the solving of problems

        #build the key path if it does not exist
        if not team in self.scores:
            self.scores[team] = {}
        if not problem in self.scores[team]:
            self.scores[team][problem] = False
        if not "score" in self.scores[team]:
            self.scores[team]["score"] = 0

        #credit the team for finding the solution
        if self.scores[team][problem] == False:
            self.scores[team][problem] = True
            self.scores[team]["score"] += points
            self.sync()
            return True
        else:
            self.logger.info("Team %s attempted duplicate solve", team)
            return False

    def hasSolved(self, team, problem):
        #check if they solve key is set for the problem
        try:
            return self.scores[team][problem]
        except KeyError:
            return False

    def getScore(self, team):
        #get the score from the server for the client
        return self.scores[team]["score"]

    def getRanks(self):
        #return a ranked list of teams
        rankedTeams = []
        for team in self.scores.keys():
            rankedTeams.append((team, self.scores[team]["score"]))
        return sorted(rankedTeams, key = lambda team: team[1])

if __name__ == "__main__":
    s = ScoreBoard("data")
    s.solve("team1", "problem1", 100)
    s.solve("team2", "problem1", 130)
    s.solve("team3", "problem1", 13)
    s.solve("team4", "problem1", 153)
    s.solve("team5", "problem1", 170)
    print s.getRanks()
