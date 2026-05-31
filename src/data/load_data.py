"""
load_data.py — Load and basic clean ai_impact_jobs_2010_2025.csv
"""
from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "raw" / "ai_impact_jobs_2010_2025.csv"


def load_raw_data() -> pd.DataFrame:
    """Load raw CSV from data/raw."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Missing raw data file: {DATA_FILE}")
    return pd.read_csv(DATA_FILE)


def load() -> pd.DataFrame:
    """Load dataset and add basic derived columns for analysis."""
    df = load_raw_data()

    # Split multi-value skill columns into lists for analysis
    df["core_skills_list"] = df["core_skills"].str.split(", ")
    df["ai_skills_list"] = df["ai_skills"].str.split(", ")
    df["ai_keywords_list"] = df["ai_keywords"].str.split(", ")

    # Ordinal ordering helpers
    df["seniority_level"] = pd.Categorical(
        df["seniority_level"],
        categories=["Junior", "Mid", "Senior", "Lead", "Executive"],
        ordered=True,
    )
    df["company_size"] = pd.Categorical(
        df["company_size"],
        categories=["Startup", "Small", "Medium", "Large", "Enterprise"],
        ordered=True,
    )
    df["ai_job_displacement_risk"] = pd.Categorical(
        df["ai_job_displacement_risk"],
        categories=["Low", "Medium", "High"],
        ordered=True,
    )
    df["industry_ai_adoption_stage"] = pd.Categorical(
        df["industry_ai_adoption_stage"],
        categories=["Emerging", "Growing", "Mature"],
        ordered=True,
    )
    return df


if __name__ == "__main__":
    df = load()
    print(f"Loaded {len(df):,} rows x {df.shape[1]} columns")
