# CleanSlate Development Specification

> **Project Name**: CleanSlate
> **Django Project Name**: cleanslate
> **Status**: MVP Specification — Single source of truth

---

## 1. Project Overview

CleanSlate is a web-based no-code data preparation platform for data analysts, business users, and anyone working with structured datasets. It provides an end-to-end environment for dataset profiling, cleaning, transformation, validation, merging, conversion, and reusable preprocessing pipelines.

The objective is to simplify repetitive preprocessing work. Instead of writing Python scripts, SQL queries, or manually repeating steps in spreadsheet software, users build configurable preprocessing pipelines through a graphical interface and reuse them whenever similar datasets are received.

CleanSlate is a data preparation platform — not a BI tool, ML platform, or enterprise ETL system. It focuses entirely on producing high-quality, analysis-ready datasets while keeping users in control of every operation.

---

## 2. Product Philosophy

**Analyze → Inform → Let the User Decide**

The platform analyzes datasets and presents options, but every transformation is initiated by the user. CleanSlate never performs automatic preprocessing without explicit confirmation. This ensures transparency and prevents unwanted modifications to business-critical data.

---

## 3. Problem Statement

Most structured datasets are not immediately ready for analysis. Common issues include:

- Missing values
- Duplicate records
- Incorrect data types
- Inconsistent date formats
- Invalid email addresses
- Invalid phone numbers
- Unnecessary whitespace
- Outliers
- Formatting inconsistencies
- Multiple datasets requiring merging

Preparing data manually is repetitive, time-consuming, and error-prone. Existing solutions either require programming knowledge or provide far more functionality than many analysts need.

---

## 4. Target Users

### Primary
- **Data Analysts** — professionals working with CSV, Excel, and JSON datasets before analysis or visualization.
- **Business Users** — users working with operational datasets who lack programming or database knowledge.

### Secondary
- Students, Researchers, Operations teams, and anyone working with structured tabular datasets.

---

## 5. Supported File Formats

| Direction | Formats |
|---|---|
| Input | CSV, Excel (.xlsx), JSON |
| Output | CSV, Excel (.xlsx), JSON |

Supported conversions: CSV ↔ Excel, CSV ↔ JSON, Excel ↔ JSON.

---

## 6. Overall User Workflow

1. User Registration
2. Login
3. Upload Dataset
4. Dataset Validation & Profiling
5. Dataset Health Report
6. Data Preview
7. Build Preprocessing Pipeline
8. Review Pipeline Execution Summary
9. Execute Pipeline
10. Compare Before & After Results
11. Download Processed Dataset
12. Save & Reuse Pipeline on Future Datasets

---

## 7. Tech Stack & Dependencies

### Backend
- **Language**: Python 3.12+
- **Framework**: Django 6.0.7 (server-side rendering, ORM, auth, forms, routing)
- **Data Engine**: Pandas, NumPy
- **File Handling**: OpenPyXL (Excel), python-dateutil (dates)
- **Validation**: email-validator, phonenumbers
- **Database**: SQLite (dev), schema designed for PostgreSQL migration

### Frontend
- Django Templates + DTL
- HTML5, CSS3
- Bootstrap 5
- Minimal vanilla JavaScript (only where absolutely necessary)
- **No** React, Vue, Angular, Next.js, or any separate frontend framework

### Required Packages
```
django, pandas, numpy, openpyxl, python-dateutil, email-validator, phonenumbers
```

---

