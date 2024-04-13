import psycopg2
from configparser import ConfigParser

reader = ConfigParser()
reader.read('config.ini')

class database_manager:
    def connector(self):
        '''Connects to the given database. Mostly used in other methods'''
        self._conn = psycopg2.connect(
            host = reader['POSTGRESDATA']['HOST'],
            user = reader['POSTGRESDATA']['USER'],
            password = reader['POSTGRESDATA']['PASSWORD'],
            database = reader['POSTGRESDATA']['DB']
        )
        self._curr = self._conn.cursor()
        self._curr.execute('''CREATE TABLE IF NOT EXISTS registered_accounts(
                           id SERIAL PRIMARY KEY,
                           username TEXT,
                           password TEXT
        )''')

    def disconnect(self):
        '''Disconnects from the database. Used in other methods after connector() to avoid memory leakage'''
        self._curr.close()
        self._conn.close()
    

    def insert_data(self, name, password):
        '''Registers the account and inserts the data into the database.'''
        self.connector()
        with self._conn:
            self._curr.execute('INSERT INTO registered_accounts(username, password) VALUES(%s, %s)', (name, password))
        self.disconnect()


    def get_username(self, name):
        '''Checks if an account exists by selecting the columns with the given username.'''
        self.connector()
        self._curr.execute('SELECT * FROM registered_accounts WHERE username=%s', (name,))
        result = self._curr.fetchall()
        self.disconnect()
        return result
    
    def account_checker(self, name, password):
        '''Checks if an account with the given credentials already exists. (get_username is used in the register page, this authenticates the account on the login page)'''
        self.connector()
        self._curr.execute('SELECT * FROM registered_accounts WHERE username=%s and password=%s', (name, password))
        if self._curr.fetchall():
            self.disconnect()
            return True
    

