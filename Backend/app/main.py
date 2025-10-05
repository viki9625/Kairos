from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from api import auth as auth_router
from api import chat as chat_router
from core.config import settings
from db.session import init_db  # <-- Make sure this import is here

app = FastAPI(title="Kairos Wellness Companion")

# --- CORS Middleware ---
origins = [
    "http://localhost:3000",
    "http://34.56.91.122:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------

# SessionMiddleware for Google Login
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)

# --- This startup event handler is now UNCOMMENTED ---
@app.on_event("startup")
async def startup_event():
    """
    This function runs when the application starts.
    It initializes the database connection.
    """
    print("--- Application is starting up... ---")
    await init_db()
    print("--- Application startup complete. ---")
# ----------------------------------------------------

# Include your API routers
app.include_router(auth_router.router)
app.include_router(chat_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Kairos API"}

