from celery import shared_task
from celery_progress.backend import ProgressRecorder
from time import sleep
from smtplib import SMTP
import pandas as pd
from pandas.core.frame import DataFrame
import gspread
import time

credentials = {
    "type": "service_account",
    "project_id": "gaia-269412",
    "private_key_id": "c80751bdad79cd754f6a6499be5039725947c690",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC5FdODiX+z97B7\nHxuIdQx0NdqEx8wKzb9OcF/Pr6voec1HtmOoO/qvy4LdcL742+HJ9mbYB47L9MDN\nybP4fNju0pp8nXxF2g4WIsqhUEZyJWWZHrh6W1dJ1u5Vv+8hb+yTVIToDKFFtpbh\nnqzuAlEfyt/n2SQJ48flupi5+fDUjDvAPwFw/xs+icNba1rb8xM/m8vR59kPT/vm\nQA4Y0RaSOZ5/Y1AtM9cnTT4//25Rdto4Rn1NQu2Ukod+aM2xvMNf1RCKSFo3lCWT\nsq0m2yt+jtqpXf5foj8cDFW3qxU/nZNp0bECKcf54g0uRsgBXN3Yzir1YAM37egm\ni9SC1InnAgMBAAECggEAIY8mkeQdhpkzo69pQ53Ni0i0fXzor1DNDkDr7nFw3y8u\nnIEior91Xeitqs8loWPlFcSaszLznmGbj/SxsC2a+/qtzkiT3uqBwVu/l+5BR7Mm\nL9RVKMJlGlthTaUGi+6KW9BoZNbdaxGHXBN0UZeT9ArJ/HTvxudJOItT4+zA0Rjp\nMdHBU3ELGhk+HMnnVHdsJesdXKM7Hz30Z7tM4wGKv7vZrAFv7zK2ykMGX59QUP7J\ndJUTz3QPsmcH1Qj7A35rsg6PVHh+0hj/Fx1xcNprILPtlxHt+KUwoQFV+wpcn6j8\nOK2WKd+eU4fs2K6Q4QD7fBPQY5Wu+KinTWNcyEiDOQKBgQDmCcUGh8iqCQkNIoJo\n4C2XNnrFuXcaiQznPQ5Hws2fxqaxQ3PjrcgVIzLaWszrgMlshWfyUICBYPtnp20A\nxZRbh4qr4EfRlUeNaIfumWrHmQjcmJVqAp1UfDoe3HacIoYYH0T5/xi6ZafoYIsd\ncvSnXxUtyprtQXZ+x7hO8QkKJQKBgQDN+UiZfNHouoaWrp9kwjZ849pxEE5HrlTA\n/kEJIqqaVfos5d35l9vTqRuawJoSRA/Dq56HcVrhxnqeD6AL0aZuKxkM8FLNNx/z\n1VOfKEu+zpmctggWqrkDZR2+5QV5AWU2ciEF31Sx6KDwzm9j/Us59tcTMoYfwfOn\nMvMZxikYGwKBgFYSzcAVyoWk/9gEU5t+VlDAN8wIC4LISSW0+MTtJRdlszWcsZ49\nhiIym3KMiySLedK7UBug95Rxf2BXizfAtjRRURfiwbywCKfmtwYWLZglsOUpyq5x\n8ACOwwiNIWxmlposCRkp1EzagKs4hJUuUFDYCQqrRrEDz5y8ikAvfFxpAoGAJZ68\nVdxocntvDaKDVmHqldEAGtqBkbITpNRLiKGeS2YctYqeinHkIrqmYhN/kIqB3pk/\n8TkRAl/AEZKFBuOZ5FFW1/glB3pkCaMTDOTNQOJ3SBovTASOmkIjtrQZ1coddF5Q\nDcSGsZ/tlU3/JmIjFUkyaz01JiPEnus9X53D77UCgYAN+UyKGatLmrqW9oED/hrU\ni2kJlgWociBdltERE9j6DFmD8c9MfIg+Xe8dE4W/cR/oLfAQENqF8n9HGtn+5RVw\nURe0KDMJaB3iTUcaXzDsMZvaa8g+i4WrkTjRTG0Wa9oCGyeXgMEZmlSCWYl/c9ZA\ncYhhhFV5BbT4TwFs3RKQwg==\n-----END PRIVATE KEY-----\n",
    "client_email": "backend@gaia-269412.iam.gserviceaccount.com",
    "client_id": "117377217054336128994",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/backend%40gaia-269412.iam.gserviceaccount.com"
  }

gc = gspread.service_account_from_dict(credentials)


@shared_task(bind=True)
def import_subscription_csv(self, dict):
    progress_recorder = ProgressRecorder(self)
    sh = gc.open('Mad')
    worksheet = sh.worksheet("Uge")
    num_df = DataFrame.from_dict(dict)
    num_df["Antal"] = pd.to_numeric(num_df["Antal"])
    sales = num_df.groupby('Ret').sum()
    sales = sales.reset_index()
    print(len(sales.index))
    progress= 0
    missing = []
    for row in sales.itertuples():
        progress = progress + 1
        progress_recorder.set_progress(progress, len(sales.index))
        try:
            cell = worksheet.find(row.Ret)
            time.sleep(1)
            worksheet.update_cell(cell.row, cell.col+4, row.Antal)
        except gspread.exceptions.CellNotFound:  # or except gspread.CellNotFound:
            print('Not found - ' +row.Ret)
            missing.append(row.Ret + ' - ' + str(row.Antal) + ' \n')
    return missing

@shared_task(bind=True)
def import_sales_csv(self, dict):
    progress_recorder = ProgressRecorder(self)
    sh = gc.open('Mad')
    worksheet = sh.worksheet("Uge")
    df = DataFrame.from_dict(dict)
    df = df.replace('–', '-', regex=True)
    df = df.replace('’', '\'', regex=True)
    progress = 0
    missing = []
    for index, row in df.iterrows():
        print(row[0])
        progress = progress + 1
        progress_recorder.set_progress(progress, len(df.index))
        try:
            cell = worksheet.find(row[0])
            print(cell)
            time.sleep(1)
            worksheet.update_cell(cell.row, cell.col+1, row[1])
        except gspread.exceptions.CellNotFound:  # or except gspread.CellNotFound:
             missing.append(row[0] + ' - ' + str(row[1]) + '\n')
    return missing

@shared_task(bind=True)
def get_juice(self):
    sh = gc.open('Mad')
    val = sh.values_get("Uge!A62:F69")
    rows = val.get('values', [])
    df = pd.DataFrame(rows)
    smtp = SMTP()
    try:
        smtp.set_debuglevel(1)
        smtp.connect('mail.dandomain.dk', 366)
        print('Connect')
        try:
            smtp.login('andreas@gaiamadservice.dk', '17129223Ab')
            print('Login')
        except:
            print('Error: Unable to login')
        from_addr = "Andreas Broch <sri@gaiamadservice.dk>"
        to_addr = "andreas@gaiamadservice.dk"
        message_subject = "disturbance in sector 7"
        message_text = "Three are dead in an attack in the sewers below sector 7."
        message = """From: Andreas Broch <sri@gaiamadservice.dk>\n
        To: <andreas@gaiamadservice.dk>\n 
        Subject: Test af Python\n
        Dette er en autogeneret email med vores bestilling af juice. Hej.
        """.format(df.to_string())
        smtp.sendmail(from_addr, to_addr, message)
        smtp.quit()     
        print("Successfully sent email")
    except:
        print ("Error: unable to connect")
    return df