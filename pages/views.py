from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import pandas as pd
from .tasks import import_sales_csv

def home_view(request, *args, **kvargs):
    return render(request, "home.html", {})


def index(request):
    if request.method == 'POST' and request.FILES['product-sales']:
        myfile = request.FILES['product-sales']
        df = pd.read_csv(myfile)
        task = import_sales_csv.delay(df.to_dict())
        return render(request, 'home.html', {'task_id' : task.task_id})

    return render(request, 'home.html', {})