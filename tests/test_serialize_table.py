from typing import Generator
import shutil
import pytest
from pathlib import Path

from agreement.bible_api import get_chapter
from agreement.synoptic_table_model import SynopticTableModel, ParallelTuple, build_synoptic_table
from tests import config


@pytest.fixture
def test_temp_dir() -> Generator[Path, None, None]:
    # Create the temporary directory test_temp under ./tests, for json files
    temp_dir = Path(__file__).parent / 'test_temp'
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    yield temp_dir  # Provide the path to the test
    
    # Cleanup after the test runs
    shutil.rmtree(temp_dir)


def run_test(temp_dir: Path, table_title: str, passages, report_filename, color_scheme=None):
    synopsis_model: SynopticTableModel = build_synoptic_table(table_title, passages)

    json_path = temp_dir / f"{table_title}.json"

    # Serialize the table to JSON, and write it out to a file
    json_str = synopsis_model.to_json()
    assert isinstance(json_str, str)
    with open(json_path, 'w') as file:
        file.write(json_str)

    # Read the file back, and use it to build back a SynopticTableModel
    with open(json_path, 'r') as file:
        json_str = file.read()
    assert isinstance(json_str, str)
    recovered_model = SynopticTableModel.from_json(json_str)
    assert isinstance(recovered_model, SynopticTableModel)
    assert recovered_model.table_title == table_title
    assert recovered_model.column_headings == synopsis_model.column_headings
    assert recovered_model.word_counts == synopsis_model.word_counts
    assert recovered_model.token_agreements == synopsis_model.token_agreements

def test_round_trip_two_column(test_temp_dir: Path):
    run_test(
        test_temp_dir,
        "291 False Christs and False Prophets",
        [
            ParallelTuple(title="Mark 13:21-23", text=get_chapter("grc-byz1904", "καταμαρκον", 13, 21, 23)),
            ParallelTuple(title="Matt. 24:23-25", text=get_chapter("grc-byz1904", "καταματθαιον", 24, 23, 25))
        ],
        "291-Mark+Matt.svg"
    )


def test_round_trip_three_column(test_temp_dir: Path):
    run_test(
        test_temp_dir,
        "128 The Parable of the Mustard Seed (First Verse)",
        [
            ParallelTuple(title="Matt. 13:31", text=config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_13_31),
            ParallelTuple(title="Mark 4:30", text=config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_4_30),
            ParallelTuple(title="Luke 13:18-19", text=config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19)
        ],
        "128-Matt+Mark+Luke.html"
    )
