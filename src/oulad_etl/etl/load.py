from __future__ import annotations

import logging
import pathlib
import sys

import pandas as pd

from ..settings import settings
from .csv_models import TablesCsvSchema
from .excel_models import TablesExcelSchema

log = logging.getLogger(__name__)


def load_raw_csv(target: pathlib.Path) -> dict[str, pd.DataFrame]:
    """
    Load raw data from CSV file.
    :param target: Directory with csv files
    :return: Dictionary of dataframes
    """
    dataset = {}
    csv_tablas = {
        f"{TablesCsvSchema.courses}.csv": TablesCsvSchema.courses,
        f"{TablesCsvSchema.studentInfo}.csv": TablesCsvSchema.studentInfo,
        f"{TablesCsvSchema.assessments}.csv": TablesCsvSchema.assessments,
        f"{TablesCsvSchema.vle}.csv": TablesCsvSchema.vle,
        f"{TablesCsvSchema.studentAssessment}.csv": TablesCsvSchema.studentAssessment,
        f"{TablesCsvSchema.studentRegistration}.csv": TablesCsvSchema.studentRegistration,
        f"{TablesCsvSchema.studentVle}.csv": TablesCsvSchema.studentVle,
    }
    for file_name in csv_tablas:
        file_path = target / file_name
        try:
            df_name = file_name.replace(
                ".csv", ""
            )  # DataFrame name without csv extension
            dataset[df_name] = pd.read_csv(file_path)
            log.debug(f"  - '{file_name}' loaded as '{df_name}'")
        except FileNotFoundError:
            log.error("Expected %s not found", file_path)
            sys.exit(1)
    return dataset


def load_raw_excel() -> dict[str, pd.DataFrame]:
    """
    Load raw data from an Excel file.
    :return: Dictionary of dataframes
    """
    dataset = {}
    for table in [*TablesExcelSchema]:
        try:
            dataset[table] = pd.read_excel(
                settings.excel_absolute_path, sheet_name=table
            )
            log.debug(f"  - sheet '{table}' loaded as '{table}'")
        except FileNotFoundError:
            log.error("Expected %s not found", table)
            sys.exit(1)
    return dataset


def save_to_csv(df: pd.DataFrame, target_file_path: pathlib.Path) -> None:
    # Guardar resultado
    df.to_csv(target_file_path, index=False)
    log.info(f"ETL file save correctly in: {target_file_path}")
