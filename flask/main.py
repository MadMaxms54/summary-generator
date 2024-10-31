import json
import requests
from scholarly import scholarly
from flask import Flask, redirect, render_template,request, url_for
from flask_pymongo import PyMongo
import xml.etree.ElementTree as ET
from scholar import get_author_and_institute_info
from dblp import search_dblp
from semantic import get_author_papers 



app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/muthu"  
mongo = PyMongo(app)
top_publications=[]
affilation=""
email=''
name=""
@app.route("/muthu")
def home():
    return render_template('muthu.html')

@app.route("/hello")
def hello():
    return "<h1>Hello, World!</h1>"

# @app.route("/login", methods=['POST','GET'])
# def log():
#     if request.method=='POST':
#         n=request.form.get('name')
#         a=request.form.get('age')
#         c=request.form.get('city')
#         return n

@app.route('/suc',methods=['POST','GET'])
def suc():
         if request.method=='POST':
          n=request.form.get('name')
          a=request.form.get('age')
          c=request.form.get('city')
          mongo.db.multiple_values.insert_one({"names": n, "ages": a, "cities": c})
          return render_template('sucess.html',name=n,age=a,city=c)

@app.route('/aut')
def aut():
    return render_template('author.html')

@app.route('/mu',methods=['POST','GET'])
def mu():
     name=request.form.get('name')
     
     author_info = mongo.db.multiple_values.find_one({"name": name})
    
     if  author_info:
          return render_template("display.html",authorinfo=author_info)
     else:
         return redirect(url_for('muthu'))
     
@app.route('/mut',methods=['POST','GET'])
def muthu():
    top_publications=get_author_and_institute_info(name)
    top_publications=search_dblp(name)
    top_publications=get_author_papers(name)
    author_info={
      "name":name,
      "affilation":affilation,
      "publication":top_publications
    }

    mongo.db.multiple_values.insert_one()
    return render_template("display.html",author_info)


if __name__ == "__main__":
    app.run(debug=True)
