from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.database import init_db
from api.dishes import router as dishes_router
from api.orders import router as orders_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="我的饭 API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dishes_router, prefix="/api")
app.include_router(orders_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "我的饭 API", "version": "1.0.0"}
