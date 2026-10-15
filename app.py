"""
DataCleaner Pro - Main Application
==================================
A professional, interactive data-cleaning tool built with Streamlit and Pandas.
Upload CSV/Excel files, detect data quality issues, apply cleaning operations,
inspect interactive charts and audit logs, and download cleaned datasets.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io
import os
import re
from datetime import datetime

# ─────────────────────────────────────────────
#  Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DataCleaner Pro | Data Cleaning Utility",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  Custom CSS (Dark Modern Theme)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0b091a 0%, #171333 40%, #1f1b45 100%);
    min-height: 100vh;
}

/* ── Main content wrapper ── */
.main .block-container {
    padding-top: 1.8rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, rgba(99,102,241,0.18) 0%, rgba(168,85,247,0.18) 50%, rgba(236,72,153,0.15) 100%);
    border: 1px solid rgba(129,140,248,0.35);
    border-radius: 20px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
    backdrop-filter: blur(14px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}
.hero-banner h1 {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #818cf8 0%, #c084fc 50%, #fb7185 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
}
.hero-banner p {
    color: #cbd5e1;
    font-size: 1.1rem;
    margin-top: 0.6rem;
    margin-bottom: 0;
}

/* ── Metric cards ── */
.metric-card-box {
    background: rgba(30, 27, 75, 0.65);
    border: 1px solid rgba(129,140,248,0.25);
    border-radius: 16px;
    padding: 1.2rem 1rem;
    text-align: center;
    backdrop-filter: blur(10px);
    transition: all 0.25s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.metric-card-box:hover {
    transform: translateY(-3px);
    border-color: rgba(168,85,247,0.6);
    box-shadow: 0 8px 25px rgba(99,102,241,0.25);
}
.metric-card-box .value {
    font-size: 2rem;
    font-weight: 700;
    color: #a5b4fc;
}
.metric-card-box .label {
    font-size: 0.8rem;
    color: #94a3b8;
    margin-top: 0.35rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
}

/* ── Section headings ── */
.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #f1f5f9;
    border-left: 4px solid #818cf8;
    padding-left: 0.85rem;
    margin-top: 1.5rem;
    margin-bottom: 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b091a 0%, #161236 100%);
    border-right: 1px solid rgba(129,140,248,0.2);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #c084fc;
}

/* ── Info boxes ── */
.info-box {
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(99,102,241,0.35);
    border-radius: 14px;
    padding: 1.1rem 1.4rem;
    color: #bfdbfe;
    margin-bottom: 1.2rem;
    line-height: 1.5;
}

/* ── Action Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.25rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.35) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(99,102,241,0.55) !important;
}

/* ── Download buttons ── */
.stDownloadButton > button {
    background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.25rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(16,185,129,0.35) !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #047857 0%, #059669 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(16,185,129,0.5) !important;
}

/* ── DataFrames ── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    border: 1px solid rgba(129,140,248,0.2);
    overflow: hidden;
}

/* ── Divider ── */
hr {
    border-color: rgba(129,140,248,0.2) !important;
    margin: 1.8rem 0 !important;
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  SESSION STATE INITIALISATION
# ═══════════════════════════════════════════════════════════════
def init_session():
    defaults = {
        "original_df": None,
        "working_df": None,
        "cleaning_log": [],
        "duplicate_rows_removed": 0,
        "columns_converted": 0,
        "flash_message": None,
        "_last_file": None,
        "_selected_ops": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_session()


def notify(msg: str, kind: str = "success"):
    """Queue a flash message and toast across Streamlit reruns."""
    st.session_state["flash_message"] = (kind, msg)


# ═══════════════════════════════════════════════════════════════
#  UTILITY / HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def log_operation(operation: str, column: str, affected: int, method: str, status: str = "Success"):
    """Append an entry to the audit cleaning log."""
    st.session_state["cleaning_log"].append({
        "Timestamp": datetime.now().strftime("%H:%M:%S"),
        "Operation": operation,
        "Column": str(column),
        "Affected Rows/Values": int(affected),
        "Method": method,
        "Status": status,
    })


def missing_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame with per-column missing value statistics."""
    total = max(len(df), 1)
    missing = df.isnull().sum()
    pct = (missing / total * 100).round(2)
    return pd.DataFrame({
        "Column": df.columns,
        "Missing Count": missing.values,
        "Missing %": pct.values,
        "Dtype": df.dtypes.values.astype(str),
    }).sort_values("Missing Count", ascending=False).reset_index(drop=True)


def memory_usage_str(df: pd.DataFrame) -> str:
    """Return human-readable DataFrame memory footprint."""
    bytes_used = df.memory_usage(deep=True).sum()
    if bytes_used < 1024:
        return f"{bytes_used} B"
    if bytes_used < 1024 ** 2:
        return f"{bytes_used / 1024:.1f} KB"
    return f"{bytes_used / 1024 ** 2:.2f} MB"


