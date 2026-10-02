# Guoliang | Original learning example
# Decode by waiting for a complete codeword
# Python 3.12+ | Run: python huffman-coding-prefix-code-decode.py
codes = {"A": "0", "B": "10", "C": "110", "D": "111"}
reverse = {bits: symbol for symbol, bits in codes.items()}
def decode(bits):
    pending = ""
    result = []
    for bit in bits:
        pending += bit
        if pending in reverse:
            result.append(reverse[pending])
            pending = ""
    if pending:
        raise ValueError("incomplete codeword")
    return "".join(result)
message = "ABCD"
encoded = "".join(codes[symbol] for symbol in message)
print("encoded:", encoded)
print("decoded:", decode(encoded))
try:
    decode("11")
except ValueError as error:
    print("rejected:", error)
