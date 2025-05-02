from __future__ import annotations

import shlex

import pytest

from em import cli

copier_deps_installed = cli.try_copy_to_clipboard("checking if copy works")


@pytest.mark.parametrize(
    "args, expected_out",
    [
        (
            "-s sky",
            "🥃 tumbler_glass\n"
            "🏙️ cityscape\n"
            "🌆 cityscape_at_dusk\n"
            "🪂 parachute\n"
            "🌔 waxing_gibbous_moon\n"
            "🌙 crescent_moon\n"
            "🌞 sun_with_face\n"
            "🌌 milky_way\n"
            "☁️ cloud\n"
            "🌈 rainbow\n"
            "🈳 japanese_vacancy_button",
        ),
        (
            "-s warn",
            "🚨 police_car_light\n"
            "🚧 construction\n"
            "⚠️ warning\n"
            "🚸 children_crossing\n"
            "❕ white_exclamation_mark\n"
            "❗ exclamation_mark",
        ),
    ],
)
def test_search_with_s_arg(args, expected_out):
    # Act
    ret = cli.main(shlex.split(args))
    # Assert
    assert ret == expected_out


sky_dataset = [
    ("cityscape", "🏙️ cityscape\nEmoji 🏙️ copied!"),
    ("cityscape_at_dusk", "🌆 cityscape_at_dusk\nEmoji 🌆 copied!"),
    ("parachute", "🪂 parachute\nEmoji 🪂 copied!"),
    ("waxing_gibbous_moon", "🌔 waxing_gibbous_moon\nEmoji 🌔 copied!"),
    ("crescent_moon", "🌙 crescent_moon\nEmoji 🌙 copied!"),
    ("sun_with_face", "🌞 sun_with_face\nEmoji 🌞 copied!"),
    ("milky_way", "🌌 milky_way\nEmoji 🌌 copied!"),
    ("cloud", "☁️ cloud\nEmoji ☁️ copied!"),
    ("rainbow", "🌈 rainbow\nEmoji 🌈 copied!"),
    ("japanese_vacancy_button", "🈳 japanese_vacancy_button\nEmoji 🈳 copied!"),
]


@pytest.mark.parametrize("args, expected_out", sky_dataset)
def test_hard_search(args, expected_out):
    # Act
    ret = cli.main(shlex.split(args))

    # Assert
    assert ret == expected_out


def test_random_from_search():
    # Arrange
    args = "-sr sky"

    # Act
    ret = cli.main(shlex.split(args))

    # Assert
    assert any(ret == data[1] for data in sky_dataset)
