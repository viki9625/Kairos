from fastapi import FastAPI
from core.config import settings
from api import auth as auth_router
from api import chat as chat_router
from api import admin as admin_router
from db.base import init_db


app = FastAPI(title='Mental Wellness API', version='1.0.0')


@app.on_event("startup")
async def on_startup():
	await init_db()


app.include_router(auth_router.router)
app.include_router(chat_router.router)
app.include_router(admin_router.router)


@app.get("/health")
async def health():
	return {"status": "ok"}