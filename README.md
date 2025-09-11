# em: the cli emoji keyboard

[![PyPI version](https://img.shields.io/pypi/v/em-keyboard.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/em-keyboard/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/em-keyboard.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/em-keyboard/)
[![PyPI downloads](https://img.shields.io/pypi/dm/em-keyboard.svg)](https://pypistats.org/packages/em-keyboard)
[![GitHub Actions status](https://github.com/hugovk/em-keyboard/workflows/Test/badge.svg)](https://github.com/hugovk/em-keyboard/actions)
[![Codecov](https://codecov.io/gh/hugovk/em-keyboard/branch/main/graph/badge.svg)](https://codecov.io/gh/hugovk/em-keyboard)
[![Licence](https://img.shields.io/github/license/hugovk/em-keyboard.svg)](LICENSE)
[![Code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)

**Emoji your friends and colleagues from the comfort of your own terminal.**

**em** is a nifty command-line utility for referencing emoji characters by name. Provide
the names of a few emoji, and those lucky chosen emojis will be displayed in your
terminal, then copied to your clipboard. Automagically.

Emoji can be also searched by both categories and aspects.

## Example Usage

Let's serve some delicious cake:

<!-- [[[cog
from scripts.run_command import run
run("em sparkles shortcake sparkles")
]]] -->

```console
$ em sparkles shortcake sparkles
Copied! ✨ 🍰 ✨
```

<!-- [[[end]]] -->

Let's skip the copying (for scripts):

<!-- [[[cog run("em 'chocolate bar' --no-copy") ]]] -->

```console
$ em 'chocolate bar' --no-copy
🍫
```

<!-- [[[end]]] -->

Let's find some emoji, by color:

<!-- [[[cog run("em -s yellow") ]]] -->

```console
$ em -s yellow
💛  yellow_heart
👩  woman
🐤  baby_chick
🐠  tropical_fish
🌻  sunflower
🌼  blossom
🚧  construction
🌕  full_moon
⭐  star
📒  ledger
🚸  children_crossing
🔰  japanese_symbol_for_beginner
🟡  yellow_circle
🟨  yellow_square
🫚  ginger_root
```

<!-- [[[end]]] -->

If there's only a single search result, it's copied:

<!-- [[[cog run("em -s ukraine") ]]] -->

```console
$ em -s ukraine
Copied! 🇺🇦  flag_ukraine
```

<!-- [[[end]]] -->

Pick a random emoji:

<!-- [[[cog run("em --random") ]]] -->

```console
$ em --random
Copied! 💤  zzz
```

<!-- [[[end]]] -->

Pick a random emoji:

<!-- [[[cog run("em --search yellow --random") ]]] -->

```console
$ em --search yellow --random
Copied! 🟨  yellow_square
```

<!-- [[[end]]] -->

## Installation

At this time, **em** requires Python and pip:

```sh
python3 -m pip install em-keyboard
```

On Linux, an additional dependency is required for automatic copying to clipboard. This
would be either [`xclip`](https://github.com/astrand/xclip) in an X11 session or
[`wl-clipboard`](https://github.com/bugaevc/wl-clipboard) in a Wayland session. On a
Debian-based distribution these are installable with:

```sh
sudo apt install xclip
sudo apt install wl-clipboard
```

## Tests

If you wanna develop, you might want to write and run tests:

```sh
python3 -m pip install tox
tox
```

## Have fun!

✨🍰✨
