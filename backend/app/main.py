from typing import List
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

import datetime

from database.db import session
from models.model import Member, MemberTable
from crud import member_crud as crud
from router import member_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(member_router.router, tags=["Member"], prefix="/member")