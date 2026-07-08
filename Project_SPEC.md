# CleanSlate Development Specification


Project Name - CleanSlate

Django Project Name - cleanslate

This document is the single source of truth for the CleanSlate project.

Any code generated for this project must follow this specification.

If implementation decisions need to be made, prefer consistency with this document over introducing additional features.

Do not implement functionality outside the defined MVP unless explicitly instructed.

If an ambiguity exists, preserve modularity and maintainability rather than adding complexity.


## Implementation Rules

The project must be built as if it were a production-quality software project rather than a college assignment.

## Required Dependencies

Automatically install the latest stable versions of in the virtual environment created already by me

- django
- pandas
- numpy
- openpyxl
- python-dateutil
- email-validator
- phonenumbers

Generate a requirements.txt after installation.

If additional packages become necessary during implementation, install them automatically and update requirements.txt.


The virtual environment (venv) has already been created and activated.

Do NOT create another virtual environment.

Continue by:
- Activating it 
- Install required dependencies
- Create the Django project
- Create Django apps
- Configure Bootstrap
- Configure Static Files
- Configure Media Files
- Configure SQLite
- Generate requirements.txt
- Generate .gitignore
- Initialize Git repository

Verify that the Django development server starts successfully before implementing features.
Verify that the Django server starts successfully before implementing features.

### General Rules

- Build the application module by module.
- Every module must be fully functional before proceeding.
- Do not create placeholder implementations.
- Avoid duplicated logic.
- Prefer reusable helper functions.
- Keep business logic outside Django views whenever possible.
- Keep files reasonably small.
- Follow modular architecture.

---

### Code Style

- Use meaningful variable names.
- Use type hints where appropriate.
- Add comments only where necessary.
- Avoid overly clever code.
- Prioritize readability.

---

### Project Structure

The preprocessing engine must be separated into independent modules.

Example:

processing/
    profiling.py
    cleaning.py
    transformation.py
    validation.py
    conversion.py
    merging.py
    outliers.py
    pipeline_executor.py

No single preprocessing.py file should contain all logic.

---

### Development Order

Always implement features in the following order:

1. Project setup
2. Authentication
3. Dashboard
4. File upload
5. Dataset profiling
6. Dataset overview
7. Cleaning engine
8. Transformation engine
9. Validation engine
10. Outlier detection
11. Merge engine
12. Conversion engine
13. Pipeline builder
14. Pipeline execution
15. Processing history
16. Export module

Do not skip steps.

Each completed module should be tested before moving to the next.

---

### Backend Code

- python
- Django


The project will not use React, Next.js, Vue, Angular, or any separate frontend framework.

The objective is to fully leverage Django's server-side rendering, template inheritance, forms, authentication system, ORM, and routing capabilities.

### UI Guidelines

Use:
Frontend:

Frontend

The frontend must be implemented entirely using Django's server-side rendering.

Use:

- Django Templates
- Django Template Language (DTL)
- Django Forms
- Template Inheritance
- HTML5
- CSS3
- Bootstrap 5

Use JavaScript only where absolutely necessary for small interactive features.

Do not use React, Vue, Angular, Next.js or any other frontend framework.

Do not introduce React, Vue, Angular, or other frontend frameworks.

The UI should remain clean, responsive, and easy to navigate.

---

## Django Features to Utilize

The project should make use of Django's core capabilities wherever appropriate.

These include:

- Django Authentication
- Django ORM
- Django Models
- Django Forms
- Django Template Language
- Template Inheritance
- URL Routing
- Middleware (if required)
- Static File Management
- Media File Handling
- Django Admin
- Migrations

### Database

Use Django ORM.

Development:

- SQLite

The schema should be designed so PostgreSQL can replace SQLite later with minimal changes.

---

### Dependencies

Automatically create:

- Virtual Environment
- requirements.txt
- .gitignore

Automatically install all required packages.

If additional dependencies are needed, install them automatically.

---

### Git

Initialize a Git repository.

Commit after completing each major module using meaningful commit messages.

---

### Testing

Each module should be manually verified before proceeding.

The application should remain runnable throughout development.

Never leave the project in a broken state.

---

### Final Goal

The completed project should be:

