import pathlib
import importlib


def test_answers() -> None:
    repo_root = pathlib.Path(__file__).resolve().parent.parent
    with open(repo_root / 'answers') as f:
        for line in f:
            puzzle, input_file, result = line.split()
            day = puzzle[:-2]
            part = puzzle[-2:]

            day_mod = importlib.__import__(f'{day}')
            part_function = getattr(day_mod, part)
            assert part_function(repo_root / "input" / input_file) == int(result)