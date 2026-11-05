# Leon | Original learning example
# Build the gadget without running it
# Python 3.12+ | Run: python reductions-closure-reduction-gadget-demo.py
# A toy machine is a generator function. Each yield is one step.
# Returning "accept" or "reject" halts it. Never returning means looping.

def run(machine, text, budget):
    """Run for at most `budget` steps. Return the answer, or None if unfinished."""
    steps = machine(text)
    for _ in range(budget):
        try:
            next(steps)
        except StopIteration as done:
            return done.value
    return None


def even_ones(text):                 # accepts when the number of 1s is even
    ones = 0
    for ch in text:
        yield
        ones += ch == "1"
    return "accept" if ones % 2 == 0 else "reject"


def spin(text):                      # loops forever
    while True:
        yield


def slow_accept(text):               # accepts, but only after 5000 steps
    for _ in range(5000):
        yield
    return "accept"


def build_Mw(M, w):
    """The reduction. It writes down a new machine and runs nothing."""
    def Mw(x):
        yield
        if x != w:
            return "reject"
        answer = yield from M(w)     # simulate M on w, one step at a time
        return "accept" if answer == "accept" else "reject"
    return Mw


def stand_in_for_R(machine, probes, budget):
    """A budgeted guess at 'is the language empty?'. A real decider cannot exist."""
    return all(run(machine, p, budget) != "accept" for p in probes)


def S(M, w, budget):
    Mw = build_Mw(M, w)                              # step 1: always finishes
    empty = stand_in_for_R(Mw, [w, "", "0"], budget)  # step 2: ask R
    return not empty                                 # step 3: flip the answer


cases = [("even_ones", even_ones, "1001"), ("even_ones", even_ones, "1011"),
         ("spin", spin, "1001"), ("slow_accept", slow_accept, "1001")]
print("machine      w     M accepts w  R says empty  S accepts  S correct")
for name, M, w in cases:
    truth = run(M, w, 20000) == "accept"
    says = S(M, w, 100)
    print(f"{name:<12} {w}  {str(truth):<11}  {str(not says):<12}  {str(says):<9}  {says == truth}")

print("building M_w for a looping M returns at once:", callable(build_Mw(spin, "1001")))
print("running that M_w on w for 100 steps gives:", run(build_Mw(spin, "1001"), "1001", 100))
