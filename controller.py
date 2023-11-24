from flask import Flask, url_for,request,redirect,session,jsonify
from flask import render_template
from flask import current_app as app  
from flask_cors import CORS, cross_origin
from backend.locator import *

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/")
def main():
     return render_template('index.html')
     
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=='POST':
        user_email = request.form['Email']
        password = request.form['password']
        print(user_email,password) 
        all_users=db.session.query(User).filter(User.user_email == user_email).all()
        if len(all_users)!=0 and all_users[0].user_password==password:
            uid=all_users[0].user_id
            return redirect(url_for('user_dashboard',uid=uid))
        else:
            return render_template('login.html',msg='Wrong credentials,try again')
    return render_template('login.html',msg='')

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
		uid = request.form.get('uid')
		description = request.form.get('description')
		valid = validator(uid,type_,description)
		
		return jsonify({'discription':valid})
	return 'Provide query'
	


if __name__ == '__main__':
    app.run(debug=True)
	
	
	
	
