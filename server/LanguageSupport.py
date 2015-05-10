import logging, json, os, subprocess

class LangSupport:
    def __init__(self, dataDir):
        """init some internal instances of stuff"""
        self.logger = logging.getLogger("LangSupport")
        self.languages = json.load(open(os.path.join(dataDir, "languages.json")))
        self.logger.info("Loaded the following compilers:")
        for lang in self.languages:
            self.logger.info(self.languages[lang]["name"])

    def generateBaseName(self, teamFile):
        """generate a language agnostic handle for the file"""
        baseName =  teamFile.split(".")[0]
        self.logger.debug("Basename: " + baseName)
        return baseName

    def getLangs(self):
        """get a listing of supported languages"""
        langs = []
        for lang in self.languages:
            langs.append(self.languages[lang]["name"])
        return langs

    def getCompiler(self, lang):
        """get the compile command associated with a language"""
        return self.languages[lang]["compile"]

    def compile(self, lang, teamFile, problemDir):
        """use the compile directive obtained above to compile"""
        baseName = self.generateBaseName(teamFile)
        cmd = self.getCompiler(lang).replace("{base}", baseName)
        self.logger.debug(cmd)
        proc = subprocess.Popen(cmd.split(), cwd=problemDir)
        #hold until the compile task finishes before proceeding to run
        proc.wait()
        return proc

    def getRunTime(self, lang):
        """return the runtime for various languages"""
        return self.languages[lang]["run"]

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    l = LangSupport("data")
    print l.getLangs()
    print l.getCompiler("java")
    print l.compile("java", "program.java")
