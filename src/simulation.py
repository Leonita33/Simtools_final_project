import numpy as np 
import pandas as pd 
import os 

# Help function 
def logistic(x):
    return 1 / (1 + np.exp(-x))

# Main function: complete simulation 
def run_simulation(
        years=range(1995,2026),
        population=1000,
        runs=30,
        output_dir="data/results"
):
    
    # Create folder
    os.makedirs(output_dir, exist_ok=True)

    results = []

    # Generate fictitious macro variables
    years_array = np.array(list(years))
    n_years = len(years_array)

    interest_rates = np.clip(
        0.06 - 0.05 * (np.linspace(0,1,n_years)**1.4),
        0.01, 0.12
    )

    credit_availability = np.clip(
        0.3 + 0.5 * (np.linspace(0,1,n_years)),
        0.1, 0.95
    )

    marketing_index = np.clip(
        0.2 + 0.8 * ((years_array - 1995) / (2025 - 1995))**1.5,
        0, 1
    )

    # Parameters for the simulation
    w_income = -0.00025
    w_interest = 2.0 
    w_credit = 1.5 
    w_marketing = 1.8 
    w_peer = 1.2 
    baseline_addiction = -3.0 

    # Run simulation
    columns = [
        "year", "run", "addiction_rate", "mean_debt", "pct_over_50"
    ]

    for run in range(runs):
        np.random.seed(42 + run)

        # Characteristics of individuals 
        impulsivity = np.random.normal(0.0, 0.7, population)
        selfcontrol = np.random.normal(0.0, 0.7, population)
        debts = np.zeros(population)

        addicted = np.zeros(population, dtype=bool)

        for i, year in enumerate(years_array):

            incomes = np.random.normal(2000 + i * 40, 200, population)
            incomes = np.maximum(incomes, 500)

            peer = np.random.normal(0, 0.5, population)

            logit = (
                baseline_addiction + 
                w_marketing * marketing_index[i] +
                w_credit * credit_availability[i] +
                w_interest * interest_rates[i] + 
                w_income * incomes +
                w_peer * peer +
                0.9 * impulsivity -
                1.1 * selfcontrol
            )

            p_add = logistic(logit)

            new_addicted = np.random.rand(population) < p_add
            addicted = addicted | new_addicted

            spend_fraction = 0.75 + 0.05 * impulsivity - 0.04 * selfcontrol
            spend_fraction = np.clip(spend_fraction, 0.3, 0.95)

            extra_mult = 1 + addicted.astype(float) * 0.5
            spend = incomes * spend_fraction * extra_mult

            diff = spend - incomes
            diff[diff < 0] = 0 

            borrow_prob = credit_availability[i]
            borrowed = diff * (np.random.rand(population) < borrow_prob)

            debts += borrowed
            debts *= (1 + interest_rates[i])

            pct_over_50 = np.mean(debts > 0.5 * incomes)

            results.append([
                year,
                run,
                addicted.mean(),
                debts.mean(),
                pct_over_50
            ])

    df_results = pd.DataFrame(results, columns=columns)

    df_agg = (
        df_results
        .groupby("year")[["addiction_rate", "mean_debt", "pct_over_50"]]
        .mean()
        .reset_index()
    )

    raw_path = os.path.join(output_dir, "simulation_raw_data_all_runs.csv")
    agg_path = os.path.join(output_dir, "time_series_key_figures_1995_2025.csv")

    df_results.to_csv(raw_path, index=False)
    df_agg.to_csv(agg_path, index=False)

    return df_agg

if __name__ == "__main__":
    run_simulation()