# DataPrep

**A no-code data preparation platform** — clean, transform, validate, and export structured datasets through reusable preprocessing pipelines. Built with Django, Pandas, and Bootstrap 5.

![Python](https://img.shields.io/badge/python-3.12%2B-blue) ![Django](https://img.shields.io/badge/django-6.0%2B-092E20) ![License](https://img.shields.io/badge/license-MIT-green) ![Status](https://img.shields.io/badge/status-MVP-brightgreen)

---

## Philosophy

**Analyze → Inform → Let the User Decide.** DataPrep never modifies your data without explicit confirmation. Every operation is transparent, reversible in design, and auditable through before/after comparisons.

---

## Features

### 🔐 Authentication
User registration, login, and logout with session management.

### 📂 Dataset Management
Upload CSV, Excel (.xlsx), and JSON files with automatic format detection and encoding fallback (8 encodings tried). Browse pre-loaded sample datasets to explore features instantly.

### 📊 Dataset Profiling & Health Reports
Automatic column type detection, schema identification, comprehensive health scoring (0–100), and detailed reports covering missing cells, duplicates, and invalid entries.

### 🧹 Data Cleaning (6 operations)
| Operation | Description |
|-----------|-------------|
| Remove Duplicates | Drop duplicate rows with optional subset and keep strategy |
| Fill Missing Values | Fill with constant, mean, median, mode, or drop rows |
| Trim Spaces | Strip leading/trailing whitespace from string columns |
| Normalize Text | Replace multiple spaces with a single space |
| Standardize Capitalization | Apply upper, lower, or title case |
| Rename Columns | Rename one or multiple columns at once |

### 🔄 Data Transformation (10 operations)
| Operation | Description |
|-----------|-------------|
| Convert Dtype | Change column type (string, integer, float, datetime) |
| Auto-Detect Dtypes | Automatically detect and convert booleans, datetimes, and numerics |
| Boolean Conversion | Map values to True/False |
| Format Dates | Parse and reformat date columns |
| Uppercase / Lowercase / Title Case | Text case transformations |
| Remove Special Characters | Strip non-alphanumeric characters |
| Regex Replace | Find and replace using regular expressions |
| Add Derived Column | Create columns via concat, sum, difference, product, quotient, or custom formula |

### 📅 Date/Time Operations (8 operations)
| Operation | Description |
|-----------|-------------|
| Extract Year / Month / Day / Weekday / Quarter | Decompose date columns |
| Calculate Age | Compute age from birthdate to reference date |
| Days Between Dates | Calculate day difference between two date columns |
| Add / Subtract Days | Offset a date column by a number of days |

### 🔢 Numeric Operations (10 operations)
| Operation | Description |
|-----------|-------------|
| Min-Max Normalize | Scale values to [0, 1] range |
| Z-Score Standardize | Center and scale using mean and standard deviation |
| Log Transform | Apply natural logarithm |
| Square Root Transform | Apply square root |
| Absolute Value | Convert to absolute values |
| Round / Floor / Ceiling / Clip | Rounding and boundary operations |
| Scale by Constant | Multiply values by a constant factor |

### 🏷️ Encoding (5 operations)
| Operation | Description |
|-----------|-------------|
| Label Encoding | Map categories to integers (sklearn) |
| One-Hot Encoding | Create binary columns (with drop_first option) |
| Ordinal Encoding | Custom category-to-integer mapping |
| Binary Encoding | One binary column per unique value |
| Frequency Encoding | Replace categories with their occurrence frequencies |

### ⚙️ Feature Engineering (5 operations)
| Operation | Description |
|-----------|-------------|
| Conditional Column | IF-ELSE logic with operators (==, !=, >, <, >=, <=, in, contains, isnull, notnull) |
| Bin Values | Numerical binning via equal-width (cut) or equal-frequency (qcut) |
| Percentage Column | Compute percentage from numerator/denominator |
| Average Columns | Row-wise mean across multiple columns |
| Count Non-Null | Count non-null values across columns |

### 📈 Statistical Operations (8 operations)
| Operation | Description |
|-----------|-------------|
| Mean / Median / Mode | Central tendency measures |
| Standard Deviation / Variance | Dispersion measures |
| Skewness / Kurtosis | Distribution shape measures |
| Correlation Matrix | Pairwise correlations between numeric columns |

### ✅ Data Validation (3 operations)
| Operation | Description |
|-----------|-------------|
| Validate Emails | Flag or remove invalid email addresses |
| Validate Phones | Flag or remove invalid phone numbers (region-aware) |
| Validate Dates | Flag or remove invalid dates |

### ⚠️ Outlier Detection (2 operations)
| Operation | Description |
|-----------|-------------|
| IQR Method | Detect outliers beyond Q1 − 1.5×IQR / Q3 + 1.5×IQR |
| Z-Score Method | Detect outliers with |z| > configurable threshold |

### 🔗 Data Merging (1 operation)
| Operation | Description |
|-----------|-------------|
| Merge Datasets | Inner, left, and right joins on key columns or indices |

---

## Pipeline Builder & Execution

- **Drag-and-drop editor** — Build reusable preprocessing pipelines with an intuitive interface
- **59 operations** across 10 categories — mix and match any combination
- **Before/after comparison** — Review changes with heatmap-style highlighting
- **Processing history** — Full audit trail with runtime tracking
- **Export/Import pipelines** — Share pipeline configurations as JSON files
- **Multiple output formats** — Download processed data as CSV, Excel, or JSON

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0, Python 3.12+ |
| Data Processing | Pandas 3.0, NumPy 2.5 |
| Encoding | scikit-learn compatibility |
| Validation | email-validator, phonenumbers |
| File Handling | openpyxl (Excel), Django FileField |
| Frontend | Bootstrap 5, vanilla JavaScript (drag-and-drop, dark mode) |
| Database | SQLite (development), swappable to PostgreSQL/MySQL |
| Storage | Local filesystem media management |

---

## Project Structure

```
DataPrep/
├── cleanslate/                  # Django project settings & routing
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py
│   └── __init__.py
│
├── authentication/              # User registration, login, logout
│   ├── forms.py                 # SignUpForm with email
│   ├── views.py                 # signup, logout views
│   └── urls.py
│
├── dashboard/                   # Landing page with statistics
│   ├── views.py                 # Recent pipelines, datasets, activity
│   └── urls.py
│
├── datasets/                    # File upload, profiling & management
│   ├── models.py                # Dataset model (profiling, health report)
│   ├── forms.py                 # Upload form (.csv/.xlsx/.json)
│   ├── views.py                 # upload, overview, preview, sample gallery
│   ├── utils.py                 # Multi-encoding CSV reader, validation
│   └── urls.py
│
├── pipelines/                   # Pipeline CRUD, execution & history
│   ├── models.py                # Pipeline, PipelineStep, ProcessingHistory
│   ├── forms.py                 # Pipeline & step forms
│   ├── views.py                 # Editor, executor, results, history, export
│   └── urls.py
│
├── processing/                  # Modular data processing engine
│   ├── profiling.py             # Type detection, health scoring
│   ├── cleaning.py              # Duplicates, missing values, text cleanup
│   ├── transformation.py        # Type conversion, dates, regex, derived cols
│   ├── datetime_ops.py          # Date decomposition & arithmetic
│   ├── numeric.py               # Scaling, transforms, rounding
│   ├── encoding.py              # Label, one-hot, ordinal, binary, frequency
│   ├── feature_engineering.py   # Conditional columns, binning, aggregation
│   ├── statistical.py           # Descriptive stats & correlation
│   ├── validation.py            # Email, phone, date validation
│   ├── outliers.py              # IQR & Z-score detection
│   ├── merging.py               # DataFrame joins
│   ├── conversion.py            # CSV / XLSX / JSON export
│   └── pipeline_executor.py     # Sequential step orchestrator (59 ops)
│
├── templates/                   # Bootstrap 5 HTML templates
│   ├── base.html                # Layout, navbar, dark mode toggle
│   ├── authentication/          # login.html, signup.html
│   ├── dashboard/               # home.html
│   ├── datasets/                # upload, overview, list, samples
│   └── pipelines/               # create, edit, execute, results, history, export
│
├── media/
│   ├── uploads/                 # User-uploaded datasets
│   ├── processed/               # Processed output files
│   ├── samples/                 # Pre-loaded sample datasets (sales, employees)
│   └── merge_uploads/           # Secondary files for merge operations
│
├── static/                      # Static assets (CSS, JS, images)
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── Project_SPEC.md              # Full MVP specification
└── README.md                    # You are here
```

---

## Quick Start

```bash
# 1. Clone the repository
git clone <repo-url>
cd DataPrep

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate     # macOS/Linux
# .venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
python manage.py migrate

# 5. (Optional) Load sample data
python manage.py collectstatic --noinput

# 6. Start the development server
python manage.py runserver

# 7. Open your browser
open http://127.0.0.1:8000
```

---

## Usage Walkthrough

1. **Register** an account and log in
2. **Upload** a CSV, Excel, or JSON dataset — or explore with pre-loaded sales/employee samples
3. **Review** the automatic profiling report — type detection, schema, health score
4. **Build a pipeline** — drag, drop, and configure preprocessing steps (59 operations available)
5. **Execute** the pipeline and inspect the before/after comparison with color-highlighted changes
6. **Download** the cleaned dataset as CSV, Excel, or JSON
7. **Reuse** saved pipelines on new datasets — or export/import them as JSON to share with your team

---

## Development

The project follows the MVP specification in `Project_SPEC.md`. Key architectural decisions:

- **Modular processing engine** — Each `processing/` module is independent, stateless, and testable in isolation
- **Pipeline orchestrator** — `pipeline_executor.py` maps 59 operation strings to functions and executes them sequentially
- **Fail-continue strategy** — Pipeline execution logs errors per step and continues, providing partial results
- **Dark mode** — Built-in theme toggle with persistent preference

### Running Tests
```bash
python manage.py test
```

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
