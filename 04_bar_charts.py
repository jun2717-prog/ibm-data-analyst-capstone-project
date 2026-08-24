"""
04_bar_charts.py  (Lab 24: Bar Charts)

Distribution, relationship, composition, and comparison views built
with bar-style charts: histogram, box plot, scatter, bubble, and
several bar chart variants.

Requires `df` (with Age_numeric already added) from 00_setup_and_load_data.py.
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

# --- Task 1-1: Histogram of ConvertedCompYearly ------------------------------
comp_data = df["ConvertedCompYearly"].dropna()
comp_cap = comp_data.quantile(0.99)
comp_data_capped = comp_data[comp_data <= comp_cap]

plt.figure(figsize=(8, 5))
plt.hist(comp_data_capped, bins=40, color="skyblue", edgecolor="white")
plt.title("Distribution of Yearly Compensation")
plt.xlabel("Yearly Compensation (USD)")
plt.ylabel("Number of Respondents")
plt.tight_layout()
plt.show()

# --- Task 1-2: Box plot of Age -----------------------------------------------
age_data = df.dropna(subset=["Age_numeric"])
plt.figure(figsize=(6, 6))
plt.boxplot(age_data["Age_numeric"], vert=True)
plt.title("Box Plot of Age")
plt.ylabel("Age (numeric)")
plt.tight_layout()
plt.show()

# --- Task 2-1: Age vs. Compensation scatter ----------------------------------
scatter_data = df.dropna(subset=["Age_numeric", "ConvertedCompYearly"])
scatter_data = scatter_data[scatter_data["ConvertedCompYearly"] <= scatter_data["ConvertedCompYearly"].quantile(0.99)]

plt.figure(figsize=(8, 5))
plt.scatter(scatter_data["Age_numeric"], scatter_data["ConvertedCompYearly"], alpha=0.3, color="teal")
plt.title("Age vs. Compensation")
plt.xlabel("Age (numeric)")
plt.ylabel("Yearly Compensation (USD)")
plt.tight_layout()
plt.show()

# --- Task 2-2: Compensation vs. Job Satisfaction bubble (size = Age) --------
bubble_data = df.dropna(subset=["ConvertedCompYearly", "JobSatPoints_6", "Age_numeric"])
bubble_data = bubble_data[bubble_data["ConvertedCompYearly"] <= bubble_data["ConvertedCompYearly"].quantile(0.99)]

plt.figure(figsize=(9, 6))
plt.scatter(
    bubble_data["ConvertedCompYearly"], bubble_data["JobSatPoints_6"],
    s=bubble_data["Age_numeric"] * 2, alpha=0.25, color="mediumorchid",
)
plt.title("Compensation vs. Job Satisfaction (Bubble Size = Age)")
plt.xlabel("Yearly Compensation (USD)")
plt.ylabel("Job Satisfaction (JobSatPoints_6)")
plt.tight_layout()
plt.show()

# --- Task 3-1: Distribution of MainBranch (horizontal bar) ------------------
main_branch_counts = df["MainBranch"].value_counts()

plt.figure(figsize=(9, 5))
main_branch_counts.plot(kind="barh", color="cornflowerblue")
plt.title("Distribution of Respondents by Main Branch")
plt.xlabel("Number of Respondents")
plt.ylabel("Main Branch")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# --- Task 3-2: Top 10 languages respondents want to work with ---------------
def top_n(column_name, n=10):
    data = df[column_name].dropna()
    exploded = data.str.split(";").explode()
    return exploded.value_counts().head(n)

top10_languages_future = top_n("LanguageWantToWorkWith", 10)
top10_languages_future.plot(kind="bar", color="skyblue", figsize=(8, 5))
plt.title("Top 10 Programming Languages Respondents Want to Work With")
plt.xlabel("Programming Language")
plt.ylabel("Number of Respondents")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- Task 3-3: Median JobSatPoints_6/7 by age group (stacked bar) -----------
stacked_data = df.dropna(subset=["Age", "JobSatPoints_6", "JobSatPoints_7"])
stacked_summary = stacked_data.groupby("Age")[["JobSatPoints_6", "JobSatPoints_7"]].median()

stacked_summary.plot(kind="bar", stacked=True, figsize=(9, 5), color=["steelblue", "salmon"])
plt.title("Median JobSatPoints_6 and JobSatPoints_7 by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Median Score")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# --- Task 3-4: Top 10 databases in use (bar) ---------------------------------
top10_databases_current = top_n("DatabaseHaveWorkedWith", 10)
top10_databases_current.plot(kind="bar", color="lightgreen", figsize=(10, 5))
plt.title("Top 10 Databases Currently Used by Respondents")
plt.xlabel("Database")
plt.ylabel("Number of Respondents")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# --- Task 4-2: Top 15 countries by respondent count (horizontal bar) -------
country_counts = df["Country"].value_counts().head(15)

plt.figure(figsize=(9, 6))
country_counts.plot(kind="barh", color="goldenrod")
plt.title("Top 15 Countries by Respondent Count")
plt.xlabel("Number of Respondents")
plt.ylabel("Country")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
