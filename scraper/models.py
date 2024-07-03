from datetime import date

from sqlmodel import Field, Relationship, SQLModel


class Concert(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    venue_id: int = Field(default=None, foreign_key="venue.id")
    date: date
    setlists: list["Setlist"] = Relationship(back_populates="concert")


class Venue(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    city: str
    state: str | None
    country: str


class Song(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    setlists: list["SetlistSong"] = Relationship(back_populates="song")


class Setlist(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    concert_id: int = Field(default=None, foreign_key="concert.id")
    concert: Concert = Relationship(back_populates="setlists")
    setlist_songs: list["SetlistSong"] = Relationship(back_populates="setlist")
    notes: str


class SetlistSong(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    setlist_id: int = Field(default=None, foreign_key="setlist.id")
    song_id: int = Field(default=None, foreign_key="song.id")
    song: Song = Relationship(back_populates="setlists")
    setlist: Setlist = Relationship(back_populates="setlist_songs")
    order: int
    transition: bool
