"""
CLI for em
"""

from __future__ import annotations

import argparse
import os
import random
import sys

from em import __version__

CUSTOM_EMOJI_PATH = os.path.join(os.path.expanduser("~/.emojis.json"))

EmojiDict = dict[str, list[str]]

# I think we can add it for prod version
# (it makes an errors more user-friendly)
sys.tracebacklimit = 0


class ArgumentNotProvided(Exception):
    def __str__(self):
        return "The 'name' argument is required"


class EmojiNotFound(Exception):
    def __init__(self, emoji_name, additional = ""):
        self.emoji_name = emoji_name
        self.additional = additional

    def __str__(self):
        return f"Emoji '{self.emoji_name}' not found :(" + self.additional


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


def do_find(lookup: EmojiDict, terms: tuple[str, ...]) -> list[tuple[str, str]]:
    """Match terms against keywords."""
    assert terms, "at least one search term required"
    return [
        (keywords[0], emoji)
        for emoji, keywords in lookup.items()
        if all(any(term in kw for kw in keywords) for term in terms)
    ]


def clean_name(name: str) -> str:
    """Clean emoji names"""
    if name[0] == ":" and name[-1] == ":":
        name = name[1:-1]

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


def search_emoji(lookup: dict, names: str | tuple) -> list | None:
    """
    Searches emojis by keyword and returns matching (name, emoji) pairs.

    Args:
        lookup(dict): Dict that contains pairs of emoji and their keywords
        names(str | tuple): Name of keyword that user search

    Returns:
        list[tuple[str, str]]: List of (emoji_name, emoji_symbol) pairs.


    Example:
        search_emoji(lookup, "stone")
        [('curling_stone', '🥌'), ('gem_stone', '💎'), ('moai', '🗿')]


        search_emoji(lookup, "gawfgsah")
        None
    """

    names = tuple(map(clean_name, names))
    found = do_find(lookup, names)
    if len(found) == 0:
        return None
    else:
        return found


def hard_search_emoji(lookup: dict, name:tuple | str) -> tuple:
    """
    Returns random emoji and its keyword from the given pool
    (more accurate than search_emoji func).

    Args:
        lookup(dict): Dict that contains pairs of emoji and their keywords
        name(str | tuple): Name of keyword that user search

    Returns:
        list[tuple[str, str]]: List of (emoji_name, emoji_symbol) pairs.
    """
    results = tuple(r for r in name if r is not None)
    search_result = search_emoji(lookup, results)
    for res in search_result:
        if res[0] in name:
            return res[0], res[1]


def pick_random_emoji(emoji_pool: list | dict) -> tuple:
    """
    Returns random emoji and its keyword from the given pool.

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

        is_copied: If True adds to message "Emoji {...} copied!"

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

    name = tuple(map(clean_name, args.name))

    if (not name) and ((not args.random) or (args.random and args.search)):
        raise ArgumentNotProvided

    lookup = parse_emojis()

    if os.path.isfile(CUSTOM_EMOJI_PATH):
        lookup.update(parse_emojis(CUSTOM_EMOJI_PATH))


    #Used em -sr:
    if args.search and args.random:
        search_result = search_emoji(lookup, name)
        if search_result:
            emoji, keyword = pick_random_emoji(search_result)
            is_copied = try_copy_to_clipboard(search_result[0][1])

            return f"{emoji} {keyword}\nEmoji {emoji} copied!" if is_copied \
              else f"{emoji} {keyword}\nEmoji found but not copied"


    #Used em -s:
    if args.search:
        search_result = search_emoji(lookup, name)

        if search_result is None:
            raise EmojiNotFound("".join(name))

        if len(search_result) == 1 and not args.no_copy:
            is_copied = try_copy_to_clipboard(search_result[0][1])

            return make_search_msg(search_result, is_copied)
        else:
            return make_search_msg(search_result, is_copied=False)


    #Used em -r:
    if args.random:
        emoji, keyword = pick_random_emoji(lookup)
        is_copied = try_copy_to_clipboard(emoji)

        return f"{emoji} {keyword}\nEmoji {emoji} copied!" if is_copied \
          else f"{emoji} {keyword}\nEmoji found but not copied"


    # If user don't enter args at all:
    search_result = hard_search_emoji(lookup, name)
    if search_result:
        keyword, emoji = search_result
    else:
        raise EmojiNotFound("".join(name), "\n\n(but you can try -s arg)")

    is_copied = try_copy_to_clipboard(emoji)
    return f"{emoji} {keyword}\nEmoji {emoji} copied!" if is_copied \
        else f"{emoji} {keyword}\nEmoji found but not copied"


if __name__ == "__main__":
    print(main())

