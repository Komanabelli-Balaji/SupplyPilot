from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set")

os.environ["GOOGLE_API_KEY"] = api_key
MODEL = os.getenv("MODEL")
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL")