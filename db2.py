import mysql.connector
import json

#from passlib.handlers import mysql


class db2():
    try:

        f = open( "config.json", "r" )

        j = json.loads( f.read() )

        conn = mysql.connector.connect(
            user=j['user'],
            password=j['password'],
            host=j['host'],
            database=j['database'] )

        mycursor = conn.cursor()

        print(1)
    except:
        pass


    def exect(self, sql):
        self.mycursor.execute( sql)
        self.conn.commit()

    def get(self, sql):
        self.mycursor.execute( sql)
        self.myresult = self.mycursor.fetchall()
        return self.myresult
