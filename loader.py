import logging, glob, os, json, sys, collections

class Loader:
    def __init__(self, directoryPath):
        self.problemsDictionary = {}

        #allows for logging of messages during execution
        self.logger = logging.getLogger(__name__)

        #verifies that root directory contains problems directory
        problemsExists = False
        for dirs in os.listdir(directoryPath):
            if (dirs == "problems"):
                problemsExists = True
        
        if (problemsExists == True):
            #builds initializing dictionary
            self.problemsDictionary = self.createProblemsDict(os.path.join(directoryPath, "problems"))

        else:
            self.logger.error("problems dir not found")


    def createProblemsDict(self, path):
        tmpProblemsDictionary = {}
        self.meta_defaults = {}
        defaultPath = path

        self.meta_defaults = self.metaDefaultsIn(os.path.join(defaultPath, "meta_defaults.json"))
        
        #finds subdirectories of problems dir and makes those the 
        #dictionary keys through passing them to the probStats function
        for problem in os.listdir(path):
            if (os.path.isdir(os.path.join(path,problem)) == True):
                tmpProblemsDictionary.update(self.probStats(path, problem, self.meta_defaults))

        return tmpProblemsDictionary

    #Establishes meta default values by reading in from the meta-defaults.json
    #file
    def metaDefaultsIn(self, defaultPath):
        defaults = {}
        
        with open(defaultPath) as f:
            defaults = json.load(f)

        f.close();

        return defaults

    #Defines each problem and its attributes within the dictionary
    def probStats(self, path, problem, meta_defaults):
        problemList = []
        tmpDict = {}
        problemPath = os.path.join(path, problem)

        self.logger.info("Logging " + problem);
        
        #Puts description in the problemList
        with open(os.path.join(problemPath, "description.txt")) as desc:
            problemList.append(desc.read())

        #Decides whether to use each meta value within the problem directory or
        #the default value if there is no value (null) for the dictionary value
        #and adds it to the problemList
        with open(os.path.join(problemPath, "meta.json")) as meta:
            tmpDict = json.load(meta)

        meta.close();

        for key in tmpDict.keys():
            if (tmpDict[key] == ""):
                tmpDict[key] = meta_defaults[key]

        problemList.append(tmpDict)

        #Checks whether the input values exist and, if so, it adds it to the
        #problemList
        try:
            newPath = os.path.join(problemPath, "in.txt")
            open(newPath)

        except:
            self.logger.warning("Invalid contents at in.txt file")

        #Add out.txt to problemList
        problemList.append(os.path.join(problemPath, "out.txt"))

        #Return problem to be stored in the dictionary
        return {problem: problemList}



if __name__ == "__main__":
    print "Hello"
    logging.basicConfig(level=logging.DEBUG)
    loader = Loader("/home/ibrown/testLoader")
    print loader.problemsDictionary