- Fully functional
- Modular
- Extensible
- Easy to maintain
- Suitable for production-style portfolio presentation



# CleanSlate

## Project Overview

CleanSlate is a web-based no-code data preparation platform designed for data analysts, business users, and anyone working with structured datasets. The platform focuses on preparing raw datasets for analysis by providing an end-to-end environment for dataset profiling, cleaning, transformation, validation, merging, conversion, and reusable preprocessing pipelines.

The objective of CleanSlate is to simplify the repetitive preprocessing work that is required before data analysis. Instead of writing Python scripts, SQL queries, or manually repeating preprocessing steps in spreadsheet software, users can build configurable preprocessing pipelines through a graphical interface and reuse them whenever similar datasets are received.

CleanSlate is designed as a data preparation platform rather than a business intelligence tool, machine learning platform, or enterprise ETL orchestration system. The platform focuses entirely on preparing high-quality, analysis-ready datasets while allowing users to remain in complete control of every preprocessing operation.

---

# Problem Statement

Most structured datasets received by analysts and businesses are not immediately ready for analysis. Before any reporting or visualization can begin, datasets commonly contain:

* Missing values
* Duplicate records
* Incorrect data types
* Inconsistent date formats
* Invalid email addresses
* Invalid phone numbers
* Unnecessary whitespace
* Outliers
* Formatting inconsistencies
* Multiple datasets requiring merging

Preparing this data manually is repetitive, time-consuming, and error-prone. Similar preprocessing workflows are repeatedly applied to recurring datasets such as monthly sales reports, customer records, inventory data, HR datasets, and operational reports.

Existing solutions either require programming knowledge (Python, SQL, Pandas) or provide significantly more functionality than many analysts actually require.

CleanSlate focuses specifically on solving the data preparation stage through a guided, reusable workflow.

---

# Target Users

## Primary Users

### Data Analysts

Professionals who frequently work with CSV, Excel, and JSON datasets before performing analysis or visualization.

### Business Users

Users who regularly work with operational datasets but do not possess programming or database knowledge.

---

## Secondary Users

* Students
* Researchers
* Operations teams
* Anyone working with structured tabular datasets

---

# Product Philosophy

CleanSlate follows an assisted preprocessing approach.

The platform analyzes datasets and presents preprocessing options, but every transformation is initiated by the user.

The platform never performs automatic preprocessing without explicit confirmation.

The philosophy can be summarized as:

**Analyze → Inform → Let the User Decide**

This ensures transparency and prevents unwanted modifications to business-critical data.

---

# Supported File Formats

## Input

* CSV
* Excel (.xlsx)
* JSON

## Output

* CSV
* Excel (.xlsx)
* JSON

Supported conversions include:

* CSV ↔ Excel
* CSV ↔ JSON
* Excel ↔ JSON

---

# Overall User Workflow

1. User Registration
2. Login
3. Upload Dataset
4. Dataset Validation
5. Dataset Profiling
6. Dataset Health Report
7. Data Preview
8. Build Preprocessing Pipeline
9. Review Pipeline Execution Summary
10. Execute Pipeline
11. Compare Before & After Results
12. Download Processed Dataset
13. Save Pipeline
14. Reuse Pipeline on Future Datasets

---

# Authentication Module

Users can:

* Register
* Login
* Logout

Authentication exists primarily to store user-specific preprocessing pipelines.

The platform does not function as cloud storage for datasets during Version 1.

---

# File Upload Module

Users may upload:

* CSV files
* Excel (.xlsx) files
* JSON files

The upload system performs validation before processing.

Validation includes:

* Unsupported file formats
* Empty files
* Corrupted files
* Invalid file structures
* Encoding errors where applicable

Only valid datasets proceed to profiling.

---

# Dataset Overview Dashboard

After upload, CleanSlate generates a complete dataset overview.

## Data Preview

Displays:

* First few rows
* Column names
* Sample records

---

## Dataset Profiling

Displays:

* Total rows
* Total columns
* Column names
* Detected data types
* Numeric columns
* Text columns
* Date columns

---

## Schema Detection

Each column is analyzed to determine:

* Detected data type
* Suggested data type (where applicable)
* Nullable status

Example:

