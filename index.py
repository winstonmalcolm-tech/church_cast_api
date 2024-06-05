from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging
from pydantic import BaseModel

app = FastAPI()

class Detail(BaseModel):
    title: str
    message: str
    tokens: list
    data: dict
    

cred = credentials.Certificate("serviceAccountKey.json")

default_app = firebase_admin.initialize_app(cred)



@app.post("/send") 
def home(detail: Detail):
    print(detail.data)
    message = messaging.MulticastMessage(
        data = detail.data,
        notification = messaging.Notification(
            title = detail.title,
            body = detail.message
        ),
        tokens = detail.tokens
    )
    
    response = messaging.send_multicast(message)
    
    print(response)
    
    return {"Data": "Sent"}

