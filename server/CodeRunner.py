import logging, LanguageSupport, subprocess, shutil, os

class Evaluate:
    def __init__(self, dataDir):
        """init some internal instances of stuff"""
        self.logger = logging.getLogger("Evaluator")
        self.logger.info("Loading an evaluator")
        self.support = LanguageSupport.LangSupport(dataDir)

    def evaluate(self, lang, teamFile, problemDir, problem):
        """top level function to provide the evaluation steps"""
        self.support.compile(lang, teamFile, problemDir)
        baseName = self.support.generateBaseName(teamFile)
        runTime = self.support.getRunTime(lang)
        return self._run(runTime, baseName, problemDir, problem)

    def _run(self, runTime, baseName, problemDir, problem):
        #if it exists copy in the input file
        if problem["in"] is not None:
            self.logger.debug("Attempting to copy IO file")
            shutil.copy(problem["in"], os.path.join(problemDir, "in.txt"))

        #actually execute the code
        cmd = runTime.replace("{base}", baseName).split()
        self.logger.debug("Attempting to run in " + problemDir)
        self.logger.debug("Attempting to run: " + str(cmd))

        #hook into the output for the run
        output = subprocess.Popen(cmd, cwd=problemDir, stdout=subprocess.PIPE)
        with open(problem["out"]) as f:
            outputText = f.read()
        lazyMode = problem["meta"]["lazyMode"]

        #return the result of the grading run
        return self.compare(output.stdout.read(), outputText, lazyMode)

    def compare(self, run, good, lazy):
        """grade the run, lazy mode is lenient with whitespace"""
        if lazy:
            good = good.strip()
            run = run.strip()
        runStatus = (run == good)
        
        self.logger.debug("Expected output: " + good)
        self.logger.debug("Recieved output: " + run)
        self.logger.debug("The run is: " + str(runStatus))
        #return a boolean of if the run was good or not
        return runStatus, run, good, lazy

    def getLangs(self):
        return self.support.getLangs()

if __name__=="__main__":
    logging.basicConfig(level=logging.DEBUG)
    e = Evaluate("data")
    print e.evaluate("java", "program.java").stdout.read()
