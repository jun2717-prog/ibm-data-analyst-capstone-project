"""
02_scatter_plots.py  (Lab 19: Scatter Plots)

Explores relationships between age, compensation, job satisfaction,
work experience, and programming language using scatter and bubble
plots.

Requires `df` from 00_setup_and_load_data.py.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Age -> numeric mapping (reused across scripts) -------------------------
AGE_MAP = {
    "Under 18 years old": 16,
    "18-24 years old": 21,
    "25-34 years old": 29.5,
    "35-44 years old": 39.5,
    "45-54 years old": 49.5,
    "55-64 years old": 59.5,
    "65 years or older": 70,
    "Prefer not to say": np.nan,
}
df["Age_numeric"] = df["Age"].map(AGE_MAP)

# --- Task 1-1: Age vs. Job Satisfaction -------------------------------------
d1 = df.dropna(subset=["Age", "JobSatPoints_6"])
plt.figure(figsize=(8, 5))
plt.scatter(d1["Age"], d1["JobSatPoints_6"], alpha=0.3, color="steelblue")
plt.title("Age vs. Job Satisfaction")
plt.xlabel("Age")
plt.ylabel("Job Satisfaction (JobSatPoints_6)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# --- Task 1-2: Compensation vs. Job Satisfaction ----------------------------
d2 = df.dropna(subset=["ConvertedCompYearly", "JobSatPoints_6"])
cap = d2["ConvertedCompYearly"].quantile(0.99)
d2 = d2[d2["ConvertedCompYearly"] <= cap]
plt.figure(figsize=(8, 5))
plt.scatter(d2["ConvertedCompYearly"], d2["JobSatPoints_6"], alpha=0.3, color="darkorange")
plt.title("Compensation vs. Job Satisfaction")
plt.xlabel("Yearly Compensation (USD)")
plt.ylabel("Job Satisfaction (JobSatPoints_6)")
plt.tight_layout()
plt.show()

# --- Task 2-1: Age vs. Job Satisfaction with trend line ---------------------
d3 = df.dropna(subset=["Age_numeric", "JobSatPoints_6"])
plt.figure(figsize=(8, 5))
plt.scatter(d3["Age_numeric"], d3["JobSatPoints_6"], alpha=0.3, color="steelblue")
z = np.polyfit(d3["Age_numeric"], d3["JobSatPoints_6"], 1)
p = np.poly1d(z)
x_line = np.linspace(d3["Age_numeric"].min(), d3["Age_numeric"].max(), 100)
plt.plot(x_line, p(x_line), color="red", linewidth=2, label="Trend Line")
plt.title("Age vs. Job Satisfaction (with Trend Line)")
plt.xlabel("Age (numeric)")
plt.ylabel("Job Satisfaction (JobSatPoints_6)")
plt.legend()
plt.tight_layout()
plt.show()

# --- Task 2-2: Age vs. Work Experience --------------------------------------
d4 = df.dropna(subset=["Age_numeric", "YearsCodePro"]).copy()
d4["YearsCodePro_numeric"] = pd.to_numeric(d4["YearsCodePro"], errors="coerce")
d4 = d4.dropna(subset=["YearsCodePro_numeric"])
plt.figure(figsize=(8, 5))
plt.scatter(d4["Age_numeric"], d4["YearsCodePro_numeric"], alpha=0.3, color="seagreen")
plt.title("Age vs. Work Experience")
plt.xlabel("Age (numeric)")
plt.ylabel("Years of Professional Coding Experience")
plt.tight_layout()
plt.show()

# --- Task 3-1: Compensation vs. Job Satisfaction bubble plot (size = Age) --
d5 = df.dropna(subset=["ConvertedCompYearly", "JobSatPoints_6", "Age_numeric"])
cap5 = d5["ConvertedCompYearly"].quantile(0.99)
d5 = d5[d5["ConvertedCompYearly"] <= cap5]
plt.figure(figsize=(9, 6))
plt.scatter(
    d5["ConvertedCompYearly"], d5["JobSatPoints_6"],
    s=d5["Age_numeric"] * 2, alpha=0.25, color="mediumpurple",
)
plt.title("Compensation vs. Job Satisfaction (Bubble Size = Age)")
plt.xlabel("Yearly Compensation (USD)")
plt.ylabel("Job Satisfaction (JobSatPoints_6)")
plt.tight_layout()
plt.show()

# --- Task 3-2: Average job satisfaction by top-10 language ------------------
lang_sat = df.dropna(subset=["LanguageHaveWorkedWith", "JobSatPoints_6"]).copy()
lang_sat["LanguageHaveWorkedWith"] = lang_sat["LanguageHaveWorkedWith"].str.split(";")
lang_sat = lang_sat.explode("LanguageHaveWorkedWith")

top10_langs = lang_sat["LanguageHaveWorkedWith"].value_counts().head(10).index
lang_sat_top10 = lang_sat[lang_sat["LanguageHaveWorkedWith"].isin(top10_langs)]
avg_sat_by_lang = (
    lang_sat_top10.groupby("LanguageHaveWorkedWith")["JobSatPoints_6"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 5))
plt.scatter(avg_sat_by_lang.index, avg_sat_by_lang.values, s=100, color="crimson")
plt.title("Average Job Satisfaction by Programming Language (Top 10)")
plt.xlabel("Programming Language")
plt.ylabel("Average Job Satisfaction (JobSatPoints_6)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
