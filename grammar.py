from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Production:
    number: int
    lhs: str
    rhs: tuple

    def __str__(self):
        rhs_text = " ".join(self.rhs) if self.rhs else "ε"
        return f"#{self.number}: {self.lhs} -> {rhs_text}"


class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        # Ordered list of every production (including alternatives separately)
        self.all_productions = productions
        # Lookup: non-terminal -> its Production objects
        self.productions_by_lhs = {}
        for production in productions:
            self.productions_by_lhs.setdefault(production.lhs, []).append(production)
        self.start_symbol = start_symbol

    def display(self):
        print("Grammar")
        print("======")
        print(f"Start symbol: {self.start_symbol}")
        print("Non-terminals:", ", ".join(sorted(self.non_terminals)))
        print("Terminals:", ", ".join(sorted(self.terminals)))
        print("\nProduction rules:")
        for production in self.all_productions:
            print(production)


def load_grammar(filename):
    grammar_path = Path(__file__).parent / "grammars" / filename
    raw_rules = []
    non_terminals = set()

    # Pass 1: read rules and collect all left-hand-side non-terminals.
    with open(grammar_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "->" not in line:
                raise ValueError(f"Line {line_number}: expected '->' in grammar rule")

            lhs, rhs = line.split("->", maxsplit=1)
            lhs = lhs.strip()
            rhs = rhs.strip()
            if not lhs or not rhs:
                raise ValueError(f"Line {line_number}: empty left- or right-hand side")

            non_terminals.add(lhs)
            raw_rules.append((lhs, rhs, line_number))

    if not raw_rules:
        raise ValueError("Grammar file contains no productions.")

    # Pass 2: split alternatives and assign global production numbers.
    productions = []
    number = 1
    for lhs, rhs, line_number in raw_rules:
        for alternative in rhs.split("|"):
            alternative = alternative.strip()
            if not alternative:
                raise ValueError(f"Line {line_number}: empty alternative")
            if alternative == "ε":
                symbols = ()
            else:
                symbols = tuple(alternative.split())
                if "ε" in symbols:
                    raise ValueError(
                        f"Line {line_number}: ε must be the entire alternative"
                    )
            productions.append(Production(number, lhs, symbols))
            number += 1

    terminals = {
        symbol
        for production in productions
        for symbol in production.rhs
        if symbol not in non_terminals
    }

    start_symbol = raw_rules[0][0]
    return Grammar(non_terminals, terminals, productions, start_symbol)
