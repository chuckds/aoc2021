import pytest # type: ignore
import pathlib
import importlib


def get_puzzle_info() -> list[tuple[str, str, str, int]]:
    day_parts = []
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    with open(repo_root / 'answers') as f:
        for line in f:
            puzzle, input_file, result = line.split()
            day = puzzle[:-2]
            part = puzzle[-2:]
            day_parts.append((day, part, str(repo_root / "input" / input_file), int(result)))

    return day_parts


@pytest.mark.parametrize("day,part,input_file,result", get_puzzle_info()) # type: ignore
def test_puzzle(day: str, part: str, input_file: str, result: int) -> None:
    day_mod = importlib.__import__(day)
    part_function = getattr(day_mod, part)
    assert part_function(input_file) == result