# ═══════════════════════════════════════════════════════════════
#  CORE CLEANING FUNCTIONS
# ═══════════════════════════════════════════════════════════════

# ── A. Missing Values ──────────────────────────────────────────
def handle_missing_values(df: pd.DataFrame, strategy: str, columns: list,
                          fill_value=None) -> tuple[pd.DataFrame, str]:
    """
    Apply a missing-value strategy to specified columns.
    Returns: (modified_df, status_message)
    strategy: "drop_rows" | "drop_cols" | "mean" | "median" | "zero" |
              "mode" | "custom" | "ffill" | "bfill"
    """
    df = df.copy()

    if strategy == "drop_rows":
        before = len(df)
        df = df.dropna(subset=columns)
        after = len(df)
        removed = before - after
        log_operation("Drop Rows with Missing", ", ".join(columns), removed, "dropna")
        return df, f"Dropped {removed:,} row(s) containing missing values."

    elif strategy == "drop_cols":
        dropped = [c for c in columns if c in df.columns and df[c].isnull().any()]
        df = df.drop(columns=dropped)
        log_operation("Drop Columns with Missing", ", ".join(dropped), len(dropped), "drop columns")
        return df, f"Dropped {len(dropped)} column(s): {', '.join(dropped)}"

    elif strategy in ("mean", "median", "zero"):
        total_filled = 0
        for col in columns:
            if col not in df.columns:
                continue
            if pd.api.types.is_numeric_dtype(df[col]):
                if strategy == "mean":
                    val = df[col].mean()
                elif strategy == "median":
                    val = df[col].median()
                else:
                    val = 0
                filled = int(df[col].isnull().sum())
                df[col] = df[col].fillna(val)
                total_filled += filled
                log_operation(f"Fill Missing ({strategy})", col, filled, strategy)
            else:
                st.warning(f"⚠️ Column '{col}' is non-numeric — skipped for {strategy} imputation.")
        return df, f"Filled {total_filled:,} numeric missing value(s) using {strategy}."

    elif strategy == "mode":
        total_filled = 0
        for col in columns:
            if col not in df.columns:
                continue
            mode_series = df[col].mode()
            if not mode_series.empty:
                mode_val = mode_series[0]
                filled = int(df[col].isnull().sum())
                df[col] = df[col].fillna(mode_val)
                total_filled += filled
                log_operation("Fill Missing (mode)", col, filled, "mode")
        return df, f"Filled {total_filled:,} missing value(s) using mode."

    elif strategy == "custom":
        total_filled = 0
        for col in columns:
            if col not in df.columns:
                continue
            filled = int(df[col].isnull().sum())
            try:
                if pd.api.types.is_numeric_dtype(df[col]):
                    val = float(fill_value)
                else:
                    val = str(fill_value)
                df[col] = df[col].fillna(val)
                total_filled += filled
                log_operation("Fill Missing (custom)", col, filled, f"value='{fill_value}'")
            except Exception as e:
                log_operation("Fill Missing (custom)", col, 0, f"value='{fill_value}'", "Error")
                return df, f"Error filling '{col}': {e}"
        return df, f"Filled {total_filled:,} missing value(s) with custom value: '{fill_value}'."

    elif strategy in ("ffill", "bfill"):
        total_filled = 0
        for col in columns:
            if col not in df.columns:
                continue
            before_nulls = int(df[col].isnull().sum())
            if strategy == "ffill":
                df[col] = df[col].ffill()
            else:
                df[col] = df[col].bfill()
            after_nulls = int(df[col].isnull().sum())
            filled = max(0, before_nulls - after_nulls)
            total_filled += filled
            log_operation(f"Fill Missing ({strategy})", col, filled, strategy)
        return df, f"Applied {strategy} to selected columns ({total_filled:,} value(s) imputed)."

    return df, "No operation applied."


# ── B. Data Type Conversion ───────────────────────────────────
def convert_column_dtype(df: pd.DataFrame, col: str, target_type: str,
                         errors: str = "coerce") -> tuple[pd.DataFrame, str, bool]:
    """
    Convert a column into int, float, string, or datetime.
    Returns: (modified_df, status_message, is_success)
    """
    df = df.copy()
    if col not in df.columns:
        return df, f"Column '{col}' not found.", False

    original_nulls = int(df[col].isnull().sum())
    try:
        if target_type == "int":
            s = pd.to_numeric(df[col], errors=errors)
            if errors == "ignore" and s.dtype == object:
                df[col] = s
            else:
                df[col] = s.astype("Int64")
        elif target_type == "float":
            s = pd.to_numeric(df[col], errors=errors)
            if errors == "ignore" and s.dtype == object:
                df[col] = s
            else:
                df[col] = s.astype(float)
        elif target_type == "string":
            df[col] = df[col].astype(str)
        elif target_type == "datetime":
            df[col] = pd.to_datetime(df[col], errors=errors)

        new_nulls = int(df[col].isnull().sum())
        coerced = max(0, new_nulls - original_nulls)
        log_operation(
            f"Type Conversion → {target_type}",
            col,
            coerced,
            f"pd.to_{target_type}(errors='{errors}')"
        )
        st.session_state["columns_converted"] += 1
        msg = f"Converted '{col}' to {target_type}."
        if coerced > 0:
            msg += f" ({coerced} invalid value(s) coerced to NaN)"
        return df, msg, True
    except Exception as e:
        log_operation(f"Type Conversion → {target_type}", col, 0, f"pd.to_{target_type}", "Error")
        return df, f"Conversion failed for '{col}': {e}", False


