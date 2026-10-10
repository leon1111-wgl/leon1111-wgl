# Leon | Original learning example
# Search for witnesses and counterexamples in a finite model
# Python 3.12+ | Run: python predicate-logic-finite-witness-search.py
students = ["Ana", "Bo", "Cy"]
mentors = ["Ivy", "Noah"]
relation = {("Ana", "Ivy"), ("Bo", "Noah"), ("Cy", "Ivy")}

def inspect(students, mentors, relation):
    witnesses = {x: [y for y in mentors if (x, y) in relation] for x in students}
    every_has_someone = all(witnesses[x] for x in students)
    shared = [y for y in mentors if all((x, y) in relation for x in students)]
    uncovered = [x for x in students if all((x, y) not in relation for y in mentors)]
    assert bool(uncovered) == (not every_has_someone)
    return witnesses, every_has_someone, shared, uncovered

witnesses, every, shared, uncovered = inspect(students, mentors, relation)
print("witnesses:", witnesses)
print("every student has a mentor:", every)
print("one mentor for everybody:", bool(shared))
assert every and not shared
broken = relation - {("Bo", "Noah")}
print("counterexample after removal:", inspect(students, mentors, broken)[3])
assert inspect([], mentors, relation)[1] is True
assert inspect(students, [], relation)[1] is False
