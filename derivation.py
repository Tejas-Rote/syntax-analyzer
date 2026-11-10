from collections import deque


def derive_once(sentential_form, position, production_rhs):
    """Replace the symbol at position with the RHS of a production."""
    return (
        sentential_form[:position]
        + production_rhs
        + sentential_form[position + 1:]
    )


def find_leftmost_non_terminal(sentential_form, non_terminals):
    """Return the leftmost non-terminal's index, or -1 if none exists."""
    for index, symbol in enumerate(sentential_form):
        if symbol in non_terminals:
            return index
    return -1


def leftmost_derivation(grammar, target):
    """
    Find a leftmost derivation for target.

    Returns a list of (sentential_form, production_used) pairs.
    The first pair is (start_form, None); later pairs identify the
    numbered Production used to obtain that sentential form.
    Returns None if no derivation is found.
    """
    target = tuple(target)
    start_form = (grammar.start_symbol,)

    # Queue entries: (current sentential form, derivation trace)
    queue = deque([(start_form, [(start_form, None)])])
    visited = {start_form}

    while queue:
        current_form, trace = queue.popleft()

        if current_form == target:
            return trace

        position = find_leftmost_non_terminal(
            current_form, grammar.non_terminals
        )
        if position == -1:
            continue

        non_terminal = current_form[position]
        for production in grammar.productions_by_lhs[non_terminal]:
            new_form = derive_once(current_form, position, production.rhs)

            if new_form in visited:
                continue

            visited.add(new_form)
            new_trace = trace + [(new_form, production)]
            queue.append((new_form, new_trace))

    return None
