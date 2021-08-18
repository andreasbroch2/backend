web: gunicorn mysite.wsgi
worker: celery -A mysite worker --pool=solo -l info -c 4