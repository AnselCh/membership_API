from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as member_router

config = dotenv_values(".env")  # 讀取.env

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(member_router, tags=["membership"], prefix="/membership")
