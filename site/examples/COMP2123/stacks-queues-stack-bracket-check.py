# Guoliang | Original learning example
# Match brackets with a stack
# Python 3.12+ | Run: python stacks-queues-stack-bracket-check.py
def balanced(text):
    stack = []
    opening = {')': '(', ']': '[', '}': '{'}
    for char in text:
        if char in "([{":
            stack.append(char)
        elif char in opening:
            if not stack or stack.pop() != opening[char]:
                return False
    return not stack

print(balanced("([])"))
print(balanced("([)]"))
print(balanced("(("))
