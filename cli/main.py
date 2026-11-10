from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from grammar import load_grammar
from derivation import leftmost_derivation
from formatter import print_grammar, print_derivation

def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "grammar.txt"
    grammar = load_grammar(name)
    print_grammar(grammar)
    raw = input("Target (space-separated symbols; blank = ε): ").strip()
    target = tuple(raw.split()) if raw else ()
    print_derivation(leftmost_derivation(grammar, target), target)

if __name__ == "__main__":
    main()
