"""
Replace spaces in emoji keywords with underscores
"""

from __future__ import annotations

import json

from em.cli import EmojiDict, clean_name, parse_emojis  # type: ignore[import]

INPUT_EMOJILIB_PATH = "src/em/emoji-en-US.json"
OUTPUT_EMOJI_PATH = "src/em/emojis.json"


def save_emojis(data: EmojiDict, filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=None, separators=(",", ":"))
        outfile.write("\n")


def main() -> None:
    data = parse_emojis(INPUT_EMOJILIB_PATH)
    for emoji, keywords in data.items():
        keywords = [clean_name(keyword) for keyword in keywords]
        data[emoji] = keywords
    save_emojis(data, OUTPUT_EMOJI_PATH)
    print(f"Emojis saved to {OUTPUT_EMOJI_PATH}")


if __name__ == "__main__":
    main()