# ── C. Duplicate Removal ──────────────────────────────────────
def remove_duplicates(df: pd.DataFrame, keep: str) -> tuple[pd.DataFrame, str]:
    """
    Remove duplicate rows.
    keep: "first" | "last" | "none"
    Returns: (modified_df, status_message)
    """
    df = df.copy()
    before = len(df)
    keep_param = keep if keep in ("first", "last") else False
    df = df.drop_duplicates(keep=keep_param)
    removed = before - len(df)
    st.session_state["duplicate_rows_removed"] += removed
    log_operation("Remove Duplicates", "All columns", removed, f"keep='{keep}'")
    return df, f"Removed {removed:,} duplicate row(s) (kept: {keep})."


# ── D. Column Name Standardization ────────────────────────────
def standardize_column_names(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """
    Standardize column names:
    - Lowercase
    - Replace whitespace & special characters with underscores
    - Collapse multiple underscores & strip leading/trailing underscores
    - Deduplicate collision names with _1, _2 suffixes
    """
    df = df.copy()
    new_names = []
    seen = {}
    for col in df.columns:
        clean = str(col).strip().lower()
        clean = re.sub(r"[^a-z0-9]+", "_", clean)
        clean = re.sub(r"_+", "_", clean).strip("_")
        if not clean:
            clean = "column"
        if clean in seen:
            seen[clean] += 1
            clean = f"{clean}_{seen[clean]}"
        else:
            seen[clean] = 0
        new_names.append(clean)

    old_names = list(df.columns)
    df.columns = new_names
    changed = sum(1 for o, n in zip(old_names, new_names) if o != n)
    log_operation("Column Standardization", "All columns", changed, "regex_clean")
    return df, f"Standardized {changed} column name(s)."


# ═══════════════════════════════════════════════════════════════
#  CHART VISUALIZATIONS
# ═══════════════════════════════════════════════════════════════
def plot_missing_bar(stats_df: pd.DataFrame, title: str):
    """Plot horizontal or vertical bar chart of missing percentages."""
    top = stats_df[stats_df["Missing Count"] > 0].head(25)
    if top.empty:
        st.info("🎉 No missing values detected in the selected columns!")
        return
    fig = px.bar(
        top,
        x="Column",
        y="Missing %",
        color="Missing %",
        color_continuous_scale=["#818cf8", "#c084fc", "#f43f5e"],
        title=title,
        text=top["Missing Count"].astype(str) + " nulls",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        title_font_color="#c084fc",
        xaxis=dict(gridcolor="rgba(129,140,248,0.15)", tickangle=-30),
        yaxis=dict(gridcolor="rgba(129,140,248,0.15)"),
        coloraxis_showscale=False,
        margin=dict(t=50, b=40, l=40, r=40),
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)


def plot_dtype_pie(df: pd.DataFrame):
    """Plot donut chart of column data types."""
    dtype_counts = df.dtypes.astype(str).value_counts().reset_index()
    dtype_counts.columns = ["dtype", "count"]
    fig = px.pie(
        dtype_counts,
        names="dtype",
        values="count",
        title="Column Data Types",
        color_discrete_sequence=["#818cf8", "#a855f7", "#ec4899", "#10b981", "#38bdf8"],
        hole=0.45,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        title_font_color="#c084fc",
        margin=dict(t=50, b=20, l=20, r=20),
    )
    st.plotly_chart(fig, use_container_width=True)


def plot_before_after_missing(before_df: pd.DataFrame, after_df: pd.DataFrame):
    """Grouped bar chart comparing missing values before vs after cleaning."""
    before_missing = before_df.isnull().sum()
    cols_with_missing = before_missing[before_missing > 0].index.tolist()
    if not cols_with_missing:
        st.info("🎉 No missing values were present in the original dataset!")
        return

    # Normalized lookup mapping to handle column renaming or dropped columns
    norm_after_cols = {
        re.sub(r"[^a-z0-9]+", "_", str(c).lower()).strip("_"): c
        for c in after_df.columns
    }

    after_vals = []
    labels = []
    for col in cols_with_missing:
        labels.append(str(col))
        if col in after_df.columns:
            after_vals.append(int(after_df[col].isnull().sum()))
        else:
            norm_c = re.sub(r"[^a-z0-9]+", "_", str(col).lower()).strip("_")
            matched = norm_after_cols.get(norm_c)
            if matched and matched in after_df.columns:
                after_vals.append(int(after_df[matched].isnull().sum()))
            else:
                after_vals.append(0)  # Dropped column

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Original Dataset",
        x=labels,
        y=before_missing[cols_with_missing].values,
        marker_color="#818cf8",
        text=before_missing[cols_with_missing].values,
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name="Cleaned Dataset",
        x=labels,
        y=after_vals,
        marker_color="#34d399",
        text=after_vals,
        textposition="outside",
    ))
    fig.update_layout(
        barmode="group",
        title="Missing Values: Original vs. Cleaned Dataset",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        title_font_color="#c084fc",
        xaxis=dict(gridcolor="rgba(129,140,248,0.15)", tickangle=-30),
        yaxis=dict(gridcolor="rgba(129,140,248,0.15)"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=50, b=40, l=40, r=40),
    )
    st.plotly_chart(fig, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
#  DOWNLOAD HELPERS
# ═══════════════════════════════════════════════════════════════
def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Encode DataFrame to UTF-8 CSV bytes."""
    return df.to_csv(index=False).encode("utf-8")


def df_to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Encode DataFrame to Excel bytes using openpyxl."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="CleanedData")
    return buffer.getvalue()


def generate_summary_report(original_df: pd.DataFrame, working_df: pd.DataFrame) -> str:
    """Generate a structured text summary report."""
    orig_missing = int(original_df.isnull().sum().sum())
    clean_missing = int(working_df.isnull().sum().sum())
    orig_dups = int(original_df.duplicated().sum())
    clean_dups = int(working_df.duplicated().sum())

    lines = [
        "=" * 68,
        "              DataCleaner Pro - Summary Audit Report",
        "=" * 68,
        f"Generated At      : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "1. ORIGINAL DATASET",
        f"   - Total Rows      : {len(original_df):,}",
        f"   - Total Columns   : {len(original_df.columns):,}",
        f"   - Missing Cells   : {orig_missing:,}",
        f"   - Duplicate Rows  : {orig_dups:,}",
        f"   - Memory Footprint: {memory_usage_str(original_df)}",
        "",
        "2. CLEANED DATASET",
        f"   - Total Rows      : {len(working_df):,}",
        f"   - Total Columns   : {len(working_df.columns):,}",
        f"   - Rows Removed    : {len(original_df) - len(working_df):,}",
        f"   - Missing Cells   : {clean_missing:,}",
        f"   - Duplicate Rows  : {clean_dups:,}",
        f"   - Memory Footprint: {memory_usage_str(working_df)}",
        f"   - Duplicates Cut  : {st.session_state.get('duplicate_rows_removed', 0):,}",
        f"   - Columns Casted  : {st.session_state.get('columns_converted', 0):,}",
        "",
        "3. AUDIT LOG (OPERATIONS APPLIED)",
        "-" * 68,
    ]
    log = st.session_state.get("cleaning_log", [])
    if log:
        for idx, entry in enumerate(log, start=1):
            lines.append(
                f"{idx:02d}. [{entry['Timestamp']}] {entry['Operation']} | "
                f"Target: {entry['Column']} | Affected: {entry['Affected Rows/Values']} | "
                f"Method: {entry['Method']} | Status: {entry['Status']}"
            )
    else:
        lines.append("   No cleaning operations recorded.")

    lines.append("=" * 68)
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR NAVIGATION & CONTROLS
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🧹 DataCleaner Pro")
    st.markdown("<p style='color:#94a3b8; font-size:0.85rem;'>Automated Data Quality &amp; Cleaning Suite</p>", unsafe_allow_html=True)
    st.markdown("---")

    # ── File Upload ─────────────────────────────────────────
    st.markdown("### 📂 Data Source")
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        help="Upload a dataset in CSV or Excel format to begin.",
    )

    # Demo Dataset Loader
    if st.button("✨ Load Sample Dataset (Demo)", use_container_width=True):
        if os.path.exists("sample_data.csv"):
            sample_df = pd.read_csv("sample_data.csv")
            st.session_state["original_df"] = sample_df.copy()
            st.session_state["working_df"] = sample_df.copy()
            st.session_state["cleaning_log"] = []
            st.session_state["duplicate_rows_removed"] = 0
            st.session_state["columns_converted"] = 0
            st.session_state["_last_file"] = "sample_data.csv"
            notify("✅ Loaded sample dataset (50 employee records with quality anomalies)!", "success")
            st.rerun()
        else:
            st.error("sample_data.csv not found in working directory.")

    if uploaded_file is not None and st.session_state.get("_last_file") != uploaded_file.name:
        try:
            if uploaded_file.name.endswith((".xlsx", ".xls")):
                df_upload = pd.read_excel(uploaded_file)
            else:
                df_upload = pd.read_csv(uploaded_file)

            if df_upload.empty:
                st.error("The uploaded file is empty. Please upload a populated dataset.")
            else:
                st.session_state["original_df"] = df_upload.copy()
                st.session_state["working_df"] = df_upload.copy()
                st.session_state["cleaning_log"] = []
                st.session_state["duplicate_rows_removed"] = 0
                st.session_state["columns_converted"] = 0
                st.session_state["_last_file"] = uploaded_file.name
                notify(f"✅ Successfully loaded '{uploaded_file.name}' ({len(df_upload):,} rows, {len(df_upload.columns)} columns)!", "success")
                st.rerun()
        except Exception as e:
            st.error(f"❌ Failed to parse file: {e}")

    # ── Cleaning Controls (Active only if data is loaded) ──
    if st.session_state["working_df"] is not None:
        st.markdown("---")
        st.markdown("### ⚙️ Cleaning Pipeline")

        cleaning_ops = st.multiselect(
            "Select operations to configure:",
            [
                "Handle Missing Values",
                "Convert Data Types",
                "Remove Duplicates",
                "Standardize Column Names",
            ],
            default=st.session_state.get("_selected_ops", ["Handle Missing Values", "Convert Data Types"]),
        )
        st.session_state["_selected_ops"] = cleaning_ops

        st.markdown("---")
        # Reset button
        if st.button("🔄 Reset to Original", use_container_width=True):
            st.session_state["working_df"] = st.session_state["original_df"].copy()
            st.session_state["cleaning_log"] = []
            st.session_state["duplicate_rows_removed"] = 0
            st.session_state["columns_converted"] = 0
            notify("Dataset restored to original uploaded state.", "warning")
            st.rerun()

        st.markdown(
            "<div style='color:#64748b; font-size:0.78rem; margin-top:1rem; text-align:center;'>"
            "💡 Changes apply incrementally to your working dataset."
            "</div>",
            unsafe_allow_html=True,
        )


# ═══════════════════════════════════════════════════════════════
#  MAIN CONTENT AREA
# ═══════════════════════════════════════════════════════════════

# Display queued flash message (if any)
if st.session_state.get("flash_message"):
    kind, msg = st.session_state.pop("flash_message")
    if kind == "success":
        st.success(msg)
        st.toast(msg, icon="✅")
    elif kind == "warning":
        st.warning(msg)
        st.toast(msg, icon="⚠️")
    elif kind == "error":
        st.error(msg)
        st.toast(msg, icon="❌")

# ── Hero Banner ───────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <h1>🧹 DataCleaner Pro</h1>
    <p>Upload CSV/Excel · Audit Quality · Interactive Imputation &amp; Conversion · Download Clean Data</p>
</div>
""", unsafe_allow_html=True)


