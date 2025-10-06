from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware

# --- THIS IS THE FIX ---
# We are changing the imports to be relative by adding a '.' at the beginning.
# This tells Python to look for these folders in the same directory as main.py.
from .api import auth as auth_router
from .api import chat as chat_router
from .api import users as users_router
from .core.config import settings
from .db.session import init_db
# ----------------------

app = FastAPI(title="Kairos Wellness Companion")

# --- CORS Middleware ---
origins = [
    "http://localhost:3000",
    "http://34.56.91.122:3000",
    "https://kairos-wine.vercel.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

@app.on_event("startup")
async def startup_event():
    print("--- Application is starting up... ---")
    await init_db()
    print("--- Application startup complete. ---")

app.include_router(auth_router.router)
app.include_router(chat_router.router)
app.include_router(users_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Kairos API"}

