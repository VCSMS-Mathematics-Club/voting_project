set -o errexit


pip install -r requirements.txt


python manage.py collectstatic --no-input

python manage.py migrate --noinput

gunicorn voting_project.wsgi:application --bind 0.0.0.0:10000

if [[$CREATE_SUPERUSER]]
then
  python manage.py createsuperuser --no-input
fi