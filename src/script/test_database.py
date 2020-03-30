# import unittest
# import psycopg2
# from psycopg2 import OperationalError
# from database import Database


# class TestDatabase(unittest.TestCase):

#     def test_connection(self):
#         try:
#             # print("Trying to connect")
#             connection = create_connection()
#             # print("trying to create cursor")
#             cursor = connection.cursor()
#             print('PostgreSQL database version:')
#             cursor.execute('SELECT version()')
#             db_version = cursor.fetchone()
#             print(db_version)
#             cursor.close()
#         except (Exception, psycopg2.DatabaseError) as error:
#             print(error)
#         finally:
#             if connection is not None:
#                 connection.close()
#                 print('Database connection closed')

import psycopg2
from psycopg2 import OperationalError
from database import Database

import csv

def main():
    db = Database()
    db.create_connection()
    # id,stats = db.new_user('shakakanenobu')
    # id,stats = db.new_user('nlama')
    # id,stats = db.new_user('alexcha')
    # id,stats = db.new_user('jlee11')
    # rows = db.update_stats(id,True)
    
    # print("ID is: ", id)
    # print("Stats is: ", stats)


    with open("credentialstwo.csv", newline='') as credentials_csv:
            reader = csv.DictReader(credentials_csv)
            for index, row in enumerate(reader):
                db.new_user(row['username'])

    with open("credentialsthree.csv", newline='') as credentials_csv:
            reader = csv.DictReader(credentials_csv)
            for index, row in enumerate(reader):
                db.new_user(row['username'])
    db.close_connection()



if __name__ == "__main__":
    main()