from pydantic import BaseSettings, Field

class DBSettings(BaseSettings):
    dsn: str = Field(
        title="DB連線資訊",
        description="DB server",
        # env="DB_DSN"
    )

    class Config:
        env_file: str
        env_file_encoding: str
        # env_prefix: str = "DB"

