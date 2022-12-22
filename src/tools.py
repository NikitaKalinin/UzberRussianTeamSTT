#!/usr/bin/env python

import subprocess as sp
from pathlib import Path
from typing import Any


__all__ = [
    "Singleton",
    "Settings",
    "APP_TEMP_DIRECTORY",
    "convert_ogg_to_wav_mono"
]

APP_TEMP_DIRECTORY = Path(__file__).parent.parent.resolve() / "tmp"


def check_is_not_none(arg: Any) -> Any:
    assert arg is not None
    return arg


def convert_ogg_to_wav_mono(path: Path) -> None:
    command = [
        "ffmpeg", "-i",
        str(path.with_suffix(".ogg")),
        "-ac", "1", "-ar", "8000",
        str(path.with_suffix(".wav")),
    ]
    sp.run(command, stderr=sp.DEVNULL, stdout=sp.DEVNULL)
    assert path.with_suffix(".wav").exists(), "Convert OGG to WAV 8khz failed"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Settings(metaclass=Singleton):
    def __init__(self) -> None:
        self._STT_API_KEY = None
        self._STT_SECRET_KEY = None
        self._BOT_TOKEN = None

    def set(self, stt_api_key: str, stt_secret_key: str, bot_token: str) -> None:
        self._STT_API_KEY = stt_api_key
        self._STT_SECRET_KEY = stt_secret_key
        self._BOT_TOKEN = bot_token

    def bot_token(self) -> str:
        return check_is_not_none(self._BOT_TOKEN)

    def stt_api_key(self) -> str:
        return check_is_not_none(self._STT_API_KEY)

    def stt_secret_key(self) -> str:
        return check_is_not_none(self._STT_SECRET_KEY)
