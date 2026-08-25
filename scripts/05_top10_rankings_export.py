"""
05_top10_rankings_export.py

プログラミング言語・データベース・プラットフォーム・Webフレームワークの
「現在の利用状況」と「来年の需要」について、それぞれ上位10件を集計し、
Looker Studioのデータソースとして使える、シンプルな2列（Name, Count）の
CSVファイルとして出力する。

事前に 00_setup_and_load_data.py を実行し、`df` が作られている必要がある。
"""

import pandas as pd


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
