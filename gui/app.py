from pathlib import Path
import sys

from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import (
    Header,
    Footer,
    Button,
    Select,
    Input,
    TextArea,
    Static,
    RichLog,
)

ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_DIR = ROOT / "grammars"

sys.path.insert(0, str(ROOT))

from grammar import load_grammar
from derivation import leftmost_derivation


def display_grammar(source: str) -> str:
    """Display grammar arrows and epsilon using Unicode."""
    return source.replace("->", "→").replace("epsilon", "ε").replace("Epsilon", "ε")


class SyntaxAnalyzerApp(App):
    TITLE = "Syntax Analyzer"

    # CSS = """
    # Screen {
    #     layout: vertical;
    #     background: $background;
    # }

    # /* Main workspace */
    # #workspace {
    #     height: 1fr;
    #     padding: 1;
    # }

    # /* Panels */
    # #left {
    #     width: 42%;
    #     border: round $primary;
    #     padding: 1;
    #     background: $surface;
    # }

    # #right {
    #     width: 58%;
    #     border: round $secondary;
    #     padding: 1;
    #     background: $surface;
    # }

    # /* Section headings */
    # .section-title {
    #     text-style: bold;
    #     color: $text;
    #     margin: 0 0 1 0;
    # }

    # /* Grammar selector */
    # #grammar-select {
    #     margin-bottom: 1;
    #     width: 100%;
    # }

    # /* Grammar editor */
    # #grammar-editor {
    #     height: 1fr;
    #     padding: 0;
    #     border: round $surface-lighten-1;
    #     background: $surface;
    # }

    # /* New / Save buttons */
    # #grammar-actions {
    #     height: 3;
    #     margin-top: 1;
    # }

    # #grammar-actions Button {
    #     width: 1fr;
    #     min-width: 0;
    #     margin: 0;
    # }

    # /* Filename input */
    # #grammar-filename {
    #     margin-top: 1;
    #     margin-bottom: 1;
    #     width: 100%;
    # }

    # /* Input field */
    # #target-input {
    #     margin-top: 1;
    #     margin-bottom: 1;
    #     width: 100%;
    # }

    # /* Run button */
    # #run {
    #     margin-top: 1;
    #     width: 100%;
    #     min-width: 0;
    # }

    # /* Status */
    # #status {
    #     margin-top: 1;
    #     color: $text-muted;
    # }

    # /* Derivation output */
    # #derivation {
    #     height: 1fr;
    #     border: round $surface-lighten-1;
    #     background: $surface;
    #     padding: 0 1;
    # }

    # /* Step navigation */
    # #step-controls {
    #     height: 2;
    #     margin-top: 1;
    #     align: center middle;
    # }

    # #step-label {
    #     width: 1fr;
    #     content-align: center middle;
    #     text-style: bold;
    #     color: $text-muted;
    # }

    # #step-controls Button {
    #     width: 12;
    #     min-width: 10;
    #     margin: 0;
    # }

    # /* General buttons */
    # Button {
    #     height: 3;
    #     padding: 0;
    #     margin: 0;
    #     border: none;
    # }

    # /* Hover effect */
    # Button:hover {
    #     border: none;
    #     background: $primary-darken-1;
    # }

    # /* Focus effect */
    # Button:focus {
    #     border: none;
    #     background: $primary;
    # }

    # /* Footer hint */
    # #hint {
    #     margin-top: 1;
    #     color: $text-muted;
    # }
    # """

    CSS = """
        /* =========================
        GLOBAL
        ========================= */

        Screen {
            layout: vertical;
            background: #080808;
        }

        #workspace {
            height: 1fr;
            padding: 0;
        }

        /* =========================
        PANELS
        ========================= */

        #left {
            width: 42%;
            border: round #292929;
            padding: 0 1;
            background: #0c0c0c;
        }

        #right {
            width: 58%;
            border: round #292929;
            padding: 0 1;
            background: #0c0c0c;
        }

        /* =========================
        SECTION HEADINGS
        ========================= */

        .section-title {
            text-style: bold;
            color: #bdbdbd;
            margin: 0 0 1 0;
        }

        /* =========================
        GRAMMAR SELECTOR
        ========================= */

        #grammar-select {
            width: 100%;
            margin: 0 0 1 0;
            background: #141414;
            border: round #303030;
        }

        #grammar-select:focus {
            border: round #1677cc;
        }

        /* =========================
        GRAMMAR EDITOR
        ========================= */

        #grammar-editor {
            height: 1fr;
            padding: 0;
            border: round #262626;
            background: #101010;
        }

        #grammar-editor:focus {
            border: round #303030;
        }

        /* =========================
        GRAMMAR ACTIONS
        ========================= */

        #grammar-actions {
            height: 3;
            margin-top: 1;
        }

        #grammar-actions Button {
            width: 1fr;
            min-width: 0;
            height: 3;
            padding: 0 1;
            margin: 0;
            text-wrap: nowrap;
        }

        #grammar-actions Button:hover {
            background: #242424;
            color: #ffffff;
        }

        #grammar-actions #save {
            background: #075ca8;
            color: #ffffff;
        }

        #grammar-actions #save:hover {
            background: #0875ce;
        }

        /* =========================
        INPUT FIELDS
        ========================= */

        #grammar-filename {
            width: 100%;
            margin: 1 0;
            background: #141414;
            border: round #282828;
        }

        #grammar-filename:focus {
            border: round #1677cc;
        }

        #target-input {
            width: 100%;
            margin: 0 0 1 0;
            background: #141414;
            border: round #282828;
        }

        #target-input:focus {
            border: round #1677cc;
        }

        /* =========================
        RUN BUTTON
        ========================= */

        /* Run button */
        #run {
            width: 100%;
            min-width: 0;
            height: 3;
            padding: 0 1;
            margin: 0;
            text-wrap: nowrap;
            background: #075ca8;
            color: #ffffff;
            border: none;
        }

        #run:hover {
            background: #0875ce;
            color: #ffffff;
        }

        /* =========================
        STATUS
        ========================= */

        #status {
            margin-top: 1;
            color: #777777;
        }

        /* =========================
        DERIVATION OUTPUT
        ========================= */

        #derivation {
            height: 1fr;
            padding: 0 1;
            border: round #262626;
            background: #101010;
        }

        /* =========================
        STEP NAVIGATION
        ========================= */
        /* Step navigation */
        #step-controls {
            height: 3;
            margin-top: 1;
            align: center middle;
        }

        #step-label {
            width: 1fr;
            content-align: center middle;
            text-style: bold;
            color: #777777;
        }

        #step-controls Button {
            width: 14;
            min-width: 14;
            height: 3;
            padding: 0 1;
            margin: 0;
            text-wrap: nowrap;
            border: none;
            background: #151515;
            color: #aaaaaa;
        }

        #step-controls Button:hover {
            background: #252525;
            color: #ffffff;
        }

        /* =========================
        GENERAL BUTTONS
        ========================= */

        Button {
            height: 2;
            padding: 0;
            margin: 0;
            border: none;
        }

        Button:focus {
            border: none;
        }

        /* =========================
        FOOTER HINT
        ========================= */

        #hint {
            margin-top: 1;
            color: #555555;
        }
        """

    def __init__(self):
        super().__init__()

        self.grammar = None
        self.trace = None
        self.target = ()
        self.step = 0

        self.active_filename = None

        self.grammar_files = self.get_grammar_files()

    def get_grammar_files(self):
        """Return available grammar filenames."""
        GRAMMAR_DIR.mkdir(exist_ok=True)

        return sorted(
            path.name
            for path in GRAMMAR_DIR.glob("*.txt")
            if path.is_file()
        )

    def grammar_options(self):
        return [(name, name) for name in self.grammar_files]

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal(id="workspace"):

            # LEFT PANEL
            with Vertical(id="left"):

                yield Static("GRAMMAR", classes="section-title")

                yield Select(
                    self.grammar_options(),
                    prompt="Choose a grammar",
                    id="grammar-select",
                )

                yield TextArea(
                    id="grammar-editor",
                    language="text",
                )

                with Horizontal(id="grammar-actions"):
                    yield Button("New Grammar", id="new-grammar")
                    yield Button("Save Grammar", variant="primary", id="save")

                yield Input(
                    placeholder="Filename (e.g. custom.txt)",
                    value="custom.txt",
                    id="grammar-filename",
                )

                yield Static(
                    "INPUT (space-separated symbols)",
                    classes="section-title",
                )

                yield Input(
                    placeholder="e.g. id + num * id",
                    id="target-input",
                )

                yield Button(
                    "Run derivation",
                    variant="primary",
                    id="run",
                )

                yield Static(
                    "Choose a grammar or create a new one.",
                    id="status",
                )

            # RIGHT PANEL
            with Vertical(id="right"):

                yield Static("DERIVATION", classes="section-title")

                yield RichLog(
                    id="derivation",
                    wrap=True,
                    markup=False,
                )

                with Horizontal(id="step-controls"):
                    yield Button("← Previous", id="prev")

                    yield Static(
                        "Step 0 / 0",
                        id="step-label",
                    )

                    yield Button("Next →", id="next")

                yield Static(
                    "Terminal output is preserved when launched from a terminal.",
                    id="hint",
                )

        yield Footer()

    def on_mount(self):
        """Load the first grammar when the application starts."""
        if self.grammar_files:
            self.query_one(Select).value = self.grammar_files[0]

    # ---------------------------------------------------------
    # GRAMMAR SELECTION
    # ---------------------------------------------------------


    def on_select_changed(self, event: Select.Changed):
        if event.select.id != "grammar-select":
            return

        # Ignore dropdown clearing / no-selection events
        if event.value is Select.NULL or event.value is None:
            return

        filename = str(event.value)
        path = GRAMMAR_DIR / filename

        if not path.is_file():
            return

        self.query_one(TextArea).text = display_grammar(
            path.read_text(encoding="utf-8")
        )

        self.query_one("#grammar-filename", Input).value = filename

        self.active_filename = filename

        self.clear_derivation()

        self.query_one("#status", Static).update(
            f"Loaded {filename}"
        )


    # ---------------------------------------------------------
    # NEW GRAMMAR
    # ---------------------------------------------------------

   
    def new_grammar(self):
        """Start a new, unsaved grammar."""

        self.active_filename = None

        # Clear grammar editor
        self.query_one(TextArea).text = ""

        # Set default filename
        self.query_one("#grammar-filename", Input).value = "custom.txt"

        # Clear dropdown using Textual's API
        self.query_one("#grammar-select", Select).clear()

        # Clear derivation
        self.clear_derivation()

        self.query_one("#status", Static).update(
            "New grammar · unsaved"
        )

    # ---------------------------------------------------------
    # SAVE GRAMMAR
    # ---------------------------------------------------------

    def save_grammar(self):
        """Save the editor contents to a grammar file."""

        filename = self.query_one(
            "#grammar-filename",
            Input,
        ).value.strip()

        grammar_text = self.query_one(
            TextArea,
        ).text

        # Validate filename
        if not filename:
            self.query_one("#status", Static).update(
                "Enter a filename first."
            )
            return

        # Only allow simple filenames
        if Path(filename).name != filename:
            self.query_one("#status", Static).update(
                "Use a filename without directory paths."
            )
            return

        # Automatically append .txt
        if not filename.endswith(".txt"):
            filename += ".txt"

        path = GRAMMAR_DIR / filename

        # Do not overwrite another existing grammar accidentally
        if path.exists() and filename != self.active_filename:
            self.query_one("#status", Static).update(
                f"{filename} already exists. Choose another filename."
            )
            return

        try:
            # Validate grammar before saving
            temp = ROOT / ".gui_grammar_validation.txt"

            temp.write_text(
                grammar_text.replace("→", "->"),
                encoding="utf-8",
            )

            try:
                load_grammar(
                    temp.name,
                    grammar_dir=ROOT,
                )
            finally:
                temp.unlink(missing_ok=True)

            # Save grammar
            path.write_text(
                grammar_text.replace("→", "->"),
                encoding="utf-8",
            )

            # Update current filename
            self.active_filename = filename

            # Refresh dropdown
            self.grammar_files = self.get_grammar_files()

            grammar_select = self.query_one(
                "#grammar-select",
                Select,
            )

            grammar_select.set_options(
                self.grammar_options()
            )

            # Select newly saved grammar
            grammar_select.value = filename

            self.query_one(
                "#grammar-filename",
                Input,
            ).value = filename

            self.query_one("#status", Static).update(
                f"Saved {filename}"
            )

        except Exception as exc:
            self.query_one("#status", Static).update(
                f"Save error: {exc}"
            )

    # ---------------------------------------------------------
    # GRAMMAR PARSING
    # ---------------------------------------------------------

    def parse_editor_grammar(self):
        """Parse the grammar currently present in the editor."""

        temp = ROOT / ".gui_grammar_temp.txt"

        editor_text = self.query_one(
            TextArea,
        ).text.replace("→", "->")

        temp.write_text(
            editor_text,
            encoding="utf-8",
        )

        try:
            return load_grammar(
                temp.name,
                grammar_dir=ROOT,
            )
        finally:
            temp.unlink(missing_ok=True)

    # ---------------------------------------------------------
    # BUTTON HANDLING
    # ---------------------------------------------------------

    def on_button_pressed(self, event: Button.Pressed):

        button_id = event.button.id

        if button_id == "new-grammar":
            self.new_grammar()

        elif button_id == "save":
            self.save_grammar()

        elif button_id == "run":
            self.run_derivation()

        elif button_id == "prev":
            self.show_step(
                max(0, self.step - 1)
            )

        elif button_id == "next" and self.trace:
            self.show_step(
                min(
                    len(self.trace) - 1,
                    self.step + 1,
                )
            )

    # ---------------------------------------------------------
    # DERIVATION
    # ---------------------------------------------------------

    def clear_derivation(self):
        self.trace = None
        self.step = 0

        self.query_one(
            "#derivation",
            RichLog,
        ).clear()

        self.query_one(
            "#step-label",
            Static,
        ).update("Step 0 / 0")

    def run_derivation(self):

        log = self.query_one(
            "#derivation",
            RichLog,
        )

        log.clear()

        try:
            self.grammar = self.parse_editor_grammar()

            raw = self.query_one(
                "#target-input",
                Input,
            ).value.strip()

            self.target = tuple(raw.split()) if raw else ()

            self.trace = leftmost_derivation(
                self.grammar,
                self.target,
            )

            if not self.trace:
                log.write(
                    Text(
                        "No derivation found for this input.",
                        style="bold red",
                    )
                )

                self.query_one(
                    "#status",
                    Static,
                ).update("Rejected · no derivation")

                self.query_one(
                    "#step-label",
                    Static,
                ).update("Step 0 / 0")

                self.step = 0
                return

            self.step = 0

            self.show_step(0)

            self.query_one(
                "#status",
                Static,
            ).update(
                f"Accepted · {len(self.trace) - 1} derivation steps"
            )

        except Exception as exc:

            log.write(
                Text(
                    f"Error: {exc}",
                    style="bold red",
                )
            )

            self.query_one(
                "#status",
                Static,
            ).update("Grammar or input error")

            self.query_one(
                "#step-label",
                Static,
            ).update("Step 0 / 0")

            self.trace = None
            self.step = 0

    # ---------------------------------------------------------
    # DERIVATION DISPLAY
    # ---------------------------------------------------------

    def colored_form(self, form):
        """Render non-terminals cyan and terminals green."""

        text = Text()

        if not form:
            text.append("ε", style="bold magenta")
            return text

        for i, symbol in enumerate(form):

            if i:
                text.append(" ")

            text.append(
                symbol,
                style=(
                    "bold cyan"
                    if symbol in self.grammar.non_terminals
                    else "green"
                ),
            )

        return text

    def show_step(self, index):

        if not self.trace:
            return

        self.step = index

        log = self.query_one(
            "#derivation",
            RichLog,
        )

        log.clear()

        for i, (form, production) in enumerate(
            self.trace[:index + 1]
        ):

            line = Text()

            line.append(
                f"{i:>2}. ",
                style="dim",
            )

            line.append_text(
                self.colored_form(form)
            )

            line.append("    ")

            line.append(
                "[Start]"
                if production is None
                else f"[#{production.number}]",
                style="bold yellow",
            )

            log.write(line)

        self.query_one(
            "#step-label",
            Static,
        ).update(
            f"Step {index} / {len(self.trace) - 1}"
        )


if __name__ == "__main__":
    SyntaxAnalyzerApp().run()
