#!/bin/sh

set -e

echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

#if [ "$AWS_RDS_USERNAME" ]
#then
#    python manage.py createsuperuser \
#        --noinput \
#        --username $AWS_RDS_USERNAME \
#        --email $DJANGO_E
#fi

uwsgi --socket :8000 --need-app --master --enable-threads --module app.wsgi --wsgi-file DjangoProject/wsgi.py