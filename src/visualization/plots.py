"""
plots.py — Run all visualization steps.
"""
from . import (
    step_01_overview,
    step_02_univariate,
    step_03_bivariate,
    step_04_trends,
    step_05_text_skills,
    step_06_strategic_insights,
)


def run_all() -> None:
    import matplotlib
    matplotlib.use("Agg")

    modules = [
        step_01_overview,
        step_02_univariate,
        step_03_bivariate,
        step_04_trends,
        step_05_text_skills,
        step_06_strategic_insights,
    ]

    for mod in modules:
        print(f"\n{'=' * 40}")
        print(f"Running {mod.__name__}...")
        mod.main()

    print("\nDone! Outputs saved in reports/figures.")


if __name__ == "__main__":
    run_all()
