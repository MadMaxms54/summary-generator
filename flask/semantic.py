import requests

def get_author_papers(author_name):
    # Define the Semantic Scholar API endpoint for author search
    search_url = f"https://api.semanticscholar.org/graph/v1/author/search?query={author_name}"
    
    # Make the request to the Semantic Scholar API
    response = requests.get(search_url)
    data = response.json()
    
    if data and 'data' in data and len(data['data']) > 0:
        # Get the first author from the search results
        author = data['data'][0]
        author_id = author.get('authorId', None)
        
        if author_id:
            # Define the Semantic Scholar API endpoint for author details
            author_url = f"https://api.semanticscholar.org/graph/v1/author/{author_id}?fields=papers"
            response = requests.get(author_url)
            data = response.json()
            
            # Retrieve papers
            papers = data.get('papers', [])
            publication_list = []
            
            for paper in papers[:5]:  # Limit to top 5 publications
                title = paper.get('title', 'N/A')
                year = paper.get('year', 'N/A')
                citations = paper.get('citationCount', 'N/A')
                
                publication_list.append({
                    'title': title,
                    'year': year,
                    'citations': citations
                })
            
            return publication_list
        else:
            print("Author ID not found.")
            return []
    else:
        print("Author not found!")
        return []