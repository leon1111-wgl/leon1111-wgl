# Leon | Original learning example
# Adjust a connector, keep the feature
# Python 3.12+ | Run: python visual-instruction-tuning-frozen-feature.py
fixed_feature = 2.0
target = 1.0
for weight in [1.0, 0.75]:
    output = weight * fixed_feature
    error = output - target
    loss = error ** 2 / 2
    print(f"weight={weight:.2f}; feature={fixed_feature:.1f}; loss={loss:.3f}")
