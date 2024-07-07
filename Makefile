init:
    pip install -r requirements.txt

test:
    python -m unittest discover --pattern 'test_*.py' --start-directory 'tests' --verbose

.PHONY: init test
