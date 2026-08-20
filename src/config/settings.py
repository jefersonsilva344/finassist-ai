import os

from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")


if not OPENAI_API_KEY:
    raise RuntimeError(
        "A variável OPENAI_API_KEY não foi configurada."
    )


if not OPENAI_MODEL:
    raise RuntimeError(
        "A variável OPENAI_MODEL não foi configurada."
    )