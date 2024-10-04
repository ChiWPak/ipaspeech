"""Wrapper around Polly client
"""

from __future__ import annotations

import os

import boto3


POLLY_HOME_PATH = os.getenv("POLLY_HOME_PATH")


polly_client = boto3.client("polly", region_name="us-east-1")


class Polly:
    """Wrapper around Polly boto3 client
    """

    def __init__(self):
        pass

    @property
    def polly(self):
        """boto3 Polly client
        """
        return polly_client

    @property
    def audio_path(self) -> str:
        """Audio path"""
        return f"{POLLY_HOME_PATH}/speech.mp3"

    def tts(
            self,
            text: str,
            engine: str = "generative",
            output_format: str = "mp3",
            text_type: str = "ssml",
            voice_id: str = "Ruth",
        ) -> dict:
        """Make Polly synthesize speech call
        """
        response = self.polly.synthesize_speech(
            Engine=engine,
            OutputFormat=output_format,
            Text=text,
            TextType=text_type,
            VoiceId=voice_id,
        )
        self._write(response)
        return response

    def _write(self, response: dict) -> None:
        """Save audio response to file
        """
        with open(self.audio_path, "wb") as f:
            f.write(response["AudioStream"].read())
