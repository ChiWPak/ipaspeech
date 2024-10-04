"""Router for Text to Speech
"""
from fastapi import APIRouter, Depends, Form, HTTPException, Path
from fastapi.responses import FileResponse

from routers.providers.polly import Polly


router = APIRouter(
    prefix="/tts",
    tags=["tts"],
    responses={404: {"description": "Not found"}},
)


def get_tts_client(provider: str = Path(...)):
    """Get TTS client based on provider"""
    if provider == "polly":
        tts_client = Polly()
    else:
        raise HTTPException(f"Provider {provider} is not supported.")
    return tts_client


@router.post("/{provider}", status_code=200, response_class=FileResponse, include_in_schema=False)
async def polly(text: str = Form(...), tts_client = Depends(get_tts_client)):
    """Polly text to speech"""
    tts_client.tts(text=text)
    return FileResponse(path=tts_client.audio_path, media_type="mp3")
