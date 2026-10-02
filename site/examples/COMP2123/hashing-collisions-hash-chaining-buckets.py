# Guoliang | Original learning example
# Store colliding keys in one bucket
# Python 3.12+ | Run: python hashing-collisions-hash-chaining-buckets.py
buckets = [[] for _ in range(7)]
for key, value in [(10, "ten"), (17, "seventeen"), (24, "twenty-four")]:
    buckets[key % 7].append((key, value))
print("bucket 3:", buckets[3])
def lookup(key):
    for stored_key, value in buckets[key % 7]:
        if stored_key == key:
            return value
    return None
print("24:", lookup(24))
print("31:", lookup(31))
