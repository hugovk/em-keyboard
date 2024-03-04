"""em: the technicolor cli emoji keyboard

Examples:

  $ em sparkle shortcake sparkles
  $ em red_heart

  $ em -s food

Notes:
  - If all names provided map to emojis, the resulting emojis will be
    automatically added to your clipboard.
  - ✨ 🍰 ✨  (sparkles shortcake sparkles)
"""
from __future__ import annotations

import argparse
import importlib.metadata
import itertools
import json
import os
import random
import re
import sys

__version__: str = importlib.metadata.version("em_keyboard")

if sys.version_info >= (3, 9):
    from functools import cache

    EmojiDict = dict[str, list[str]]
else:
    from functools import lru_cache as cache

    EmojiDict = "dict[str, list[str]]"

try:
    from importlib.resources import as_file, files

    with as_file(files("em_keyboard").joinpath("emojis.json")) as em_json:
        EMOJI_PATH = em_json
except ImportError:
    from importlib.resources import path

    with path("em_keyboard", "emojis.json") as em_json:
        EMOJI_PATH = em_json

CUSTOM_EMOJI_PATH = os.path.join(os.path.expanduser("~/.emojis.json"))


@cache
def get_copier():
    try:
        import pyperclip as copier  # type: ignore[import]
    except ImportError:
        try:
            import xerox as copier  # type: ignore[import]
        except ImportError:
            copier = None

    return copier


def parse_emojis(filename: str | os.PathLike[str] = EMOJI_PATH) -> EmojiDict:
    return json.load(open(filename, encoding="utf-8"))


def translate(lookup: EmojiDict, code: str) -> list[str] | list[None]:
    output = []
    if code[0] == ":" and code[-1] == ":":
        code = code[1:-1]

    for emoji, keywords in lookup.items():
        if code == keywords[0]:
            output.append(emoji)
            break
    else:
        return [None]

    return output


def do_find(lookup: EmojiDict, term: str) -> list:
    """Match term against keywords."""
    output = []
    seen = set()

    for emoji, keywords in lookup.items():
        for keyword in keywords:
            if term in keyword and emoji not in seen:
                output.append((keywords[0], emoji))
                seen.add(emoji)

    return output


def clean_name(name: str) -> str:
    """Clean emoji name replacing specials chars by underscore"""
    special_chars = "[-. ]"  # square brackets are part of the regex
    return re.sub(special_chars, "_", name).lower()


def cli() -> None:
    # CLI argument parsing.
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("name", nargs="*", help="Text to convert to emoji")
    parser.add_argument("-s", "--search", action="store_true", help="Search for emoji")
    parser.add_argument("-r", "--random", action="store_true", help="Get random emoji")
    parser.add_argument(
        "--no-copy", action="store_true", help="Does not copy emoji to clipboard"
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()
    no_copy = args.no_copy

    # Grab the lookup dictionary.
    lookup = parse_emojis()

    if os.path.isfile(CUSTOM_EMOJI_PATH):
        lookup.update(parse_emojis(CUSTOM_EMOJI_PATH))

    if args.random:
        emoji, keywords = random.choice(list(lookup.items()))
        name = keywords[0]
        if not no_copy and (copier := get_copier()):
            copier.copy(emoji)
            print(f"Copied! {emoji}  {name}")
        else:
            print(f"{emoji}  {name}")
        sys.exit(0)

    if not args.name:
        sys.exit("Error: the 'name' argument is required")

    names = tuple(map(clean_name, args.name))

    # Marker for if the given emoji isn't found.
    missing = False

    # Search mode.
    if args.search:
        # Lookup the search term.
        found = do_find(lookup, names[0])

        # print them to the screen.
        for name, emoji in found:
            # Some registered emoji have no value.
            try:
                # Copy the results (and say so!) to the clipboard.
                if not no_copy and len(found) == 1 and (copier := get_copier()):
                    copier.copy(emoji)
                    print(f"Copied! {emoji}  {name}")
                else:
                    print(f"{emoji}  {name}")

            # Sometimes, an emoji will have no value.
            except TypeError:
                pass

        if len(found):
            sys.exit(0)
        else:
            sys.exit(1)

    # Process the results.
    results = (translate(lookup, name) for name in names)
    results = list(itertools.chain.from_iterable(results))

    if None in results:
        no_copy = True
        missing = True
        results = (r for r in results if r)

    # Prepare the result strings.
    print_results = " ".join(results)
    results = "".join(results)

    # Copy the results (and say so!) to the clipboard.
    if not no_copy and not missing and (copier := get_copier()):
        copier.copy(results)
        print(f"Copied! {print_results}")

    # Script-kiddies.
    else:
        print(print_results)

    sys.exit(int(missing))


if __name__ == "__main__":
    cli()
