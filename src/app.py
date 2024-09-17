"""API entry point
"""

from fastapi import (
    FastAPI,
    Request
)
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

from routers import tts

templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="IPA",
    summary="IPA speech",
    docs_url="/swagger",
    redoc_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=RedirectResponse, include_in_schema=False)
def root():
    """Docs"""
    return "/docs"


@app.get("/ping", status_code=200, include_in_schema=False)
def ping():
    """Health check"""
    return {"response": "pong"}


@app.get("/home", status_code=200, include_in_schema=False)
async def homepage(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", context={"request": request})


app.include_router(tts.router)
