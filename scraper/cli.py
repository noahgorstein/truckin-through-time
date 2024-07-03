import logging

import click

from .llm import Client
from .logger import setup_logging
from .scraper import fetch_and_process_concert_data

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--ollama-host",
    envvar="OLLAMA_HOST",
    default="http://localhost:11434",
    show_default=True,
    help="Where Ollama is running",
)
@click.option(
    "--ollama-model",
    envvar="OLLAMA_MODEL",
    default="llama3",
    show_default=True,
    help="The model hosted by --ollama-host that will be used to extract information.",
)
@click.option(
    "--database",
    default="database.db",
    show_default=True,
    help="The name of the sqlite database that will be created in the cwd.",
)
def scrape(ollama_host, ollama_model, database):
    setup_logging()
    client = Client(ollama_host=ollama_host, model=ollama_model)
    fetch_and_process_concert_data(client=client, database_file=database)
