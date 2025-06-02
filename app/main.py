from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, todo
from .database import engine, Base

#for create all table
Base.metadata.create_all(bind = engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only! Specify domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(todo.router)

@app.get("/")
def home():
    return {"message" : "todo api"}