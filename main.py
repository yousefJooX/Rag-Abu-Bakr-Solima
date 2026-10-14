from  fastapi import FastAPI
app = FastAPI()
# call a  funiction useing api  

@app.get("/welcome")  #  listening to the root endpoint  
def welcome():
    return {"message": "Welcome to the mini-rag API! made by joox "}