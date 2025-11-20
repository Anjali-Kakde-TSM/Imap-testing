import os
from dotenv import load_dotenv

load_dotenv()  

def env(key: str):
    value = os.getenv(key)
    if not value:
        raise Exception(f"Missing environment variable: {key}")
    return value
