
run args="":
    uv run python -m gui.main {{args}}

test:
    uv run python -m pytest