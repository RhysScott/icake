from fastapi import FastAPI
from common.utils import ApiResponse
from typing import Any

app = FastAPI()

@app.get("/")
def name()->dict[str,str]:
    return{"name":"宾宇轩"}

@app.get("/王明鑫")
def _()->dict[str,Any]:
    return ApiResponse.success({"name":"王明鑫"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)