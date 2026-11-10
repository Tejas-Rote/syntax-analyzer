# Syntax Analyzer (CLI + TUI)

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the TUI
```bash
python gui/app.py
```

## Run the existing terminal interface
```bash
python cli/main.py grammar.txt
```

## Grammar format
- One production per line: `A -> x B | y`
- Separate symbols with spaces (multi-character symbols such as `id` and `num` are supported).
- Use `ε` as an entire alternative for an empty production.
- The first production's left-hand side is the start symbol.

## TUI controls
- Choose a grammar from the dropdown.
- Edit the grammar in the left pane.
- Enter a space-separated target string.
- Run derivation; use Previous/Next to reveal derivation steps progressively.
