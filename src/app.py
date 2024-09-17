"""API entry point
"""

from fastapi import (
    Depends,
    FastAPI,
    Form,
    HTTPException,
    Path,
    Request
)
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

from .tts.polly import Polly

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


def get_tts_client(provider: str = Path(...)):
    """Get TTS client based on provider"""
    if provider == "polly":
        tts_client = Polly()
    else:
        raise HTTPException(f"Provider {provider} is not supported.")
    return tts_client


@app.post("/tts/{provider}", status_code=200, response_class=FileResponse, include_in_schema=False)
async def polly(text: str = Form(...), tts_client = Depends(get_tts_client)):
    """Polly text to speech"""
    tts_client.tts(text=text)
    return FileResponse(path=tts_client.audio_path, media_type="mp3")