## 8. System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Django Web Layer                        │
│  Templates (DTL) · Views · Forms · URL Routing · Auth       │
├─────────────────────────────────────────────────────────────┤
│                   Django Apps                               │
│  authentication · dashboard · datasets · pipelines          │
├─────────────────────────────────────────────────────────────┤
│              Data Processing Engine (processing/)            │
│  profiling · cleaning · transformation · validation          │
│  outliers · merging · conversion · pipeline_executor         │
├─────────────────────────────────────────────────────────────┤
│              Database (SQLite → PostgreSQL-ready)            │
│  Users · Datasets · Pipelines · PipelineSteps · History     │
└─────────────────────────────────────────────────────────────┘
```

### Django Features to Utilize
- Authentication system, ORM, Models, Forms, Template Language, Template Inheritance, URL Routing, Middleware (as needed), Static/Media File Management, Admin, Migrations

---

## 9. Project Structure

```
CleanSlate/
├── cleanslate/              # Django project config (settings, urls, wsgi, asgi)
├── authentication/          # App: user registration, login, logout
├── dashboard/               # App: home page with stats
├── datasets/                # App: file upload, profiling, overview
├── pipelines/               # App: pipeline builder, execution, history, export
├── processing/              # Core engine (no Django dependency)
│   ├── profiling.py
│   ├── cleaning.py
│   ├── transformation.py
│   ├── validation.py
│   ├── outliers.py
│   ├── merging.py
│   ├── conversion.py
│   └── pipeline_executor.py
├── templates/               # Django HTML templates
│   ├── base.html
│   ├── authentication/
│   ├── dashboard/
│   ├── datasets/
│   └── pipelines/
├── static/                  # Static assets
├── media/                   # Uploaded & processed files
│   ├── uploads/
│   ├── processed/
│   └── samples/
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

The preprocessing engine is modular — every operation is an independent function. The Pipeline Executor simply calls those functions sequentially.

---

## 10. Database Design (Version 1)

### Users
Django's built-in `auth.User` model.

### Dataset
| Field | Type |
|---|---|
| id | BigAutoField (PK) |
| user | FK → User |
| file | FileField |
| original_name | CharField(255) |
| file_format | CharField(10): csv/xlsx/json |
| file_size | BigIntegerField |
| uploaded_at | DateTimeField (auto) |
| profiling_data | JSONField (nullable) |
| health_report | JSONField (nullable) |
| health_score | FloatField (nullable) |
| row_count | IntegerField (nullable) |
| column_count | IntegerField (nullable) |

### Pipeline
| Field | Type |
|---|---|
| id | BigAutoField (PK) |
| user | FK → User |
| name | CharField(255) |
| description | TextField |
| output_format | CharField(10): csv/xlsx/json |
| created_at | DateTimeField (auto) |
| updated_at | DateTimeField (auto) |

### PipelineStep
| Field | Type |
|---|---|
| id | BigAutoField (PK) |
| pipeline | FK → Pipeline |
| step_order | PositiveIntegerField |
| operation | CharField(50) |
| config | JSONField |

Unique together: `(pipeline, step_order)`

### ProcessingHistory
| Field | Type |
|---|---|
| id | BigAutoField (PK) |
| pipeline | FK → Pipeline (SET_NULL) |
| dataset | FK → Dataset (SET_NULL) |
| executed_at | DateTimeField (auto) |
| runtime | FloatField |
| output_format | CharField(10) |
| summary | JSONField |
| output_file | FileField (nullable) |

---

## 11. Module Specifications

### 11.1 Authentication Module
- Register, Login, Logout
- Purpose: store user-specific pipelines (not cloud storage for datasets in V1)

### 11.2 File Upload Module
- Accept CSV, Excel (.xlsx), JSON
- Validate: unsupported formats, empty files, corrupted files, invalid structures, encoding errors
- Only valid datasets proceed to profiling

### 11.3 Dataset Overview Dashboard
- **Data Preview**: first rows, column names, sample records
- **Dataset Profiling**: total rows/columns, column names, detected/suggested data types, nullable status
- **Schema Detection**: per-column detected type + suggested type + nullable
- **Health Report**: missing values, duplicates, invalid dates/emails/phones, formatting issues, outlier counts
- **Health Score**: 0–100 quality score from detected issues

### 11.4 Data Cleaning Module
- **Duplicate Handling**: detect and remove duplicate rows
- **Missing Values**: remove rows, replace with constant/mean/median/mode
- **Format Cleaning**: trim spaces, normalize text, standardize capitalization
- **Column Management**: rename columns, standardize naming

### 11.5 Data Transformation Module
- **Type Conversion**: text ↔ numeric, text ↔ date
- **Date Formatting**: DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD, etc.
- **Text Operations**: uppercase, lowercase, title case, remove special chars, regex replace
- **Derived Columns**: concat, sum, difference, product, quotient, custom formula

### 11.6 Data Validation Module
- **Email Validation**: detect invalid formats
- **Phone Validation**: detect invalid numbers and incorrect lengths
- **Date Validation**: detect invalid dates and incorrect formats

