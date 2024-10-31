import binascii
import json
import os
import requests
from scholarly import scholarly
from flask import Flask, flash, redirect, render_template,request, url_for
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/muthu"  
mongo = PyMongo(app)


@app.route("/muthu")
def home():
    return render_template('author.html')

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

@app.route('/search', methods=['POST', 'GET'])
def mu():

    author_names = request.form.get('name')

    author_infos = []  # Array to hold all author info

    try:
        # Check if author_names is provided
        if author_names:
            # Split by comma if present; otherwise, treat it as a single name
            if ',' in author_names:
                author_names = [name.strip() for name in author_names.split(',')]
            else:
                author_names = [author_names.strip()]  # Ensure it's a list with a single entry
        else:
            author_names = []  # Set to empty list if no names provided

        for author_name in author_names:
            if author_name:  # Ensure author_name is not empty
                # First, check if the author is already in the database
                author_info = mongo.db.multiple_values.find_one({"name": author_name})

                if author_info:
                    author_infos.append(author_info)  # If found, add to the list
                else:
                    # If author not found, perform search
                    search_query = scholarly.search_author(author_name)
                    author = next(search_query, None)

                    if author:
                        # Fill in the author details
                        author = scholarly.fill(author)

                        author_info = {
                            "name": author.get('name', 'N/A'),
                            "affiliation": author.get('affiliation', 'N/A'),
                            "total_citations": author.get('citedby', 'N/A'),
                            "h_index": author.get('hindex', 'N/A'),
                            "i10_index": author.get('i10index', 'N/A'),
                            "email": author.get('email', 'N/A'),
                            "top_publications": []
                        }

                        # Gather publications from scholarly
                        for publication in author.get('publications', []):
                            pub_info = {
                                "title": publication['bib'].get('title', 'N/A'),
                                "year": publication['bib'].get('pub_year', 'N/A'),
                                "citations": publication.get('num_citations', 'N/A')
                            }
                            author_info["top_publications"].append(pub_info)

                        # Semantic Scholar API call
                        search_url = f"https://api.semanticscholar.org/graph/v1/author/search?query={author_name}"
                        response = requests.get(search_url)
                        data = response.json()

                        if data and 'data' in data and len(data['data']) > 0:
                            author_data = data['data'][0]
                            author_id = author_data.get('authorId', None)
                            author_url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}?fields=name,affiliations,citationCount,papers"
                            response = requests.get(author_url)
                            data = response.json()
                            papers = data.get('papers', [])
                            
                            if papers:
                                for paper in papers:
                                    pub1_info = {
                                        "title": paper.get('title', 'N/A'),
                                        "year": paper.get('year', 'N/A'),  # Updated to use 'year'
                                        "citations": paper.get('citationCount', 'N/A')  # Updated to use 'citationCount'
                                    }
                                    author_info["top_publications"].append(pub1_info)

                        # Insert the gathered author information into MongoDB
                        mongo.db.multiple_values.insert_one(author_info)
                        author_infos.append(author_info)

    except Exception as e:
        print(f"An error occurred: {e}")  # Log the error for debugging

    # After processing, render the display template with author information
    return render_template("display.html", authorinfos=author_infos)



if __name__ == "__main__":
    app.run(debug=True)
