import psycopg
from psycopg.rows import dict_row
import os

class Database:
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def query(self, query, args=None):
        '''Executes a query on the database and returns the result.'''
        with psycopg.connect(self.connection_string, row_factory=dict_row) as connection:
            with connection.cursor() as cursor:
                # Executes the query replacing placeholders (%s) with 'args' values
                cursor.execute(query, args)
            
                # Query is a SELECT
                if query.strip().lower().startswith('select'):
                    # Return query result
                    return cursor.fetchall()

                # Query is INSERT, UPDATE or DELETE
                # Return number of affected rows
                return cursor.rowcount       
    