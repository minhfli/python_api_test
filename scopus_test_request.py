import re
import requests
import time

APIKEY='29cf4e9fcf07256282cdbe3a59dca2a6'
header={
    'X-ELS-APIKey':APIKEY,
}

def call_request(query):
    time.sleep(1)
    request=requests.get(query,headers=header)
    
    print('request limit:' + request.headers['X-RateLimit-Limit'])
    print('request remaining:' + request.headers['X-RateLimit-Remaining'])
    print('request reset:' + request.headers['X-RateLimit-Reset'])
    print('request: ' + query)
    if request.status_code != 200:
        print('Error' + str(request.status_code))
    else:
        print('Success')
        #if (request.json() is not None):
            #return request.json()
    return request

max_item_count=1 # max number of items per request, can't be more than 25 (current service level)
start_index=0 # start index of the item in the search result

base_url='https://api.elsevier.com/content/search/scopus?'
abstract_url='https://api.elsevier.com/content/abstract/scopus_id/'
author_url='https://api.elsevier.com/content/author/author_id/'
affil_url='https://api.elsevier.com/content/affiliation/affiliation_id/'

#test id
doc_scopus_id='85180440817'
auid='58777680400'
afid='121501240'

# ABSTRACT --------------------------------------------------------------------
query=abstract_url+doc_scopus_id+f'?view=META_ABS'
response=call_request(query)
with open('scopus_test_abstract_metaabs.txt','w') as outfile:
    outfile.write(response.text)
    
query=abstract_url+doc_scopus_id+f'?view=FULL'
response=call_request(query)
with open('scopus_test_abstract_full.txt','w') as outfile:
    outfile.write(response.text)

# AUTHOR ----------------------------------------------------------------------
query=author_url+auid+f'?view=LIGHT'
response=call_request(query)
with open('scopus_test_author_light.txt','w') as outfile:
    outfile.write(response.text)
    
query=author_url+auid+f'?view=STANDARD'
response=call_request(query)
with open('scopus_test_author_standard.txt','w') as outfile:
    outfile.write(response.text)
    
# AFFILIATION -----------------------------------------------------------------
query=affil_url+afid+f'?view=STANDARD'
response=call_request(query)
with open('scopus_test_affil_standard.txt','w') as outfile:
    outfile.write(response.text)

