from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from .tasks import import_sales_csv

def home_view(request, *args, **kvargs):
    return render(request, "home.html", {})


def index(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        filepath = fs.location + '/' + filename
        task = import_sales_csv.delay(filepath)
        return render(request, 'home.html', {'task_id' : task.task_id})

    return render(request, 'home.html', {})