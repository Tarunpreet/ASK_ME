from flask import render_template, url_for, flash, redirect,request,session
from flaskblog import app,auth1,db
from flaskblog.forms import RegistrationForm, LoginForm,UpdateAccountForm,PostForm,AddAnswer,ResetForm,OnlyPostForm
import math
from firebase_admin import auth
from firebase_admin import firestore
import pyrebase
import datetime
import re
import urllib.parse
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer


@app.route("/<int:pageNo>")
def hello1(pageNo):
  current_user=auth1.current_user
  if (auth1.current_user):
    email=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('email')
    print(auth1.get_account_info(current_user['idToken']))
  postsPerPage = 4
  baseRef = db.collection(u'questions')
  total_question=0
  for question_in in baseRef.get():
      total_question=total_question+1
  total_pages=total_question/postsPerPage
  total_pages=(math.ceil(total_pages))
  print(total_pages)
  if (pageNo == 1):
    currentPageRef = baseRef.limit(postsPerPage)
  else:
    lastVisibleRef = baseRef.limit((pageNo-1) * postsPerPage)
    lastVisibleQuerySnapshot = lastVisibleRef.get()
    for question_in in lastVisibleQuerySnapshot:
      last_question=question_in
    currentPageRef = baseRef.start_after(last_question).limit(postsPerPage)
  currentPageQuerySnapshot = currentPageRef.get()
  # users_ref = db.collection(u'questions')
  # docs = users_ref.get()
  # print(docs)
  docs1={}
  docs1=currentPageQuerySnapshot  
  return render_template('home.html',current_user=current_user,questions=docs1,current_page=pageNo,total_pages=total_pages)

@app.route("/")
def hello():
  current_user=auth1.current_user
  postsPerPage = 4
  baseRef = db.collection(u'questions')
  total_question=0
  for question_in in baseRef.get():
    total_question=total_question+1
  total_pages=total_question/postsPerPage
  total_pages=math.ceil(total_pages)
  currentPageRef = baseRef.limit(postsPerPage)
  currentPageQuerySnapshot = currentPageRef.get()
  # users_ref = db.collection(u'questions')
  # docs = users_ref.get()
  # # print(docs)
  question_print=db.collection(u'questions').document('FrcE4xi97gyoI6U9BBR3').get()
  for tag in question_print.get('tags'):
    print(tag)
  docs1={}
  docs1=currentPageQuerySnapshot
  return render_template('home.html',current_user=current_user,questions=docs1,current_page=1,total_pages=total_pages)

# @app.route("/")
# def landing():
#   current_user=auth1.current_user
#   if (auth1.current_user):
#     return redirect(url_for('hello'))
#   else:
#     return render_template('landing.html')
#   return render_template('landing.html')

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

def striphtml(data):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', str(data))
    return cleantext
stop_words = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")


tags_predicted=[]
title_question=" "
content_question=" "

@app.route("/post/new",methods=['GET','POST'])
def quest():
  current_user=auth1.current_user
  if (auth1.current_user):
    form=PostForm()
    if request.method == 'POST':
      if form.submit2.data:
        title=form.title.data
        content=form.content.data
        global title_question
        title_question=title
        global content_question
        content_question=content
        title=re.sub(r'[^A-Za-z]+',' ',title)
        content=re.sub(r'[^A-Za-z]+',' ',content)
        print(title)
        main_url='http://127.0.0.1:5000/'
        url=main_url+'query='+title+" "+content+'/query_content='+content
        print(url)
        try:
          json=requests.get(url).json()
        except:
          flash('An Error has occured','danger')
          return redirect(url_for('quest')) 
        tags=json.get('Tags')
        global tags_predicted
        tags_predicted=tags
        print(tags)
        for tag in tags:
          print(tag)
        print(json)
        return redirect(url_for('pred_tags'))
      elif form.submit.data:
        author=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('displayName')
        author_id=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('localId')
        answers=[]
        tag1=form.tag1.data
        tag2=form.tag2.data
        tag3=form.tag3.data
        tags=[]
        tags.append(tag1)
        tags.append(tag2)
        tags.append(tag3)
        data={
        u'author': author,
        u'author_id': author_id,
        u'content':content,
        u'date_posted': datetime.datetime.now(),
        u'title':title,
        u'answers':answers,
        u'tags':tags
        }
        answers_fire = db.collection(u'questions').document().set(data)
        flash('Question Added','success')
        return redirect(url_for('hello'))
  else:
    flash('Please Login To access This Page','danger')
    return redirect(url_for('login'))
  
  return render_template('create.html',title='NEW QUESTION',form=form,legend='New Question',current_user=current_user)

