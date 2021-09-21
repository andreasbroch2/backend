from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pandas as pd
from .tasks import import_sales_csv, import_subscription_csv, get_juice
import gspread
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

def home_view(request, *args, **kvargs):
    return render(request, "home.html", {})


def index(request):
    if 'product-sales' in request.FILES:
        myfile = request.FILES['product-sales']
        df = pd.read_csv(myfile)
        task = import_sales_csv.delay(df.to_dict())
        return render(request, 'home.html', {'task_id' : task.task_id})
    elif 'subscription-sales' in request.FILES:
        file = request.FILES['subscription-sales']
        lines = file.readlines()
        string = "order_items"
        string= string.encode('utf-8')
        newlines = []
        for line in lines:
            if string in line:
                lines.remove(line)
            else:
                line = line.decode()
                line = line.replace('"', '')
                newlines.append(line)
        csv = pd.DataFrame([sub.split(",") for sub in newlines])
        df = pd.DataFrame(columns=['Ret', 'Antal'])

        for column in csv:
            if(column > 1):
                if (column % 2) == 0:
                    xtra = pd.DataFrame(data=csv.iloc[:, [column, column+1]])
                    xtra.columns = ['Ret', 'Antal']
                    df = df.append(xtra, ignore_index=True)                             
        df = df.dropna()
        # Eliminate invalid data from dataframe (see Example below for more context)
        num_df = (df.drop(['Antal'], axis=1).join(df['Antal'].apply(pd.to_numeric, errors='coerce')))
        num_df = num_df.dropna()
        # print(num_df)
        task = import_subscription_csv.delay(num_df.to_dict())
        return render(request, 'home.html', {
            'task_id' : task.task_id
            })
    elif 'juice' in request.POST:
        sh = gc.open('Mad')
        val = sh.values_get("Uge!A62:F69")
        rows = val.get('values', [])
        df = pd.DataFrame(rows)
        smtp = SMTP()
        status = ''
        loginstatus = ''
        test = ''
        try:
            smtp.set_debuglevel(1)
            smtp.connect('mail.dandomain.dk', 366)
            print('Connect')
            try:
                smtp.login('andreas@gaiamadservice.dk', '17129223Ab')
                loginstatus = 'Succesfull Login'
            except:
                loginstatus = 'Error: Unable to login'    
            message = MIMEMultipart()
            test = '1'
            message['Subject'] = 'Juice order - Gaia'
            message['From'] = '<Andreas>sri@gaiamadservice.dk'
            message['To'] = 'andreas@gaiamadservice.dk'

            body_content = """
            <html>
            <head></head>
            <body>
                {0}
            </body>
            </html>
            """.format(df.to_html())
            message.attach(MIMEText(body_content, "html"))
            msg_body = message.as_string()
            test = '2'
            smtp.sendmail(message['From'], message['To'], msg_body)
            test = '3'
            smtp.quit()
            status = "Successfully sent email"
        except:
            status = "Error: unable to connect"
        return render(request, 'home.html', {
            'df' : str(df),
            'status' : status,
            'login' : loginstatus,
            'test' : test
        })
    return render(request, 'home.html', {})

def opskrifter(request):
    return render(request, 'opskrifter.html')