from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"
    embedding_model: str = "all-MiniLM-L6-v2"
    data_dir: str = "data"
    chunk_size: int = 180
    chunk_overlap: int = 30
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
