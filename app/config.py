from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    openai_api_key: str | None = Field(default=None, alias='OPENAI_API_KEY')
    pageindex_api_key: str | None = Field(default=None, alias='PAGEINDEX_API_KEY')
    llm_model: str = Field(default='gpt-4.1-mini', alias='LLM_MODEL')
    use_mock_pageindex: bool = Field(default=True, alias='USE_MOCK_PAGEINDEX')
    max_retries: int = Field(default=2, alias='MAX_RETRIES')
    log_level: str = Field(default='INFO', alias='LOG_LEVEL')


@lru_cache
def get_settings() -> Settings:
    return Settings()
