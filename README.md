# Truckin' Through Time: Building a Grateful Dead Setlist Database

This repository contains the source code for creating a Grateful Dead setlist database, as described in my [associated blog post](https://noahgorstein.com/blog/truckin-through-time).

## Prerequisites

- Python
- [Ollama](https://ollama.com/)

## Installation

To install the package, run:

```sh
pip install .
```

## Running the Scraper

After installation, the `scrape` script will be available in your shell. You can use it to scrape and build the database. To see the available options, use the `--help` flag:

```sh
❯ scrape --help
Usage: scrape [OPTIONS]

Options:
  --ollama-host TEXT   Specify where Ollama is running. Default: http://localhost:11434
  --ollama-model TEXT  Specify the model hosted by --ollama-host that will be used to extract information. Default: llama3
  --database TEXT      Specify the name of the SQLite database to be created in the current working directory. Default: database.db
  --help               Show this message and exit.
```

For more information, please refer to the [blog post](https://noahgorstein.com/blog/truckin-through-time).
