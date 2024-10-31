import json
from scholarly import scholarly

def get_author_and_institute_info(author_name):
    # Search for the author
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
        
        # Get top 5 publications
        for publication in author.get('publications', [])[:5]:
            pub_info = {
                "title": publication['bib'].get('title', 'N/A'),
                "year": publication['bib'].get('pub_year', 'N/A'),
                "citations": publication.get('num_citations', 'N/A')
            }
            author_info["top_publications"].append(pub_info)
        
        # Print author information in JSON format
        print(json.dumps(author_info, indent=4))
    else:
        print(json.dumps({"error": "Author not found!"}, indent=4))

# Example usage
author_name = "Prabaldeep Das"  # Replace with the author's name you want to search
get_author_and_institute_info(author_name)
