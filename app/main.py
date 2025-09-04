from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware import init_middleware
from app.routers import auth, departments, files, users

app = FastAPI(title="File Management API")


init_middleware(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👉 change later to ["http://localhost:3000"] etc.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router)
app.include_router(departments.router)
app.include_router(files.router)


@app.get("/")
async def root():
    return {"message": "API is working 🚀"}
