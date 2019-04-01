from flask import render_template, url_for, flash, redirect,request,session
from flaskblog import app,bcrypt,auth1,db
from flaskblog.forms import RegistrationForm, LoginForm,UpdateAccountForm,PostForm,AddQuest,ResetForm
from sqlalchemy import exc
from firebase_admin import auth
from firebase_admin import firestore
from flask_login import login_user,current_user,logout_user,login_required
import pyrebase
import datetime



 

@app.route("/")
def hello():
  current_user=auth1.current_user
  if (auth1.current_user):
    email=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('email')
    print(auth1.get_account_info(current_user['idToken']))
  users_ref = db.collection(u'questions')
  docs = users_ref.get()
  print(docs)
  docs1={}
  docs1=docs
  # data={
  #    u'author': u'Tarunpreet',
  #    u'author_id': u'3SewEk4mFthFlTlvVtMS9tU0qgn1',
  #    u'content': u'In Android programming, what exactly is a Context class and what is it used for? /n I read about it on the developer site, but I am unable to understand it clearly.',
  #    u'date_posted': datetime.datetime.now(),
  #    u'title': u'What is Context on Android?'
  # }
  # db.collection(u'questions').document().set(data)
  
  return render_template('home.html',current_user=current_user,questions=docs1)

@app.route("/login",methods=['GET','POST'])
def login(): 
  current_user=auth1.current_user
  if (auth1.current_user):
    return redirect(url_for('hello'))
    
  else:
    form = LoginForm()
    if request.method == 'POST':
      password=form.password.data
      email=form.email.data
      try:
        user=auth1.sign_in_with_email_and_password(email,password)
        user = auth1.refresh(user['refreshToken'])
        user1_token=user['idToken']
      except:
        flash(f'Login Unsuccessful! Please Check Your Details ','danger')
        return redirect(url_for('login'))
      flash(f'Login Successful ','success')
        # form1=UpdateAccountForm()
      return redirect(url_for('hello'))
    
  return render_template('login.html',form=form,current_user=current_user,title='Login') 

@app.route("/reset",methods=['GET','POST'])
def reset(): 
  current_user=auth1.current_user
  if (auth1.current_user):
    return redirect(url_for('hello'))
  else:
    form = ResetForm()
    if request.method == 'POST':
      email=form.email.data
      try:
        auth1.send_password_reset_email(email)
      except:
        flash(f'Reset Unsuccessful','danger')
        return redirect(url_for('reset'))
      flash(f'Reset Email Sent ','success')
      return redirect(url_for('login'))
  return render_template('reset.html',form=form,current_user=current_user) 

@app.route("/Register",methods=['GET','POST'])
def Register():
  current_user=auth1.current_user
  if (auth1.current_user):
    return redirect(url_for('hello'))
  else:
    form = RegistrationForm()
    if request.method == 'POST':
      username=form.username.data
      password=form.password.data
      email=form.email.data
      user = auth.create_user(
      email=email,
      email_verified=False,
      password=password,
      display_name=username,
      disabled=False)
      flash(f'Account created ','success')
      return redirect(url_for('login'))
  return render_template('Register.html',form=form,current_user=current_user) 

@app.route("/logout")
def logout():
  print(auth1.current_user)
  auth1.current_user = None
  session['usr']=None
  flash(f'Logout Successful ','success')
  return redirect(url_for('hello'))

@app.route("/account",methods=['GET','POST'])
def account():
  current_user=auth1.current_user
  if (auth1.current_user):
    form=UpdateAccountForm()
    email=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('email')
    uid=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('localId')
    username=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('displayName')
    username_update=form.username.data
    email_update=form.email.data
    if request.method == 'POST':
      auth.update_user(
      uid,
      display_name=username_update,
      email=email_update
      )
      flash('Your account deltails has been changed', 'success')
      return redirect(url_for('account'))
    elif request.method == 'GET':
      form.email.data = email
      form.username.data=username
  else:
    return redirect(url_for('hello'))
  return render_template('account.html',title='Account',form=form,current_user=current_user,email=email,username=username) 

@app.route("/post/new",methods=['GET','POST'])
def quest():
  current_user=auth1.current_user
  if (auth1.current_user):
   form=PostForm()
   if request.method == 'POST':
    title=form.title.data
    content=form.content.data
    author=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('displayName')
    author_id=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('localId')
    data={
     u'author': author,
     u'author_id': author_id,
     u'content':content,
     u'date_posted': datetime.datetime.now(),
     u'title':title
     }
    answers_fire = db.collection(u'questions').document().set(data)
    flash('Your Question Has Been Added!','success')
    return redirect(url_for('hello'))
  else:
   flash('Please Login To access This Page','danger')
   return redirect(url_for('login'))
  
  return render_template('create.html',title='NEW QUESTION',form=form,legend='New Question',current_user=current_user)

@app.route("/post/<string:post_id>")
def post(post_id):
  current_user=auth1.current_user
  if (auth1.current_user):
    uid=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('localId')
  else:
    uid=None
  quest_doc = db.collection(u'questions').document(post_id)
  
  quest= quest_doc.get()
  answers_fire = db.collection(u'questions').document(post_id).collection(u'answers').get()
  answers={}
  answers=answers_fire

  return render_template('question.html', title=quest.get('title'), question=quest,current_user=current_user,author_id=uid,answers=answers)

@app.route("/answer/new/<string:post_id>",methods=['GET','POST'])
def add_answer(post_id):
  current_user=auth1.current_user
  if (auth1.current_user):
   form=AddQuest()
   if request.method == 'POST':
    content=form.content.data
    author=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('displayName')
    author_id=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('localId')
    data={
     u'author': author,
     u'author_id': author_id,
     u'content':content,
     u'date_posted': datetime.datetime.now()
     }
    answers_fire = db.collection(u'questions').document(post_id).collection(u'answers').document().set(data)
    flash('Your Answer Has Been Added!','success')
    return redirect(url_for('hello'))
  else:
   flash('Please Login To access This Page','danger')
   return redirect(url_for('login'))
  
  return render_template('add_answer.html',form=form,current_user=current_user)

@app.route("/post/<string:post_id>/delete", methods=['POST'])
def delete_post(post_id):
  current_user=auth1.current_user
  if (auth1.current_user):
    question=db.collection(u'questions').document(post_id).get()
    author_id=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('localId')
    if question.get('author_id') != author_id:
      flash('You cannot delete that Question!', 'danger')
      return redirect(url_for('hello'))
    else:
      question=db.collection(u'questions').document(post_id).delete()
      flash('Your Question has been deleted!', 'success')
      return redirect(url_for('hello'))
  else:
   flash('Please Login To access This Page','danger')
   return redirect(url_for('login'))
  
  

