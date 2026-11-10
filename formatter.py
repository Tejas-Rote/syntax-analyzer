from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()


def format_sentential_form(form):
    """Convert a tuple/list of grammar symbols into readable text."""
    return " ".join(form) if form else "ε"


def print_grammar(grammar):
    console.print(Panel(
        f"[bold]Start symbol:[/bold] {grammar.start_symbol}\n"
        f"[bold]Non-terminals:[/bold] {', '.join(sorted(grammar.non_terminals))}\n"
        f"[bold]Terminals:[/bold] {', '.join(sorted(grammar.terminals))}",
        title="Grammar",
        expand=False
    ))

    table = Table(title="Production Rules", show_lines=True)
    table.add_column("No.", justify="right", style="cyan")
    table.add_column("Production", style="white")
    for production in grammar.all_productions:
        table.add_row(str(production.number), f"{production.lhs} → {format_sentential_form(production.rhs)}")
    console.print(table)


def print_derivation(trace, target=None):
    """Print a derivation as a mathematical sequence with production labels."""
    if trace is None:
        console.print(f"[bold red]No derivation found[/bold red]" +
                      (f" for [yellow]{format_sentential_form(target)}[/yellow]" if target is not None else ""))
        return

    console.print(Panel("Leftmost Derivation", style="bold cyan", expand=False))

    # First sentential form is the start symbol; subsequent forms follow by ⇒.
    for index, (form, production) in enumerate(trace):
        form_text = format_sentential_form(form)
        if index == 0:
            console.print(Text(f"    {form_text}", style="bold"))
        else:
            production_label = f"  [#{production.number}]" if production else ""
            console.print(Text("⇒   ") + Text(form_text, style="bold") +
                          Text(production_label, style="dim"))

    if target is not None:
        console.print(f"\n[green]Result:[/green] {format_sentential_form(target)}")
