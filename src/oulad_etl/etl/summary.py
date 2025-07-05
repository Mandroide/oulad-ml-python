import pandas as pd
from tabulate import tabulate

from ..log import log  # global logging setup


def describe(df: pd.DataFrame) -> pd.DataFrame:
    """Return basic summary stats."""
    return df.describe(include="all")


def generate_report(dataset: dict[str, pd.DataFrame]) -> None:
    """Return raw summary stats."""
    summary_data = []
    for table_name, df in dataset.items():
        rows, cols = df.shape
        missing_rows = (
            df.isnull().any(axis=1).sum()
        )  # Número de filas con al menos un valor faltante
        column_names = df.columns.tolist()  # Para obtener los nombres de las columnas

        summary_data.append(
            {
                "Nombre_entidad": table_name,
                "Filas, Columnas": f"{rows}, {cols}",
                "Filas_faltantes": missing_rows,
                "nombre_columnas": column_names,
            }
        )
        log.info(f"  - Resumen de '{table_name}' calculado.")

    # Imprimir el DataFrame de resumen
    log.info("--- Resumen de datos ---")
    log.info(
        tabulate(
            summary_data,
            headers="keys",
            tablefmt="grid",
            stralign="left",
            showindex=False,
            maxcolwidths=[None, None, None, 30],
        )
    )
    log.info("Resumen generado con éxito.")
