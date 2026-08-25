"""
03_line_charts.py  (Lab 23: Line Charts)

年齢層および実務経験年数に応じて、報酬(compensation)と
仕事満足度(job satisfaction)がどのように変化するかを
折れ線グラフで追跡する。

事前に 00_setup_and_load_data.py（と、可能であれば
02_scatter_plots.py で作成済みの Age_numeric）が必要。
Age_numeric が無ければ、このスクリプト内で作成する。
"""

import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Age_numeric が未作成の場合は、ここで作成する
# （02_scatter_plots.py と同じ変換ロジック）
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
# Task 1-1: 年齢層(Age_numeric)ごとの報酬の中央値を折れ線グラフにする
# ==============================================================

# ------------------------------------------------------------
# Step 1: 欠損値を除外する
# ------------------------------------------------------------
age_comp = df.dropna(subset=["Age_numeric", "ConvertedCompYearly"])

# ------------------------------------------------------------
# Step 2: Age_numericでグループ化し、各年齢の報酬の中央値を計算する
# 平均値ではなく中央値(median)を使うのは、高額報酬の外れ値に
# 引っ張られにくく、実態に近い代表値になるため
# sort_index()でx軸（年齢）が小さい順に並ぶようにする
# ------------------------------------------------------------
median_comp_by_age = age_comp.groupby("Age_numeric")["ConvertedCompYearly"].median().sort_index()

# ------------------------------------------------------------
# Step 3: 折れ線グラフを描画する（marker='o'で各点を丸印で表示）
# ------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.plot(median_comp_by_age.index, median_comp_by_age.values, marker="o", color="steelblue")
plt.title("Median Compensation by Age Group")
plt.xlabel("Age (numeric)")
plt.ylabel("Median Yearly Compensation (USD)")
plt.tight_layout()
plt.show()


# ==============================================================
# Task 1-2: 25〜45歳に絞り込んだ場合の報酬中央値の推移
# 若手〜中堅層の変化だけをより詳しく見るための拡大版
# ==============================================================

# ------------------------------------------------------------
# Step 1: Age_numericが25以上45以下の行だけに絞り込む
# ------------------------------------------------------------
age_comp_2545 = age_comp[(age_comp["Age_numeric"] >= 25) & (age_comp["Age_numeric"] <= 45)]

# ------------------------------------------------------------
# Step 2: 同様に年齢ごとの報酬中央値を計算する
# ------------------------------------------------------------
median_comp_2545 = age_comp_2545.groupby("Age_numeric")["ConvertedCompYearly"].median().sort_index()

# ------------------------------------------------------------
# Step 3: 折れ線グラフを描画する
# ------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.plot(median_comp_2545.index, median_comp_2545.values, marker="o", color="darkorange")
plt.title("Median Compensation by Age (25-45 years old)")
plt.xlabel("Age (numeric)")
plt.ylabel("Median Yearly Compensation (USD)")
plt.tight_layout()
plt.show()


# ==============================================================
# Task 2-1 & 3-1: 実務経験年数(YearsCodePro)ごとの
# 満足度・報酬の中央値の推移
# ==============================================================

# ------------------------------------------------------------
# Step 1: YearsCodeProを数値に変換する
# "Less than 1 year"のような文字列はerrors='coerce'でNaNになる
# ------------------------------------------------------------
exp = df.copy()
exp["YearsCodePro_numeric"] = pd.to_numeric(exp["YearsCodePro"], errors="coerce")

# ------------------------------------------------------------
# Step 2: 満足度（JobSatPoints_6）側の推移を計算・描画する
# ------------------------------------------------------------
exp_sat = exp.dropna(subset=["YearsCodePro_numeric", "JobSatPoints_6"])
median_sat_by_exp = exp_sat.groupby("YearsCodePro_numeric")["JobSatPoints_6"].median().sort_index()

plt.figure(figsize=(8, 5))
plt.plot(median_sat_by_exp.index, median_sat_by_exp.values, marker="o", color="seagreen")
plt.title("Job Satisfaction by Years of Professional Experience")
plt.xlabel("Years of Professional Coding Experience")
plt.ylabel("Median Job Satisfaction (JobSatPoints_6)")
plt.tight_layout()
plt.show()

# ------------------------------------------------------------
# Step 3: 報酬（ConvertedCompYearly）側の推移も同様に計算・描画する
# ------------------------------------------------------------
exp_comp = exp.dropna(subset=["YearsCodePro_numeric", "ConvertedCompYearly"])
median_comp_by_exp = exp_comp.groupby("YearsCodePro_numeric")["ConvertedCompYearly"].median().sort_index()

plt.figure(figsize=(8, 5))
plt.plot(median_comp_by_exp.index, median_comp_by_exp.values, marker="o", color="purple")
plt.title("Median Compensation by Years of Professional Experience")
plt.xlabel("Years of Professional Coding Experience")
plt.ylabel("Median Yearly Compensation (USD)")
plt.tight_layout()
plt.show()
