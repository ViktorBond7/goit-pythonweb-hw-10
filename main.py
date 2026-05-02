from fastapi import FastAPI
import uvicorn
from src.api.contact_api import router as contact_router
from src.api.user_api import router as user_router
from src.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

app = FastAPI()

app.include_router(contact_router)
app.include_router(user_router)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/")
async def root():
    return {"message": "Hello World!!!!!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