### 11.7 Outlier Detection Module
- **IQR Method**: values outside [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
- **Z-Score Method**: values with |z| > threshold (default 3)

### 11.8 Data Merging Module
- Inner, Left, Right joins
- Join on specified keys or common columns

### 11.9 Conversion Module
- DataFrame → CSV (string), XLSX (bytes), JSON (string)
- Appropriate MIME types per format

### 11.10 Pipeline Builder
- Ordered list of preprocessing operations
- Add, delete, reorder, configure steps
- Sequential execution

### 11.11 Pipeline Execution
- Before execution: display pipeline name, execution order, estimated operations
- User must explicitly approve execution
- After execution: processing report with runtime, operations performed
- Before vs After comparison (rows, columns, missing, duplicates)

### 11.12 Pipeline Management
- Create, edit, delete, save, rename pipelines
- Each pipeline stores: name, description, created date, last modified, output format, ordered steps
- Saved pipelines reusable on future datasets (manual selection only)

### 11.13 Processing History
- Lightweight execution records: pipeline name, execution date/time, runtime, output format
- Datasets themselves are not stored

### 11.14 Data Export
- Processed datasets downloadable as CSV, Excel, JSON
- Preview before download

---

## 12. Application Pages (Version 1)

| Page | Route |
|---|---|
| Login | `/auth/login/` |
| Signup | `/auth/signup/` |
| Dashboard | `/dashboard/` |
| Upload Dataset | `/datasets/upload/` |
| Dataset Overview | `/datasets/<id>/` |
| Pipeline Builder | `/pipelines/create/<id>/` and `/pipelines/<id>/` |
| Pipeline Execution | `/pipelines/<id>/execute/` |
| Results | `/pipelines/<id>/results/<hist_id>/` |
| Saved Pipelines | `/pipelines/` |
| Processing History | `/pipelines/history/` |
| Export | `/pipelines/export/` |

---

## 13. Implementation Rules

### Development Order
Always implement features in this exact order. Do not skip steps. Each module must be fully functional before proceeding.

1. Project setup (Django project, apps, settings, static/media, SQLite, requirements.txt, .gitignore, git init)
2. Authentication (register, login, logout)
3. Dashboard (home page with stats)
4. File upload (CSV/XLSX/JSON with validation)
5. Dataset profiling (type detection, schema detection)
6. Dataset overview (preview, profile, health report, health score)
7. Cleaning engine (duplicates, missing values, format cleaning, column management)
8. Transformation engine (type conversion, date formatting, text ops, derived columns)
9. Validation engine (email, phone, date validation)
10. Outlier detection (IQR, Z-score)
11. Merge engine (inner, left, right joins)
12. Conversion engine (CSV/XLSX/JSON output)
13. Pipeline builder (step management, ordering, configuration)
14. Pipeline execution (sequential orchestration)
15. Processing history (execution records)
16. Export module (download, pipeline export/import)

### General Rules
- Build module by module; every module fully functional before proceeding
- No placeholder implementations
- Avoid duplicated logic; prefer reusable helper functions
- Keep business logic outside Django views whenever possible
- Keep files reasonably small
- Follow modular architecture
- Each completed module should be tested before moving on
- The application must remain runnable throughout development
- Never leave the project in a broken state

### Code Style
- Meaningful variable names
- Type hints where appropriate
- Comments only where necessary
- Prioritize readability over cleverness

### Git
- Initialize git repository
- Commit after completing each major module with meaningful commit messages
- Every commit should leave the application in a runnable state

### Testing
- Manual verification per module before proceeding
- The application should remain runnable throughout development

---

## 14. Final Product Definition

CleanSlate is a no-code data preparation platform that enables users to inspect, profile, clean, transform, validate, merge, convert, and export structured datasets through configurable and reusable preprocessing pipelines. The platform emphasizes transparency, user control, and workflow reusability, allowing analysts and business users to standardize repetitive data preparation tasks without writing code while maintaining complete visibility into every transformation applied to their data.

### Non-Functional Requirements
- Modular and maintainable
- Support datasets with at least 100,000 rows
- Avoid unnecessary memory usage
- Handle invalid input gracefully
- Remain responsive
- Suitable for production-style portfolio presentation
