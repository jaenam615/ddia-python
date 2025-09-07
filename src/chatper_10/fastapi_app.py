from fastapi import FastAPI
from chatper_10.api.router import router as user_router

app = FastAPI(title="Chapter 10 API")

app.include_router(user_router)