# ── Guard: If no data loaded yet ─────────────────────────────
if st.session_state["original_df"] is None:
    st.markdown("""
    <div class="info-box">
        👋 <strong>Welcome!</strong> Upload your CSV or Excel file using the sidebar on the left, 
        or click the <strong>demo button below</strong> to test all cleaning features instantly with our pre-built benchmark dataset.
    </div>
    """, unsafe_allow_html=True)

    col_btn, _ = st.columns([1, 2])
    with col_btn:
        if st.button("✨ Load Sample Benchmark Dataset (1-Click)", use_container_width=True):
            if os.path.exists("sample_data.csv"):
                sample_df = pd.read_csv("sample_data.csv")
                st.session_state["original_df"] = sample_df.copy()
                st.session_state["working_df"] = sample_df.copy()
                st.session_state["cleaning_log"] = []
                st.session_state["duplicate_rows_removed"] = 0
                st.session_state["columns_converted"] = 0
                st.session_state["_last_file"] = "sample_data.csv"
                notify("✅ Sample dataset loaded! Explore the cleaning operations below.", "success")
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="metric-card-box">
            <div class="value">🔍</div>
            <div class="label">Detect Data Issues</div>
            <p style="color:#94a3b8; font-size:0.85rem; margin-top:0.5rem;">
                Spot missing values, duplicates, and type mismatches with interactive Plotly visualisations.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="metric-card-box">
            <div class="value">🧼</div>
            <div class="label">Precision Cleaning</div>
            <p style="color:#94a3b8; font-size:0.85rem; margin-top:0.5rem;">
                Impute numericals with mean/median/zero, categoricals with mode/custom, and cast datetimes safely.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="metric-card-box">
            <div class="value">⬇️</div>
            <div class="label">Export &amp; Audit</div>
            <p style="color:#94a3b8; font-size:0.85rem; margin-top:0.5rem;">
                Download cleaned CSV or Excel files alongside a complete chronological audit trail log.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.stop()


