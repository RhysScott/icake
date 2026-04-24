from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def name():
    return {"name": "金鑫"}

@app.get("/name_1")
def name_1():
    return {"name1": "向可欣"}


@app.get("/lkl")
def lkl():
    return {"lkl":"龙科霖"}

@app.get("/hsj")
def hsj():
    return {"hsj":"黄树军"}