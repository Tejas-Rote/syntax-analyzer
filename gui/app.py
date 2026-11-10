from pathlib import Path
import sys

from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Button, Select, Input, TextArea, Static, RichLog

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grammar import load_grammar
from derivation import leftmost_derivation


def display_grammar(source: str) -> str:
    """Show grammar arrows as Unicode while preserving parser compatibility."""
    return source.replace("->", "→").replace("epsilon", "ε").replace("Epsilon", "ε")


class SyntaxAnalyzerApp(App):
    TITLE = "Syntax Analyzer"

    CSS = """
    Screen { layout: vertical; }
    #workspace { height: 1fr; }
    #left { width: 42%; border: round $primary; padding: 1; }
    #right { width: 58%; border: round $secondary; padding: 1; }
    .section-title { text-style: bold; margin: 0 0 1 0; }
    #grammar-editor { height: 1fr; padding: 0; }
    #derivation { height: 1fr; border: round $surface; padding: 0 1; }
    #step-controls { height: 3; align: center middle; }
    #step-label { width: 1fr; content-align: center middle; text-style: dim; }
    Button { height: 3; min-width: 10; padding: 0 1; margin: 0; }
    #run { margin-top: 1; width: auto; min-width: 12; }
    #step-controls Button { width: 12; min-width: 10; }
    """

    def __init__(self):
        super().__init__()
        self.grammar = None
        self.trace = None
        self.target = ()
        self.step = 0
        self.grammar_files = sorted(p.name for p in (ROOT / "grammars").glob("*.txt"))

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="workspace"):
            with Vertical(id="left"):
                yield Static("GRAMMAR", classes="section-title")
                yield Select([(name, name) for name in self.grammar_files],
                            prompt="Choose a grammar", id="grammar-select")
                yield TextArea(id="grammar-editor", language="text")
                yield Static("INPUT (space-separated symbols)", classes="section-title")
                yield Input(placeholder="e.g. id + num * id", id="target-input")
                yield Button("Run derivation", variant="primary", id="run")
                yield Static("Choose a grammar and enter a target.", id="status")
            with Vertical(id="right"):
                yield Static("DERIVATION", classes="section-title")
                yield RichLog(id="derivation", wrap=True, markup=False)
                with Horizontal(id="step-controls"):
                    yield Button("← Previous", id="prev")
                    yield Static("Step 0 / 0", id="step-label")
                    yield Button("Next →", id="next")
                yield Static("Terminal output is preserved when launched from a terminal.", id="hint")
        yield Footer()

    def on_mount(self):
        if self.grammar_files:
            self.query_one(Select).value = self.grammar_files[0]

    def on_select_changed(self, event: Select.Changed):
        if event.select.id != "grammar-select" or event.value is Select.BLANK:
            return
        path = ROOT / "grammars" / str(event.value)
        self.query_one(TextArea).text = display_grammar(path.read_text(encoding="utf-8"))
        self.query_one("#status", Static).update(f"Loaded {event.value}")
        self.trace = None
        self.query_one("#derivation", RichLog).clear()
        self.query_one("#step-label", Static).update("Step 0 / 0")

    def parse_editor_grammar(self):
        """Convert Unicode arrow back to ASCII before using the existing parser."""
        temp = ROOT / ".gui_grammar_temp.txt"
        editor_text = self.query_one(TextArea).text.replace("→", "->")
        temp.write_text(editor_text, encoding="utf-8")
        try:
            return load_grammar(temp.name, grammar_dir=ROOT)
        finally:
            temp.unlink(missing_ok=True)

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "run":
            self.run_derivation()
        elif event.button.id == "prev":
            self.show_step(max(0, self.step - 1))
        elif event.button.id == "next" and self.trace:
            self.show_step(min(len(self.trace) - 1, self.step + 1))

    def run_derivation(self):
        log = self.query_one("#derivation", RichLog)
        log.clear()
        try:
            self.grammar = self.parse_editor_grammar()
            raw = self.query_one("#target-input", Input).value.strip()
            self.target = tuple(raw.split()) if raw else ()
            self.trace = leftmost_derivation(self.grammar, self.target)
            if not self.trace:
                log.write(Text("No derivation found for this input.", style="bold red"))
                self.query_one("#status", Static).update("Rejected · no derivation")
                self.query_one("#step-label", Static).update("Step 0 / 0")
                self.step = 0
                return
            self.step = 0
            self.show_step(0)
            self.query_one("#status", Static).update(
                f"Accepted · {len(self.trace) - 1} derivation steps"
            )
        except Exception as exc:
            log.write(Text(f"Error: {exc}", style="bold red"))
            self.query_one("#status", Static).update("Grammar or input error")
            self.query_one("#step-label", Static).update("Step 0 / 0")
            self.trace = None
            self.step = 0

    def colored_form(self, form):
        """Render non-terminals cyan and terminals green."""
        text = Text()
        if not form:
            text.append("ε", style="bold magenta")
            return text
        for i, symbol in enumerate(form):
            if i:
                text.append(" ")
            text.append(symbol, style="bold cyan" if symbol in self.grammar.non_terminals else "green")
        return text

    def show_step(self, index):
        if not self.trace:
            return
        self.step = index
        log = self.query_one("#derivation", RichLog)
        log.clear()
        for i, (form, production) in enumerate(self.trace[:index + 1]):
            line = Text()
            line.append(f"{i:>2}. ", style="dim")
            line.append_text(self.colored_form(form))
            line.append("    ")
            line.append("[Start]" if production is None else f"[#{production.number}]",
                        style="bold yellow")
            log.write(line)
        self.query_one("#step-label", Static).update(
            f"Step {index} / {len(self.trace) - 1}"
        )


if __name__ == "__main__":
    SyntaxAnalyzerApp().run()
