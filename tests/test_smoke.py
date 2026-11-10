from grammar import load_grammar
from derivation import leftmost_derivation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_arithmetic_derivation():
    g = load_grammar("two.txt")
    trace = leftmost_derivation(g, ("a", "+", "b", "*", "c"))
    assert trace is not None
