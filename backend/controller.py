from flask import Flask, url_for,request,redirect,session,jsonify
from flask import render_template
from flask import current_app as app  
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/")
def main():
     return render_template('home.html')
     
@app.route("/user_login", methods=["GET","POST"])
def user_login():
    if request.method=='POST':
        user_email = request.form['Email']
        password = request.form['password']
        print(user_email,password) 
        all_users=db.session.query(User).filter(User.user_email == user_email).all()
        if len(all_users)!=0 and all_users[0].user_password==password:
            uid=all_users[0].user_id
            return redirect(url_for('user_dashboard',uid=uid))
        else:
            return render_template('user_login.html',msg='Wrong credentials,try again')
    return render_template('user_login.html',msg='')

@app.route('/user_register', methods =['GET', 'POST'])
def user_register():
   if request.method=='POST':
      if request.method=='POST':
            username = request.form['username']
            password = request.form['password']
            email=request.form['email']
            confirm=request.form['confirm']
            
            all_users=db.session.query(User).filter(User.user_email == email).all()
            if len(all_users)!=0:
                 return render_template('user_register.html',msg='user already exists')
            '''elif(email!=confirm):
                return render_template('user_register.html',msg='incorrect confirmation')'''
            new_user=User(user_email=email,user_name=username,user_password=password,role=0)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for('user_login'))
   return render_template('user_register.html',msg='')

    
if __name__ == '__main__':
    
    app.run(debug=True)
	
