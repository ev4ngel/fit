class FitEnv:
    def __init__(self,path):
        self._target=path
        self._prompt=">>"
        self._cur=os.getcwd()
    def request(self):
        ri=""
        while ri=="":
            ri=raw_input(self._prompt)
        return ri
    def begin(self):
        #move * *,test *
        self.showTitle()
        cmd=self.request()
    def showTitle(self):
        print "FitEnv v0.0.1"
        print "CD[{0}]:TD[{1}]".format(os.getcwd(),self._target)
        print "print \"help\" for more infomation"
