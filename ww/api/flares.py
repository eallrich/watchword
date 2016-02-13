from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.mail import send_mail
import requests


class Email(object):
    def send(self, flare, watch, from_email=settings.EMAIL_AUTHOR):
        parameters = {
            'subject': 'Flare from Watchword: %s status is "%s"' % (watch.name, watch.status()),
            'message': 'The Watch for %s (word=%s) was last contacted %s (at precisely %s). The Watch status is %s.' % (watch.name, watch.word, naturaltime(watch.last_ping), watch.last_ping, watch.status()),
            'from_email': from_email,
            'recipient_list': [flare.config,],
        }
        return send_mail(**parameters)


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
            tmpl = "Connection timed out (limit of %d seconds)"
            return tmpl % options['timeout']
        except requests.exceptions.ConnectionError as exc:
            return "Unable to connect. Exception: %r" % exc
