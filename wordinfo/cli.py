import inflect
import requests
import random
import time

from sys import argv
from typing import Sequence
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning


class NoDefinitionFoundException(requests.RequestException):
    """See https://github.com/meetDeveloper/freeDictionaryAPI/blob/4f274a853dd7a352aa2a349d1b92624ff18a36a8/modules/errors.js#L2"""

    pass


def define(words: list[str], language_code: str | None) -> dict[str, str]:
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


def parse_arguments(
    args: Sequence[str],
) -> tuple[list[str], dict[str, str | bool]]:
    """Parse arguments.

    Keyword arguments must follow positional arguments.

    Flag arguments are treated as keyword arguments, with a value of `True`.

    Keyword arguments and flags are a dictionary, i.e., duplicate kwargs are silently ignored.

    ### Parameters
    - :param `Sequence[str]` `args`: List of arguments.

    ### Returns
    :return: Tuple containing positional arguments and keyword arguments, respectively.
    :rtype: `tuple[list[str], dict[str, str | bool]]`
    """
    keyword_args: dict[str, str | bool] = dict()
    positional_args: list[str] = list()

    is_processing_keyword_args = False
    last_keyword_arg = ""

    for arg in args[1:]:
        # Consume keyword args
        if arg.startswith("-"):
            is_processing_keyword_args = True

            if arg.startswith("--"):
                keyword_args[arg] = ""
                last_keyword_arg = arg
            else:  # arg starts with only '-'
                keyword_args[arg] = True

            continue

        # Consume arguments passed to keyword args
        if is_processing_keyword_args:
            if (val := keyword_args[last_keyword_arg]) and isinstance(val, str):
                val += f" {arg}"
            else:
                val = arg

            keyword_args[last_keyword_arg] = val
            continue

        # Consume positional args
        positional_args.append(arg)

    return positional_args, keyword_args


def usage():
    print(
        """usage:
  wordinfo define <words>... [--language <language_code>]
  wordinfo plural <word>
  wordinfo indefinite <noun>
  wordinfo ordinal <number>
"""
    )


def main():
    positional_args, keyword_args = parse_arguments(argv)

    """
    >>> print(f"{positional_args = }")
    >>> print(f"{keyword_args = }")

    $ poetry run wordinfo positional1 positional2 --fullname cameron ball --username camball --password password

    positional_args = ['positional1', 'positional2']
    keyword_args = {'--fullname': 'cameron ball', '--username': 'camball', '--password': 'password'}
    """

    disable_warnings(InsecureRequestWarning)
    random.seed(time.time())

    # Match on the subcommand, e.g., `$ wordinfo define dog` runs the `define` subcommand
    match positional_args[0]:
        case "define":
            if not positional_args[1:]:
                print("At least one word is required to define.")
                return

            language_code = keyword_args.get("--language")
            if isinstance(language_code, bool) or (
                "--language" in keyword_args.keys() and not language_code
            ):
                print("`--language` requires a language code to be specified.")
                return

            definitions = define(positional_args[1:], language_code)

            formatted_definitions = "\n\n".join(
                [f"{word}: {definition}" for word, definition in definitions.items()]
            )
            print(formatted_definitions)

        case "plural":
            try:
                print(plural(positional_args[1]))
            except IndexError:
                usage()
        case "indefinite":
            try:
                print(with_indefinite_article(positional_args[1]))
            except IndexError:
                usage()
        case "ordinal":
            try:
                print(ordinal(positional_args[1]))
            except IndexError:
                usage()
        case _:
            usage()
