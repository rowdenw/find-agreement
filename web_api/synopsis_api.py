from flask import Flask, abort
from collections import OrderedDict
import re
import json

from pathlib import Path

current_dir = Path(__file__).resolve().parent.parent
MODEL_FOLDER = current_dir / "table_models"

app = Flask(__name__)


def load_synopsis_data(table_name):
    """
    Load a pre-computed synoptic table from a JSON file, 
    and serve it back to the Flask web service. This will
    probably eventually be pointed to the live synopsis application.
    """
    match = re.match(r"(\d+)", table_name)
    if not match:
        abort(404, description="Valid table number not found in table_name")

    table_number = match.group(1)
    file_path = MODEL_FOLDER / f"{table_number}.json"


    try:
        with open(file_path, 'r') as file:
            data = json.load(file, object_pairs_hook=OrderedDict)
            logging.info(f"data keys: {','.join(data)}")

            return data
    except FileNotFoundError:
        abort(404, description=f"Model file '{file_path} not found")

if __name__ == '__main__':
    app.run(host='0.0.0.0')  # 0.0.0.0 to make it accessible in PythonAnywhere environment
