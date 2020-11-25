from flask import Flask ,render_template, request, flash, url_for, redirect, session

import requests
import json
import xmltodict
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
# from dbconnect import connection
import sqlalchemy
# from wtforms import Form, BooleanField, TextField, PasswordField, validators
# from flask_login import LoginManager

app=Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
# login=LoginManager(app)

engine= sqlalchemy.create_engine('mysql://root:password@localhost')

conn = engine.connect()
# engine.execute("USE books")
conn.execute("USE books")


def is_active(self):
	return True
def get_id(self):
	return self.email
def is_authenticated(self):
	return self.authenticated
def is_anonymous(self):
	return False


# cur=conn.cursor()


@app.route('/',methods=["GET","POST"])
def registeration():
	return render_template("user.html")

@app.route('/register',methods=["GET","POST"])
def register():
	return render_template("register.html")

@app.route('/registeration_complete',methods=['POST','GET'])
def registeration_complete():
	username=request.form.get("username")
	email=request.form.get("email")
	password=request.form.get("password")
	confirm_password=request.form.get("confirm_password")
	# print(email)	
	y=conn.execute("SELECT COUNT(*) FROM login WHERE username= %s",username)
	# x=dict(y);
	b=y.first()
	x=dict(b)
	result=int(x['COUNT(*)'])
	# print(x['COUNT(*)'])
	# print(type(x))
	print (result)
	print(type(result))
	# return (x)
	if request.method == "POST":
		if result>0:
			flash("This username has already been taken")
			return redirect(url_for('register'))
		# selif
		if password != confirm_password:
			# print("*")
			flash("Password did'nt matched")
			return redirect(url_for('register'))
			# return("hello")
		else:
			print(username)
			conn.execute("INSERT INTO login (username, email, password) VALUES(%s, %s, %s)", (username, email, password))
			return redirect(url_for('index', username=username))

	return("err")


@app.route('/login',methods=["GET","POST"])
def login():
	return render_template("login.html")

@app.route('/login_user',methods=["POST","GET"])
def login_user():
	username=request.form.get("username")
	password=request.form.get("password")
	print(type(username))
	print(type(password))
	y=conn.execute("SELECT password FROM login WHERE username= %s",username).first()
	a=dict(y)
	x=a['password']
	print(x)
	print(type(x))
	# print(password)
	# if request.method == "POST":

	if x != password:
		flash("Wrong password")
		return redirect(url_for('login'))

	else:
		return redirect(url_for('index', username=username))
	# return("ho")



	


@app.route('/index/<string:username>',methods=['GET','POST'])
def index(username):
	print(username)
	# engine.execute("INSERT INTO reviews (id, review, rating) VALUES(25, 'Nice book', 4)")
	# return ("hi")
	return render_template("index.html",username=username)


@app.route('/submit', methods=['GET','POST'])
def submit():
	name=request.args.get("name")
	
	res=requests.get(" https://www.goodreads.com/search/index.xml", params={"q":name, "key": 'NMGFquxvAKoublJMRYoJfw'})
	
	xpars = xmltodict.parse(res.content)
	jsondata=json.loads(json.dumps(xpars))

	# print(jsondata)
	content= (jsondata['GoodreadsResponse']['search']['results']['work'])
	# print(jsondata)
	n=len(jsondata['GoodreadsResponse']['search']['results']['work'])
	# for i in range(n):
		# for key,val in content[i].items():
			# if key=='best_book':http://127.0.0.1:5000/
				# print(key, "=>", val)



	return render_template("search.html", content=content)

@app.route("/review/<string:book_id>",methods=['GET','POST'])
def review(book_id):
	# res=requests.get("https://www.goodreads.com/book/show.json",params={"key":'NMGFquxvAKoublJMRYoJfw',"id":id })
	# print(book_id)
	return render_template("review.html",book_id=book_id)

@app.route("/review_stored", methods=['POST'])
def review_stored():
	book_id =request.form.get("book_id")
	review=request.form.get("review")
	rating=request.form.get("rating")
	print(book_id)
	conn.execute("INSERT INTO reviews (book_id, review, rating) VALUES (%s, %s, %s)", (book_id, review, rating))
	# engine.commit()
	data=conn.execute("SELECT review,rating FROM reviews WHERE book_id= %s",book_id)
	flash("Thankyou your review has been recorded")
	return render_template("book_review.html",value=data)
	# return("hi")

@app.route("/show_review/<string:book_id>",methods=['GET','POST'])
def show_review(book_id):
	# book_id=request.args.get("book_id")
	# id=book_id
	print(type(book_id))
	data=conn.execute("SELECT review,rating FROM reviews WHERE book_id= %s",book_id)

	print(book_id)

	# for rows in data:
		# print(rows)
	 
	return render_template("book_review.html",value=data)
	# return ("HELLO")


	
