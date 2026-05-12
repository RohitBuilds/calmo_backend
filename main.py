from fastapi import FastAPI
from src.user.router import router as user_router
from src.stressEntries.router import router as stressAnalyze_router
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from src.utils.db import engine,Base

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(stressAnalyze_router)

@app.get("/")
def home():
    return {"message": "Welcome Home"}