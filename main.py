from grammar import load_grammar
from derivation import leftmost_derivation
from formatter import print_grammar, print_derivation
from rich.console import Console

console = Console()

grammar = load_grammar("three.txt")
print_grammar(grammar)  

# target = "aabb"
# target = ("id", "+", "num", "*", "id")
# target = ()
target = (
    "id", "=", "num", "+", "id", "*", "num", ";"
)
trace = leftmost_derivation(grammar, target)

print_derivation(trace, target)
