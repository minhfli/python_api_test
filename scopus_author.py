import requests

APIKEY='29cf4e9fcf07256282cdbe3a59dca2a6'
header={
    'X-ELS-APIKey':APIKEY,
    'Accept':'application/xml'
}

request=requests.get('https://api.elsevier.com/content/author/author_id/58777680400',headers=header)

print(request.text)