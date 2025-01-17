import base64
import io
import json
import logging
import os
import os.path as osp
import traceback
from typing import Union

import pandas as pd

from utils.utils_logging import configure_default_logging

configure_default_logging()
logger = logging.getLogger(__name__)



def check_cwd():
    basename = osp.basename(osp.normpath(os.getcwd()))
    assert basename.lower() in [
        "dygetviz"], "Must run this file from parent directory (dygetviz/)"


def to_dict(obj):
    # Convert object to a dict
    obj_dict = vars(obj).copy()

    # Iterate over attributes
    for key, val in obj_dict.items():
        # Check if value is an object with attributes
        if hasattr(val, "__dict__"):
            # Recursively convert object attribute to dict
            obj_dict[key] = to_dict(val)
    return obj_dict


def parse_contents(contents, filename):
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assuming the uploaded file is a CSV, parse it
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            return df
        else:
            return "Invalid file format, please upload a CSV file."
    except Exception as e:
        print(e)
        return "An error occurred while processing the file."



def read_markdown_into_html(path: str):
    """
    An archived function that reads markdown into html.
    Args:
        path:

    Returns:

    """
    import markdown
    with open(path, 'r', encoding='utf-8') as markdown_file:
        markdown_text = markdown_file.read()

    # Convert Markdown to HTML
    html_output = markdown.markdown(markdown_text)



    return html_output

def dump_and_check(d: Union[list, dict], outdir: str, max_tries: int = 10):
    """Dump tweets to json file and check if the file exists"""

    num_retries = 0
    while True:
        try:
            json.dump(d, open(outdir, 'w', encoding='utf-8'), indent=2,
                      sort_keys=True)
            json.load(open(outdir, 'r', encoding='utf-8'))

            break

        except Exception as e:
            num_retries += 1
            logger.error(
                f"[ERROR] Dumping or reloading failed, retrying {num_retries}...")
            logger.error(outdir)
            traceback.print_exc()
            if num_retries >= max_tries:
                exit(1)

def get_modified_time_of_file(path):
    import datetime, pathlib
    model_metadata = pathlib.Path(path).stat()
    mtime = datetime.datetime.fromtimestamp(model_metadata.st_mtime)
    ctime = datetime.datetime.fromtimestamp(model_metadata.st_ctime)
    logger.info(f"\t{osp.basename(path)}: modified {mtime} | created {ctime}")
    return mtime, ctime

