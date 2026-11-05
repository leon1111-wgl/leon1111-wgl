# Leon | Original learning example
# Report where the brackets go wrong
# Python 3.12+ | Run: python stack-queue-applications-delimiter-error-report.py
def check_delimiters(text):
    closer_to_opener = {")": "(", "]": "[", "}": "{"}
    stack = []                              # holds (opening character, position)
    for position, char in enumerate(text):
        if char in "([{":
            stack.append((char, position))
        elif char in closer_to_opener:
            if not stack:
                return "extra " + char + " at " + str(position)
            opener, where = stack.pop()
            if opener != closer_to_opener[char]:
                return ("found " + char + " at " + str(position) +
                        " but " + opener + " from " + str(where) + " is still open")
    if stack:
        opener, where = stack[-1]
        return "unclosed " + opener + " from " + str(where)
    return "ok"

for text in ["f(a[1], {b})", "f(a[1)]", "a)", "{(x)", ""]:
    print(repr(text), "->", check_delimiters(text))
