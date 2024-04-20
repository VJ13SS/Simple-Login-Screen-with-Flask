#importing the necessary libraries
from flask import Flask,render_template, redirect, url_for,request,session,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

#app initialization and defining the secret key
app= Flask(__name__)
app.secret_key = ('J06x1r@13')

#comfigurations for sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_info.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #db is then used to define models and to perform sql alchemy operations

#defining database model
class User(db.Model):
	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(100),nullable = False)
	email = db.Column(db.String(100),nullable = False)
	password = db.Column(db.String(100),nullable = False)


#permanent session
app.permanent_session_lifetime = timedelta(minutes = 5)

#Login page
@app.route('/', methods = ['POST','GET'])
def login():
	
	if 'user' in session:
		return redirect(url_for('home'))
		
	if request.method == 'POST':
		
		session.permanent = True
		
		user = request.form['name']
		lock = request.form['password']
		
		if user =='' or user ==' ' or lock == '' or lock == ' ':
			flash('User not exists....!')
			return redirect(url_for('login'))
			
			
		#checking if user exists in database		
		existing_user = User.query.filter_by(name = user).first()		
		
		#to check if the entered login details do matches or not
		if existing_user:#if user already exists
			user_password = User.query.filter_by(password = lock).first()
			
			if user_password:
				session['user'] = user
				session['password'] = lock
				return redirect(url_for('home'))
			else:
				flash('Invalid Credidentials')
		else:
			flash('User not exists...!')
			
	return render_template('Login_FP.html')
	
#sign in page
@app.route('/signin',methods = ['POST','GET'])
def signin():
	if request.method == 'POST':		
		
		#Fetching the entered data
		name = request.form['name']
		password = request.form['password']
		email = request.form['email']
				
		#checking if user exists
		existing_email = User.query.filter_by(email = email).first()
		
		if existing_email:
			flash('Account Already exists...!')
			return redirect(url_for('signin'))
		
		
		#Create new object
		if name!= '' and password!='':
		      new_user = User(name = name,password = password, email = email)
		      
		      #adding to database		
		      db.session.add(new_user)	
		      db.session.commit()
		      
		      flash('Account Created Successfully')
		      return redirect(url_for('login'))
				      
	return render_template('Sign_in_FP.html')

#home page
@app.route('/home')
def home():
	if 'user' in session :
		user_name = session['user']
			
		return render_template('Home_FP.html',user = user_name)


#logout
@app.route('/logout')
def logout():
	if 'user' in session:
		session.pop('user')
		session.pop('password')
	
	flash('Logged out Successfully')
	return redirect(url_for('login'))

if __name__ == '__main__':
	with app.app_context():
		
		db.create_all()
		
	app.run(debug = True)
