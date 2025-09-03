from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/ping")
def ping_pong():
    return "pong";

@app.get("/health")
def get_health():
    return Response(status_code=200, content="Ok", media_type="text/plain")o

