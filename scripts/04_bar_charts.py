"""
04_bar_charts.py  (Lab 24: Bar Charts)

分布(distribution)・関係性(relationship)・構成(composition)・
比較(comparison)の4つの観点から、ヒストグラム・箱ひげ図・散布図・
バブルプロット・各種棒グラフを作成する。

事前に 00_setup_and_load_data.py（と、可能であれば Age_numeric）が必要。
"""

import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Age_numeric が未作成の場合は、ここで作成する
# ------------------------------------------------------------
if "Age_numeric" not in df.columns:
    import numpy as np
    AGE_MAP = {
        "Under 18 years old": 16, "18-24 years old": 21, "25-34 years old": 29.5,
        "35-44 years old": 39.5, "45-54 years old": 49.5, "55-64 years old": 59.5,
        "65 years or older": 70, "Prefer not to say": np.nan,
    }
    df["Age_numeric"] = df["Age"].map(AGE_MAP)


# ==============================================================
# Task 1-1: ConvertedCompYearly（年収）の分布をヒストグラムで見る
# ==============================================================

# ------------------------------------------------------------
# Step 1: 欠損値を除外する
# ------------------------------------------------------------
comp_data = df["ConvertedCompYearly"].dropna()

# ------------------------------------------------------------
# Step 2: 上位1%の極端な高額報酬（外れ値）を除いて見やすくする
# ------------------------------------------------------------
comp_cap = comp_data.quantile(0.99)
comp_data_capped = comp_data[comp_data <= comp_cap]

# ------------------------------------------------------------
# Step 3: ヒストグラムを描画する
# bins=40で40本の区間（ビン）に分けて度数を集計する
# ------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.hist(comp_data_capped, bins=40, color="skyblue", edgecolor="white")
plt.title("Distribution of Yearly Compensation")
plt.xlabel("Yearly Compensation (USD)")
plt.ylabel("Number of Respondents")
plt.tight_layout()
plt.show()


# ==============================================================
# Task 1-2: Age（数値化した年齢）の箱ひげ図
# 箱ひげ図は、中央値・四分位範囲(IQR)・外れ値を一目で見られる
# ==============================================================

# ------------------------------------------------------------
# Step 1: 欠損値を除外する
# ------------------------------------------------------------
age_data = df.dropna(subset=["Age_numeric"])

# ------------------------------------------------------------
# Step 2: 箱ひげ図を描画する（vert=Trueで縦向きの箱にする）
# ------------------------------------------------------------
plt.figure(figsize=(6, 6))
plt.boxplot(age_data["Age_numeric"], vert=True)
plt.title("Box Plot of Age")
plt.ylabel("Age (numeric)")
plt.tight_layout()
plt.show()


# ==============================================================
# Task 2-1: Age_numeric と Compensation の関係を散布図で見る
# ==============================================================

# ------------------------------------------------------------
# Step 1: 欠損値を除外し、報酬の外れ値（上位1%）も除く
# ------------------------------------------------------------
scatter_data = df.dropna(subset=["Age_numeric", "ConvertedCompYearly"])
scatter_data = scatter_data[
    scatter_data["ConvertedCompYearly"] <= scatter_data["ConvertedCompYearly"].quantile(0.99)
]

# ------------------------------------------------------------
# Step 2: 散布図を描画する
# ------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.scatter(scatter_data["Age_numeric"], scatter_data["ConvertedCompYearly"], alpha=0.3, color="teal")
plt.title("Age vs. Compensation")
plt.xlabel("Age (numeric)")
plt.ylabel("Yearly Compensation (USD)")
plt.tight_layout()
plt.show()


# ==============================================================
# Task 2-2: Compensation × Job Satisfaction のバブルプロット
# バブルのサイズ(s)にAge_numericを使う
# ==============================================================

# ------------------------------------------------------------
# Step 1: 欠損値を除外し、報酬の外れ値（上位1%）も除く
# ------------------------------------------------------------
bubble_data = df.dropna(subset=["ConvertedCompYearly", "JobSatPoints_6", "Age_numeric"])
bubble_data = bubble_data[
    bubble_data["ConvertedCompYearly"] <= bubble_data["ConvertedCompYearly"].quantile(0.99)
]

