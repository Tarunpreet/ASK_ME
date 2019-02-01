from flask import Flask
from flask_cors import CORS, cross_origin
from flask import render_template
app = Flask(__name__)
# api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
question=[
   {
     'author':'Tarunpreet Singh',
     'date_created':'20/1/2019',
     'Title':"What is 'Context' on Android?",

   },
   {
     'author':'Tarunpreet',
     'date_created':'20/1/2019',
     'Title':"What is 'Context' on Android?",

   },
    {
     'author':'Tarunpreet',
     'date_created':'20/1/2019',
     'Title':"What is 'Context' on Android?",

   }


]
@app.route("/")
def hello():
	return render_template('home.html',questions=question) 




if __name__ == '__main__':
    app.run(debug=True)