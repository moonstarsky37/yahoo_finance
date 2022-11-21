from functools import lru_cache

from pydantic import BaseSettings, BaseModel

from db import DbSettings


class Setting(BaseModel):
    db: DbSettings


class Settings(BaseSettings):
    v0: Setting

    class Config:
        env_prefix: str = 'APP_'
        env_nested_delimiter: str = '__'


@lru_cache
def settings() -> Settings:
    return Settings()


if __name__ == '__main__':
    settings = Settings()
    print(settings)
