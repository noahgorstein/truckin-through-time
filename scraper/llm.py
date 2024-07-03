import datetime
import json
import logging

from httpx import ConnectError
from ollama import Client as OllamaClient

from .prompts import PARSE_CONCERT_PROMPT, PARSE_SETLIST_PROMPT

logger = logging.getLogger(__name__)


class LLMParseError(Exception):
    """Represents an error that occurred while the LLM was trying parse and extract information
    out of some given text.
    """

    def __init__(self, msg):
        super().__init__(msg)


class Client:
    """
    A client to interact with the LLM served by Ollama for parsing concert and setlist information.
    """

    def __init__(self, ollama_host: str, model: str):
        self.model = model
        self.ollama_url = ollama_host
        self.client = OllamaClient(host=ollama_host)
        self._validate_config()

    def _validate_config(self):
        """
        Validates the availability of the Ollama server.
        """
        try:
            self.client.list()
        except ConnectError:
            raise RuntimeError(
                f"Failed to establish a connection to the Ollama server running on {self.ollama_url}"
            )

    def _chat_with_llm(self, prompt: str, prompt_formatters: dict[str, str]) -> dict:
        try:
            completion = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a text extraction assistant. You will be helping me parse concert"
                            " and setlist information from text files."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt.format(**prompt_formatters),
                    },
                ],
                format="json",
            )
            content = completion["message"]["content"]
            return json.loads(content)
        except json.JSONDecodeError:
            raise LLMParseError(
                f"LLM did not return valid JSON: {completion['message']['content']}"
            )
        except Exception as e:
            raise LLMParseError(str(e))

    def parse_setlist(self, setlist: str) -> tuple[list[dict], str]:
        message = self._chat_with_llm(
            prompt=PARSE_SETLIST_PROMPT, prompt_formatters={"setlist": setlist}
        )
        songs = message.get("songs", [])
        notes = message.get("notes", "")
        return songs, notes

    def parse_concert_name(
        self, concert: str
    ) -> tuple[str, str, str, str, datetime.date]:
        message = self._chat_with_llm(
            prompt=PARSE_CONCERT_PROMPT, prompt_formatters={"concert": concert}
        )
        venue = message.get("venue", "")
        city = message.get("city", "")
        state = message.get("state", "")
        country = message.get("country", "")
        concert_date_str = message.get("date", "")
        concert_date = datetime.datetime.strptime(concert_date_str, "%m/%d/%Y").date()
        return venue, city, state, country, concert_date
