import numpy as np
import pandas as pd 
from sklearn.ensemble import RandomForestClassifier

def analyze_impact(n=2000, random_state=42):
    """
    Generates synthetic data for simplified impact analysis.
    Objective: Over-indebtedness risk (debt > threshold) as a function of parameters.
    """
    rng = np.random.default_rng(random_state)
    data = []

    for _ in range(n):
        addiction_strength = rng.uniform(0.5, 2.0)
        income = rng.uniform(1200, 3000)
        interest_rate = rng.uniform(0.01, 0.15)

        base_spending = rng.uniform(800, 1800)
        savings_buffer = rng.uniform(0, 1000)
        shock = rng.normal(0, 150)

        spending = base_spending * (1 + 0.6 * (addiction_strength - 1))
        borrow_need = max(0, spending + shock - income - 0.3 * savings_buffer)
        debt = borrow_need * (1 + interest_rate)

        data.append([addiction_strength, income, interest_rate, savings_buffer, debt])

    return pd.DataFrame(data, columns=[
        "addiction_strength",
        "income",
        "interest_rate",
        "savings_buffer",
        "debt"
    ])

def train_impact_model(df, debt_threshold=500, random_state=42, n_estimators=400):
    """
    Trains a RandomForestClassifier on over-indebtedness (debt > threshold)
    and returns the influence of the parameters on the risk of over-indebtedness.
    """
    X = df[["addiction_strength", "income", "interest_rate", "savings_buffer"]]
    y = (df["debt"] > debt_threshold).astype(int)

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=random_state
    )
    model.fit(X, y)

    importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    return importances