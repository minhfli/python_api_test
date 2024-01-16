


from calendar import c
import json
import re
import time
from tracemalloc import start
from flask import request
import requests


APIKEY='29cf4e9fcf07256282cdbe3a59dca2a6'
header={
    'X-ELS-APIKey':APIKEY,
    'Accept':'application/json'
}
max_item_count=5 # max number of items per request, can't be more than 25 (current service level)
start_index=0 # start index of the item in the search result

base_url='https://api.elsevier.com/content/search/scopus?'
abstract_url='https://api.elsevier.com/content/abstract/scopus_id/'
author_url='https://api.elsevier.com/content/author/author_id/'
affil_url='https://api.elsevier.com/content/affiliation/affiliation_id/'

fulltext_url='https://api.elsevier.com/content/article/scopus_id/'

def format_query(input):
    input=input.replace('(','%28')
    input=input.replace(')','%29')
    input=input.replace(' ','+')
    input=input.replace('"','%22')
    input=input.replace('{','%7B')
    input=input.replace('}','%7D')
    return input

def call_request(query):
    time.sleep(1)
    request=requests.get(query,headers=header)
    print('request: ' + query)
    if request.status_code != 200:
        print('Error' + str(request.status_code))
    else:
        json_data=request.json()
        return json_data

def request_data_identifiers(request_data):
    identifiers={}
    if 'eid' in request_data['coredata']:
        identifiers['eid']=request_data['coredata']['eid']
    if 'pii' in request_data['coredata']:
        identifiers['pii']=request_data['coredata']['pii']
    if 'prism:doi' in request_data['coredata']:
        identifiers['DOI']=request_data['coredata']['prism:doi']
    if 'prism:isbn' in request_data['coredata']:
        identifiers['ISBN']=request_data['coredata']['prism:isbn']
    if 'prism:issn' in request_data['coredata']:
        identifiers['ISSN']=request_data['coredata']['prism:issn']
    if 'pubmed-id' in request_data['coredata']:
        identifiers['pubmed-id']=request_data['coredata']['pubmed-id']
    identifiers['ScopusID']=request_data['coredata']['dc:identifier']
    
    return identifiers

def request_data_source(request_data):
    source={}
    source['Title']=request_data['coredata']['prism:publicationName']
    if 'prism:volume' in request_data['coredata']:
        source['vol']=request_data['coredata']['prism:volume']
    if 'prism:issueIdentifier' in request_data['coredata']: 
        source['issue']=request_data['coredata']['prism:issueIdentifier']
    if 'prism:issn' in request_data['coredata']:    
        source['issn']=request_data['coredata']['prism:issn']
    if 'prism:isbn' in request_data['coredata']:    
        source['isbn']=request_data['coredata']['prism:isbn']
    if 'prism:pageRange' in request_data['coredata']:
        source['pageRange']=request_data['coredata']['prism:pageRange']
    if 'article-number' in request_data['coredata']:
        source['articleNumber']=request_data['coredata']['article-number']
    source['coverDate']=request_data['coredata']['prism:coverDate']
    source['type']=request_data['coredata']['prism:aggregationType']
    return source

def request_data_authors(request_data):
    authors=[]
    for author in request_data['coredata']['dc:creator']['author']:
        my_author=json.loads(json.dumps(author))
        #print(auID)
        #affil_info=call_request(author['affiliation']['@href'])
        #my_author['affiliation']=affil_info
        authors.append(my_author)
    return authors
    
    
def request_data_to_my_data(request_data):
    wanted_data={}
    wanted_data['affilliation']=request_data['affiliation']
    
    wanted_data['ScopusID']=request_data['coredata']['dc:identifier']
    wanted_data['docTitle']=request_data['coredata']['dc:title']
    wanted_data['publisher']=request_data['coredata']['dc:publisher']
    wanted_data['docType']=request_data['coredata']['subtypeDescription']
    wanted_data['citationCount']=request_data['coredata']['citedby-count']
    wanted_data['openaccess']=request_data['coredata']['openaccessFlag']

    wanted_data['identifiers']=request_data_identifiers(request_data)
    wanted_data['source']=request_data_source(request_data)
    wanted_data['authors']=request_data_authors(request_data)
    
    wanted_data['coverDate']=request_data['coredata']['prism:coverDate']
    wanted_data['link']=request_data['coredata']['link']
    
    return wanted_data
        

vnu='affil(affilorg({Vietnam National University, Hanoi})) AND PUBYEAR IS 2023'
#vnu='affil(affilorg({Vietnam National University Hanoi}))'
uet='affil(affilorg({VNU University of Engineering and Technology}))'

query=base_url+ f'query=' +vnu
query+=f'&start={start_index}&count={max_item_count}'

inital_request=requests.get(query,headers=header)
initial_json=inital_request.json()

abstract_data={}
my_data={}


if 'search-results'  in initial_json:
    abstract_data['search-results']=[]
    abstract_data['search-info']={}
    abstract_data['search-info']['Total']=initial_json['search-results']['opensearch:totalResults']
    abstract_data['search-info']['startIndex']=initial_json['search-results']['opensearch:startIndex']
    abstract_data['search-info']['itemsPerPage']=initial_json['search-results']['opensearch:itemsPerPage']

    my_data=json.loads(json.dumps(abstract_data)) # deep copy
    
    for item in initial_json['search-results']['entry']:
        scopus_id=item['dc:identifier'].split(':')[1]
        query=abstract_url+scopus_id
        abstract_data_json=call_request(query)
        abstract_data['search-results'].append(abstract_data_json['abstracts-retrieval-response'])
    
        my_data['search-results'].append(request_data_to_my_data(abstract_data_json['abstracts-retrieval-response']))
        

with open('scopus_initial_data.json','w') as f:
    json.dump(initial_json,f,indent=4,sort_keys=True)
with open('scopus_abstract_data.json','w') as f:
    json.dump(abstract_data,f,indent=4,sort_keys=True)
with open('scopus_modified_data.json','w') as f:
    json.dump(my_data,f,indent=4,sort_keys=True)
    

    