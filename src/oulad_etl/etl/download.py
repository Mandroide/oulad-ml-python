import io
import logging
import pathlib
import zipfile

import requests

URL = "https://analyse.kmi.open.ac.uk/open-dataset/download"


def download_oulad(target: pathlib.Path) -> pathlib.Path:
    log = logging.getLogger(__name__)
    log.info("Downloading OULAD dataset…")
    resp = requests.get(URL, timeout=60)
    resp.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(resp.content))
    z.extractall(target)
    log.info("Downloaded & extracted to %s ✅", target)
    return target
