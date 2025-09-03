from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()

@app.get("/ping")
def ping_pong():
    return "pong";

@app.get("/health")
def get_health():
    return Response(status_code=200, content="Ok", media_type="text/plain")

class Characteristic(BaseModel):
    ram_memory: int
    rem_memory: int

class PhoneModel(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristic

stored_phones: list[PhoneModel] = []

@app.post("/phones")
def post_phones(phones: list[PhoneModel]):
    for phone in phones:
        for stored_phone in stored_phones:
            if not (stored_phone.identifier == phone.identifier):
                stored_phones.append(phone)
    return Response(content={
        "message": "Phones created",
    }, status_code=201, media_type="application/json")

def serialize_phones(phones: list[PhoneModel]):
    return [phone.model_dump() for phone in phones]

@app.get("/phones")
def get_phones():
    return Response(
        content={
            "data": stored_phones
        }, status_code=200, media_type="application/json"
    )

@app.get("/phones/{id}")
def get_phones_by_id(id: str):
    target_phone = None
    for stored_phone in stored_phones:
        if stored_phone.identifier == id:
            target_phone = stored_phone
    if target_phone is None:
        return Response(
            content={
                "message": "Phone not found."
            },
            status_code=404,
            media_type="application/json"
        )

@app.put("/phones/{id}/characteristics")
def put_charac_phone(id: str, charac: Characteristic):
    found = False
    new_phone = None
    for stored_phone in stored_phones:
        if stored_phone.identifier == id:
            stored_phone.characteristics = charac
            new_phone = stored_phone
            found = True
    if not found:
        return Response(content={
            "message": "Phone not found",
        }, status_code=404, media_type="application/json")
    else:
        return Response(
            content={
                "data": new_phone
            },
            status_code=200,
            media_type="application/json"
        )
