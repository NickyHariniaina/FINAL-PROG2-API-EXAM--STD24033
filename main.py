from fastapi import FastAPI, Response
from fastapi.routing import JSONResponse;

app = FastAPI()

@app.get("/ping")
def ping_pong():
    return "pong";

