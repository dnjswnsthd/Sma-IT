from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from router import member_router

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(member_router.router, tags=["Member"], prefix="/api/member")

@app.get("/api/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}