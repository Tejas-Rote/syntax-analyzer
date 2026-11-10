from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Production:
    number: int
    lhs: str
    rhs: tuple[str, ...]

    def __str__(self):
        return f"#{self.number}: {self.lhs} -> {' '.join(self.rhs) if self.rhs else 'ε'}"


class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = set(non_terminals)
        self.terminals = set(terminals)
        self.all_productions = list(productions)
        self.productions_by_lhs = {}
        for production in productions:
            self.productions_by_lhs.setdefault(production.lhs, []).append(production)
        self.start_symbol = start_symbol

    def display(self):
        from formatter import print_grammar
        print_grammar(self)


def load_grammar(filename, grammar_dir=None):
    grammar_path = Path(grammar_dir) / filename if grammar_dir else Path(__file__).parent / "grammars" / filename
    raw_rules, non_terminals = [], set()

    with open(grammar_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "->" not in line:
                raise ValueError(f"Line {line_number}: expected '->' in grammar rule")
            lhs, rhs = (part.strip() for part in line.split("->", maxsplit=1))
            if not lhs or not rhs:
                raise ValueError(f"Line {line_number}: empty left- or right-hand side")
            non_terminals.add(lhs)
            raw_rules.append((lhs, rhs, line_number))

    if not raw_rules:
        raise ValueError("Grammar file contains no productions.")

    productions, number = [], 1
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
                    raise ValueError(f"Line {line_number}: ε must be the entire alternative")
            productions.append(Production(number, lhs, symbols))
            number += 1

    terminals = {s for p in productions for s in p.rhs if s not in non_terminals}
    return Grammar(non_terminals, terminals, productions, raw_rules[0][0])
