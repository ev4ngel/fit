#-*- coding:utf-8 -*-
import os,sys,hashlib,time,sqlite3,ConfigParser,datetime
from fitmain import *
class FitCommand:
    def __init__(self,argv):
        cmds={"connect":self.connect,\
              "init":self.init,\
              "test":self.test,\
              "copy":self.copy,\
              "move":self.move,\
              "remove":self.remove,\
              "reinit":self.reinit,\
              "info":self.info,\
              "update":self.update}
        self._av=argv
        self._fm=FitMain()
        cmds[argv[1]]()
    def connect(self):
        path=None
        try:
            path=self._av[2]
        except:
            pass
        finally:
            self._fm.connect(path)
    def test(self):
        self._fm.test()
    def init(self):
        self._fm.init(self._av[2])
    def reinit(self):
        pass
    def move(self):
        pass
    def remove(self):
        pass
    def copy(self):
        pass
    def info(self):
        pass
    def update(self):
        pass
