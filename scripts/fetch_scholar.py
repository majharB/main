import json
from scholarly import scholarly
import time

# Your Google Scholar ID (from your profile URL)
SCHOLAR_ID = "-sM9QXkAAAAJ"

# Search for the author
author = scholarly.search_author_id(SCHOLAR_ID)
scholarly.fill(author, sections=['basics', 'indices', 'publications'])

# Prepare the output structure
data = {
    "name": author.get('name', ''),
    "affiliation": author.get('affiliation', ''),
    "interests": author.get('interests', []),
    "citedby": author.get('citedby', 0),
    "hindex": author.get('hindex', 0),
    "i10index": author.get('i10index', 0),
    "publications": []
}

# Fetch all publications (with a small delay to avoid rate limits)
for pub in author['publications']:
    scholarly.fill(pub)
    pubs = data['publications']
    pubs.append({
        "title": pub.get('bib', {}).get('title', ''),
        "authors": pub.get('bib', {}).get('author', ''),
        "venue": pub.get('bib', {}).get('venue', ''),
        "year": pub.get('bib', {}).get('year', ''),
        "citation": pub.get('num_citations', 0),
        "url": pub.get('pub_url', '')
    })
    time.sleep(2)   # be gentle to Google Scholar

# Save to a JSON file
with open('publications.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)