from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from router import member_router, face_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(member_router.router, tags=["Member"], prefix="/member")
app.include_router(face_router.router, tags=["Face"], prefix="/face")