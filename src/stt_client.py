#!/usr/bin/env python

import logging
from tinkoff_voicekit_client import ClientSTT
from src.tools import Settings

__all__ = ["STTClient"]

logger = logging.getLogger(__name__)


class STTClient:

    def __init__(self) -> None:
        self._client = ClientSTT(
            Settings().stt_api_key(),
            Settings().stt_secret_key()
        )
        self._stt_config = {
            "encoding": "LINEAR16",
            "sample_rate_hertz": 8000,
            "num_channels": 1
        }
        logging.info(f"STT Client initialized")

    def recognize(self, wav_path: str) -> str:
        logging.info(f"Got audio: {wav_path}")
        json_output = self._client.recognize(wav_path, self._stt_config)
        results = json_output["results"]
        if len(results) == 0:
            return "Empty result"
        alternatives = results[0]["alternatives"]
        if len(alternatives) == 0:
            return "Empty result"
        return alternatives[0]["transcript"]
