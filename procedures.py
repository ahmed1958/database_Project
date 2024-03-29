import pymysql
from support import *


conn = pymysql.connect(
    host='database-1.cfo6vewprtg5.eu-north-1.rds.amazonaws.com',
    user='admin',
    password="0123456789",
    db="student_enroll")
cur = conn.cursor()

def db_drop_course(table, course_id,id):
   sql = '''DELETE FROM {} WHERE {}= %s and {}= %s''' .format(
       table, col_val[table], "C_id")
   cur.execute(sql, (id, course_id))
   conn.commit()

def db_enroll_course(id,course_id,year,univ_year):
   try:
      cur = conn.cursor()
      sql = "INSERT INTO Enroll (S_id, C_id, year, univ_yr) VALUES (%s, %s, %s, %s)"
      cur.execute(sql, (id,course_id,year,univ_year))
      conn.commit()
   except Exception as e:
       print(f"An error occurred: {e}")
       conn.rollback()
   finally:
       cur.close()


def db_teach_course(id,course_id):

   try:
      cur = conn.cursor()
      sql = "INSERT INTO Teach (I_id, C_id) VALUES (%s, %s)"
      cur.execute(sql, (id,course_id))
      conn.commit()
   except Exception as e:
       print(f"An error occurred: {e}")
       conn.rollback()
   finally:
       cur.close()

def db_delete(table, id):
   sql = '''DELETE FROM {} WHERE id= %s''' .format(table)
   cur.execute(sql, (id))
   conn.commit()


def db_update(table,column,id,value):
   try:
      cur = conn.cursor()
      sql = "UPDATE {} SET {} = %s WHERE id = %s".format(table,column)
      cur.execute(sql, (value,id))
      conn.commit()
   except Exception as e:
       print(f"An error occurred: {e}")
       conn.rollback()
   finally:
       cur.close()




def db_insert(table_name,values):
   try:
      cur = conn.cursor()
      sql = '''INSERT INTO {} ({}) VALUES {}''' .format(table_name,",".join(tuple(col_val[table_name])),values)
      cur.execute(sql)
      conn.commit()
   except Exception as e:
       print(f"An error occurred: {e}")
       conn.rollback()
   finally:
       cur.close()

def db_degree(id,deg,univer,year):
   id = int(id)
   sql = '''INSERT INTO Degree ({}, {}, {}, {}) VALUES (%s, %s,%s, %s) ''' .format( 'I_id','degree','univ','year')
   cur.execute(sql, (id,deg,univer,year))
   conn.commit()
   
def db_search(table_name,feild_name,key_value):
   cur = conn.cursor()
   sql = '''
                 select id,fname,lname,gender,YEAR(NOW()) -  YEAR(dob) as age,COUNT({}) as Courses  FROM {} 
                 left JOIN {} ON id = {}
                 WHERE {}='{}' GROUP BY id'''.format(join_col[table_name][1],table_name,join_col[table_name][0],join_col[table_name][1],feild_name,key_value)

   cur.execute(sql)

   rows = cur.fetchall()

   for row in rows:
      print(row)


def db_view():
   cur = conn.cursor()
   sql = '''
                 select id,name,description,COUNT(Enroll.S_id) as enrollment FROM Courses
                 left JOIN Enroll ON id = Enroll.S_id GROUP BY id'''

   cur.execute(sql)

   rows = cur.fetchall()
   for row in rows:
         print(row)

   cur.close()


