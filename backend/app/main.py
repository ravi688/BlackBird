from fastapi import FastAPI


app = FastAPI(
        title="BlackBird Backend",
        description="BlackBird Backend",
        version="0.0.1"
        )

@app.get("/")
async def root():
        return { "message" : "Hello World!" }

@app.get("/health")
async def health():
        return { "status" : "healthy" }


