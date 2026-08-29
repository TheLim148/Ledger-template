run *args:
    . ./postgres.dev.env.sh && uv run python main.py {{args}}

test:
    . ./postgres.test.env.sh && uv run python -m pytest -rP