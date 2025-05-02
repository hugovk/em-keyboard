"""
CLI for em
"""

from __future__ import annotations

import argparse
import os
import random

from em import __version__

CUSTOM_EMOJI_PATH = os.path.join(os.path.expanduser("~/.emojis.json"))

EmojiDict = dict[str, list[str]]


def try_copy_to_clipboard(text: str) -> bool:
    try:
        import pyperclip  # type: ignore[import]
    except ModuleNotFoundError:
        pyperclip = None
        try:
            import xerox  # type: ignore[import]
        except ModuleNotFoundError:
            return False
    copier = pyperclip if pyperclip else xerox
    copier_error = pyperclip.PyperclipException if pyperclip else xerox.ToolNotFound
    try:
        copier.copy(text)
    except copier_error:
        return False
    return True


def parse_emojis(filename: str | None = None) -> EmojiDict:
    import json

    if filename is None:
        from importlib.resources import files

        emoji_traversable = files("em").joinpath("emojis.json")
        return json.loads(emoji_traversable.read_text("utf-8"))

    with open(filename, encoding="utf-8") as f:
        return json.load(f)


def translate(lookup: EmojiDict, code: str) -> str | None:
    if code[0] == ":" and code[-1] == ":":
        code = code[1:-1]

    for emoji, keywords in lookup.items():
        if code == keywords[0]:
            return emoji
    return None


def do_find(lookup: EmojiDict, terms: tuple[str, ...]) -> list[tuple[str, str]]:
    """Match terms against keywords."""
    assert terms, "at least one search term required"
    return [
        (keywords[0], emoji)
        for emoji, keywords in lookup.items()
        if all(any(term in kw for kw in keywords) for term in terms)
    ]


def clean_name(name: str) -> str:
    """Clean emoji name replacing specials chars by underscore"""
    return name.replace("-", "_").replace(" ", "_").lower()


def parse_args(arg_list: list[str] | None):
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
    args = parser.parse_args(arg_list)
    return args


def search_emoji(lookup: dict, name: str) -> list | None:
    """
    Searches emojis by keyword and returns matching (name, emoji) pairs.

    Args:
        lookup(dict): Dict that contains pairs of emoji and their keywords
        name(str): Name of keyword that user search

    Returns:
        list[tuple[str, str]]: List of (emoji_name, emoji_symbol) pairs.


    Example:
        search_emoji(lookup, "stone")
        [('curling_stone', '🥌'), ('gem_stone', '💎'), ('moai', '🗿')]


        search_emoji(lookup, "gawfgsah")
        None
    """

    names = tuple(map(clean_name, name))
    found = do_find(lookup, names)
    if len(found) == 0:
        return None
    else:
        return found



def pick_random_emoji(emoji_pool: list | dict) -> tuple:
    """
    Returns random emoji and its keyword from the given pool

    Args:
        emoji_pool(list | dict): pool of emojis.

    Returns:
        tuple[str, str]: Random pair (emoji, keyword) from emoji pool.
    """

    if isinstance(emoji_pool, list):
        keyword, emoji = random.choice(emoji_pool)
    else:
        emoji, keywords = random.choice(list(emoji_pool.items()))
        keyword = keywords[0]

    return emoji, keyword


def make_search_msg(emojis_meta: list, is_copied: bool) -> str:
    """
    Returns string to print to user.

    Args:
        emojis_meta: List of tuples that contains info about emoji like:
        [('paw_prints', '🐾'), ('chess_pawn', '♟️')]

        is_copied: If True adds to message "Emoji {..} copied!"

    Returns:
         String that will be printed to user
    """

    res = ""
    for emoji_meta in emojis_meta:
        keyword, emoji = emoji_meta
        line = f"{emoji} {keyword}\n"
        res += line

    return res.strip() + f"\nEmoji {res[0]} copied!" if is_copied else res.strip()


def main(arg_list: list[str] | None = None):
    """
    Returns final string to be printed to user depending on what args user entered.

    Args:
        arg_list: List of args that user entered while called em-keyboard.

    Returns:
        String with message to user.
    """

    args = parse_args(arg_list)

    if (not args.name) and ((not args.random) or (args.random and args.search)):
        return "ERROR: the 'name' argument is required"

    lookup = parse_emojis()

    if os.path.isfile(CUSTOM_EMOJI_PATH):
        lookup.update(parse_emojis(CUSTOM_EMOJI_PATH))


    if args.search and args.random:
        search_result = search_emoji(lookup, args.name)
        if search_result:
            emoji, keyword = pick_random_emoji(search_result)
            is_copied = try_copy_to_clipboard(search_result[0][1])

            return f"{emoji} {keyword}\nEmoji {emoji} copied!" if is_copied \
              else f"{emoji} {keyword}\nEmoji found but not copied"


    if args.search:
        search_result = search_emoji(lookup, args.name)

        if search_result is None:
            return "Emoji not found :("

        if len(search_result) == 1 and not args.no_copy:
            is_copied = try_copy_to_clipboard(search_result[0][1])

            return make_search_msg(search_result, is_copied)
        else:
            return make_search_msg(search_result, is_copied=False)


    if args.random:
        emoji, keyword = pick_random_emoji(lookup)
        is_copied = try_copy_to_clipboard(emoji)

        return f"{emoji} {keyword}\nEmoji {emoji} copied!" if is_copied \
          else f"{emoji} {keyword}\nEmoji found but not copied"


if __name__ == "__main__":
    print(main())

