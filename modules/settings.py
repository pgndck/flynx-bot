import os

from dotenv import load_dotenv
from typing import Optional

load_dotenv(".env")


class Settings:
    OPENAI_KEY = str(os.getenv("OPENAI_KEY", ""))
    TELEGRAM_BOT_TOKEN = str(os.getenv("TELEGRAM_BOT_TOKEN", ""))
    ADMINS = [62020038]
    ADMIN_GROUP = -4087837707
