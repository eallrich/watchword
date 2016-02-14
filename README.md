watchword
=========

Get notified when things don't happen.

Rough and Ready Setup
---------------------
```shell
$ sudo adduser --disabled-password --gecos "" watchword
$ sudo -iu watchword
# Should now be in the watchword user's home directory
$ git clone https://github.com/eallrich/watchword
$ cd watchword
$ virtualenv .
$ echo "export DJANGO_SETTINGS_MODULE=ww.settings" >> bin/activate
$ source bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
# Define a better secret key
$ echo "SECRET_KEY = $(python -c "import base64, os; print base64.b64encode(os.urandom(40))")" > ww/local.py
# Set up Mailgun config for sending emails
$ echo "EMAIL_AUTHOR = 'watchword@example'" >> ww/local.py
$ echo "EMAIL_BACKEND = 'django_mailgun.MailgunBackend'" >> ww/local.py
$ echo "MAILGUN_ACCESS_KEY = 'SUPER-SECRET'" >> ww/local.py
$ echo "MAILGUN_SERVER_NAME = 'example.com'" >> ww/local.py
# Schedule cron to send flares for alarms
$ crontab -e
# Add three lines like the following:
#     ROOT=/home/watchword/watchword
#     DJANGO_SETTINGS_MODULE=ww.settings
#     */5 * * * * $ROOT/bin/python $ROOT/manage.py fireflares > $ROOT/cron.log 2>&1
# Then save and close the file
$ honcho start
```

Inspiration and Prior Art
-------------------------
I first learned about this concept (of alerting on non-events) from
[Dead Man's Snitch](https://deadmanssnitch.com/) and subsequently saw it on
[Cronitor](https://cronitor.io/). Open source implementations exist, such as
[Coal Mine](https://github.com/quantopian/coal-mine) and
[healthchecks](https://github.com/healthchecks/healthchecks) (which also comes
in a [hosted version](https://healthchecks.io/)).

Building my own implementation enables experimentation and provides learning
opportunities. Plus, it's fun!

I've greatly benefited from the architecture and design of healthchecks in
constructing watchword. Thank you, [cuu508](https://github.com/cuu508)!
