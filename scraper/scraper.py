import logging
import sys

import requests
from bs4 import BeautifulSoup
from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

from .crud import (
    add_songs_to_setlist,
    create_or_get_concert,
    create_or_get_venue,
    create_setlist,
)
from .llm import Client, LLMParseError
from .schema import ConcertData, SetlistSongData, TouringYear

ROOT_URL = "https://www.cs.cmu.edu/~mleone/gdead/"
logger = logging.getLogger(__name__)


def get_touring_years() -> list[TouringYear]:
    logger.info("Fetching yearly setlists...")
    response = requests.get(f"{ROOT_URL}/setlists.html")
    if not response.ok:
        logger.fatal(f"Unable to yearly setlists. Status Code: {response.status_code}")
        sys.exit(1)
    soup = BeautifulSoup(response.text, "html.parser")
    touring_year_links = soup.find_all("ul")[1].find_all("a")

    touring_years = [
        TouringYear(year=link.text, relative_url=link["href"])
        for link in touring_year_links
    ]
    for touring_year in touring_years:
        logger.info(f"Getting setlists for {touring_year.year}")
        url = f"{ROOT_URL}/{touring_year.relative_url}"
        response = requests.get(url)
        if not response.ok:
            logger.fatal(
                f"Unable to get setlists for year {touring_year.year}. Status Code: {response.status_code}"
            )
            sys.exit(1)
        soup = BeautifulSoup(response.text, "html.parser")
        concert_links = soup.find_all("ul")[0].find_all("a")
        setlists = [
            ConcertData(
                touring_year=touring_year,
                name=link.text.strip(),
                relative_url=link["href"],
            )
            for link in concert_links
        ]

        touring_year.concerts = setlists
    return touring_years


def create_database_and_tables(filename: str = "database.db") -> Engine:
    engine = create_engine(f"sqlite:///{filename}")
    SQLModel.metadata.create_all(engine)
    return engine


def create_concert_setlist(
    engine: Engine, concert_id: int, setlist_songs: list[SetlistSongData], notes: str
):
    setlist_id = create_setlist(engine=engine, concert_id=concert_id, notes=notes)
    add_songs_to_setlist(engine=engine, setlist_id=setlist_id, songs=setlist_songs)


def parse_song_data_from_setlist(
    setlist_relative_url: str,
    client: Client,
) -> tuple[list[SetlistSongData], str]:
    url = f"{ROOT_URL}/{setlist_relative_url}"
    response = requests.get(url)

    raw_setlist = response.text
    songs, notes = client.parse_setlist(raw_setlist)
    setlist_songs: list[SetlistSongData] = []

    for song in songs:
        title = song.get("title")
        order = song.get("order")
        if title and isinstance(title, str) and order and isinstance(order, int):
            setlist_song = SetlistSongData(
                title=title,
                order=order,
                transition=song.get("transition", False),
            )
            setlist_songs.append(setlist_song)
    return setlist_songs, notes


def fetch_and_process_concert_data(client: Client, database_file: str):
    engine = create_database_and_tables(filename=database_file)
    touring_years = get_touring_years()
    for touring_year in touring_years:
        _process_touring_year(engine=engine, client=client, touring_year=touring_year)


def _process_touring_year(engine: Engine, client: Client, touring_year: TouringYear):
    if not touring_year.concerts:
        logger.warn(f"No concerts for {touring_year.year}. Nothing to process.")
        return

    for concert in touring_year.concerts:
        logger.info(f"Processing {concert.name}")
        _process_concert(engine=engine, client=client, concert=concert)


def _process_concert(engine: Engine, client: Client, concert: ConcertData):
    try:
        venue, city, state, country, concert_date = client.parse_concert_name(
            concert.name
        )
    except LLMParseError as e:
        logger.error(
            f"Unable to parse concert data for {concert.name}. {str(e)}", exc_info=True
        )
        return

    venue_id = create_or_get_venue(engine, venue, city, state, country)
    concert_id = create_or_get_concert(engine, venue_id, concert_date)

    try:
        setlist_songs, notes = parse_song_data_from_setlist(
            setlist_relative_url=concert.relative_url, client=client
        )
    except LLMParseError as e:
        logger.error(f"Unable to parse setlist for {concert.name}. {str(e)}")
        return
    create_concert_setlist(engine, concert_id, setlist_songs, notes)
