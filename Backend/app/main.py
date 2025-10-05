from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from api import auth as auth_router
from api import chat as chat_router
from api import users as users_router  # <-- 1. Import the new users router
from core.config import settings
from db.session import init_db

app = FastAPI(title="Kairos Wellness Companion")

# --- CORS Middleware ---
# This list defines which frontend URLs are allowed to talk to your backend.
origins = [
    "http://localhost:3000",
    "http://34.56.91.122:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <-- Corrected to use your specific origins list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------

# SessionMiddleware for Google Login
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# Startup event to initialize the database connection
@app.on_event("startup")
async def startup_event():
    print("--- Application is starting up... ---")
    await init_db()
    print("--- Application startup complete. ---")

# Include your API routers
app.include_router(auth_router.router)
app.include_router(chat_router.router)
app.include_router(users_router.router)  # <-- 2. Add the new users router

@app.get("/")
def read_root():
    return {"message": "Welcome to the Kairos API"}

