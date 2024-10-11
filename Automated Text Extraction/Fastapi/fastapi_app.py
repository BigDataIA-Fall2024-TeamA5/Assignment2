# fastapi_app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from jwtauth import auth_router
from pdf_routes import pdf_router  # Import the PDF router

# Create the FastAPI app
app = FastAPI()

# CORS Configuration (if needed)
origins = [
    "http://localhost:8501",
    "http://127.0.0.1:8501"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication routes from `jwtauth.py`
app.include_router(auth_router, prefix="/auth")

# Include PDF routes from `pdf_routes.py`
app.include_router(pdf_router, prefix="/pdf")

# Root endpoint to test the server
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Application!"}