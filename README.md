# 🧹 DataCleaner Pro

A **professional, interactive Data Cleaning Utility** built with Python, Pandas, and Streamlit.  
Upload any CSV file, detect data quality issues, apply cleaning operations, and download your clean dataset — all from a beautiful dark-themed dashboard.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **CSV & Excel Upload** | Upload CSV or Excel (.xlsx, .xls) files or load the 1-click sample dataset |
| **Missing Value Handling** | Drop rows/columns, fill with mean/median/mode/zero/custom/ffill/bfill |
| **Data Type Conversion** | AI auto-detection & manual casting to int, float, string, or datetime |
| **Duplicate Removal** | Detect and remove duplicates (keep first, last, or none) |
| **Column Standardization** | Lowercase, underscore-separated, deduplicated column headers |
| **Cleaning Dashboard** | 6 summary metric cards and Plotly before/after visual charts |
| **Cleaning Log** | Full chronological audit trail of every operation applied |
| **Multi-Format Export** | Download Cleaned CSV + Cleaned Excel (.xlsx) + Cleaning Log CSV + Summary TXT |
| **Reset Button** | Restore the original dataset at any time with a single click |

---

## 🚀 Quick Start (Local)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/data-cleaning-utility.git
cd data-cleaning-utility
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open automatically at **http://localhost:8501**.

---

## 🧪 Testing with Sample Data

A sample CSV file (`sample_data.csv`) is included in the project. It contains:
- **50 employee records** across 10 columns
- **Intentional missing values** in Age, Email, Salary, Join Date, Phone, Rating, and Active columns
- **2 exact duplicate rows** for testing duplicate removal
- **Mixed data types** for testing type conversion
- **Date strings** in the `Join Date` column

Upload `sample_data.csv` from the sidebar to explore all cleaning features.

---

## 📁 Project Structure

```
data-cleaning-utility/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── sample_data.csv     # Sample dataset for testing
├── README.md           # This file
└── .streamlit/
    └── config.toml     # (Optional) Streamlit theme config
```

---

## ☁️ Deploy on Render

### Step 1 – Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit – DataCleaner Pro"
git remote add origin https://github.com/YOUR_USERNAME/data-cleaning-utility.git
git push -u origin main
```

### Step 2 – Create a Render Web Service
1. Go to [render.com](https://render.com) and sign in.
2. Click **New → Web Service**.
3. Connect your GitHub repository.
4. Configure the service:

| Setting | Value |
|---------|-------|
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true` |

5. Click **Create Web Service**.

Render will install dependencies and deploy your app automatically. Each push to `main` triggers a redeploy.

### Optional – `.streamlit/config.toml`
Create this file to customize the Streamlit theme:
```toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = false

[theme]
base = "dark"
primaryColor = "#6366f1"
backgroundColor = "#0f0c29"
secondaryBackgroundColor = "#1e1b4b"
textColor = "#e2e8f0"
```

---

## 🛠 Technical Stack

- **Python 3.9+**
- **Streamlit 1.41** – interactive web UI
- **Pandas 2.2** – data manipulation
- **NumPy 2.2** – numerical operations
- **Plotly 5.24** – interactive charts

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 👩‍💻 Author

Built with ❤️ as a complete data engineering portfolio project.
