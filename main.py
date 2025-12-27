from fastapi import FastAPI, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from gemini_client import get_answer_from_gemini
from contextlib import asynccontextmanager
from db import Base, engine, add_request_data, get_user_requests 

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Все таблицы созданы")
    yield

app = FastAPI(
    title="Мой стартап",
    lifespan=lifespan
)

@app.get("/requests")
def get_my_requests(request: Request):
    user_ip_address = request.client.host
    print(f"{user_ip_address=}")
    user_request = get_user_requests(ip_address=user_ip_address) 
    return user_request

@app.post("/requests")
def send_prompt(
    request: Request,
    prompt: str = Body(embed=True)
):
    user_ip_address = request.client.host
    answer = get_answer_from_gemini(prompt)
    add_request_data(
        ip_address=user_ip_address,
        prompt=prompt,
        response=answer,
    )
    return {"answer": answer}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)