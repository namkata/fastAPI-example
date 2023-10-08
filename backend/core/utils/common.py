from typing import Optional
from passlib.context import CryptContext

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CommonQueryParams:
    def __int__(self,
                search: Optional[str] = None,
                page: Optional[int] = None,
                limit: Optional[int] = None,
                to_sorted: Optional[str] = None,
                fields: Optional[str] = None,
                from_page: Optional[int] = None,
                to_page: Optional[int] = None
                ):
        self.search = search
        self.page = page
        self.limit = limit
        self.to_sorted = to_sorted
        self.fields = fields
        self.from_page = from_page
        self.to_page = to_page


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
