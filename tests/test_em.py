from __future__ import annotations

import random
import shlex

import pytest

from em import cli  # type: ignore[import-untyped]

copier_deps_installed = cli.try_copy_to_clipboard("checking if copy works")


@pytest.mark.parametrize(
    "test_args, expected_output",
    [
        ("star", "⭐"),
        (":star:", "⭐"),
        ("STAR", "⭐"),
        (":Star:", "⭐"),
        ("--search ukraine", "🇺🇦  flag_ukraine"),
        ("--random", "😽  kissing_cat"),
        ("--random --no-copy", "😽  kissing_cat"),
        ("--search big tent", "🎪  circus_tent"),
    ],
)
def test_success(
    test_args: str, expected_output: str, capsys: pytest.LogCaptureFixture
) -> None:
    # Arrange
    random.seed(123)

    # Act
    ret = cli.main(shlex.split(test_args))

    # Assert
    output = capsys.readouterr().out.rstrip()
    if copier_deps_installed and "--no-copy" not in test_args:
        assert output == f"Copied! {expected_output}"
    else:
        assert output == expected_output
    assert ret == 0


@pytest.mark.parametrize(
    "test_args",
    [
        "xxx --no-copy",
        "--search twenty_o_clock",
        "--search",
    ],
)
def test_error(test_args: str, capsys: pytest.LogCaptureFixture) -> None:
    # Act
    ret = cli.main(shlex.split(test_args))

    # Assert
    output = capsys.readouterr().out.rstrip()
    assert output == ""
    assert ret != 0


def test_search_star(capsys: pytest.LogCaptureFixture) -> None:
    # Arrange
    args = "--search star"
    expected = (
        "💫  dizzy",
        "⭐  star",
        "✳️  eight_spoked_asterisk",
    )

    # Act
    ret = cli.main(shlex.split(args))

    # Assert
    output = capsys.readouterr().out.rstrip()
    for arg in expected:
        assert arg in output
    assert ret == 0
