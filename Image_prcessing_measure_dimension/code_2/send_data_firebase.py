import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("../code_2/impro-55674-firebase-adminsdk-qt6ir-86bcd1c6eb.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://impro-55674-default-rtdb.firebaseio.com/'
})

width = 999
length = 999
thick = 999

root = db.reference()
# data = db.reference().get()
# print(data)
send_data = root.child('measurement').push({
    'length' : length,
    'thick' : thick,
    'width' : width
})
