
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


def terminal_sequence(sentential_form, non_terminals):
    """Extract terminals from a sentential form, preserving their order."""
    return tuple(
        symbol
        for symbol in sentential_form
        if symbol not in non_terminals
    )


def can_match_target(sentential_form, target, non_terminals):
    """
    Check whether the terminals already present in a sentential form
    are compatible with the target.

    Existing terminals cannot disappear or change order during derivation.
    Therefore, they must form a subsequence of the target.
    """
    terminals = terminal_sequence(sentential_form, non_terminals)

    target_index = 0

    for terminal in terminals:
        while (
            target_index < len(target)
            and target[target_index] != terminal
        ):
            target_index += 1

        if target_index == len(target):
            return False

        target_index += 1

    return True


def leftmost_derivation(grammar, target, max_states=100000):
    """
    Find a leftmost derivation for target using BFS.

    Returns:
        A list of (sentential_form, production_used) pairs.
        The first pair is (start_form, None).
        Later pairs contain the numbered Production used.

        Returns None if no derivation exists.

    Raises RuntimeError if the search limit is reached.
    """

    target = tuple(target)
    start_form = (grammar.start_symbol,)

    # A terminal-only sentential form must equal the target.
    # All terminals already generated must appear in the target
    # in the same order.
    if not can_match_target(
        start_form, target, grammar.non_terminals
    ):
        return None

    queue = deque([
        (start_form, [(start_form, None)])
    ])

    visited = {start_form}
    explored_states = 0

    while queue:

        current_form, trace = queue.popleft()

        explored_states += 1

        if explored_states > max_states:
            raise RuntimeError(
                f"Search limit reached ({max_states} sentential forms). "
                "Grammar may generate infinitely many candidates."
            )

        # Success: exact target reached.
        if current_form == target:
            return trace

        # Find the leftmost non-terminal.
        position = find_leftmost_non_terminal(
            current_form,
            grammar.non_terminals
        )

        # No non-terminal remains, but target was not reached.
        if position == -1:
            continue

        non_terminal = current_form[position]

        # Expand the leftmost non-terminal using all productions.
        for production in grammar.productions_by_lhs[non_terminal]:

            new_form = derive_once(
                current_form,
                position,
                production.rhs
            )

            # Avoid revisiting identical sentential forms.
            if new_form in visited:
                continue

            # Pruning 1:
            # A derivation cannot remove existing terminals.
            # Their sequence must remain compatible with target.
            if not can_match_target(
                new_form,
                target,
                grammar.non_terminals
            ):
                continue

            # Pruning 2:
            # Every terminal in the final target must already
            # be present or still be generated.
            # Existing terminals cannot exceed target length.
            existing_terminals = terminal_sequence(
                new_form,
                grammar.non_terminals
            )

            if len(existing_terminals) > len(target):
                continue

            # Pruning 3:
            # Every symbol requires at least one position in
            # the final sentential form, except that epsilon
            # productions may remove non-terminals later.
            #
            # We intentionally do not use total form length
            # as a strict bound because nullable productions
            # can remove non-terminals.

            visited.add(new_form)

            new_trace = trace + [
                (new_form, production)
            ]

            queue.append((new_form, new_trace))

    # Exhaustive BFS completed without finding a derivation.
    return None
