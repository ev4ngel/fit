#-*- coding:utf-8 -*-
import sqlite3,os,time
class FitDatabaseNotExists(Exception):
    pass
class FitDatabaseTableExists(Exception):
    pass
class FitDBConf:
    """
    
    """
    @staticmethod
    def dbname():
    """
    static method
    return the name of the database
    """
        return ".fitdb"
    @staticmethod
    def sql_create_table():
    """
    static method
    return the create tablse string
    """
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
