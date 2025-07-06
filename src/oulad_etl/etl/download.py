import io
import logging
import pathlib
import shutil
import zipfile

import requests

from oulad_etl.settings import settings

URL = "https://analyse.kmi.open.ac.uk/open-dataset/download"


def download_oulad(target: pathlib.Path) -> pathlib.Path:
    """
    Download the OULAD dataset from KMI website to the target path.
    :param target: Directory to save the OULAD dataset
    :return: input target path
    """
    log = logging.getLogger(__name__)
    log.info("Downloading OULAD dataset…")
    resp = requests.get(URL, timeout=60)
    resp.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(resp.content))
    z.extractall(target)
    log.info("Downloaded & extracted to %s ✅", target)
    shutil.copyfile(
        settings.excel_absolute_path, target / settings.excel_absolute_path.name
    )
    return target


def copy_excel_file(target: pathlib.Path) -> pathlib.Path:
    """
    Copy an Excel file to the target path.
    :param target: Directory to copy the Excel file
    :return: input target path
    """
    log = logging.getLogger(__name__)
    log.info("Copying %s to %s ✅", settings.excel_absolute_path, target)
    shutil.copyfile(
        settings.excel_absolute_path, target / settings.excel_absolute_path.name
    )
    log.info("Excel file copied %s ✅", target)

    return target
