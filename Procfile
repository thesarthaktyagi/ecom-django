release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn ecom_website.wsgi --log-file -