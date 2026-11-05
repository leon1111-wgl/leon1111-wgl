# Leon | Original learning example
# Run a rule table on one tape and on two
# Python 3.12+ | Run: python turing-machine-variants-rule-table-simulator.py
def run_tm(rules, tapes, start="start", halt="halt", limit=500):
    """Run a deterministic k-tape machine. Every tape starts with its head on cell 0.

    rules maps (state, symbols read) to (new state, symbols written, moves)."""
    cells = [dict(enumerate(t)) for t in tapes]
    heads = [0] * len(tapes)
    state, steps, history = start, 0, []

    def snapshot():
        shown = []
        for tape, head in zip(cells, heads):
            used = [i for i, c in tape.items() if c != "_"] + [head]
            lo, hi = min(used), max(used)
            shown.append("".join(f"[{tape.get(i, '_')}]" if i == head else tape.get(i, "_")
                                 for i in range(lo, hi + 1)))
        return state, shown

    history.append(snapshot())
    while state != halt:
        read = tuple(t.get(h, "_") for t, h in zip(cells, heads))
        if (state, read) not in rules:
            raise RuntimeError(f"no rule for {state} reading {read}")
        state, write, moves = rules[(state, read)]
        for i, (w, m) in enumerate(zip(write, moves)):
            cells[i][heads[i]] = w
            heads[i] += {"L": -1, "R": 1, "S": 0}[m]
        steps += 1
        history.append(snapshot())
        if steps > limit:
            raise RuntimeError("step limit reached")
    return steps, history


def contents(history):
    return [t.replace("[", "").replace("]", "").strip("_") for t in history[-1][1]]


# One tape: add 1 to a binary number. Rules: (state, (read,)) -> (state, (write,), (move,))
increment = {}
for bit in "01":
    increment[("start", (bit,))] = ("start", (bit,), "R")      # walk to the right end
increment[("start", ("_",))] = ("carry", ("_",), "L")           # step back onto the last bit
increment[("carry", ("1",))] = ("carry", ("0",), "L")           # 1 plus carry: write 0, carry on
increment[("carry", ("0",))] = ("halt", ("1",), "S")            # 0 plus carry: write 1, done
increment[("carry", ("_",))] = ("halt", ("1",), "S")            # ran off the left end: new leading 1

for text in ("1011", "111"):
    steps, history = run_tm(increment, [text])
    print(f"one tape : {text} + 1 = {contents(history)[0]} in {steps} steps")

# Two tapes: tape 1 holds x in binary, tape 2 holds a unary counter.
# Program:  repeat 3 times: x = x + 1
loop = {}
for bit in "01":
    loop[("start", (bit, "1"))] = ("scan", (bit, "1"), "SS")    # counter left? do one more pass
    loop[("start", (bit, "_"))] = ("halt", (bit, "_"), "SS")    # counter empty: finished
    loop[("scan", (bit, "1"))] = ("scan", (bit, "1"), "RS")     # find the end of x
    loop[("back", (bit, "1"))] = ("back", (bit, "1"), "LS")     # return to the start of x
loop[("scan", ("_", "1"))] = ("carry", ("_", "1"), "LS")
loop[("carry", ("1", "1"))] = ("carry", ("0", "1"), "LS")       # the increment, as before
loop[("carry", ("0", "1"))] = ("back", ("1", "1"), "LS")
loop[("carry", ("_", "1"))] = ("back", ("1", "1"), "LS")
loop[("back", ("_", "1"))] = ("start", ("_", "1"), "RR")        # count one pass, loop again

steps, history = run_tm(loop, ["101", "111"])
print(f"two tapes: x = 101, counter 111 -> x = {contents(history)[0]} in {steps} steps")
for state, (tape1, tape2) in history:
    if state == "start":
        print(f"  at the loop test: x = {tape1:<8} counter = {tape2}")
