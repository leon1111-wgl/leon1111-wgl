"""Fabricated parcel deliveries: one training window and four later weeks.

Every number is invented. The model predicts `late` (1 = the parcel arrived late).
"""
import numpy as np
from sklearn.linear_model import LogisticRegression

CARRIERS = np.array(["A", "B", "C"])
FEATURES = ["distance_km", "items", "hour", "order_value", "carrier"]


def make_window(n, seed, miles_share=0.0, order_scale=1.0, late_shift=0.0):
    """n deliveries. The keyword arguments are the things that can go wrong later:

    miles_share  share of rows whose distance now arrives in miles but is still called distance_km
    order_scale  prices went up by this factor
    late_shift   carriers are overloaded: more parcels are late for the same inputs
    """
    rs = np.random.RandomState(seed)
    distance = rs.lognormal(2.6, 0.7, n)
    items = rs.poisson(2.5, n) + 1
    hour = rs.randint(7, 22, n)
    order_value = rs.lognormal(3.4, 0.6, n)
    carrier = rs.choice(CARRIERS, n, p=[0.5, 0.3, 0.2])
    peak = (hour >= 17) & (hour <= 20)
    logit = (-3.2 + 0.8 * np.log(distance / 13.5) + 0.12 * (items - 3.5) + 0.7 * peak
             + 0.5 * (carrier == "B") + 0.9 * (carrier == "C") + late_shift)
    late = (rs.rand(n) < 1 / (1 + np.exp(-logit))).astype(int)

    reported = distance.copy()                       # what the pipeline writes down
    if miles_share:
        in_miles = rs.rand(n) < miles_share
        reported[in_miles] *= 0.621
    cols = {"distance_km": reported, "items": items, "hour": hour,
            "order_value": order_value * order_scale, "carrier": carrier}
    return cols, late


def design(cols):
    """The matrix the model sees. order_value is deliberately not one of its inputs."""
    return np.column_stack([
        np.log(cols["distance_km"]), cols["items"],
        ((cols["hour"] >= 17) & (cols["hour"] <= 20)).astype(float),
        cols["carrier"] == "B", cols["carrier"] == "C",
    ]).astype(float)


def fit_reference():
    """Train on the reference window. Returns the model, its data, and how much it relies on each feature."""
    cols, late = make_window(8000, seed=1)
    X = design(cols)
    model = LogisticRegression(max_iter=1000).fit(X, late)
    weight = np.abs(model.coef_[0]) * X.std(axis=0)           # size of each input's push on the logit
    reliance = {"distance_km": weight[0], "items": weight[1], "hour": weight[2],
                "order_value": 0.0, "carrier": weight[3] + weight[4]}
    return model, cols, late, reliance


def later_windows():
    """The four weeks after training, each with one thing different. Labels are all kept here;
    monitor.py decides whether to look at them."""
    return {
        "w1": make_window(2000, seed=2),
        "w2": make_window(2000, seed=3, order_scale=1.5),
        "w3": make_window(2000, seed=4, miles_share=0.9),
        "w4": make_window(2000, seed=5, late_shift=0.55),
    }
