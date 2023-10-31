from fastapi import FastAPI

from app.routers import files, jwt_auth

app = FastAPI()
app.include_router(jwt_auth.router)
app.include_router(files.router)


@app.get("/")
async def root():
    return {"message": "Welcome to FitGalgo API"}
