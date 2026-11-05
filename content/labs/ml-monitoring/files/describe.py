"""What the model is, what it relies on, and what each later week is supposed to contain."""
from world import FEATURES, design, fit_reference, later_windows

model, cols, late, reliance = fit_reference()
score = model.predict_proba(design(cols))[:, 1]
print(f"training window: {len(late)} deliveries, late rate {late.mean():.3f}, mean predicted {score.mean():.3f}")
print("\nhow much each input moves the model (|coefficient| x spread; 0 = not an input)")
for feature in FEATURES:
    print(f"  {feature:<12} {reliance[feature]:.2f}")

print("\nlater weeks (what the fabricated process did in each)")
for name, (_, week_late) in later_windows().items():
    print(f"  {name}: {len(week_late)} deliveries, true late rate {week_late.mean():.3f}")
print("The monitoring job is not told what changed. That is the point.")
