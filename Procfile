web: python manage.py migrate && python manage.py seed_data && python manage.py collectstatic --noinput && gunicorn treefel.wsgi --bind 0.0.0.0:$PORT
