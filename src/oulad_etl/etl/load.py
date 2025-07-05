from __future__ import annotations

import logging
import pathlib
import sys

import pandas as pd

from .models import TablesSchema

log = logging.getLogger(__name__)


def load_raw(target: pathlib.Path) -> dict[str, pd.DataFrame]:
    """
    Load raw data from CSV file.
    :param target: Directory with csv files
    :return: Dictionary of dataframes
    """
    dataset = {}
    csv_tablas = {
        f"{TablesSchema.courses}.csv": TablesSchema.courses,
        f"{TablesSchema.studentInfo}.csv": TablesSchema.studentInfo,
        f"{TablesSchema.assessments}.csv": TablesSchema.assessments,
        f"{TablesSchema.vle}.csv": TablesSchema.vle,
        f"{TablesSchema.studentAssessment}.csv": TablesSchema.studentAssessment,
        f"{TablesSchema.studentRegistration}.csv": TablesSchema.studentRegistration,
        f"{TablesSchema.studentVle}.csv": TablesSchema.studentVle,
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


def save_to_csv(df: pd.DataFrame, target_file_path: pathlib.Path) -> None:
    # Guardar resultado
    df.to_csv(target_file_path, index=False)
    log.info(f"ETL file save correctly in: {target_file_path}")
