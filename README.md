# Monte-Carlo simulation for the development of compulsive buying and debt (1995–2025)

## Project description

This project uses a **Monte-Carlo-simulation** to examine how compulsive buying and debt among **15- to 25-year-olds** may develop between **1995 and 2025**. In addition, an **impact analysis** is carried out to determine which factors have the greatest influence on the risk of over-indebtedness.

The simulation is based on **fictitious but plausible assumptions** and is not intended as a forecast, but rather to analyze **correlations and trends**.

---

## Questions

### questions 1 

**Which parameters have the greatest influence on the risk of over-indebtedness?**

→ Answered by an influence analysis (Random Forest Feature Importance).

### questions 2 

**How have key indicators (compulsive buying, debt) changed between 1995 and 2025?**

→ Answered by aggregated time series from the Monte Carlo simulation.

---

## Project structure

```
Simtools_final_project/
├── data/
│   └── results/
│       ├── factors_influencing_over-indebtedness.csv
│       ├── simulation_raw_data_all_runs.csv
│       └── time_series_key_figures_1995_2025.csv
|
├── notebook/
│   └── evaluation_shopping_addiction_debt.ipynb
|
├── src/
│   ├── impact_analysis.py    # question 1
│   ├── run.py                # Central execution
│   └── simulation.py         # question 2
│
├── README.md
└── requirements.txt
```

---

## Methodology

* Simulation of a population of 1,000 individuals per year
* Period: 1995–2025
* 30 independent Monte Carlo runs
* Factors taken into account:

  * income 
  * Compulsive buying / impulsiveness
  * credit availability
  * interest rate
  * marketing pressure

The results of all runs are aggregated and stored as a time series.

### Impact analysis

* Separate synthetic data generation
* Random forest classifier
* Target variable: Over-indebtedness (debts > defined threshold value)
* Output: Feature importances for evaluating the influence of individual parameters

---

## Results

### Results Question 1

The file `influencing_factors_overindebtedness.csv` contains the relative importance of the parameters examined. The analysis shows that:

* Income and addiction severity have the greatest influence
* Savings act as a buffer
* Interest rates are relevant, but less dominant

### Results Question 2

The file `time_series_key_figures_1995_2025.csv` contains the aggregated simulation results per year:

* Development of the prevalence of compulsive buying
* Average debt
* Proportion of heavily indebted individuals

These results are displayed graphically and interpreted in the notebook.

---

## Reproducibility

* Fixed random seeds are used
* Results are reproducible when the simulation is rerun
* Monte Carlo property is achieved through multiple random runs per year

---

## Use 

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Perform simulations and analyses:

```bash
python src/run.py
```

3. Analyze results:

* CSV files under `data/results/`
* Visualization in the notebook `notebook/evaluation_shopping_addiction_debts.ipynb`

---

## Restrictions

* All data and parameters are fictitious
* The model is used to analyze correlations, not to predict real developments
* Social, legal, and cultural factors are only represented in simplified form

---

## Conclusion

The project demonstrates how Monte-Carlo simulations and influence analyses can be combined to examine complex socioeconomic issues in a structured manner.
