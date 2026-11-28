from fastapi import FastAPI
from app.routers import admin, public


app = FastAPI(
        title="BlackBird Backend",
        description="BlackBird Backend",
        version="0.0.1"
        )

app.include_router(admin.router, prefix="/api")
app.include_router(public.router, prefix="/api")

@app.get("/")
async def root():
        return { "message" : "Hello World!" }

@app.get("/health")
async def health():
        return { "status" : "healthy" }


