from pydantic import BaseModel, PostgresDsn


class DbSettings(BaseModel):
    dsn: PostgresDsn
