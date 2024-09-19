import inflect
import requests
import random
import time

from docopt import docopt
from typing import Iterable, Sequence
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning


class NoDefinitionFoundException(requests.RequestException):
    """See https://github.com/meetDeveloper/freeDictionaryAPI/blob/4f274a853dd7a352aa2a349d1b92624ff18a36a8/modules/errors.js#L2"""

    pass


def define(words: Iterable[str], language_code: str | None) -> dict[str, str]:
    definitions: dict[str, str] = dict()

    if language_code is None:
        language_code = "en"

    for word in words:
        resp = requests.get(
            f"https://api.dictionaryapi.dev/api/v2/entries/{language_code}/{word}",
            verify=False,
        )
        if not isinstance(resp.json(), list):
            raise NoDefinitionFoundException("Bad response")

        try:
            definitions[word] = (
                resp.json()[0]
                .get("meanings")[0]
                .get("definitions")[0]
                .get("definition")
            )
        except IndexError:
            raise ValueError("Bad response") from None

        # Simulate a really long API call...
        time.sleep(random.random())

    return definitions


def plural(word: str) -> str:
    inf = inflect.engine()
    time.sleep(random.random())  # Simulate long processing time...
    return inf.plural(word)  # type: ignore


def with_indefinite_article(word: str) -> str:
    inf = inflect.engine()
    time.sleep(random.random())  # Simulate long processing time...
    return inf.a(word)  # type: ignore


def ordinal(number: str | int) -> str:
    inf = inflect.engine()
    time.sleep(random.random())  # Simulate long processing time...
    return inf.ordinal(number)  # type: ignore


USAGE = """Word Information

Usage:
    wordinfo define <words>... [--language <language_code>]
    wordinfo plural <word>
    wordinfo indefinite <noun>
    wordinfo ordinal <number>
    wordinfo (-h | --help)

Options:
    -h --help                    Show this help message.
    --language <language_code>   Specify a language code.
"""


def main():
    arguments = docopt(USAGE)

    disable_warnings(InsecureRequestWarning)
    random.seed(time.time())

    if arguments.get("define"):
        words = arguments.get("<words>")
        if not words:
            print("At least one word is required to define.")
            return

        language_code = arguments.get("--language")
        if arguments.get("--language") and not language_code:
            print("`--language` requires a language code to be specified.")
            return

        definitions = define(words, language_code)

        formatted_definitions = "\n\n".join(
            [f"{word}: {definition}" for word, definition in definitions.items()]
        )
        print(formatted_definitions)

    elif arguments.get("plural"):
        try:
            print(plural(arguments.get("<word>")))  # type: ignore
        except IndexError:
            print(USAGE)
    elif arguments.get("indefinite"):
        try:
            print(with_indefinite_article(arguments.get("<noun>")))  # type: ignore
        except IndexError:
            print(USAGE)
    elif arguments.get("ordinal"):
        try:
            print(ordinal(arguments.get("<number>")))  # type: ignore
        except IndexError:
            print(USAGE)
    else:
        print(USAGE)