@app.route("/pred/new",methods=['GET','POST'])
def pred_tags():
  current_user=auth1.current_user
  if (auth1.current_user):
    form=OnlyPostForm()
    if request.method == 'POST':
      author=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('displayName')
      author_id=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('localId')
      answers=[]
      tag1=form.tag1.data
      tag2=form.tag2.data
      tag3=form.tag3.data
      tags=[]
      tags.append(tag1)
      tags.append(tag2)
      tags.append(tag3)
      data={
      u'author': author,
      u'author_id': author_id,
      u'content':content,
      u'date_posted': datetime.datetime.now(),
      u'title':title,
      u'answers':answers,
      u'tags':tags
        }
      answers_fire = db.collection(u'questions').document().set(data)
      flash('Question Added','success')
    elif request.method=='GET':
      global title_question
      global content_question
      global tags_predicted
      form.title.data=title_question
      form.content.data=content_question
      length_tag=len(tags_predicted)
      if length_tag==0:
        flash('No Tags Predicted','danger')
      elif length_tag==1:
        form.tag1.data=tags_predicted[0]
        flash('1 Tag Predicted','success')
      elif length_tag==2:
        form.tag1.data=tags_predicted[0]
        form.tag2.data=tags_predicted[1]
        flash('2 Tags Predicted','success')
      elif length_tag>=3:
        form.tag1.data=tags_predicted[0]
        form.tag2.data=tags_predicted[1]
        form.tag3.data=tags_predicted[2]  
        flash('3 Tags Predicted','success')
      tags_predicted=[]
      title_question=" "
      content_question=" "
  else:
   flash('Please Login To access This Page','danger')
   return redirect(url_for('login'))
  return render_template('create_pred.html',title='NEW QUESTION',form=form,legend='New Question',current_user=current_user)


@app.route("/post/<string:post_id>")
def post(post_id):
  current_user=auth1.current_user
  if (auth1.current_user):
    uid=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('localId')
  else:
    uid=None
  quest_doc = db.collection(u'questions').document(post_id)
  
  quest= quest_doc.get()
  answers=[]
  answers=quest.get('answers')
  #  print((quest.get('answers')[0].get('content')))
  # for i in quest.get('answers'):
  #   print(i.get('content'))
  return render_template('question.html', title=quest.get('title'), question=quest,current_user=current_user,author_id=uid,answers=answers,index=-1)

@app.route("/answer/new/<string:post_id>",methods=['GET','POST'])
def add_answer(post_id):
  current_user=auth1.current_user
  if (auth1.current_user):
   form=AddAnswer()
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
    
    # db.collection(u'questions').document(post_id).update({u'answers': ([data])})
    quest_doc = db.collection(u'questions').document(post_id)
    quest= quest_doc.get()
    answers=[]
    answers=quest.get('answers')
    answers.append(data)
    db.collection(u'questions').document(post_id).update({u'answers': answers})
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

@app.route("/questions/<string:post_id>/answers/<int:index>/delete", methods=['POST'])
def delete_answer(post_id,index):
  current_user=auth1.current_user
  if (auth1.current_user):
    quest_doc = db.collection(u'questions').document(post_id)
    quest= quest_doc.get()
    answers=[]
    answers=quest.get('answers')
    newanswers=[]
    # print((answers))
    author_id=(auth1.get_account_info(current_user['idToken']).get('users')[0]).get('localId')

    if answers[index].get('author_id') != author_id:
      flash('You cannot delete that Answer!', 'danger')
      return redirect(url_for('hello'))
    else:
      indexs=0
      for answer in answers:
        if indexs!=index:
          newanswers.append(answer)
        indexs=indexs+1
      
      db.collection(u'questions').document(post_id).update({u'answers': newanswers})
      flash('Your Answer has been deleted!', 'success')
      return redirect(url_for('hello'))
  else:
   flash('Please Login To access This Page','danger')
   return redirect(url_for('login'))
  
  

