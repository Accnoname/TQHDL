"""
helper.py — Các tiện ích định dạng tiền tệ USD, thống kê chung cho dự án
"""
import numpy as np
import pandas as pd


def fmt_usd(x: float, pos=None) -> str:
    """Định dạng số tiền sang dạng chuỗi tiền tệ USD ($150,000).

    Args:
        x (float): Giá trị tiền tệ dạng số.
        pos: Tham số phụ phục vụ cho ticker Matplotlib.

    Returns:
        str: Chuỗi đã được định dạng.
    """
    return f"${int(x):,}"


def calculate_salary_stats(df: pd.DataFrame) -> dict:
    """Tính toán nhanh các chỉ số thống kê tiền lương chung.

    Args:
        df (pd.DataFrame): DataFrame dữ liệu.

    Returns:
        dict: Bộ các giá trị thống kê chính.
    """
    stats = {
        "median": df["salary_usd"].median(),
        "mean": df["salary_usd"].mean(),
        "std": df["salary_usd"].std(),
        "count": len(df)
    }
    return stats
