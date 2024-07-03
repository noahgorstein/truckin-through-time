"""Not to be confused with models.py which is used for database models."""

from pydantic import BaseModel, Field


class TouringYear(BaseModel):
    year: str
    relative_url: str
    concerts: list["ConcertData"] | None = Field(default_factory=list)


class ConcertData(BaseModel):
    touring_year: TouringYear
    name: str
    relative_url: str


class SetlistSongData(BaseModel):
    title: str
    order: int
    transition: bool
