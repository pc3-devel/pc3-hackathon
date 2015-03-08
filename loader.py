import logging, glob, os, json, sys, collections

class Loader:
    
    def __init__(self, directoryPath):
        self.logger = logging.getLogger("loader")
        problemsExists = False
        self.problemsDictionary = {}
        for dirs in os.listdir(directoryPath):
            if (dirs == "problems"):
                problemsExists = True
        
        if (problemsExists == True):
            self.problemsDictionary = self.createProblemsDict(os.path.join(directoryPath, "problems"))

        else:
            self.logger.error("problems dir not found")


    def createProblemsDict(self, path):
        tmpProblemsDictionary = {}
        defaultPath = path
        self.meta_defaults = {}
        self.meta_defaults = self.metaDefaultsIn(os.path.join(defaultPath, "meta_defaults.json"))
        
        for problem in os.listdir(path):
            if (os.path.isdir(os.path.join(path,problem)) == True):
                print tmpProblemsDictionary
                print '\n'
                tmpProblemsDictionary.update(self.probStats(path, problem, self.meta_defaults))

        return tmpProblemsDictionary


    def metaDefaultsIn(self, defaultPath):
        defaults = {}
        
        with open(defaultPath) as f:
            defaults = json.load(f)

        return defaults

    def probStats(self, path, problem, meta_defaults):
        problemPath = os.path.join(path, problem)
        problemList = []
        tmpDict = {}

        self.logger.info("Logging " + problem);
        
        with open(os.path.join(problemPath, "description.txt")) as desc:
            problemList.append(desc.read())

        with open(os.path.join(problemPath, "meta.json")) as meta:
            tmpDict = json.load(meta)

        for key in tmpDict.keys():
            if (tmpDict[key] == ""):
                tmpDict[key] = meta_defaults[key]

        problemList.append(tmpDict)


        try:
            problemList.append(os.path.join(problemPath, "in.txt"))

        except:
            self.logger.error("Unexpected Error: " + sys.exc_info()[0])

        problemList.append(os.path.join(problemPath, "out.txt"))


        return {problem: problemList}


print __name__
if __name__ == "__main__":
    print "Hello"
    logging.basicConfig(level=logging.DEBUG)
    loader = Loader("/home/ibrown/testLoader")
    print loader.problemsDictionary
