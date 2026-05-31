# QUY TAC LAM VIEC

## Muc tieu
- Tra loi cau hoi nghiep vu ro rang, uu tien tinh ro net va de doc.
- Truc quan hoa theo nguyen tac "tinh toan truoc, ve sau"; tranh ve truc tiep tren data qua lon.

## Quy trinh hien tai
- Buoc 1: Data cleaning & feature engineering. Xu ly missing, chuan hoa chuoi, tach ky nang.
    Vi du minh hoa:
    - Missing: loai bo salary_usd bi thieu, hoac dien gia tri trung vi theo nganh.
    - Chuan hoa chuoi: strip, lower, mapping (vd: "FinTech" -> "fintech").
    - Tach ky nang: tach "python, sql, tableau" thanh danh sach ["python", "sql", "tableau"].
    - Kiem tra schema: dam bao co cac cot can thiet truoc khi ve bieu do.
  Cac doan code mau theo 3 muc:
  1) Handling Missing Values
      ```python
      # drop rows missing salary
      df = df.dropna(subset=["salary_usd"])
      # fill missing categorical
      df["ai_keywords"] = df["ai_keywords"].fillna("Unknown")
      # fill numeric by median per industry
      df["salary_usd"] = df.groupby("industry")["salary_usd"].transform(lambda s: s.fillna(s.median()))
      ```
  2) Filtering Outliers (IQR)
      ```python
      q1 = df["salary_usd"].quantile(0.25)
      q3 = df["salary_usd"].quantile(0.75)
      iqr = q3 - q1
      lower = q1 - 1.5 * iqr
      upper = q3 + 1.5 * iqr
      df = df[df["salary_usd"].between(lower, upper)]
      ```
  3) Data Type Formatting
      ```python
      df["posting_year"] = pd.to_numeric(df["posting_year"], errors="coerce")
      df["salary_usd"] = (
            df["salary_usd"]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .astype(float)
      )
      df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce")
      ```
- Buoc 2: EDA don bien va song bien. Ve histogram/boxplot/heatmap sau khi gom nhom neu can.
- Buoc 3: Xu huong thoi gian. Groupby theo nam; chi giu top N nhom.
- Buoc 4: Ky nang va text. Dem tan suat; top 10-20; dung bar ngang.
- Buoc 5: Chien luoc. Bieu do tong hop voi du lieu da gom; co the su dung Plotly cho ban do.
- Buoc 6: Bao cao. Cap nhat tai lieu va nhat ky.

## Quy uoc dat ten
- Ten tep (Files): snake_case. Cac tep phan tich co tien to step_XX_ (vi du: step_01_overview.py).
- Ten bien (Variables): snake_case ro nghia; tranh viet tat kho hieu.
- Ham (Functions): snake_case va co type hinting ro rang. Ham noi bo bat dau bang dau _.
- Hang so (Constants): UPPER_SNAKE_CASE.

## Style code
- Thut dau dong 4 spaces, khong dung tab.
- Ham public nen co docstring ngan.
- Tranh magic number; dua vao hang so hoac config.
- Data loading tap trung trong src/data/load_data.py.
- Bat buoc check cot thieu va thong bao ro rang khi khong du dieu kien ve bieu do.

## Du lieu
- Khong sua file CSV goc trong data/raw.
- Luu dataset da lam sach voi ten *_clean_vN.csv trong data/processed.
- Ghi ro Data Version trong EXPERIMENTS.md.
- Xu ly missing va outlier minh bach, co ghi chu neu can.

## Truc quan hoa
- Tinh toan truoc, ve sau; luon groupby cho dataset lon.
- Gioi han nhom (top N) de tranh nhieu nhom tren bieu do.
- Mau sac co dinh (Color Palette):
    - AI Skills/Keywords: Reds (#E91E63)
    - Core Skills/Overview: Blues (#4C72B0)
    - Risk: Low = #66BB6A, Medium = #FFA726, High = #EF5350
- Label day du (truc, don vi, chu thich) va legend gon.
- Tranh 3D, nen sac so; grid nhe.
- Luu anh:
    - PNG: mac dinh dpi=150, bbox_inches="tight"
    - Bieu do chien luoc co the dung dpi=300 neu can net hon
    - Plotly: luu HTML trong reports/figures neu can tuong tac
    - Ten file bat dau bang output_

## Nhat ky thay doi
- Moi thay doi code can cap nhat CHANGELOG.md.
- Dung tien to: Added, Changed, Fixed, Removed.
