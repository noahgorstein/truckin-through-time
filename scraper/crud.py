import datetime

from sqlalchemy import Engine
from sqlmodel import Session, select

from .models import Concert, Setlist, SetlistSong, Song, Venue
from .schema import SetlistSongData


def create_or_get_venue(
    engine: Engine, name: str, city: str, state: str, country: str
) -> int:
    """Create or get a venue and return its ID."""
    with Session(engine) as session:
        statement = select(Venue).where(
            Venue.name == name, Venue.country == country, Venue.city == city
        )
        result = session.exec(statement).first()
        if result and result.id:
            return result.id

        venue = Venue(name=name, city=city, state=state, country=country)
        session.add(venue)
        session.commit()
        session.refresh(venue)
        # id could technically be None
        if venue.id is not None:
            return venue.id
        raise ValueError("Failed to create or get a valid venue ID.")


def create_or_get_concert(
    engine: Engine, venue_id: int, concert_date: datetime.date
) -> int:
    """Create or get a concert and return its ID."""
    with Session(engine) as session:
        statement = select(Concert).where(
            Concert.venue_id == venue_id, Concert.date == concert_date
        )
        result = session.exec(statement).first()
        if result and result.id:
            return result.id
        concert = Concert(venue_id=venue_id, date=concert_date)
        session.add(concert)
        session.commit()
        session.refresh(concert)
        if concert.id is not None:
            return concert.id
        raise ValueError("Failed to create or get a valid concert ID.")


def create_or_get_song(engine: Engine, title: str) -> int:
    """Create or get a song and return its ID."""
    with Session(engine) as session:
        statement = select(Song).where(Song.title == title)
        result = session.exec(statement).first()
        if result and result.id:
            return result.id

        song = Song(title=title)
        session.add(song)
        session.commit()
        session.refresh(song)
        if song.id is not None:
            return song.id
        raise ValueError("Failed to create or get a valid song ID.")


def create_setlist(engine: Engine, concert_id: int, notes: str) -> int:
    """Create a setlist for a specified concert and return the setlist ID."""
    with Session(engine) as session:
        setlist = Setlist(concert_id=concert_id, notes=notes)
        session.add(setlist)
        session.commit()
        session.refresh(setlist)
        if setlist.id is not None:
            return setlist.id
        raise ValueError("Failed to create or get a valid setlist ID.")


def add_songs_to_setlist(engine: Engine, setlist_id: int, songs: list[SetlistSongData]):
    """Add songs to the setlist given its ID."""
    with Session(engine) as session:
        for song in songs:
            song_id = create_or_get_song(engine=engine, title=song.title)
            setlist_song = SetlistSong(
                setlist_id=setlist_id,
                song_id=song_id,
                order=song.order,
                transition=song.transition,
            )
            session.add(setlist_song)
        session.commit()
