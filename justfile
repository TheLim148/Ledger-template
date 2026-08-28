
run *args:
    source ./postgres.dev.env.sh
    uv run python main.py {{args}}

test:
    source ./postgres.test.env.sh
    uv run python -m pytest -rP