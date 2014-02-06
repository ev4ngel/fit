#-*- coding:utf-8 -*-
import os,sys,hashlib,time,sqlite3,ConfigParser,datetime
from fitdatabase import *
from fitenv import *
from fitcfg import *

class FitMain:
    def __init__(self):
        self._db=None
        self._cfg=FitCfg()
    def test(self,sfile,tdir):
        md5f=self.md5file(sfile)
        print "Testing [{0}]...".format(sfile)
        try:
            rlt=FitDatabase().connect(tdir).info(md5f)
            if not rlt:
                print "No File Match!"
            else:
                xfile=os.stat(sfile)
                print "Source:\n\tName:{0}\n\tSize:{1}\n\tHash:{2}".format(sfile,xfile.st_size,md5f)
                print "Target:\n\tName:{0}\n\tSize:{1}\n\tHash:{2}\n\tPath:{3}".format(rlt[0],rlt[3],rlt[1],rlt[2])
        except:
            print "The Repo doesn't exist.Please Try 'fit init %s' to initial it!"%tdir
    def connect(self,dirx=None):
        if not dirx:
            tm=datetime.datetime.fromtimestamp(float(self._cfg['timestamp']))
            print "RecentRepo:{0}\nTime:{1}".format(self._cfg['recentrepo'],tm.strftime("%Y-%m-%d %H:%M:%S"))
            return True
        if not FitDatabase.exists(dirx):
            print "The Repo doesn't exist.Please Try 'fit init %s' to initial it!"%dirx
            print "Connect to [%s] Fail"%dirx
            return False
        self._cfg['recentrepo']=dirx
        self._cfg['timestamp']=time.time()
        self._cfg.save()
        print "Connect to [%s] Success"%dirx
        return True
    def console(self):
        pass
    def init(self,dirx):
        try:
            _dirx=dirx.decode("utf8")
        except:
            _dirx=dirx
        self._db=FitDatabase()
        self._db.init(_dirx)
        infos=[]
        rfs=[]
        lat=[]
        sum_size=cur_size=0
        print "Preparing For Parse Dir Tree..."
        for cd,xd,xf in os.walk(_dirx):
            for xff in xf:
                o_size=os.stat(os.path.join(cd,xff)).st_size
                infos.append((xff,cd,o_size))
                sum_size+=o_size
        print "Calculating MD5s,[%d] Files Found,This May Take Some Seconds..."%len(infos)
        for rf in infos:
            rfs.append((rf[0],self.md5file(os.path.join(rf[1],rf[0])),rf[1],rf[2]))
            cur_size+=rf[2]
            s=int(cur_size*1.0/sum_size*10)
            if s not in lat:
                lat.append(s)
                print str(s*10)+"%=>"
        self._db.addFiles(rfs)
    @staticmethod
    def md5file(filex):
        try:
            return hashlib.md5(open(filex,'rb').read()).hexdigest()
        except IOError:
            return ""
