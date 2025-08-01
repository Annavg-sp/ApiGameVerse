from sqlmodel import SQLModel, Field

class API_Keys(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    api_key: str
    role: str
