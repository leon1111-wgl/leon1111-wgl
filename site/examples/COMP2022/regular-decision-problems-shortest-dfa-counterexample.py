# Leon | Original learning example
# Find a shortest word that separates two DFAs
# Python 3.12+ | Run: python regular-decision-problems-shortest-dfa-counterexample.py
from collections import deque
from itertools import product

def witness(a, accepting_a, b, accepting_b):
    alphabet = ("a", "b")
    start = (0, 0)
    parents = {start: None}
    queue = deque([start])
    while queue:
        pair = queue.popleft()
        x, y = pair
        if (x in accepting_a) != (y in accepting_b):
            letters = []
            while parents[pair] is not None:
                previous, letter = parents[pair]
                letters.append(letter)
                pair = previous
            return "".join(reversed(letters))
        for letter in alphabet:
            nxt = (a[x][letter], b[y][letter])
            if nxt not in parents:
                parents[nxt] = (pair, letter)
                queue.append(nxt)
    return None

def accepts(table, word):
    state = 0
    for letter in word:
        state = table[state][letter]
    return state == 2

contains = [{"a": 1, "b": 0}, {"a": 1, "b": 2}, {"a": 2, "b": 2}]
ends = [{"a": 1, "b": 0}, {"a": 1, "b": 2}, {"a": 1, "b": 0}]
word = witness(contains, {2}, ends, {2})
assert word == "aba" and witness(contains, {2}, contains, {2}) is None
for size in range(len(word)):
    for letters in product("ab", repeat=size):
        test = "".join(letters)
        assert accepts(contains, test) == accepts(ends, test)
print("shortest witness:", repr(word))
print("contains ab:", accepts(contains, word))
print("ends in ab:", accepts(ends, word))
