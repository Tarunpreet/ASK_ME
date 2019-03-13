from ASK import db
from datetime import datetime

class User(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  username = db.Column(db.String(20),unique=True,nullable=False)
  email = db.Column(db.String(120),unique=True,nullable=False)
  password=db.Column(db.String(60),nullable=False)
  posts = db.relationship('Questions',backref='author',lazy=True) 
  answers=db.relationship('Answers',backref='author',lazy=True) 
  
  def __repr__(self):
    return f"User('{self.username}','{self.email}')"
    # query function
    # user.query.all()

class Questions(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  title=db.Column(db.String(100),nullable=False)
  date_post=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
  content=db.Column(db.Text,nullable=False)
  user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
  answers = db.relationship('Answers',backref='question',lazy=True)

  def __repr__(self):
    return f"Questions('{self.title}','{self.date_post}')"
    # query function
    # user.query.all(),.first()

class Answers(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  date_post=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
  content=db.Column(db.Text,nullable=False)
  question_id=db.Column(db.Integer,db.ForeignKey('questions.id'),nullable=False)
  user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

  def __repr__(self):
    return f"Questions('{self.question_id}',{self.question_id},'{self.date_post}')"
    