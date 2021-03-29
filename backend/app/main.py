from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from router import member_router, face_router, payment_router

from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html


app = FastAPI(openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(member_router.router, tags=["Member"], prefix="/api/member")
app.include_router(face_router.router, tags=["Face"], prefix="/api/face")
app.include_router(payment_router.router, tags=["Payment"], prefix="/api/pay")

@app.get("/api/docs")
async def get_swagger_documentation():
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs")


@app.get("/api/redoc")
async def get_redoc_documentation():
    return get_redoc_html(openapi_url="/api/openapi.json", title="docs")

