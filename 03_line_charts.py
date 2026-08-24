"""
03_line_charts.py  (Lab 23: Line Charts)

Tracks how compensation and job satisfaction change across age and
professional experience.

Requires `df` (with Age_numeric already added by 02_scatter_plots.py,
or recompute it here) from 00_setup_and_load_data.py.
"""

import pandas as pd
import matplotlib.pyplot as plt

if "Age_numeric" not in df.columns:
    import numpy as np
    AGE_MAP = {
        "Under 18 years old": 16, "18-24 years old": 21, "25-34 years old": 29.5,
        "35-44 years old": 39.5, "45-54 years old": 49.5, "55-64 years old": 59.5,
        "65 years or older": 70, "Prefer not to say": np.nan,
    }
    df["Age_numeric"] = df["Age"].map(AGE_MAP)

# --- Task 1-1: Median compensation by age group -----------------------------
age_comp = df.dropna(subset=["Age_numeric", "ConvertedCompYearly"])
median_comp_by_age = age_comp.groupby("Age_numeric")["ConvertedCompYearly"].median().sort_index()

plt.figure(figsize=(8, 5))
plt.plot(median_comp_by_age.index, median_comp_by_age.values, marker="o", color="steelblue")
plt.title("Median Compensation by Age Group")
plt.xlabel("Age (numeric)")
plt.ylabel("Median Yearly Compensation (USD)")
plt.tight_layout()
plt.show()

# --- Task 1-2: Median compensation, ages 25-45 -------------------------------
age_comp_2545 = age_comp[(age_comp["Age_numeric"] >= 25) & (age_comp["Age_numeric"] <= 45)]
median_comp_2545 = age_comp_2545.groupby("Age_numeric")["ConvertedCompYearly"].median().sort_index()

plt.figure(figsize=(8, 5))
plt.plot(median_comp_2545.index, median_comp_2545.values, marker="o", color="darkorange")
plt.title("Median Compensation by Age (25-45 years old)")
plt.xlabel("Age (numeric)")
plt.ylabel("Median Yearly Compensation (USD)")
plt.tight_layout()
plt.show()

# --- Task 2/3: Satisfaction and compensation by years of experience --------
exp = df.copy()
exp["YearsCodePro_numeric"] = pd.to_numeric(exp["YearsCodePro"], errors="coerce")

exp_sat = exp.dropna(subset=["YearsCodePro_numeric", "JobSatPoints_6"])
median_sat_by_exp = exp_sat.groupby("YearsCodePro_numeric")["JobSatPoints_6"].median().sort_index()

plt.figure(figsize=(8, 5))
plt.plot(median_sat_by_exp.index, median_sat_by_exp.values, marker="o", color="seagreen")
plt.title("Job Satisfaction by Years of Professional Experience")
plt.xlabel("Years of Professional Coding Experience")
plt.ylabel("Median Job Satisfaction (JobSatPoints_6)")
plt.tight_layout()
plt.show()

exp_comp = exp.dropna(subset=["YearsCodePro_numeric", "ConvertedCompYearly"])
median_comp_by_exp = exp_comp.groupby("YearsCodePro_numeric")["ConvertedCompYearly"].median().sort_index()

plt.figure(figsize=(8, 5))
plt.plot(median_comp_by_exp.index, median_comp_by_exp.values, marker="o", color="purple")
plt.title("Median Compensation by Years of Professional Experience")
plt.xlabel("Years of Professional Coding Experience")
plt.ylabel("Median Yearly Compensation (USD)")
plt.tight_layout()
plt.show()
