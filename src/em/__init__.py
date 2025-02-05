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

from em import _version  # type: ignore[attr-defined]

__version__ = _version.__version__
