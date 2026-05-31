"""
cleaning.py — Làm sạch dữ liệu, xử lý rỗng, tách list kỹ năng
"""
import pandas as pd


def _handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()

    if "ai_mentioned" in df_clean.columns:
        if df_clean["ai_mentioned"].dtype == "object":
            df_clean["ai_mentioned"] = df_clean["ai_mentioned"].map(
                {"True": True, "False": False, True: True, False: False}
            ).fillna(False)
        else:
            df_clean["ai_mentioned"] = df_clean["ai_mentioned"].astype(bool)

    for col in ["core_skills", "ai_skills", "ai_keywords"]:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna("")

    return df_clean


def _split_skill_lists(df: pd.DataFrame) -> pd.DataFrame:
    def _parse_skills(skills_str: str) -> list:
        if not isinstance(skills_str, str) or not skills_str:
            return []
        return [s.strip() for s in skills_str.split(",") if s.strip()]

    df_clean = df.copy()
    if "core_skills" in df_clean.columns:
        df_clean["core_skills_list"] = df_clean["core_skills"].apply(_parse_skills)
    if "ai_skills" in df_clean.columns:
        df_clean["ai_skills_list"] = df_clean["ai_skills"].apply(_parse_skills)
    if "ai_keywords" in df_clean.columns:
        df_clean["ai_keywords_list"] = df_clean["ai_keywords"].apply(_parse_skills)
    return df_clean


def _format_numeric_types(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = df.copy()
    if "salary_usd" in df_clean.columns:
        df_clean["salary_usd"] = pd.to_numeric(df_clean["salary_usd"], errors="coerce").fillna(0).astype(int)
    if "ai_intensity_score" in df_clean.columns:
        df_clean["ai_intensity_score"] = pd.to_numeric(
            df_clean["ai_intensity_score"], errors="coerce"
        ).fillna(0.0)
    if "automation_risk_score" in df_clean.columns:
        df_clean["automation_risk_score"] = pd.to_numeric(
            df_clean["automation_risk_score"], errors="coerce"
        ).fillna(0.0)
    return df_clean


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Làm sạch dữ liệu theo 3 phần: missing values, tách kỹ năng, định dạng kiểu số.

    Args:
        df (pd.DataFrame): DataFrame gốc chứa dữ liệu thô.

    Returns:
        pd.DataFrame: DataFrame đã được làm sạch.
    """
    df_clean = _handle_missing_values(df)
    df_clean = _split_skill_lists(df_clean)
    df_clean = _format_numeric_types(df_clean)
    return df_clean


if __name__ == "__main__":
    from load_data import load_raw_data
    df = load_raw_data()
    df_clean = clean_data(df)
    print("Dọn dẹp thành công!")
    print(df_clean[["core_skills", "core_skills_list"]].head(3))
