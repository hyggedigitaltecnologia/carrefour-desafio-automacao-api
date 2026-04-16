import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://serverest.dev")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
