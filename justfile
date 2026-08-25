
run *args:
    uv run python main.py {{args}}

test:
    uv run python -m pytest -rP