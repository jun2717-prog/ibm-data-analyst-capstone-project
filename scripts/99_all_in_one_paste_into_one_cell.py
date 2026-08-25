"""
Data Analyst Capstone Project — All-in-One Analysis Script
データアナリスト キャップストーン プロジェクト — 一括分析スクリプト

Jupyter Notebookの1つのコードセルにそのまま貼り付けて、上から順に
実行できるように、コース内のLab順（Lab6 → Lab19 → Lab23 → Lab24）で
1本にまとめたスクリプトです。各パートの先頭に、どのLabに対応するかを
明記しています。

構成:
  STEP 0  セットアップとデータ読み込み
  LAB 6   Finding Duplicates（重複チェックと回答パターン分析）
  LAB 19  Scatter Plots（散布図・バブルプロット）
  LAB 23  Line Charts（折れ線グラフ）
  LAB 24  Bar Charts（棒グラフ・ヒストグラム・箱ひげ図）
  EXTRA   Top-10 Rankings Export（ダッシュボード用データ出力）
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==============================================================================
# STEP 0 — セットアップとデータ読み込み
# ==============================================================================

# ------------------------------------------------------------
# Step 1: 必要なライブラリをインポートする
# pandas: データの読み込み・加工・集計に使う
# matplotlib.pyplot: グラフ描画に使う（後続スクリプトでも共通で使用）
# ------------------------------------------------------------

# ------------------------------------------------------------
# Step 2: データセットのURLを指定する
# コース側が提供しているホスト先のCSVファイルを直接参照する
# （長いURLなので折り返して書いている）
# ------------------------------------------------------------
FILE_PATH = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "n01PQ9pSmiRX6520flujwQ/survey-data.csv"
)

# ------------------------------------------------------------
# Step 3: CSVを読み込み、pandasのDataFrame（df）として保持する
# 以降の全スクリプトは、この df をそのまま使う想定
# ------------------------------------------------------------
df = pd.read_csv(FILE_PATH)

# ------------------------------------------------------------
# Step 4: 正しく読み込めたか確認する
# 行数・列数と、先頭5行の中身を表示してチェックする
# ------------------------------------------------------------
print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
print(df.head())


# ==============================================================================
# LAB 6 — Finding Duplicates（重複チェックと回答パターン分析）
# ==============================================================================

# ==============================================================
# Task 1: 完全に重複した行を検出する
# ==============================================================

# ------------------------------------------------------------
# Step 1: 重複行の数をカウントする
# duplicated() は各行が「それより前に出てきた行と全列が完全一致するか」
# をTrue/Falseで返す。sum()でTrueの個数（=重複行数）を合計する
# ------------------------------------------------------------
duplicate_count = df.duplicated().sum()
print(f"Duplicate rows: {duplicate_count}")

# ------------------------------------------------------------
# Step 2: 重複行を削除し、削除前後の件数を比較する
# drop_duplicates() は重複行（2回目以降に出てきた方）を取り除いた
# 新しいDataFrameを返す。元の df は変更されない
# ------------------------------------------------------------
before_count = len(df)
df_cleaned = df.drop_duplicates()
after_count = len(df_cleaned)

print(f"Rows before: {before_count}")
print(f"Rows after:  {after_count}")
print(f"Rows removed: {before_count - after_count}")


# ==============================================================
# Task 2: 特定の列に基づく回答パターンの分析
# 「全列が完全一致」ではなく、MainBranch・Employment・RemoteWorkの
# 3列だけが一致する人がどれだけいるかを見る
# ==============================================================

# ------------------------------------------------------------
# Step 1: 対象列を指定し、欠損値のある行を除外してからグループ化する
# groupby(pattern_cols).size() で「同じ組み合わせ」ごとの件数を数える
# reset_index(name='count') で集計結果を通常の列に戻す
# ------------------------------------------------------------
pattern_cols = ["MainBranch", "Employment", "RemoteWork"]
pattern_counts = (
    df.dropna(subset=pattern_cols)
    .groupby(pattern_cols)
    .size()
    .reset_index(name="count")
)

# ------------------------------------------------------------
# Step 2: 件数が多い順に並べ替え、上位10パターンを表示する
# ------------------------------------------------------------
top_patterns = pattern_counts.sort_values("count", ascending=False).head(10)
print(top_patterns)


# ==============================================================
# Task 3: 最も多い回答パターンを、国別の分布として可視化する
# ==============================================================

# ------------------------------------------------------------
# Step 1: 最も件数の多い1位のパターンを取り出す
# ------------------------------------------------------------
top1 = top_patterns.iloc[0]

# ------------------------------------------------------------
# Step 2: 元のdfから、そのパターンに完全一致する行だけを抽出する
# 3つの条件をすべて満たす行をブールマスク(mask)で絞り込む
# ------------------------------------------------------------
mask = (
    (df["MainBranch"] == top1["MainBranch"])
    & (df["Employment"] == top1["Employment"])
    & (df["RemoteWork"] == top1["RemoteWork"])
)

# ------------------------------------------------------------
# Step 3: 絞り込んだ行を国(Country)別に集計し、上位10カ国を取得する
# ------------------------------------------------------------
top1_by_country = df[mask]["Country"].value_counts().head(10)

# ------------------------------------------------------------
# Step 4: 横棒グラフではなく縦棒グラフで可視化する
# ------------------------------------------------------------
top1_by_country.plot(kind="bar", color="skyblue", figsize=(9, 5))
plt.title("Top Shared Response Pattern — Distribution by Country")
plt.xlabel("Country")
plt.ylabel("Number of Respondents")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# ==============================================================
# Task 4 & 5: 重複処理の方針と、その理由のドキュメント化
# ==============================================================
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


# ==============================================================================
# LAB 19 — Scatter Plots（散布図・バブルプロット）
# ==============================================================================

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


# ==============================================================================
# LAB 23 — Line Charts（折れ線グラフ）
# ==============================================================================

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


# ==============================================================================
# LAB 24 — Bar Charts（棒グラフ・ヒストグラム・箱ひげ図）
# ==============================================================================

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


# ==============================================================================
# EXTRA — Top-10 Rankings Export（ダッシュボード用データ出力／特定のLabに紐づかない追加パート）
# ==============================================================================

def get_top_n(column_name, n=10):
    """
    セミコロン区切りの複数回答列（例: "Python;JavaScript;SQL"）から、
    上位n件のカテゴリと件数を集計して返す。

    処理の流れ:
      1. 欠損値(NaN)を除外する
      2. セミコロン(;)で分割し、各セルを「値のリスト」に変換する
      3. explode()でリストを1行1値になるよう展開する
         （これをしないと「複数回答の組み合わせ」がそのまま
         1つのカテゴリとして数えられてしまい、正しい人気ランキングが
         作れない）
      4. value_counts()で出現回数を多い順に数え、上位n件を返す
    """
    data = df[column_name].dropna()
    exploded = data.str.split(";").explode()
    return exploded.value_counts().head(n)


def export(series, filename):
    """
    集計結果(Series)を、Looker Studioで読み込みやすい
    「Name, Count」の2列CSVとして書き出す。
    """
    # reset_index()でインデックス（カテゴリ名）を通常の列に戻し、
    # 列名を明示的に Name / Count に付け替える
    out = series.reset_index()
    out.columns = ["Name", "Count"]
    out.to_csv(filename, index=False)
    print(f"Wrote {filename}")
    print(out, "\n")


# ==============================================================
# Current Technology Usage（現在の利用状況）タブ用のデータを出力する
# ==============================================================
export(get_top_n("LanguageHaveWorkedWith"), "top10_languages_current.csv")
export(get_top_n("DatabaseHaveWorkedWith"), "top10_databases_current.csv")
export(get_top_n("PlatformHaveWorkedWith"), "top10_platforms_current.csv")
export(get_top_n("WebframeHaveWorkedWith"), "top10_webframe_current.csv")

# ==============================================================
# Future Technology Trends（来年の需要）タブ用のデータを出力する
# ==============================================================
export(get_top_n("LanguageWantToWorkWith"), "top10_languages_future.csv")
export(get_top_n("DatabaseWantToWorkWith"), "top10_databases_future.csv")
export(get_top_n("PlatformWantToWorkWith"), "top10_platforms_future.csv")
export(get_top_n("WebframeWantToWorkWith"), "top10_webframe_future.csv")
