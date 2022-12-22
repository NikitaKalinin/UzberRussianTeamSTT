#!/usr/bin/env python

import logging
from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from src.tools import (
    Settings,
    APP_TEMP_DIRECTORY,
    convert_ogg_to_wav_mono,
)

from src.stt_client import STTClient

logger = logging.getLogger(__name__)


class TelegramClient:

    @staticmethod
    def run():
        updater = Updater(Settings().bot_token())
        updater.dispatcher.add_handler(MessageHandler(Filters.voice, TelegramClient.recognize_via_bot))
        updater.start_polling()
        updater.idle()
        logging.info("Telegram Client initialized")

    @staticmethod
    def recognize_via_bot(update: Update, context: CallbackContext) -> None:
        try:
            result_text = TelegramClient._recognize_via_bot(update)
        except Exception as ex:
            logging.error(f"Got error: {ex}")
            result_text = str(ex)
        update.message.reply_text(result_text, quote=True)

    @staticmethod
    def _recognize_via_bot(update: Update) -> str:
        attachment = update.message.voice
        assert (attachment["mime_type"] == "audio/ogg") or (attachment["mime_type"] == "ogg"), \
            f"Format: expected ogg, got {attachment['mime_type']}"
        logging.info(f"Got voice: {attachment} FROM {update.message.from_user}")
        voice = attachment.get_file()
        tmp_voice_path = APP_TEMP_DIRECTORY / str(update.message.message_id)
        with open(tmp_voice_path.with_suffix('.ogg'), 'wb') as out:
            voice.download(out=out)
        convert_ogg_to_wav_mono(tmp_voice_path)
        output = STTClient().recognize(str(tmp_voice_path.with_suffix(".wav")))
        logging.info(f"STT Result: {output}")
        tmp_voice_path.with_suffix(".wav").unlink()
        tmp_voice_path.with_suffix(".ogg").unlink()
        return output
