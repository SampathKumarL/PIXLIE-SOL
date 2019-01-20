from flask import Flask
import pymysql
import json

db = pymysql.connect("localhost", "root", "tiger", "pixlie")

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/create")
def create_hero():
	try:
		cursor = db.cursor()
		sql = "insert into hero(score) values(0)"
		cursor.execute(sql)
		db.commit()
	except Exception as ex:
		return str(ex)
	return ("Hero Created")
	
@app.route("/fight")
def fight():
	cursor = db.cursor()
	x,y= 0,0
	try : 
		query = '''SELECT * FROM hero ORDER BY RAND() LIMIT 2'''
		cursor.execute(query)
		results = cursor.fetchall()
		
		x,y = results[0], results[1]
		print(x[0]," ",y[0])
		print("query: ", "update hero set score = score+1 where id = "+ str(x[0]))
		cursor.execute('update hero set score = score+1 where id =' + str(x[0]))
		cursor.execute('delete from hero where id =' + str(y[0]))
		db.commit()
	except :
		return("Only one person remaining")
	dict = {'win':x[0],'win_score_x':x[1],'lose':y[0]}
	return json.dumps(dict)
	
@app.route("/become_champ")
def become_champ():
	
	cursor = db.cursor()
	id_to_save = 0
	try : 
		id_with_max_score = '''select * from hero where score = (select MAX(score) from hero)'''
		cursor.execute(id_with_max_score)
		results = cursor.fetchone()
		id_to_save = results[0]
		
		query = ''' Select * from hero '''
		cursor.execute(query)
		results = cursor.fetchall()
		
		for r in results:
			if r[0] != id_to_save:
				cursor.execute('delete from hero where id = '+str(r[0]))
				print(str(r[0]))
		db.commit()
	except Exception as ex:
		return(str(ex))
		
	dict = {'champ':id_to_save}
	return json.dumps(dict)
	
@app.route("/all")
def all():
	cursor = db.cursor()
	query = '''SELECT * FROM hero'''
	cursor.execute(query)
	results = cursor.fetchall()
	str1 = ""
	for r in results:
		str1 += str(r[0])+" : "+str(r[1])+" </br>"
	return str1

if __name__ == "__main__":
    app.run(debug=True)