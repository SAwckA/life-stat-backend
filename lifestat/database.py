from re import S
import psycopg2


class Database:

    def __init__(self, db, user, password, host="0.0.0.0", port="5432"):
        self.conn = psycopg2.connect(dbname=db, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    def query(self, query):
        self.cur.execute(query)

    def close(self):
        self.cur.close()
        self.conn.close()

