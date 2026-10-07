# Leon | Original learning example
# Count patches and comparisons
# Python 3.12+ | Run: python visual-tokens-patch-budget.py
height, width, channels = 32, 32, 3
for patch_size in [8, 4]:
    patches = (height // patch_size) * (width // patch_size)
    values = patch_size * patch_size * channels
    tokens = patches + 1
    print(f"P={patch_size}: patches={patches}, values={values}, pairs={tokens ** 2}")
