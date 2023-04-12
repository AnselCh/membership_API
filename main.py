from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as member_router
from fastapi.middleware.cors import CORSMiddleware

config = dotenv_values(".env")  # 讀取.env

app = FastAPI()

# 設置允許串接ip
origins = [
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(member_router, tags=["membership"], prefix="/membership")
