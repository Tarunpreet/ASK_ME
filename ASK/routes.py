from flask import flash,url_for
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,redirect
from ASK.forms import RegistrationForm, LoginForm
from ASK.models import User,Questions,Answers
from ASK import app

question=[
   {
     'author':'Tarunpreet Singh',
     'date_created':'20/1/2019',
     'Title':"What is 'Context' on Android?",

   },
   {
     'author':'Jasmeet Singh',
     'date_created':'20/1/2019',
     'Title':"What is __init__ in Python?",

   },
    {
     'author':'Prabhjot Singh',
     'date_created':'20/1/2019',
     'Title':"What is 'Toast' in Android?",

   }


]
@app.route("/")
def hello():
	return render_template('home.html',questions=question) 

@app.route("/login")
def login():
  form = LoginForm()
  return render_template('login.html',form=form) 

@app.route("/Register",methods=['GET','POST'])
def Register():
  form = RegistrationForm()
  if form.validate_on_submit():
    flash(f'Account created for {form.username.data} .','success')
    # flash layout in layout template
    #success is type of alert in bootstrap
    return  redirect(url_for('hello'))
  return render_template('Register.html',form=form) 

