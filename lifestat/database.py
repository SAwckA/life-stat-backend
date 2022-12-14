import psycopg2
import sqlite3

from psycopg2.errors import UniqueViolation

import settings.config as cfg


class Database:

    unique_exception = UniqueViolation

    def __init__(self):
        
        self.conn = psycopg2.connect(f"""
                host={cfg.DB_HOST}
                port={cfg.DB_PORT}
                dbname={cfg.DB_NAME}
                user={cfg.DB_USER}
                password={cfg.DB_PASS}
                target_session_attrs=read-write
                sslmode={cfg.DB_SSL}
            """)
        
        self.cur = self.conn.cursor()

    def query(self, query):
        try:
            self.cur.execute(query)
        except psycopg2.InterfaceError or psycopg2.OperationalError:
            self.reinitiate()
        
    def exec_commit(self, sql: str, args: list):
        try:
            self.cur.execute(sql, args)
            self.conn.commit()
        except psycopg2.InterfaceError or psycopg2.OperationalError:
            self.reinitiate()
        
    def fetchall(self, sql: str, args: list) -> list:
        try:
            self.cur.execute(sql, args)
            return self.cur.fetchall()
        
        except psycopg2.InterfaceError or psycopg2.OperationalError:
            self.reinitiate()
            
            self.cur.execute(sql, args)
            return self.cur.fetchall()

    def fetchone(self, sql: str, args: list) -> list:
        try:
            self.cur.execute(sql, args)
            return self.cur.fetchone()
        
        except psycopg2.InterfaceError or psycopg2.OperationalError:
            self.reinitiate()
            
            self.cur.execute(sql, args)
            return self.cur.fetchone()

    def reinitiate(self):
        try:
            self.close()
        except:
            ...
        self.conn = psycopg2.connect(f"""
                host={cfg.DB_HOST}
                port={cfg.DB_PORT}
                dbname={cfg.DB_NAME}
                user={cfg.DB_USER}
                password={cfg.DB_PASS}
                target_session_attrs=read-write
                sslmode={cfg.DB_PASS}
            """)

        self.cur = self.conn.cursor()
        
        
    def close(self):
        self.cur.close()
        self.conn.close()


class TempDatabase:
    """?????????? ?????????????????????? ???????? ???????????? ?? ?????????????????????? ???????????? ?????? ????????????"""
    
    unique_exception = sqlite3.IntegrityError
    
    def __init__(self) -> None:
        self.conn = sqlite3.connect("file::memory:?cache=shared")
        self.cur = self.conn.cursor()
        self.init_structure()
        self.init_data()
        
    def init_structure(self) -> None:
        with open("./init_test.sql") as sql_file:
            sql_script = sql_file.read()
            
        self.cur.executescript(sql_script)    
        self.conn.commit()
        
    def init_data(self) -> None:
        with open("./data_test.sql") as sql_file:
            sql_script = sql_file.read()
            
        self.cur.executescript(sql_script)    
        self.conn.commit()
    
    def exec_commit(self, sql: str, args: list):
        sql = sql.replace('public.user', 'user').replace('%s', '?')
        self.cur.execute(sql, args)
        self.conn.commit()    
    
    def fetchall(self, sql: str, args: list) -> list:
        sql = sql.replace('%s', '?').replace('public.user', 'user')
        self.cur.execute(sql, args)
        return self.cur.fetchall()
    
    def fetchone(self, sql: str, args: list) -> list:
        sql = sql.replace('%s', '?').replace('public.user', 'user')
        self.cur.execute(sql, args)
        res = self.cur.fetchall()
        print(res)
        if res:
            return res[0]
        return res
    
    
    def close(self):
        self.cur.close()
        self.conn.close()
        

if cfg.DB_ENV != "PROD":
    print("[WARN] USING MEMORY DATABASE")
    database_class = TempDatabase
    
if cfg.DB_ENV == "PROD":
    print(f"[INFO] USING POSTGRES AT {cfg.DB_HOST}:{cfg.DB_PORT}")
    database_class = Database