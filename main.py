from fastapi import FastAPI
import uvicorn
from src.api.contact_api import router as contact_router
from src.api.user_api import router as user_router

app = FastAPI()

app.include_router(contact_router)
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Hello World!!!!!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
