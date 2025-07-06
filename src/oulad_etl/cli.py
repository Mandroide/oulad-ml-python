import pathlib

import click

from oulad_etl.etl.csv_models import TablesCsvSchema

from .etl import download, load, summary, transform
from .log import log  # global logging setup


@click.group()
def cli() -> None:
    """Run `poetry run etl --help` for sub-commands."""
    pass


@cli.command(help="Run the full pipeline (download → transform → load).")
@click.option("--data-dir", default="data/raw", show_default=True)
def run(data_dir: str) -> None:
    raw_path = pathlib.Path(data_dir)
    processed_path = raw_path.parent / "processed"
    raw_path.mkdir(parents=True, exist_ok=True)
    processed_path.mkdir(parents=True, exist_ok=True)

    target_raw_path = download.download_oulad(raw_path)
    target_raw_path = download.copy_excel_file(target_raw_path)

    dfs_csv = load.load_raw_csv(target_raw_path)
    dfs_excel = load.load_raw_excel()

    summary.generate_report(dfs_csv)
    summary.generate_report(dfs_excel)

    # Union

    dfs_csv = transform.clean_csv(dfs_csv, processed_path)
    dfs_excel = transform.clean_excel(dfs_excel, processed_path)

    # Merge
    df_etl = transform.merge_csv(
        df_student_assessment=dfs_csv[TablesCsvSchema.studentAssessment],
        df_assessments=dfs_csv[TablesCsvSchema.assessments],
        df_student_info=dfs_csv[TablesCsvSchema.studentInfo],
    )

    load.save_to_csv(df=df_etl, target_file_path=processed_path / "etl_output.csv")

    # Encode studentInfo fields as ordinals
    dfs_csv[TablesCsvSchema.studentInfo] = transform.encode_as_ordinal(
        dfs_csv[TablesCsvSchema.studentInfo]
    )
    load.save_to_csv(
        df=dfs_csv[TablesCsvSchema.studentInfo],
        target_file_path=processed_path / "studentInfo_ordinal.csv",
    )

    log.info("Pipeline completed ✅")


if __name__ == "__main__":
    cli()
