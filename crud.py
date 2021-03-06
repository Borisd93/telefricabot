import sqlite3
import random



def connect(name):
	"""
	_________________________________________
	Crea una conexion a una database indicada
	_________________________________________
	"""
	global database,db_cursor
	database=sqlite3.connect(name)
	db_cursor=database.cursor()

def runcode(args):
	"""
	______________________
	Ejecuta codigo sqlite3
	______________________
	"""
	db_cursor.execute(args)

def create(args1,args2):
	"""
	_________________________
	CRUD
	^
	CREATE = CREA un registro
	_________________________
	"""
	db_cursor.execute("INSERT INTO "+args1+" VALUES("+args2+")")

def read(args1,*args2):
	"""
	______________________
	CRUD
	 ^
	READ = LEE un registro
	______________________
	"""
	try:
		data=db_cursor.execute("SELECT * FROM "+str(args1)+" WHERE "+str(args2[0])+"="+str(args2[1]))
	except:
		data=db_cursor.execute("SELECT * FROM "+str(args1))
	return data.fetchall()

def update(args1,*args2):
	"""
	______________________________
	CRUD
	  ^
	UPDATE = ACTUALIZA un registro
	______________________________
	"""
	db_cursor.execute("UPDATE "+str(args1)+" SET "+str(args2[0])+" = "+str(args2[1])+" where "+str(args2[2])+" = "+str(args2[3])+"")

def delete(args1,args2,args3):
	"""
	____________________________
	CRUD
	   ^
	DELETE = ELIMINA un registro
	____________________________
	"""
	db_cursor.execute("DELETE FROM "+args1+" WHERE "+args2+"="+args3)

def save():
	"""
	_____________________
	Guarda los cambios
	hechos en la database
	_____________________
	"""
	database.commit()

def close():
	"""
	__________________
	Cierra la conexión
	__________________
	"""
	database.close()
def crud_doc():
	print("connect"+connect.__doc__)
	print("runcode"+runcode.__doc__)
	print("create"+create.__doc__)
	print("read"+read.__doc__)
	print("update"+update.__doc__)
	print("delete"+delete.__doc__)
	print("save"+save.__doc__)
	print("close"+close.__doc__)