# ── Active References ─────────────────────────────────────────
original_df: pd.DataFrame = st.session_state["original_df"]
working_df: pd.DataFrame = st.session_state["working_df"]
selected_ops: list = st.session_state.get("_selected_ops", [])


# ═══════════════════════════════════════════════════════════════
#  SECTION 1 – DATASET OVERVIEW
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📊 1. Dataset Overview</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(f"""
    <div class="metric-card-box">
        <div class="value">{len(original_df):,}</div>
        <div class="label">Original Rows</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="metric-card-box">
        <div class="value">{len(working_df):,}</div>
        <div class="label">Current Rows</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="metric-card-box">
        <div class="value">{len(working_df.columns)}</div>
        <div class="label">Columns</div>
    </div>""", unsafe_allow_html=True)
with c4:
    total_nulls = int(working_df.isnull().sum().sum())
    st.markdown(f"""
    <div class="metric-card-box">
        <div class="value" style="color: {'#f87171' if total_nulls > 0 else '#34d399'};">{total_nulls:,}</div>
        <div class="label">Missing Cells</div>
    </div>""", unsafe_allow_html=True)
with c5:
    st.markdown(f"""
    <div class="metric-card-box">
        <div class="value">{memory_usage_str(working_df)}</div>
        <div class="label">Memory Size</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

with st.expander("🔍 Interactive Data Preview (Working vs. Original)", expanded=True):
    tab1, tab2 = st.tabs(["Current Working Dataset", "Original Uploaded Dataset"])
    with tab1:
        st.dataframe(working_df, use_container_width=True, height=280)
    with tab2:
        st.dataframe(original_df, use_container_width=True, height=280)

col_dtypes, col_pie = st.columns([1.6, 1])
with col_dtypes:
    st.markdown("**Column Schema &amp; Quality Metrics**")
    info_df = pd.DataFrame({
        "Column": working_df.columns,
        "Data Type": working_df.dtypes.astype(str).values,
        "Non-Null Count": working_df.notnull().sum().values,
        "Missing Count": working_df.isnull().sum().values,
        "Unique Values": working_df.nunique().values,
    })
    st.dataframe(info_df, use_container_width=True, height=240)
with col_pie:
    plot_dtype_pie(working_df)

st.markdown("---")


# ═══════════════════════════════════════════════════════════════
#  SECTION 2 – CLEANING OPERATIONS
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🛠️ 2. Cleaning Operations</div>', unsafe_allow_html=True)

if not selected_ops:
    st.markdown(
        '<div class="info-box">👈 Select one or more cleaning operations from the <strong>Sidebar</strong> to configure them.</div>',
        unsafe_allow_html=True,
    )

# ── 2A. Handle Missing Values ─────────────────────────────────
if "Handle Missing Values" in selected_ops:
    with st.expander("🔲 Handle Missing Values", expanded=True):
        mv_stats_before = missing_stats(working_df)
        total_missing = int(mv_stats_before["Missing Count"].sum())

        st.markdown(f"**Total missing cells in working dataset:** `{total_missing:,}`")
        plot_missing_bar(mv_stats_before, "Missing Values by Column")

        cols_with_missing = mv_stats_before[mv_stats_before["Missing Count"] > 0]["Column"].tolist()
        all_cols = list(working_df.columns)

        col_strat, col_targets = st.columns([1, 1.5])
        with col_strat:
            strategy = st.selectbox(
                "Imputation / Handling Strategy",
                ["drop_rows", "drop_cols", "mean", "median", "zero", "mode", "custom", "ffill", "bfill"],
                format_func=lambda x: {
                    "drop_rows": "🗑️ Drop rows with missing values",
                    "drop_cols": "🗑️ Drop columns with missing values",
                    "mean":      "🔢 Fill numeric → Mean",
                    "median":    "🔢 Fill numeric → Median",
                    "zero":      "0️⃣ Fill numeric → Zero",
                    "mode":      "🔤 Fill categorical → Mode (Most frequent)",
                    "custom":    "✏️ Fill → Custom static value",
                    "ffill":     "⏩ Forward Fill (Propagate previous value)",
                    "bfill":     "⏪ Backward Fill (Propagate next value)",
                }[x],
                key="mv_strategy",
            )
            custom_val = None
            if strategy == "custom":
                custom_val = st.text_input("Custom fill value", value="Unknown", key="mv_custom_val")

        with col_targets:
            target_cols = st.multiselect(
                "Apply to columns:",
                options=all_cols,
                default=cols_with_missing if cols_with_missing else all_cols[:1],
                key="mv_cols",
            )

        if st.button("▶ Apply Missing-Value Handling", key="apply_mv"):
            if not target_cols:
                st.warning("Please select at least one column to apply the operation to.")
            else:
                updated_df, msg = handle_missing_values(
                    st.session_state["working_df"], strategy, target_cols, custom_val
                )
                st.session_state["working_df"] = updated_df
                notify(f"✅ {msg}", "success")
                st.rerun()


# ── 2B. Convert Data Types ────────────────────────────────────
if "Convert Data Types" in selected_ops:
    with st.expander("🔄 Convert Data Types", expanded=True):
        st.markdown("Automatically inspect columns stored as strings/objects and cast them into correct native types.")

        # Auto-detect candidates
        candidates = []
        for col in working_df.columns:
            if working_df[col].dtype == object:
                # Try numeric detection
                numeric_sample = pd.to_numeric(working_df[col], errors="coerce")
                if numeric_sample.notnull().sum() / max(len(working_df), 1) > 0.6:
                    candidates.append({"Column": col, "Current": "object/text", "Recommended Type": "Numeric (int/float)"})
                else:
                    # Try datetime detection
                    try:
                        dt_sample = pd.to_datetime(working_df[col], errors="coerce")
                        if dt_sample.notnull().sum() / max(len(working_df), 1) > 0.6:
                            candidates.append({"Column": col, "Current": "object/text", "Recommended Type": "Datetime"})
                    except Exception:
                        pass

        if candidates:
            st.markdown("**🤖 AI Type Detection Suggestions:**")
            st.dataframe(pd.DataFrame(candidates), use_container_width=True)
        else:
            st.info("No obvious type mismatches detected across object columns.")

        st.markdown("**Manual Type Conversion:**")
        c_col, c_type, c_err = st.columns([1.2, 1, 1.2])
        with c_col:
            dt_col = st.selectbox("Select Column", options=list(working_df.columns), key="dt_col")
        with c_type:
            dt_target = st.selectbox("Convert To", ["int", "float", "string", "datetime"], key="dt_target")
        with c_err:
            dt_errors = st.radio(
                "On Conversion Error",
                ["coerce (set invalid to NaN)", "ignore (keep original value)"],
                key="dt_errors",
            )
            errors_param = "coerce" if "coerce" in dt_errors else "ignore"

        st.markdown(
            f"Current dtype for **{dt_col}**: `{working_df[dt_col].dtype}` | "
            f"Sample values: `{working_df[dt_col].dropna().head(4).tolist()}`"
        )

        if st.button("▶ Apply Type Conversion", key="apply_dt"):
            updated_df, msg, success = convert_column_dtype(
                st.session_state["working_df"], dt_col, dt_target, errors_param
            )
            st.session_state["working_df"] = updated_df
            notify(f"✅ {msg}" if success else f"❌ {msg}", "success" if success else "error")
            st.rerun()


# ── 2C. Remove Duplicates ─────────────────────────────────────
if "Remove Duplicates" in selected_ops:
    with st.expander("👥 Remove Duplicates", expanded=True):
        dup_count = int(working_df.duplicated().sum())
        st.markdown(f"**Duplicate rows detected in working dataset:** `{dup_count:,}`")

        if dup_count > 0:
            st.dataframe(
                working_df[working_df.duplicated(keep=False)].head(50),
                use_container_width=True,
                height=200,
            )
            col_keep, col_act = st.columns([2, 1])
            with col_keep:
                keep_choice = st.radio(
                    "Which occurrence would you like to keep?",
                    ["first occurrence", "last occurrence", "none (drop all copies)"],
                    horizontal=True,
                    key="dup_keep",
                )
                keep_val = keep_choice.split(" ")[0]

            with col_act:
                st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
                if st.button("▶ Remove Duplicates Now", key="apply_dup", use_container_width=True):
                    updated_df, msg = remove_duplicates(st.session_state["working_df"], keep_val)
                    st.session_state["working_df"] = updated_df
                    notify(f"✅ {msg}", "success")
                    st.rerun()
        else:
            st.success("🎉 No duplicate rows found in the current dataset!")


# ── 2D. Standardize Column Names ──────────────────────────────
if "Standardize Column Names" in selected_ops:
    with st.expander("🏷️ Standardize Column Names", expanded=True):
        st.markdown(
            "Converts column names to lowercase, replaces non-alphanumeric characters with underscores, "
            "strips outer whitespace, and deduplicates identical resulting headers."
        )

        # Show preview
        proposed = []
        seen_prev = {}
        for col in working_df.columns:
            clean = str(col).strip().lower()
            clean = re.sub(r"[^a-z0-9]+", "_", clean)
            clean = re.sub(r"_+", "_", clean).strip("_") or "column"
            if clean in seen_prev:
                seen_prev[clean] += 1
                clean = f"{clean}_{seen_prev[clean]}"
            else:
                seen_prev[clean] = 0
            proposed.append({"Original Header": str(col), "Proposed Clean Header": clean, "Modified": str(col) != clean})

        prev_df = pd.DataFrame(proposed)
        changes_pending = int(prev_df["Modified"].sum())

        st.dataframe(prev_df, use_container_width=True, height=200)
        st.markdown(f"**{changes_pending}** column header(s) will be renamed.")

        if st.button("▶ Apply Standardization", key="apply_std"):
            updated_df, msg = standardize_column_names(st.session_state["working_df"])
            st.session_state["working_df"] = updated_df
            notify(f"✅ {msg}", "success")
            st.rerun()

st.markdown("---")


# ═══════════════════════════════════════════════════════════════
#  SECTION 3 – CLEANING DASHBOARD
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📈 3. Data Cleaning Dashboard</div>', unsafe_allow_html=True)

d1, d2, d3, d4, d5, d6 = st.columns(6)
with d1:
    st.markdown(f"""
    <div class="metric-card-box">
        <div class="value">{len(original_df):,}</div>
        <div class="label">Original Rows</div>
    </div>""", unsafe_allow_html=True)
with d2:
    st.markdown(f"""
    <div class="metric-card-box">
        <div class="value">{len(working_df):,}</div>
        <div class="label">Cleaned Rows</div>
    </div>""", unsafe_allow_html=True)
with d3:
    diff_rows = len(original_df) - len(working_df)
    st.markdown(f"""
    <div class="metric-card-box">
        <div class="value" style="color:#f43f5e;">-{diff_rows:,}</div>
        <div class="label">Rows Removed</div>
    </div>""", unsafe_allow_html=True)
with d4:
    rem_missing = int(working_df.isnull().sum().sum())
    st.markdown(f"""
    <div class="metric-card-box">
        <div class="value" style="color: {'#34d399' if rem_missing == 0 else '#fbbf24'};">{rem_missing:,}</div>
        <div class="label">Missing Remaining</div>
    </div>""", unsafe_allow_html=True)
with d5:
    st.markdown(f"""
    <div class="metric-card-box">
        <div class="value">{st.session_state.get('duplicate_rows_removed', 0):,}</div>
        <div class="label">Duplicates Removed</div>
    </div>""", unsafe_allow_html=True)
with d6:
    st.markdown(f"""
    <div class="metric-card-box">
        <div class="value">{st.session_state.get('columns_converted', 0):,}</div>
        <div class="label">Columns Converted</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Before / After chart
plot_before_after_missing(original_df, working_df)

st.markdown("**Cleaned Dataset Table**")
st.dataframe(working_df, use_container_width=True, height=320)

st.markdown("---")


# ═══════════════════════════════════════════════════════════════
#  SECTION 4 – CLEANING LOG & AUDIT TRAIL
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📋 4. Audit Trail &amp; Cleaning Log</div>', unsafe_allow_html=True)

log = st.session_state.get("cleaning_log", [])
if log:
    log_df = pd.DataFrame(log)
    st.dataframe(log_df, use_container_width=True, height=220)
else:
    st.info("ℹ️ No cleaning operations applied yet. Configure operations above to generate an audit log.")

st.markdown("---")


# ═══════════════════════════════════════════════════════════════
#  SECTION 5 – DOWNLOAD RESULTS
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">⬇️ 5. Download Results</div>', unsafe_allow_html=True)

dl1, dl2, dl3, dl4 = st.columns(4)
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

with dl1:
    st.download_button(
        label="⬇️ Download Cleaned CSV",
        data=df_to_csv_bytes(working_df),
        file_name=f"cleaned_dataset_{stamp}.csv",
        mime="text/csv",
        use_container_width=True,
    )

with dl2:
    st.download_button(
        label="📊 Download Cleaned Excel",
        data=df_to_excel_bytes(working_df),
        file_name=f"cleaned_dataset_{stamp}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

with dl3:
    if log:
        log_bytes = df_to_csv_bytes(pd.DataFrame(log))
        st.download_button(
            label="📋 Download Cleaning Log (CSV)",
            data=log_bytes,
            file_name=f"cleaning_log_{stamp}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.button("📋 Download Cleaning Log", disabled=True, use_container_width=True)

with dl4:
    summary_text = generate_summary_report(original_df, working_df)
    st.download_button(
        label="📄 Download Summary Report (TXT)",
        data=summary_text.encode("utf-8"),
        file_name=f"cleaning_summary_{stamp}.txt",
        mime="text/plain",
        use_container_width=True,
    )

st.markdown("""
<div style="text-align:center; color:#64748b; font-size:0.85rem; margin-top:2.5rem;">
    Built with ❤️ using <strong>Python</strong>, <strong>Pandas</strong> &amp; <strong>Streamlit</strong> &nbsp;|&nbsp; DataCleaner Pro
</div>
""", unsafe_allow_html=True)
