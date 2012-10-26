web: newrelic-admin run-program gunicorn osmscraper.wsgi -b 0.0.0.0:$PORT
celeryd: newrelic-admin run-program python manage.py celeryd -E -B --loglevel=INFO
