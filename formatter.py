from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


def format_sentential_form(form):
    return " ".join(form) if form else "ε"


def print_grammar(grammar):
    console.print(Panel(
        f"[bold]Start symbol:[/bold] {grammar.start_symbol}\n"
        f"[bold]Non-terminals:[/bold] {', '.join(sorted(grammar.non_terminals))}\n"
        f"[bold]Terminals:[/bold] {', '.join(sorted(grammar.terminals))}",
        title="Grammar", expand=False))
    table = Table(title="Production Rules", show_lines=True)
    table.add_column("No.", justify="right", style="cyan")
    table.add_column("Production")
    for p in grammar.all_productions:
        table.add_row(str(p.number), f"{p.lhs} → {format_sentential_form(p.rhs)}")
    console.print(table)


def print_derivation(trace, target=None):
    if trace is None:
        console.print(f"[bold red]No derivation found[/bold red]" +
                      (f" for [yellow]{format_sentential_form(target)}[/yellow]" if target is not None else ""))
        return
    console.print(Panel("Leftmost Derivation", style="bold cyan", expand=False))
    for i, (form, production) in enumerate(trace):
        if i == 0:
            console.print(Text("    " + format_sentential_form(form), style="bold"))
        else:
            console.print(Text("⇒   ") + Text(format_sentential_form(form), style="bold") +
                          Text(f"  [#{production.number}]", style="dim"))
    if target is not None:
        console.print(f"\n[green]Result:[/green] {format_sentential_form(target)}")
