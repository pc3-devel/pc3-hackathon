import logging, json, os, subprocess

class LangSupport:
    def __init__(self, dataDir):
        self.logger = logging.getLogger("LangSupport")
        self.languages = json.load(open(os.path.join(dataDir, "languages.json")))
        self.logger.info("Loaded the following compilers:")
        for lang in self.languages:
            self.logger.info(self.languages[lang]["name"])

    def _generateBaseName(self, teamFile):
        baseName =  teamFile.split(".")[0]
        self.logger.debug("Basename: " + baseName)
        return baseName

    def getLangs(self):
        langs = []
        for lang in self.languages:
            langs.append(self.languages[lang]["name"])
        return langs

    def getCompiler(self, lang):
        return self.languages[lang]["compile"]

    def compile(self, lang, teamFile):
        baseName = self._generateBaseName(teamFile)
        cmd = self.getCompiler(lang).replace("{base}", baseName)
        self.logger.debug(cmd)
        return subprocess.call(cmd.split())

    def getRunTime(self, lang):
        return self.languages[lang]["run"]

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    l = LangSupport("data")
    print l.getLangs()
    print l.getCompiler("java")
    print l.compile("java", "program.java")
