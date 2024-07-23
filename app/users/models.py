from datetime import datetime
import uuid

from sqlalchemy import Column, String
import sqlalchemy.dialects.postgresql as pg

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(pg.UUID, primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=True, default=None)
    created_at = Column(pg.TIMESTAMP, default=datetime.now)
    updated_at = Column(pg.TIMESTAMP, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return self.username
