import requests
import json

URL='http://127.0.0.1:8000/'
newURL='http://127.0.0.1:8000/crud/'

get_response=requests.get(url=URL)
# print(get_response.json())

def get_data(id = None):
    data={}
    if id is not None:
        data={'id':id}
    json_data = json.dumps(data)
    r = requests.get(url=newURL, data=json_data)
    data = r.json()
    print(data)

def delete_data(id=None):
    data={}
    if id is not None:
        data={'id':id}
    json_data = json.dumps(data)
    r = requests.delete(url=newURL, data=json_data)
    data = r.json()
    print(data)

def post_data():
    id = int(input("Enter the id"))
    section = str(input('Enter the section'))
    name = str(input('Enter the name of the book'))
    nfp = int(input('Enter the no of pages'))
    data={
        'id':id,
        'section':section,
        'name':name,
        'nfp':nfp
    }
    json_data = json.dumps(data)
    r = requests.post(url=newURL, data=json_data)
    data = r.json()
    print(data)

def update_data():
    id = int(input("Enter the id"))
    section = str(input('Enter the section'))
    name = str(input('Enter the name of the book'))
    nfp = int(input('Enter the no of pages'))
    data={
        'id':id,
        'section':section,
        'name':name,
        'nfp':nfp
    }
    json_data = json.dumps(data)
    r = requests.put(url=newURL, data=json_data)
    data = r.json()
    print(data)


val=1
while(val!=5):
    print("1.Get a particular book using its id")
    print('2.Delete a particular book using its id')
    print('3.Create a book')
    print('4.Complete Update')
    print('5.Exit')
    val = int(input('Enter your choice'))
    if(val == 1):
        id=int(input('Enter the id'))
        get_data(id)
    elif(val == 2):
        id=int(input('Enter the id'))
        delete_data(id)
    elif(val == 3):
        post_data()
    elif(val==4):
        update_data()
    elif(val == 5):
        print('Exiting..')
        break

