# Unicode + colored derivation update

The GUI displays grammar arrows as Unicode `→`. On Run, it converts `→` to `->`
for the existing grammar parser, so `grammar.py` is unchanged. Derivation output
colors non-terminals cyan, terminals green, production labels yellow, and epsilon
magenta. This is not full live token coloring inside the TextArea editor; Textual's
TextArea needs a custom syntax-highlighting implementation for that feature.

Run from project root:
```bash
python gui/app.py
```
