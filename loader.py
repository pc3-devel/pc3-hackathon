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
            #builds initializing dictionary
                self.createProblemsDict(os.path.join(directoryPath, "problems"))
            else:
                self.logger.error("No problems directory was found!")


    def createProblemsDict(self, path):
        meta_defaults = {}
        defaultPath = path

        self.meta_defaults = self.metaDefaultsIn(os.path.join(defaultPath, "meta_defaults.json"))
        
        #finds subdirectories of problems dir and makes those the 
        #dictionary keys through passing them to the probStats function
        for problem in os.listdir(path):
            if (os.path.isdir(os.path.join(path,problem)) == True):
                self.probStats(path, problem, self.meta_defaults)

    #Establishes meta default values by reading in from the meta-defaults.json
    def metaDefaultsIn(self, defaultPath):
        defaults = {}
        
        with open(defaultPath) as f:
            defaults = json.load(f)
        return defaults

    #Defines each problem and its attributes within the dictionary
    def probStats(self, path, problem, meta_defaults):
        problemPath = os.path.join(path, problem)

        self.logger.info("Loading " + problem);
        self.problemsDictionary[problem] = {}

        #Puts description in the problemList
        with open(os.path.join(problemPath, "description.txt")) as desc:
            self.problemsDictionary[problem]["desc"] = desc.read()

        #Decides whether to use each meta value within the problem directory or
        #the default value if there is no value (null) for the dictionary value
        #and adds it to the problemList
        with open(os.path.join(problemPath, "meta.json")) as meta:
            tmpDict = json.load(meta)

        for key in tmpDict.keys():
            if (tmpDict[key] == ""):
                tmpDict[key] = meta_defaults[key]

        self.problemsDictionary[problem]["meta"] = tmpDict

        #Checks whether the input values exist and, if so, it adds it to the
        #problemList
        try:
            newPath = os.path.join(problemPath, "in.txt")
            open(newPath)
        except:
            self.logger.warning("in.txt does not appear to exist.")

        #Add out.txt to problemList
        self.problemsDictionary[problem]["in"] = os.path.join(problemPath, "out.txt")

        #Return problem to be stored in the dictionary
        return



if __name__ == "__main__":
    print "Hello"
    logging.basicConfig(level=logging.DEBUG)
    loader = Loader("data")
    print loader.problemsDictionary
