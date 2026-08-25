# Data Analyst Capstone Project
# データアナリスト キャップストーン プロジェクト

Analysis of the Stack Overflow Developer Survey to identify current
and emerging trends in programming languages, databases, and web
technologies — data cleaning, exploratory analysis, visualization,
and an interactive dashboard.

Stack Overflow Developer Survey を分析し、プログラミング言語・データベース・
Web技術における現在および新興のトレンドを明らかにするプロジェクトです。
データクリーニング、探索的分析、可視化、インタラクティブダッシュボードまでを
含みます。

---

## Overview / 概要

| | |
|---|---|
| **Dataset / データセット** | Stack Overflow Developer Survey (`survey-data.csv`) |
| **Size / 規模** | 65,437 respondents / 65,437人の回答, 114 fields / 114項目 |
| **Tools / 使用ツール** | Python (pandas, matplotlib), Google Looker Studio |
| **Duplicate rows found / 重複行** | 0 |

This project follows a standard data analysis workflow / 本プロジェクトは、以下の一般的なデータ分析ワークフローに沿って進めています:

1. **Data collection / データ収集** — loading the survey CSV directly from a hosted URL
   調査データのCSVをホスト先URLから直接読み込み
2. **Data cleaning / データクリーニング** — duplicate checks, response-pattern analysis, multi-value parsing
   重複チェック、回答パターン分析、複数値フィールドの分解
3. **Exploratory data analysis / 探索的データ分析** — distributions, outliers, relationships between variables
   分布・外れ値・変数間の関係性の分析
4. **Visualization / 可視化** — histograms, box plots, scatter/bubble plots, bar/line/stacked charts
   ヒストグラム、箱ひげ図、散布図・バブルチャート、棒グラフ・折れ線グラフ・積み上げグラフ
5. **Dashboard / ダッシュボード** — an interactive 3-tab Google Looker Studio dashboard
   3タブ構成のインタラクティブなGoogle Looker Studioダッシュボード

---

## Repository Structure / リポジトリ構成

```
.
├── README.md                          This file / 本ファイル
├── notebook/
│   └── data_analyst_capstone_analysis.ipynb   Full analysis notebook / 分析ノートブック一式
├── scripts/                           Same analysis as standalone .py files / 同内容をスクリプト単体でも用意
│   ├── 00_setup_and_load_data.py
│   ├── 01_duplicates_analysis.py      (Lab 6)
│   ├── 02_scatter_plots.py            (Lab 19)
│   ├── 03_line_charts.py              (Lab 23)
│   ├── 04_bar_charts.py               (Lab 24)
│   └── 05_top10_rankings_export.py
└── dashboard/
    └── README.md                      Dashboard structure & screenshot guide / ダッシュボード構成とスクリーンショット案内
```

The notebook (`notebook/data_analyst_capstone_analysis.ipynb`) is the
main deliverable — it contains the same analysis as the `scripts/`
folder, organized into one file with bilingual markdown section
headers, in the order it should be run.

メインの成果物は `notebook/data_analyst_capstone_analysis.ipynb` です。
`scripts/` フォルダと同じ内容を、実行順に沿って1つのファイルにまとめ、
日英併記のMarkdown見出しを付けたものです。

The PowerPoint / presentation report is being built separately and
is not included in this repository.

パワーポイント（プレゼンテーション）は別途作成中のため、本リポジトリには
含まれていません。

---

## Key Findings / 主な発見

- **JavaScript** is the most-used language today (37,492 respondents), but **Python** is the #1 language developers want to use next year — overtaking JavaScript.
  **JavaScript** は現在最も使われている言語（37,492人）だが、来年最も使いたい言語は **Python** が1位となり、JavaScriptを上回った。

- **PostgreSQL** leads both current use (25,536) and future demand (24,005) among databases, while commercial databases like Microsoft SQL Server are declining in relative demand.
  データベースでは **PostgreSQL** が現在利用（25,536人）・将来需要（24,005人）ともに首位である一方、Microsoft SQL Serverなど商用データベースの相対需要は低下している。

- **Rust** and **Go** enter the future top-10 languages despite not appearing in the current top-10, signaling rising interest in systems programming.
  **Rust** と **Go** は現在のトップ10には入っていないが、将来のトップ10には登場しており、システムプログラミングへの関心の高まりを示している。

- The respondent base skews young: 41.3% are aged 25–34, and 15.9% are 18–24.
  回答者層は若年層に偏っており、41.3%が25〜34歳、15.9%が18〜24歳である。

- No fully-duplicated rows were found in the dataset (0 out of 65,437), though many respondents naturally share the same answers on a subset of columns (e.g. employment status).
  データセットに完全な重複行はなかった（65,437件中0件）。ただし一部の列（雇用形態など）に限れば、同じ回答を持つ人が自然に多数存在する。

---

## How to Reproduce / 再現方法

### Option A: Notebook / ノートブックを使う場合

Open `notebook/data_analyst_capstone_analysis.ipynb` in Jupyter (or
JupyterLite / Google Colab) and run all cells in order — each
markdown header explains what the following code cell does.

`notebook/data_analyst_capstone_analysis.ipynb` をJupyter
（またはJupyterLite / Google Colab）で開き、上から順にすべてのセルを
実行してください。各Markdown見出しに、続くコードセルの内容を説明しています。

### Option B: Standalone scripts / スクリプト単体で使う場合

```bash
pip install pandas matplotlib

python scripts/00_setup_and_load_data.py
python scripts/01_duplicates_analysis.py
python scripts/02_scatter_plots.py
python scripts/03_line_charts.py
python scripts/04_bar_charts.py
python scripts/05_top10_rankings_export.py
```

Each script after `00_setup_and_load_data.py` assumes `df` is already
loaded in the same session. If running them as standalone processes
rather than in one interactive session, prepend the contents of
`00_setup_and_load_data.py` to each.

`00_setup_and_load_data.py` 以降のスクリプトは、同一セッション内に
`df` が読み込まれていることを前提としています。1つのセッションで
連続実行せず個別のプロセスとして実行する場合は、各スクリプトの先頭に
`00_setup_and_load_data.py` の内容を追加してください。

---

## Dashboard / ダッシュボード

See [`dashboard/README.md`](dashboard/README.md) for details on the
Google Looker Studio dashboard structure and where to add
screenshots.

Google Looker Studioダッシュボードの構成やスクリーンショットの追加方法は
[`dashboard/README.md`](dashboard/README.md) を参照してください。

---

## Data Source / データ出典

Stack Overflow Developer Survey, provided as part of an IBM /
Coursera data analytics course:
`https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/n01PQ9pSmiRX6520flujwQ/survey-data.csv`

Stack Overflow Developer Survey（IBM / Coursera データ分析コースの教材として
提供）。データ取得元URLは上記の通りです。

---

## License / ライセンス

Add a license of your choice (e.g. MIT) before publishing, if desired.

公開前に、必要であればお好みのライセンス（MITなど）を追加してください。
