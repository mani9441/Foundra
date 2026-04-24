import os


class Settings:
    APP_NAME = "Phase4 Business Model Engine"

    REQUEST_TIMEOUT = 12
    SEARCH_RESULTS_LIMIT = 5
    MAX_CONTENT_CHARS = 5000

    DEFAULT_RETRIES = 2

    USER_AGENT = (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122 Safari/537.36"
    )

    LOG_LEVEL = "INFO"

    DATA_DIR = os.path.join(os.getcwd(), "runtime_data")
    LOG_DIR = os.path.join(DATA_DIR, "logs")


settings = Settings()