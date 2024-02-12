from fastapi import FastAPI
from api.api import router as api_router
from api.avatar import router as avatar_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

"""
A
M
A
Z
I
N
G
"""
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://yourfrontenddomain.com",
    "https://yourfrontenddomain.com:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(avatar_router) 


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
