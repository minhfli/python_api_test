import json

with open('data3.json') as f:
   data = json.load(f)

output={}

count=0
for i, record in enumerate(data['hits']):
    count+=1

output['count']=count
with open('count.json', 'w') as f:
    json.dump(output, f,indent=4,sort_keys=True)