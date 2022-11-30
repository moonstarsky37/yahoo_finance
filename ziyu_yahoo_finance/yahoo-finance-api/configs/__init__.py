#!/usr/bin/python3
from functools import lru_cache

from pydantic import BaseSettings, BaseModel

# from configs.db import DbSettings
from configs.db import DBSettings

class Setting(BaseModel):
    db: DBSettings


class Settings(BaseSettings):
    mode: str
    v0: Setting

    class Config:
        env_prefix: str = 'APP_'
        env_nested_delimiter: str = '_'


@lru_cache
def settings() -> Settings:
    return Settings()


if __name__ == '__main__':
    settings = Settings()
    print(settings)


