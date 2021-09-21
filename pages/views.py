from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pandas as pd
from .tasks import import_sales_csv, import_subscription_csv, get_juice
import gspread
from smtplib import SMTP

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
        return render(request, 'home.html', {
            'df' : df.to_string(),
            'test' : 'test'
        })
    return render(request, 'home.html', {})

def opskrifter(request):
    return render(request, 'opskrifter.html')