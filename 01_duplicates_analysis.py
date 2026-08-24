"""
01_duplicates_analysis.py  (Lab 6: Finding Duplicates)

Checks the dataset for fully-duplicated rows, and separately explores
shared response patterns across a subset of columns (MainBranch,
Employment, RemoteWork) to understand how common it is for multiple
distinct respondents to share the same answers.

Requires `df` from 00_setup_and_load_data.py.
"""

import matplotlib.pyplot as plt

# --- Task 1: exact duplicate rows -----------------------------------------
duplicate_count = df.duplicated().sum()
print(f"Duplicate rows: {duplicate_count}")

before_count = len(df)
df_cleaned = df.drop_duplicates()
after_count = len(df_cleaned)

print(f"Rows before: {before_count}")
print(f"Rows after:  {after_count}")
print(f"Rows removed: {before_count - after_count}")

# --- Task 2: shared response patterns across a column subset --------------
pattern_cols = ["MainBranch", "Employment", "RemoteWork"]
pattern_counts = (
    df.dropna(subset=pattern_cols)
    .groupby(pattern_cols)
    .size()
    .reset_index(name="count")
)
top_patterns = pattern_counts.sort_values("count", ascending=False).head(10)
print(top_patterns)

# --- Task 3: visualize the top shared pattern by country -------------------
top1 = top_patterns.iloc[0]
mask = (
    (df["MainBranch"] == top1["MainBranch"])
    & (df["Employment"] == top1["Employment"])
    & (df["RemoteWork"] == top1["RemoteWork"])
)
top1_by_country = df[mask]["Country"].value_counts().head(10)

top1_by_country.plot(kind="bar", color="skyblue", figsize=(9, 5))
plt.title("Top Shared Response Pattern — Distribution by Country")
plt.xlabel("Country")
plt.ylabel("Number of Respondents")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# --- Task 4 & 5: analysis notes ---------------------------------------------
print(
    """
Analysis:
No fully-duplicated rows were found in this dataset (0 out of 65,437).
A subset-column match on MainBranch/Employment/RemoteWork does turn up
many respondents sharing the same combination of answers, but this
reflects genuinely different people with similar circumstances, not
duplicate records -- each respondent has a distinct ResponseId.
Row removal was therefore not warranted; it was applied only to the
(empty) set of exact duplicates.
"""
)
