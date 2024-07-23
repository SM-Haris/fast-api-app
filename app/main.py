import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middlewares.auth_middleware import AuthenticationMiddleware
from app.middlewares.exception_middleware import UnexpectedErrorMiddleware
from app.shared_utils.log_utils import setup_logging
from app.database import init_db
from app.users.routes import user_router
from contextlib import asynccontextmanager

version = "v1"

@asynccontextmanager
async def life_span(app: FastAPI):
    await init_db()
    print("Starting server....")
    yield
    print("Server is stoppend...")

setup_logging()
logger = logging.getLogger("fastapi")

app = FastAPI(version=version, lifespan=life_span)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthenticationMiddleware)
app.add_middleware(UnexpectedErrorMiddleware)

app.include_router(user_router, prefix=f"/api/{version}/user",tags=["User"])


@app.get("/")
async def read_root():
    return {"message": "hello world"}


