from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


def dict(self) -> dict:
    return {key: value for key, value in self.__dict__.items() if key in self.__table__.columns}


BaseModel.dict = dict
