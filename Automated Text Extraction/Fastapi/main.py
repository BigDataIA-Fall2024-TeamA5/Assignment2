from fastapi import FastAPI
from jwtauth import router  # Ensure jwtauth.py has a `router` defined

app = FastAPI()

# Include the `jwtauth.py` router
app.include_router(router, prefix="/auth")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI JWT Authentication Application!"}
