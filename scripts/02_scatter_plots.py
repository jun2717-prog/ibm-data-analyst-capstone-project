"""
02_scatter_plots.py  (Lab 19: Scatter Plots)

年齢・報酬・仕事満足度・実務経験年数・プログラミング言語の関係性を、
散布図とバブルプロットで可視化する。

事前に 00_setup_and_load_data.py を実行し、`df` が作られている必要がある。
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==============================================================
# 事前準備: Age列（文字列カテゴリ）を数値に変換する
# 例: "25-34 years old" のような文字列は、そのままでは
# 散布図の軸や回帰計算に使えないため、各区分の中央値に近い
# 数値へ変換した Age_numeric 列を新たに作る
# ==============================================================
AGE_MAP = {
    "Under 18 years old": 16,
    "18-24 years old": 21,
    "25-34 years old": 29.5,
    "35-44 years old": 39.5,
    "45-54 years old": 49.5,
    "55-64 years old": 59.5,
    "65 years or older": 70,
    "Prefer not to say": np.nan,  # 数値化できないためNaN扱い
}
df["Age_numeric"] = df["Age"].map(AGE_MAP)


# ==============================================================
# Task 1-1: Age（文字列カテゴリ）とJob Satisfactionの散布図
# ==============================================================

# ------------------------------------------------------------
# Step 1: 欠損値がある行を除いた作業用データを作る
# ------------------------------------------------------------
d1 = df.dropna(subset=["Age", "JobSatPoints_6"])

# ------------------------------------------------------------
# Step 2: 散布図を描画する
# alpha=0.3で点を半透明にし、重なりの密度が見やすいようにしている
# ------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.scatter(d1["Age"], d1["JobSatPoints_6"], alpha=0.3, color="steelblue")
plt.title("Age vs. Job Satisfaction")
plt.xlabel("Age")
plt.ylabel("Job Satisfaction (JobSatPoints_6)")
plt.xticks(rotation=45, ha="right")  # ラベルが重ならないよう斜めに表示
plt.tight_layout()
plt.show()


# ==============================================================
# Task 1-2: Compensation（報酬）とJob Satisfactionの散布図
# ==============================================================

# ------------------------------------------------------------
# Step 1: 欠損値を除外する
# ------------------------------------------------------------
d2 = df.dropna(subset=["ConvertedCompYearly", "JobSatPoints_6"])

# ------------------------------------------------------------
# Step 2: 極端な高額報酬（外れ値）を除いて見やすくする
# quantile(0.99) で「上位1%を除いた境界値」を求め、それ以下に絞り込む
# ------------------------------------------------------------
cap = d2["ConvertedCompYearly"].quantile(0.99)
d2 = d2[d2["ConvertedCompYearly"] <= cap]

# ------------------------------------------------------------
# Step 3: 散布図を描画する
# ------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.scatter(d2["ConvertedCompYearly"], d2["JobSatPoints_6"], alpha=0.3, color="darkorange")
plt.title("Compensation vs. Job Satisfaction")
plt.xlabel("Yearly Compensation (USD)")
plt.ylabel("Job Satisfaction (JobSatPoints_6)")
plt.tight_layout()
plt.show()


# ==============================================================
# Task 2-1: Age_numeric（数値化した年齢）とJob Satisfaction
# 散布図に回帰トレンドライン（傾向線）を追加する
# ==============================================================

# ------------------------------------------------------------
# Step 1: 欠損値を除外する
# ------------------------------------------------------------
d3 = df.dropna(subset=["Age_numeric", "JobSatPoints_6"])

# ------------------------------------------------------------
# Step 2: 散布図の土台を描画する
# ------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.scatter(d3["Age_numeric"], d3["JobSatPoints_6"], alpha=0.3, color="steelblue")

# ------------------------------------------------------------
# Step 3: 1次関数（直線）で回帰式を求める
# np.polyfit(x, y, 1) は「1次式（傾き・切片）」を最小二乗法で求める
# 結果として poly1d オブジェクト p を作り、任意のxに対するyを計算できる
# ------------------------------------------------------------
z = np.polyfit(d3["Age_numeric"], d3["JobSatPoints_6"], 1)
p = np.poly1d(z)

# ------------------------------------------------------------
# Step 4: 回帰直線をなめらかに描くため、x軸の範囲を100分割した点を作り
# それぞれのy値(p(x))を計算して線として重ねて描画する
# ------------------------------------------------------------
x_line = np.linspace(d3["Age_numeric"].min(), d3["Age_numeric"].max(), 100)
plt.plot(x_line, p(x_line), color="red", linewidth=2, label="Trend Line")

plt.title("Age vs. Job Satisfaction (with Trend Line)")
plt.xlabel("Age (numeric)")
plt.ylabel("Job Satisfaction (JobSatPoints_6)")
plt.legend()
plt.tight_layout()
plt.show()


# ==============================================================
# Task 2-2: Age_numeric と実務経験年数(YearsCodePro)の散布図
# ==============================================================

# ------------------------------------------------------------
# Step 1: 欠損値を除外し、作業用にコピーを作る
# ------------------------------------------------------------
d4 = df.dropna(subset=["Age_numeric", "YearsCodePro"]).copy()

# ------------------------------------------------------------
# Step 2: YearsCodeProは "Less than 1 year" のような文字列を含むため、
# pd.to_numeric(errors='coerce') で数値に変換できないものはNaNにする
# ------------------------------------------------------------
d4["YearsCodePro_numeric"] = pd.to_numeric(d4["YearsCodePro"], errors="coerce")
d4 = d4.dropna(subset=["YearsCodePro_numeric"])  # 変換できなかった行を除外

# ------------------------------------------------------------
# Step 3: 散布図を描画する
# ------------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.scatter(d4["Age_numeric"], d4["YearsCodePro_numeric"], alpha=0.3, color="seagreen")
plt.title("Age vs. Work Experience")
plt.xlabel("Age (numeric)")
plt.ylabel("Years of Professional Coding Experience")
plt.tight_layout()
plt.show()


# ==============================================================
# Task 3-1: Compensation × Job Satisfaction のバブルプロット
# バブルのサイズ(s)にAge_numericを使い、年齢の情報も同時に表現する
# ==============================================================

# ------------------------------------------------------------
# Step 1: 欠損値を除外し、報酬の外れ値（上位1%）も除く
# ------------------------------------------------------------
d5 = df.dropna(subset=["ConvertedCompYearly", "JobSatPoints_6", "Age_numeric"])
cap5 = d5["ConvertedCompYearly"].quantile(0.99)
d5 = d5[d5["ConvertedCompYearly"] <= cap5]

# ------------------------------------------------------------
# Step 2: バブルプロットを描画する
# s=d5['Age_numeric']*2 でバブルの面積を年齢に比例させる
# ------------------------------------------------------------
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


# ==============================================================
# Task 3-2: 上位10言語ごとの平均満足度を散布図で比較する
# LanguageHaveWorkedWithは「Python;JavaScript;SQL」のように
# セミコロン区切りで複数値が入っているため、まず分解が必要
# ==============================================================

# ------------------------------------------------------------
# Step 1: 欠損値を除外し、セミコロンで分割してリスト化する
# ------------------------------------------------------------
lang_sat = df.dropna(subset=["LanguageHaveWorkedWith", "JobSatPoints_6"]).copy()
lang_sat["LanguageHaveWorkedWith"] = lang_sat["LanguageHaveWorkedWith"].str.split(";")

# ------------------------------------------------------------
# Step 2: explode()でリストを1行1言語になるよう展開する
# これをしないと「言語ごと」の集計ができない
# ------------------------------------------------------------
lang_sat = lang_sat.explode("LanguageHaveWorkedWith")

# ------------------------------------------------------------
# Step 3: 出現回数が多い上位10言語だけに絞り込む
# ------------------------------------------------------------
top10_langs = lang_sat["LanguageHaveWorkedWith"].value_counts().head(10).index
lang_sat_top10 = lang_sat[lang_sat["LanguageHaveWorkedWith"].isin(top10_langs)]

# ------------------------------------------------------------
# Step 4: 言語ごとに満足度の平均値を計算し、高い順に並べる
# ------------------------------------------------------------
avg_sat_by_lang = (
    lang_sat_top10.groupby("LanguageHaveWorkedWith")["JobSatPoints_6"]
    .mean()
    .sort_values(ascending=False)
)

# ------------------------------------------------------------
# Step 5: 散布図（1言語=1点）として可視化する
# ------------------------------------------------------------
plt.figure(figsize=(9, 5))
plt.scatter(avg_sat_by_lang.index, avg_sat_by_lang.values, s=100, color="crimson")
plt.title("Average Job Satisfaction by Programming Language (Top 10)")
plt.xlabel("Programming Language")
plt.ylabel("Average Job Satisfaction (JobSatPoints_6)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
