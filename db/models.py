from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String, Enum, Boolean, DateTime
from db.database import Base
from sqlalchemy import Column, ForeignKey

from db.enums import Role


class DbUser(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True, index=True)
  username = Column(String(150))
  email = Column(String(150))
  password = Column(String(150))
  role = Column(Enum(Role), server_default='USER')
  tokens = relationship("Token", back_populates="user")


class Token(Base):
  __tablename__='token'
  id = Column(Integer, primary_key=True, index=True)
  access_token = Column(String(150), unique=True, index=True, nullable=False)
  refresh_token = Column(String(150), unique=True, index=True, nullable=False)
  expires_at = Column(DateTime, nullable=False)
  created_at = Column(DateTime, nullable=False)
  revoked = Column(Boolean, default=False)
  user_id = Column(Integer, ForeignKey("users.id"))
  user = relationship("DbUser", back_populates="tokens")