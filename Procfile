web: gunicorn hotdeal.wsgi --log-file -
web: python manage.py collectstatic --no-input; gunicorn hotdeal.wsgi --log-file - --log-level debug