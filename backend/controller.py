from flask import Flask, url_for,request,redirect,session,jsonify
from flask import render_template
from flask import current_app as app  
from flask_cors import CORS, cross_origin
from locator import *

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/")
def main():
     return True
     
@app.route("/user_login", methods=["GET","POST"])
def user_login():
	if request.method=='POST':
		email = request.form['email']
		password = request.form['password']
		print(email,password) 
		cur.execute('SELECT * FROM Users;')
		users = cur.fetchall()
		print(users)
		for i in users:
			if i[1]==email and i[3]==str(password):
				return "succesfully logged in"
			else:
				return "wrong authentication"
	return "wrong authentication"

@app.route('/user_register', methods =['GET', 'POST'])
def user_register():
	if request.method=='POST':
		try:
		    username = request.form['username']
		    password = request.form['password']
		    email=request.form['email']
		    
		    cur.execute('SELECT * FROM Users;')
		    users = cur.fetchall()
		    
		    for i in users:
		    	if i[1]==email:
		    		return "User exist already"
		    cur.execute("INSERT INTO Users (email, name, password) VALUES (%s, %s, %s)", (email, username, password))
		    conn.commit()
		    return "User added succesfully" 
		except Exception as e:
		    return e.message
			
		

@app.route('/rank',methods=['POST','GET'])
def rank():
	if request.method=='POST':
		print('api called')

		data = request.form.get('cords')
		
		data=[float(i) for i in data.split(',')]
		cords=[(data[i],data[i+1]) for i in range(0,len(data),2)]

		type_=request.form.get('type')
		size=request.form.get('size')
		state=request.form.get('state')
		result=get_rank(cords,type_,size,state)
		print(result)
		return jsonify(result)
	return 'Provide query'
	
@app.route('/validator',methods=['POST','GET'])
def valid():
	if request.method=='POST':
		print('validator called')

		type_ = request.form.get('type_')
		description = request.form.get('description')
		valid = validator(type_,description)
		
		return jsonify({'discription':valid})
	return 'Provide query'
	


if __name__ == '__main__':
    app.run(debug=True)
	
