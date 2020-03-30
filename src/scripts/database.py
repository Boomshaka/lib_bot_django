import psycopg2
from psycopg2 import OperationalError
from decimal import Decimal
import configure as cfg


class Database:

    def __init__(self,db_name="libbot", db_user="shakakanenobu", db_password="iFaceYellow", db_host="localhost", db_port=5432):
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.connection = None


    #Every method will automatically call to this for user
    def create_connection(self):
        # print("Parameters are: ",db_name,db_user,db_password,db_host,db_port)
        try:
            self.connection = psycopg2.connect(
                database = self.db_name,
                user = self.db_user,
                password = self.db_password,
                host = self.db_host,
                port = self.db_port,
            )
            # cursor = self.connection.cursor()
            print("Connection to PostgreSQL DB successful")
        except OperationalError as e:
            print(f"The error '{e}' occurred")
        # return connection
    
    def close_connection(self):
        self.connection.close()


    def new_user(self, username):
        sql_students = """INSERT INTO students(username) VALUES(%s) RETURNING id;"""
        sql_error_stats = "INSERT INTO error_stats(student_id) VALUES(%s) RETURNING id;"
        # connection = None
        id = None
        try:
            # connection = create_connection()
            cursor = self.connection.cursor()
            cursor.execute(sql_students,(username,))
            id_student = cursor.fetchone()[0]
            cursor.execute(sql_error_stats,(id_student,))
            id_stats = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        return id_student, id_stats
    
    def get_student_id(self, username):
        sql = """SELECT id FROM students WHERE username = %s;"""
        id = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql,(username,))
            id = cursor.fetchone()
            print("User", username, "has id of", id[0])
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if id is not None:
                return id[0]



    def get_reliability(self,id):
        sql = """SELECT reliability FROM error_stats WHERE student_id = %s;"""
        reliability = None
        try:
            # connection = create_connection()
            cursor = self.connection.cursor()
            cursor.execute(sql,(id,))
            reliability = cursor.fetchone()
            print("RELIABILITY IS: ", float(reliability[0]))
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if reliability is not None:
                return reliability[0]

    #Finds an exponential moving average of the reliability of users
    def new_reliability(self, ema_minus_one, success, a = 1/6):
        ema = 1 if success else 0
        if ema_minus_one is not None:
            print("EMA IS:",ema)
            ema = a * ema + (1 - a) * ema_minus_one
        return ema


    def update_stats(self,id,success):
        
        sql_success = """UPDATE error_stats 
                            SET num_tried = num_tried + 1, num_success = num_success + 1, 
                            last_ran = DATE_TRUNC('second', NOW()::TIMESTAMP), reliability = %s 
                            WHERE student_id = %s"""
        sql_fail = """UPDATE error_stats 
                        SET num_tried = num_tried + 1, 
                        last_ran = DATE_TRUNC('seconds',NOW()::TIMESTAMP), 
                        last_failed = DATE_TRUNC('seconds',NOW()::TIMESTAMP), reliability = %s 
                        WHERE student_id = %s"""
        # connection = None
        updated_rows = 0
        r = self.get_reliability(id)
        if r is not None:
            r = float(r)
        r = self.new_reliability(r, success)
        try:
            # connection = create_connection()
            cursor = self.connection.cursor()
            if success:
                cursor.execute(sql_success,(r,id))
            else:
                cursor.execute(sql_fail,(r,id))
            updated_rows = cursor.rowcount
            self.connection.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

        return updated_rows

    