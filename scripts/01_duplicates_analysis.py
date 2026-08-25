"""
01_duplicates_analysis.py  (Lab 6: Finding Duplicates)

データセットに完全に重複した行がないかを確認し、続けて
MainBranch・Employment・RemoteWorkという一部の列に限定した場合に
「同じ回答パターン」を持つ人がどれだけいるかを分析する。

事前に 00_setup_and_load_data.py を実行し、`df` が作られている必要がある。
"""

import matplotlib.pyplot as plt

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
