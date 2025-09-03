from fastapi import FastAPI
from app.routers import auth, users, files


app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(files.router, prefix="/files", tags=["Files"])


@app.get("/")
async def root():
    return {"message": "API is working 🚀"}
