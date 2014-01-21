#-*- coding:utf-8 -*-
"""
configure file tool for fit
"""
import ConfigParser,os,time
all=["fc_ItemNotExist","FitCfg"]
class fc_ItemNotExist(Exception):
    pass
class FitCfg:
    """
    Save the configure file in the $HOME path and named as .figconf
    recentrepo:the connect repo last time
    timestamp:the connect time last time
    """
    def __init__(self):
        self._f=".fitconfig "
        self._p=os.path.expanduser("~")
        self._c=ConfigParser.ConfigParser()
        self._pf=os.path.join(self._p,self._f)
        if os.path.exists(self._pf):
            with open(self._pf,'r') as f:
                self._c.readfp(f)
        else:
            self._c.add_section("repo")
            self._c.set("repo","recentrepo","")
            self._c.set("repo","timestamp","")
            self.save()
    def __getitem__(self,item):
        if item in ['recentrepo','timestamp']:
            return self._c.get("repo",item)
        else:
            return None
    def __setitem__(self,item,value):
        if item in ['recentrepo','timestamp']:
            self._c.set("repo",item,value)
        else:
            raise fc_ItemNotExist()
    def save(self):
        with open(self._pf,'w') as f:
            self._c.write(f)
