from celery import shared_task
from celery_progress.backend import ProgressRecorder
from time import sleep
from .database import Database
import numpy as np
import pandas as pd
import gspread
import time

gc = gspread.oauth()
db = Database()


@shared_task(bind=True)
def go_to_sleep(self, duration):
    progress_recorder = ProgressRecorder(self)
    for i in range(100):
        sleep(duration)
        progress_recorder.set_progress(i + 1, 100, f'On iteration {i}')
    return 'Done'

@shared_task(bind=True)
def import_sales_csv(self, file):
    progress_recorder = ProgressRecorder(self)
    sh = gc.open('Mad')
    worksheet = sh.worksheet("Uge")
    df = pd.read_csv(file)
    df = df.replace('–', '-', regex=True)
    for i, row in df.iterrows():
        print(row[0])
        progress_recorder.set_progress(i + 1, len(df.index), f'On iteration {i}')
        try:
            cell = worksheet.find(row[0])
            print(cell)
            time.sleep(1)
            worksheet.update_cell(cell.row, cell.col+1, row[1])
        except gspread.exceptions.CellNotFound:  # or except gspread.CellNotFound:
            print('Not found')
    return 'Done'