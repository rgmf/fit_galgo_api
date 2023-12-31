from fastapi import FastAPI

from app.routers import jwt_auth, users, files, activities, monitorings

app = FastAPI(debug=True)
app.include_router(jwt_auth.router)
app.include_router(users.router)
app.include_router(files.router)
app.include_router(activities.router)
app.include_router(monitorings.router)


@app.get("/")
async def root():
    return {"message": "Welcome to FitGalgo API"}
