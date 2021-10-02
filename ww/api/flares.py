from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.mail import send_mail
from raven.contrib.django.raven_compat.models import client as raven
import requests


class Email(object):
    def send(self, flare, watch, from_email=None):
        parameters = {
            'subject': 'Flare from Watchword: %s status is "%s"' % (watch.name, watch.status()),
            'message': 'The Watch for %s (word=%s) was last contacted %s (at precisely %s). The Watch status is %s.' % (watch.name, watch.word, naturaltime(watch.last_ping), watch.last_ping, watch.status()),
            'from_email': from_email,
            'recipient_list': [flare.config,],
        }
        try:
            return send_mail(**parameters)
        except:
            raven.captureException("Failed to send email")
            return 0 # the message was not successfully sent


class Webhook(object):
    def send(self, flare, watch):
        options = {
            'headers': {
                'User-Agent': 'watchword',
            },
            'timeout': 10, # seconds
        }
        url = flare.config
        try:
            r = requests.get(url, **options)
            return "Status: %d" % r.status_code
        except requests.exceptions.Timeout:
            m = "Connect timed out (limit of %d seconds)" % options['timeout']
            raven.captureException(m)
            return m
        except requests.exceptions.ConnectionError as exc:
            raven.captureException("Unable to connect")
            return "Unable to connect. Exception: %r" % exc
