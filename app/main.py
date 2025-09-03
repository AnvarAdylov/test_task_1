from fastapi import FastAPI

from app.routers import auth, departments, files, users

app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router)
app.include_router(departments.router)
app.include_router(files.router)


@app.get("/")
async def root():
    return {"message": "API is working 🚀"}
