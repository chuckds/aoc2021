import importlib


def test_answers():
    with open('../answers') as f:
        for line in f:
            puzzle, input_file, result = line.split()
            day = puzzle[:-2]
            part = puzzle[-2:]

            day_mod = importlib.__import__(f'{day}')
            part_function = getattr(day_mod, part)
            assert part_function(f"../input/{input_file}") == int(result)