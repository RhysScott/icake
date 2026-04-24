from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def name():
    return{"name":"金鑫"}