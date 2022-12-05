from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


def as_dict(self) -> dict:
    return {key: value for key, value in self.__dict__.items() if key in self.__table__.columns}


BaseModel.as_dict = as_dict