# ------------------------------------------------------------
# Step 2: バブルプロットを描画する
# ------------------------------------------------------------
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


# ==============================================================
# Task 3-1: MainBranch（回答者の主な立場）の分布を横棒グラフで見る
# ==============================================================

# ------------------------------------------------------------
# Step 1: 各カテゴリの出現回数を集計する（多い順に自動で並ぶ）
# ------------------------------------------------------------
main_branch_counts = df["MainBranch"].value_counts()

# ------------------------------------------------------------
# Step 2: 横棒グラフ(barh)を描画する
# invert_yaxis()で、件数が多いカテゴリが上に来るようにする
# ------------------------------------------------------------
plt.figure(figsize=(9, 5))
main_branch_counts.plot(kind="barh", color="cornflowerblue")
plt.title("Distribution of Respondents by Main Branch")
plt.xlabel("Number of Respondents")
plt.ylabel("Main Branch")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()


# ==============================================================
# Task 3-2: 来年使いたい言語トップ10（縦棒グラフ）
# ==============================================================

def top_n(column_name, n=10):
    """
    セミコロン区切りの複数回答列から、上位n件のカテゴリと件数を
    集計して返すヘルパー関数。
    分割(split) → 展開(explode) → 集計(value_counts) の3ステップ。
    """
    data = df[column_name].dropna()
    exploded = data.str.split(";").explode()
    return exploded.value_counts().head(n)


# ------------------------------------------------------------
# LanguageWantToWorkWith（来年使いたい言語）の上位10件を集計・描画する
# ------------------------------------------------------------
top10_languages_future = top_n("LanguageWantToWorkWith", 10)
top10_languages_future.plot(kind="bar", color="skyblue", figsize=(8, 5))
plt.title("Top 10 Programming Languages Respondents Want to Work With")
plt.xlabel("Programming Language")
plt.ylabel("Number of Respondents")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ==============================================================
# Task 3-3: 年齢層別の JobSatPoints_6 / JobSatPoints_7 の中央値を
# 積み上げ棒グラフ(stacked bar)で比較する
# ==============================================================

# ------------------------------------------------------------
# Step 1: 欠損値を除外する
# ------------------------------------------------------------
stacked_data = df.dropna(subset=["Age", "JobSatPoints_6", "JobSatPoints_7"])

# ------------------------------------------------------------
# Step 2: 年齢層(Age)ごとに、2つのスコアの中央値を計算する
# ------------------------------------------------------------
stacked_summary = stacked_data.groupby("Age")[["JobSatPoints_6", "JobSatPoints_7"]].median()

# ------------------------------------------------------------
# Step 3: stacked=True で積み上げ棒グラフとして描画する
# ------------------------------------------------------------
stacked_summary.plot(kind="bar", stacked=True, figsize=(9, 5), color=["steelblue", "salmon"])
plt.title("Median JobSatPoints_6 and JobSatPoints_7 by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Median Score")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ==============================================================
# Task 3-4: 現在使われているデータベースの上位10件（縦棒グラフ）
# ==============================================================
top10_databases_current = top_n("DatabaseHaveWorkedWith", 10)
top10_databases_current.plot(kind="bar", color="lightgreen", figsize=(10, 5))
plt.title("Top 10 Databases Currently Used by Respondents")
plt.xlabel("Database")
plt.ylabel("Number of Respondents")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ==============================================================
# Task 4-2: 回答者数が多い上位15カ国（横棒グラフ）
# ==============================================================

# ------------------------------------------------------------
# Step 1: 国(Country)ごとの回答者数を集計し、上位15件に絞る
# ------------------------------------------------------------
country_counts = df["Country"].value_counts().head(15)

# ------------------------------------------------------------
# Step 2: 横棒グラフを描画する
# ------------------------------------------------------------
plt.figure(figsize=(9, 6))
country_counts.plot(kind="barh", color="goldenrod")
plt.title("Top 15 Countries by Respondent Count")
plt.xlabel("Number of Respondents")
plt.ylabel("Country")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
