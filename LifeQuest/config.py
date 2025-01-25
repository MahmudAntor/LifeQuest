import configparser
import os

class Config:

    @staticmethod
    def load_config(file_name):
        config_path = os.path.join("configs", file_name)
        config = configparser.ConfigParser()
        config.read(config_path)
        return config

    # LLM Configurations
    LLM_CONFIG = load_config("llm_config.ini")
    LLM_API_KEY = LLM_CONFIG.get("llm", "api_key", fallback="default_api_key")
    LLM_API_URL = LLM_CONFIG.get("llm", "api_url", fallback="https://default-provider.com/api/v1/completions")
    LLM_MODEL = LLM_CONFIG.get("llm", "model", fallback="default_model")
    LLM_TIMEOUT = LLM_CONFIG.getint("llm", "request_timeout", fallback=10)
