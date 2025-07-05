import pathlib

import click

from oulad_etl.etl.models import TablesSchema

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

    dfs = load.load_raw(target_raw_path)
    summary.generate_report(dfs)

    dfs = transform.clean(dfs, processed_path)

    # Merge
    df_etl = transform.merge(
        df_student_assessment=dfs[TablesSchema.studentAssessment],
        df_assessments=dfs[TablesSchema.assessments],
        df_student_info=dfs[TablesSchema.studentInfo],
    )

    load.save_to_csv(df=df_etl, target_file_path=processed_path / "etl_output.csv")

    # Encode studentInfo fields as ordinals
    dfs[TablesSchema.studentInfo] = transform.encode_as_ordinal(
        dfs[TablesSchema.studentInfo]
    )
    load.save_to_csv(
        df=dfs[TablesSchema.studentInfo],
        target_file_path=processed_path / "studentInfo_ordinal.csv",
    )

    log.info("Pipeline completed ✅")


if __name__ == "__main__":
    cli()
