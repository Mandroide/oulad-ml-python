# OULAD-ML-PYTHON
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
![Build status](https://img.shields.io/github/actions/workflow/status/Mandroide/oulad-ml-python/ci.yml)

This is an implementation of EDA and ETL for [OULAD Dataset](https://analyse.kmi.open.ac.uk/#open-dataset).

The environment variables must be modified before running the app.

## Initial Diagram
![Relational Diagram](resources/diagram.svg)

## Basic Structure of the project
```
oulad-ml-python/                  # ── project root ────────────────────────────
└── .github/
    └── workflows/
        └── ci.yml              # lint → type-check → test → coverage
├── config/
│   ├── logging.yml             # PyYAML logging config
├── data/                       # ── datasets --------------------------------
│   ├── raw/                    # ZIP + extracted CSVs
│   └── processed/              # cleaned parquet, features, etc.
├── notebooks/                  # Jupyter EDA
│   └── 00_eda_overview.ipynb
├── resources/                  # README resources
│   └── diagram.svg
├── src/oulad_etl/              # ── importable package ----------------------
│   ├── __init__.py
│   ├── settings.py             # env handling (pydantic)
│   ├── log.py                  # loads YAML + sets root logger
│   ├── etl/
│   │   ├── download.py         # fetch + unzip
│   │   └── load.py             # Load or Save CSV FILES
│   │   └── models.py           # enums of columns of each model
│   │   └── summary.py          # contains method with raw summary stats
│   │   ├── transform.py        # tidy up (pandas)
│   └── cli.py                  # `poetry run oulad-etl …`
├── tests/
│   └── unit/
│       └── test_dummy.py
├── .env.example                # DB creds template (see below)
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml              # Poetry deps & tooling
├── README.md
```
## Requirements
-  [Poetry](https://python-poetry.org/docs/#installation)

To install poetry through pip run:

```bash
pip install poetry
```

## Quick start

### Boostrap the app
```bash
git clone <repo-url>
cd oulad-ml-python
poetry install
poetry run pre-commit install
poetry run ipython kernel install --user --name eda_overview
```

### Run the ETL and EDA pipeline
```bash
poetry run etl run
poetry run jupyter lab --notebook-dir notebooks
```
