#-*- coding:utf-8 -*-
import os,sys,hashlib,time,sqlite3,ConfigParser,datetime
class fc_ItemNotExist(Exception):
    pass
class FitCfg:
    def __init__(self):
        self._f=".fitconfig "
        self._p=os.getenv("home")
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
class FitDatabaseNotExists(Exception):
    pass
class FitDatabaseTableExists(Exception):
    pass
class FitDBConf:
    @staticmethod
    def dbname():
        return ".fitdb"
    @staticmethod
    def sql_create_table():
        return "CREATE TABLE FT_FILES(F_NAME TEXT,F_HASH TEXT,F_PATH TEXT,F_SIZE LONG,F_TIME TIMESTAMP)"
    
class FitDatabase:
    def __init__(self):
        self._db=FitDBConf.dbname()
        self._full=None
    @staticmethod
    def exists(path):
        return os.path.exists(os.path.join(path,FitDBConf.dbname()))
       
    def connect(self,path):
        self._full=os.path.join(path,self._db)
        self._cn=sqlite3.connect(self._full)
        self._cur=self._cn.cursor()
        return self
    def init(self,path):
        CREATE_FILES="CREATE TABLE FT_FILES(F_NAME TEXT,F_HASH TEXT,F_PATH TEXT,F_SIZE LONG,F_TIME TIMESTAMP)"
        self.connect(path)
        try:
            self._cur.execute(CREATE_FILES)
        except Exception:
            print "[Warning]TableExists"
        finally:
            return self
    def addFile(self,file_t):
        #(name,hash,path)
        self._cur.execute("INSERT INTO FT_FILES VALUES(?,?,?,?,?)",(file_t[0],file_t[1],file_t[2],file_t[3],time.time()))
        self._cn.commit()
    def addFiles(self,files_l):
        xl=[]
        for a in files_l:
            xl.append(tuple(list(a)+[time.time()]))
        self._cur.executemany("INSERT INTO FT_FILES VALUES(?,?,?,?,?)",xl)
        self._cn.commit()
    def info(self,file_hash):
        self._cur.execute("SELECT * FROM FT_FILES WHERE F_HASH=?",(file_hash,))
        return self._cur.fetchone()
    def close(self):
        try:
            self._cn.close()
        except:
            pass

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
        
class Fit:
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
        for cd,xd,xf in os.walk(_dirx):
            for xff in xf:
                o_size=os.stat(os.path.join(cd,xff)).st_size
                infos.append((xff,cd,o_size))
                sum_size+=o_size
        print "Calculating Md5s"
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
class FitCommand:
    def __init__(self,argv):
        pass
