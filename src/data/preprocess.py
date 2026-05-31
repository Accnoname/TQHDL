"""
preprocess.py — Định dạng dữ liệu phân cấp (Categorical levels)
"""
import pandas as pd
from pathlib import Path

# Đường dẫn lưu tệp dữ liệu đã xử lý
PROCESSED_DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "processed" / "ai_impact_jobs_processed.csv"


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Định dạng các cột dữ liệu phân cấp thành dạng Category có thứ tự.

    Args:
        df (pd.DataFrame): DataFrame đã được làm sạch.

    Returns:
        pd.DataFrame: DataFrame với định dạng Category có thứ tự.
    """
    df_prep = df.copy()

    # Định dạng các cột thành Category có thứ tự (Ordinal Categorical)
    df_prep["seniority_level"] = pd.Categorical(
        df_prep["seniority_level"],
        categories=["Junior", "Mid", "Senior", "Lead", "Executive"],
        ordered=True,
    )
    df_prep["company_size"] = pd.Categorical(
        df_prep["company_size"],
        categories=["Startup", "Small", "Medium", "Large", "Enterprise"],
        ordered=True,
    )
    df_prep["ai_job_displacement_risk"] = pd.Categorical(
        df_prep["ai_job_displacement_risk"],
        categories=["Low", "Medium", "High"],
        ordered=True,
    )
    df_prep["industry_ai_adoption_stage"] = pd.Categorical(
        df_prep["industry_ai_adoption_stage"],
        categories=["Emerging", "Growing", "Mature"],
        ordered=True,
    )

    return df_prep


def save_processed_data(df: pd.DataFrame) -> None:
    """Lưu DataFrame đã xử lý xuống tệp CSV đã xử lý.

    Args:
        df (pd.DataFrame): DataFrame dữ liệu sau xử lý.
    """
    # Đảm bảo thư mục lưu tồn tại
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Đã lưu dữ liệu sạch thành công tại → {PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    from load_data import load_raw_data
    from cleaning import clean_data

    df_raw = load_raw_data()
    df_clean = clean_data(df_raw)
    df_prep = preprocess_data(df_clean)
    save_processed_data(df_prep)