| Column      | Detected Type | Suggested Type |
| ----------- | ------------- | -------------- |
| Revenue     | String        | Currency       |
| Order_Date  | String        | Date           |
| Customer_ID | Integer       | Integer        |

---

## Dataset Health Report

Displays:

* Missing values
* Duplicate records
* Invalid dates
* Invalid emails
* Invalid phone numbers
* Formatting inconsistencies
* Outlier counts

---

## Data Health Score

An overall quality score generated from detected issues within the dataset.

This score provides users with a quick assessment of dataset quality before preprocessing.

---

# Data Cleaning Module

Available operations include:

## Duplicate Handling

* Detect duplicate rows
* Remove duplicates

---

## Missing Value Handling

Options include:

* Remove rows
* Replace with constant values
* Replace using Mean
* Replace using Median
* Replace using Mode

---

## Format Cleaning

Operations include:

* Trim leading spaces
* Trim trailing spaces
* Normalize text formatting
* Standardize capitalization

---

## Column Management

Users can:

* Rename columns
* Standardize naming conventions

---

# Data Transformation Module

Supported transformations include:

## Data Type Conversion

Examples:

* Text → Numeric
* Numeric → Text
* Text → Date
* Date → Text

---

## Date Formatting

Examples:

* DD/MM/YYYY
* MM/DD/YYYY
* YYYY-MM-DD

---

## Text Transformations

Operations include:

* Uppercase
* Lowercase
* Title Case
* Remove special characters

---

## Derived Columns

Users can generate new columns using existing columns.

Examples:

* Full Name = First Name + Last Name
* Profit = Revenue − Cost

---

# Data Validation Module

Validation includes:

## Email Validation

* Detect invalid email formats

---

## Phone Validation

* Detect invalid phone numbers
* Detect incorrect lengths

---

## Date Validation

* Detect invalid dates
* Detect incorrect formats

---

# Outlier Detection Module

Supported methods:

## IQR

Interquartile Range based outlier detection.

## Z-Score

Standard score based outlier detection.

---

# Data Merging Module

Supports combining multiple datasets.

Operations include:

* Merge datasets
* Join datasets

Supported joins:

* Inner Join
* Left Join
* Right Join

Common join keys include:

* customer_id
* employee_id
* product_id

---

# Pipeline Builder

The Pipeline Builder is the core feature of CleanSlate.

Users build preprocessing workflows as an ordered list of operations.

Example:

1. Remove Duplicates
2. Fill Missing Values
3. Standardize Dates
4. Validate Emails
5. Convert Output to Excel

Users may:

* Add steps
* Delete steps
* Reorder steps
* Edit step configurations

The pipeline executes sequentially.

---

# Pipeline Execution Preview

Before execution, CleanSlate displays a complete summary of the pipeline.

Example:

Pipeline Name:
Monthly Sales Cleaning

Execution Order:

1. Remove Duplicates
2. Fill Missing Values (Median)
3. Standardize Dates
4. Validate Emails
5. Convert Output to Excel

Estimated Operations:

* Duplicate rows detected
* Missing values to be handled
* Date formats to be standardized

The user must explicitly approve execution.

---

# Pipeline Management

Users may:

* Create pipelines
* Edit pipelines
* Delete pipelines
* Save pipelines
* Rename pipelines
* Reorder pipeline steps

Each pipeline stores:

* Name
* Description
* Created Date
* Last Modified
* Output Format
* Ordered Processing Steps

---

# Pipeline Reusability

Saved pipelines can be reused whenever users receive similar datasets.

Example:

Monthly Sales Pipeline

Instead of rebuilding the workflow every month:

Upload February Sales Dataset

↓

Select Monthly Sales Pipeline

↓

Execute

↓

Download Clean Dataset

Pipeline selection always remains manual.

The system never automatically selects or executes pipelines.

---

# Processing Summary

After execution, CleanSlate displays a processing report.

Example:

Pipeline Completed Successfully

Execution Time:
1.6 seconds

Operations Performed:

* Removed 18 duplicate rows
* Filled 42 missing values
* Standardized 67 dates
* Validated 540 email addresses
* Converted output to Excel

---

# Before vs After Comparison

Users can compare datasets before downloading.

Comparison includes:

Original Dataset

* Rows
* Columns
* Missing Values
* Duplicate Records

Processed Dataset

