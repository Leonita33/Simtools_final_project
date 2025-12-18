from simulation import run_simulation
from impact_analysis import analyze_impact, train_impact_model
import pandas as pd 
import os 

if __name__ == "__main__":

    print("\n=== START MONTE-CARLO-SIMULATION ===")

    # 1) Start simulation
    df = run_simulation()

    print("\nMonte-Carlo simulation successfully completed.")

    # Ensure that year is an integer
    df["year"] = df["year"].astype(int)

    # Show selected years
    selected_years = [1995, 2005, 2015, 2025]
    filtered = df[df["year"].isin(selected_years)]

    print("\n--- Time series selection ---")
    print(filtered)

    print("\nResults saved under 'data/results/time_series_key_figures_1995_2025.csv'")

    print("\n=== START Impact Analysis ===")

    # 2) Start impact analysis
    df_sens = analyze_impact(n=3000, random_state=42)
    importances = train_impact_model(df_sens, debt_threshold=500)

    print("\nImpact analysis successfully completed.")

    print("\n--- Strength of influencing factors on the risk of over-indebtedness ---")
    print(importances)

    # Save results
    os.makedirs("data/results", exist_ok=True)
    importance_path = "data/results/factors_influencing_over-indebtedness.csv"
    importances.index.name = "parameter"
    importances.to_csv(
        importance_path,
        header=["importance"]
    )

    print(f"\nResults saved under {importance_path}")
    print("\n=== PROGRAM ENDED ===")