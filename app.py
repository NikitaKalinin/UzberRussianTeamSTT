#!/usr/bin/env python

import logging
from argparse import ArgumentParser
from src import (
    Settings,
    TelegramClient,
    APP_TEMP_DIRECTORY,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def parse_args() -> None:
    parser = ArgumentParser(description="UzberRusTeamSTT Bot.")
    parser.add_argument("--stt_api_key", required=True, help="stt api key")
    parser.add_argument("--stt_secret_key", required=True, help="stt secret key")
    parser.add_argument("--bot_token", required=True, help="bot token")
    args = parser.parse_args()
    Settings().set(
        stt_api_key=args.stt_api_key,
        stt_secret_key=args.stt_secret_key,
        bot_token=args.bot_token,
    )


if __name__ == "__main__":
    parse_args()
    APP_TEMP_DIRECTORY.mkdir(exist_ok=True)
    TelegramClient().run()
