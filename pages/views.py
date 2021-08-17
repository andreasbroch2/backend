from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pandas as pd
from .tasks import import_sales_csv, import_subscription_csv

def home_view(request, *args, **kvargs):
    return render(request, "home.html", {})


def index(request):
    if request.method == 'POST' and request.FILES['product-sales']:
        myfile = request.FILES['product-sales']
        df = pd.read_csv(myfile)
        task = import_sales_csv.delay(df.to_dict())
        return render(request, 'home.html', {'task_id' : task.task_id})
    elif request.method == 'POST' and request.FILES['subscription-sales']:
        myfile = request.FILES['subscription-sales']
        lines = myfile.readlines()
        string = "order_items"
        for line in lines:
            if string in line:
                lines.remove(line)
        myfile.close()
        csv = pd.read_table(myfile, header=None, sep=",", names=list(range(40)))
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
        task = import_subscription_csv.delay(num_df.to_dict())
        return render(request, 'home.html', {'task_id' : task.task_id})

    return render(request, 'home.html', {})