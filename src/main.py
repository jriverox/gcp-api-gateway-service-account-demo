import os
import asyncio
import uvicorn
from fastapi import FastAPI

from routes import product_router

app = FastAPI(
    title="Products API",
    version="1.0.0",
    openapi_url="/api/docs")

app.include_router(product_router.router, prefix="/api")

class Server(uvicorn.Server):
    pass

async def main():
    server = Server(
        config=uvicorn.Config(app=app, host=os.getenv("HOST","0.0.0.0"), port=os.getenv("PORT",8000)),
    )
    app_task = asyncio.create_task(server.serve())
    await asyncio.wait([app_task])


if __name__ == "__main__":
    asyncio.run(main())