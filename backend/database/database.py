import psycopg
import os

class Database:
    def __init__(self, connection_string):
        self.connection_string = connection_string

if __name__ == '__main__':
    db = Database(os.environ.get('POSTGRESQL_CONNECTION_STRING'))
    