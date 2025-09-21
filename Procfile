web: gunicorn gestao_estoque.wsgi:application
release: python manage.py collectstatic --noinput && python manage.py migrate
