import os

REPORT_OUTPUT_PATH = 'reports'

def get_report_path(filename):
    if not os.path.exists(REPORT_OUTPUT_PATH):
        os.makedirs(REPORT_OUTPUT_PATH)
    return os.path.join(REPORT_OUTPUT_PATH, filename)
