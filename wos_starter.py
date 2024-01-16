

import requests
import json
from flask import Flask
STARTER_APIKEY="0cc5cef60cb444a1ad517c1ab959b4e677cd55c1"
# Search query for which to calculate the citation report
SEARCH_QUERY = 'OG=Vietnam National University'
RECORDS_TO_DISPLAY = 10

query=f'https://api.clarivate.com/apis/wos-starter/v1/documents?'\
    f'db=WOK&'\
    f'q=(OG=Vietnam National University AND PY=2023 AND DT=Article)'\
    f'&limit=50&page=1&sortField=RS+D'
query=f'https://api.clarivate.com/apis/wos-starter/v1/documents?'\
    f'db=WOK&'\
    f'q=(OG=Vietnam National University AND PY=2023)'\
    f'&limit=50&page=1&sortField=RS+D'
query=f'https://api.clarivate.com/apis/wos-starter/v1/documents?'\
    f'db=WOK&'\
    f'q=(OG=Vietnam National University Hanoi AND DT="Article" )'\
    f'&limit=50&page=1&sortField=RS+D'
query=f'https://api.clarivate.com/apis/wos-starter/v1/documents?'\
    f'db=WOK&'\
    f'q=(OG=Vietnam National University Hanoi AND DT="Article" AND PY=2023)'\
    f'&limit=50&page=1&sortField=RS+D'
query=f'https://api.clarivate.com/apis/wos-starter/v1/documents?'\
    f'db=WOK&'\
    f'q=(OG=Vietnam National University Hanoi)'\
    f'&limit=50&page=1&sortField=RS+D'
print(query)



initial_request = requests.get(query, headers={'X-ApiKey': STARTER_APIKEY})
initial_json = initial_request.json()
"""
for wos_document in initial_json['hits'][:RECORDS_TO_DISPLAY]:
    if 'issn' not in wos_document['identifiers']:
        wos_document['journal_link'] = None
    else:
        journal_request = requests.get(f'https://api.clarivate.com/apis/wos-starter/v1/journals?'
                                       f'issn={wos_document["identifiers"]["issn"]}',
                                       headers={'X-ApiKey': STARTER_APIKEY})
        journal_json = journal_request.json()
        if journal_json['hits']:
            wos_document['source']['sourceTitle'] = f"<a href={journal_json['hits'][0]['links'][0]['url']}>" \
                + wos_document['source']['sourceTitle'] + '</a>'
"""                
with open('data3.json', 'w') as f:
    json.dump(initial_json, f,indent=4,sort_keys=True)
    
app = Flask(__name__)


def create_authors_list(doc):
    authors = []
    for author in doc['names']['authors']:
        if 'researcherId' in author:
            profile_link = (f'https://www.webofscience.com/wos/author/record/'
                            f'{author["researcherId"]}')
            authors.append(f'<a href={profile_link}>{author["wosStandard"]}</a>')
        else:
            authors.append(author["wosStandard"])
    if len(doc['names']['authors']) < 4:
        return ', '.join(authors)
    return f"{', '.join(authors[:3])} et al."


def format_title_length(doc):
    if len(doc['title']) > 100:
        return f"{doc['title'][:100]}..."
    return doc['title']


@app.route("/")
def most_recent_wos_records():
    font_tag = '<p style="font-family:\'Source Sans Pro\'; line-height: 0.5">'
    output = f'{font_tag}Most Recent Documents of: {SEARCH_QUERY}:<br><br></p>'
    for i, record in enumerate(initial_json['hits'][:RECORDS_TO_DISPLAY]):
        authors = create_authors_list(record)
        title = format_title_length(record)

        output += (f'{font_tag}{i + 1}:  Title: <a href={record["links"]["record"]}>'
                   f'{title}</a><br></p>')
        output += f'{font_tag}    By: {authors}<br>'
        output += (f'{font_tag}    Published in: {record["source"]["sourceTitle"]}'
                   f'<br><br></p>')
    return output


#app.run()
