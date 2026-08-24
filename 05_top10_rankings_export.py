"""
05_top10_rankings_export.py

Computes top-10 rankings (current use vs. next-year demand) for
programming languages, databases, platforms, and web frameworks, and
exports each as a clean two-column CSV (name, Count) suitable for
uploading as a Looker Studio data source.

Requires `df` from 00_setup_and_load_data.py.
"""

import pandas as pd


def get_top_n(column_name, n=10):
    """Split a semicolon-delimited multi-select column, explode it into
    one row per selection, and return the top-n value counts."""
    data = df[column_name].dropna()
    exploded = data.str.split(";").explode()
    return exploded.value_counts().head(n)


def export(series, filename):
    out = series.reset_index()
    out.columns = ["Name", "Count"]
    out.to_csv(filename, index=False)
    print(f"Wrote {filename}")
    print(out, "\n")


# --- Current Technology Usage -----------------------------------------------
export(get_top_n("LanguageHaveWorkedWith"), "top10_languages_current.csv")
export(get_top_n("DatabaseHaveWorkedWith"), "top10_databases_current.csv")
export(get_top_n("PlatformHaveWorkedWith"), "top10_platforms_current.csv")
export(get_top_n("WebframeHaveWorkedWith"), "top10_webframe_current.csv")

# --- Future Technology Trends -----------------------------------------------
export(get_top_n("LanguageWantToWorkWith"), "top10_languages_future.csv")
export(get_top_n("DatabaseWantToWorkWith"), "top10_databases_future.csv")
export(get_top_n("PlatformWantToWorkWith"), "top10_platforms_future.csv")
export(get_top_n("WebframeWantToWorkWith"), "top10_webframe_future.csv")
