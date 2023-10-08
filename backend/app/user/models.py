from app.api.models import BareBaseModel
from sqlalchemy import Boolean, Column, String, DateTime

# Read more here:
# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-sqlalchemy-models-from-the-base-class


class User(BareBaseModel):
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String, default='guest')
    last_login = Column(DateTime)