* Rows
* Columns
* Missing Values
* Duplicate Records

This provides transparency regarding every preprocessing operation performed.

---

# Data Export

Processed datasets can be exported as:

* CSV
* Excel
* JSON

Users may preview processed data before downloading.

---

# Processing History

CleanSlate stores lightweight execution history.

Stored information includes:

* Pipeline Name
* Execution Date
* Execution Time
* Runtime
* Output Format

Datasets themselves are not stored.

---

# System Architecture

## Frontend

* Django Templates
* HTML5
* CSS3
* Bootstrap 5
* Minimal JavaScript

Responsible for:

* Authentication pages
* Upload interface
* Dataset overview
* Pipeline builder
* Processing reports

---

## Backend

Python

Framework:

* Django

Responsibilities:

* Authentication
* Routing
* Business Logic
* Pipeline Execution
* File Handling

---

## Data Processing Engine

Libraries:

* Pandas
* NumPy
* OpenPyXL
* Python JSON module

Responsibilities:

* Cleaning
* Transformation
* Validation
* Dataset Profiling
* Data Conversion
* Data Merging
* Outlier Detection
* Pipeline Execution

---

## Database

Development:

* SQLite


---

# Database Design (Version 1)

Tables include:

## Users

Stores authentication details.

---

## Pipelines

Stores:

* Pipeline Name
* Description
* User ID
* Output Format
* Creation Date

---

## Pipeline Steps

Stores:

* Step Order
* Processing Operation
* Configuration Parameters

---

## Processing History

Stores:

* Pipeline ID
* Execution Date
* Runtime
* Output Format

---.

---

# Final Product Definition

CleanSlate is a no-code data preparation platform that enables users to inspect, profile, clean, transform, validate, merge, convert, and export structured datasets through configurable and reusable preprocessing pipelines. The platform emphasizes transparency, user control, and workflow reusability, allowing analysts and business users to standardize repetitive data preparation tasks without writing code while maintaining complete visibility into every transformation applied to their data.

# Application Pages

Version 1 will contain the following pages.

## Authentication

- Login
- Signup

---

## Dashboard

Displays:

- Welcome message
- Upload Dataset button
- Recently Used Pipelines
- Processing History
- Saved Pipelines

---

## Upload Dataset

- Upload CSV
- Upload Excel
- Upload JSON

---

## Dataset Overview

Contains:

- Data Preview
- Dataset Profiling
- Health Report
- Schema Detection

---

## Pipeline Builder

Allows users to:

- Add preprocessing steps
- Delete steps
- Reorder steps
- Configure operations

---

## Pipeline Execution

Displays:

- Pipeline Summary
- Estimated Operations
- Execute button

---

## Results

Displays:

- Before vs After comparison
- Processing Summary
- Download button

---

## Saved Pipelines

Displays:

- Pipeline list
- Edit
- Delete
- Execute

---

## Processing History

Displays previous executions.


CleanSlate/

manage.py

requirements.txt

README.md

.gitignore

cleanslate/

authentication/

dashboard/

datasets/

pipelines/

processing/

processing/

    cleaning.py

    transformation.py

    validation.py

    conversion.py

    profiling.py

    merging.py

    outliers.py

    pipeline_executor.py

templates/

static/

media/


# Data Processing Engine

The processing engine should be modular.

Every preprocessing operation should exist as an independent function.

The Pipeline Executor should simply execute those functions sequentially.

Pipeline

↓

Operation 1

↓

Operation 2

↓

Operation 3

↓

Return Processed Data



# Functional Requirements

The application shall:

- Allow user registration.
- Allow login.
- Upload datasets.
- Profile datasets.
- Generate health reports.
- Detect duplicates.
- Detect missing values.
- Transform data.
- Merge datasets.
- Convert formats.
- Save pipelines.
- Execute pipelines.
- Export processed data.



# Non Functional Requirements

The application must:

- Be modular.
- Be maintainable.
- Support datasets containing at least 100,000 rows.
- Avoid unnecessary memory usage.
- Handle invalid input gracefully.
- Remain responsive.




Then begin implementation.


If a feature is large, implement it completely before beginning the next feature.

Do not leave partially implemented modules.

Every commit should leave the application in a runnable state.

