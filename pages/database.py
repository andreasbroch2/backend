from sshtunnel import SSHTunnelForwarder
from .config import Config
import MySQLdb as mdb
import pandas as pd

class Database:

    server = SSHTunnelForwarder(
        (Config.DATABASE_CONFIG['ssh-server'], Config.DATABASE_CONFIG['ssh-port']),
        ssh_username=Config.DATABASE_CONFIG['user'],
        ssh_password=Config.DATABASE_CONFIG['ssh-password'],
        remote_bind_address=(Config.DATABASE_CONFIG['server'], Config.DATABASE_CONFIG['port']))

    def __init__(self):
        pass 

    def insert(self, query):
        self.server.start()
        try:
            con = mdb.connect(
            Config.DATABASE_CONFIG['server'],
            Config.DATABASE_CONFIG['user'],
            Config.DATABASE_CONFIG['password'],
            Config.DATABASE_CONFIG['name'], 
            port=self.server.local_bind_port)
        except:
            print('Cant connect')
        print('Connected')

        cursor=con.cursor()
        print(query)
        resp = cursor.execute(query)
        print(resp)
        con.commit()
        con.close()
        self.server.stop()
    
    def dataframe(self, query):
        self.server.start()
        try:
            con = mdb.connect(
            Config.DATABASE_CONFIG['server'],
            Config.DATABASE_CONFIG['user'],
            Config.DATABASE_CONFIG['password'],
            Config.DATABASE_CONFIG['name'], 
            port=self.server.local_bind_port)
        except:
            print('Cant connect')
        print('Connected')
        print(query)
        df = pd.read_sql(query, con)
        print(df)
        
        con.close()
        self.server.stop()

        return df