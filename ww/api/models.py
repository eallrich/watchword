from datetime import timedelta
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from ww.api import flares

# When a Watch is first created, it is Fresh. Once a watchword is received,
# the Watch becomes Quiet. It remains Quiet as long as watchwords are seen
# at least once every cycle. If a cycle passes without a watchword, the Watch
# becomes Alert. If the grace period also passes without a watchword, then the
# Watch enters Alarm and the user is notified. When a watchword is finally
# received, the state returns to Quiet. A Watch can be put to Sleep if no
# watchwords are expected for an extended period of time.
WATCH_STATES = (
    ("fresh", "Fresh"),
    ("quiet", "Quiet"),
    ("alert", "Alert"),
    ("alarm", "Alarm"),
    ("sleep", "Sleep"),
)

# The user-presentable names for flares (e.g. 'Webhook') must match at least
# one of the class names in flares.py in order for the dynamic lookup in
# Flare.fire(...) to operate correctly.
FLARE_SIGNALS = (
    ("email", "Email"),
    ("webhook", "Webhook"),
)


def watchword():
    """Watchwords need to be long enough to be hard to guess, but not so long
    as to be difficult to work with."""
    return str(uuid.uuid4())[-10:]


class Timestamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Watch(Timestamped):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    word = models.CharField(max_length=10, default=watchword, editable=False, unique=True)
    cycle = models.DurationField(default=timedelta(days=1))
    grace = models.DurationField(default=timedelta(hours=1))
    state = models.CharField(max_length=5, choices=WATCH_STATES, default="fresh", blank=False)
    flares = models.ManyToManyField("Flare")
    # This is just for convenience. It would of course be possible to query the
    # Ping table for the most recent entry related to this Watch.
    last_ping = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    __unicode__ = __str__

    def alert_threshold(self):
        if self.last_ping:
            return self.last_ping + self.cycle
        else:
            return None

    def alarm_threshold(self):
        if self.last_ping:
            return self.alert_threshold() + self.grace
        else:
            return None

    def status(self):
        if self.state in ("fresh", "sleep"):
            return self.state

        now = timezone.now()
        if now < self.alert_threshold():
            return "quiet"
        elif now < self.alarm_threshold():
            return "alert"
        else:
            return "alarm"

    def fire_flares(self):
        if self.status() in ("quiet", "alarm"):
            launches = []
            for flare in self.flares.all():
                launches.append(flare.fire(watch=self))
            return launches


class Ping(Timestamped):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE)
    method = models.CharField(max_length=10, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    remote_addr = models.GenericIPAddressField()

    def __str__(self):
        tmpl = "%s (%s from %s)"
        return tmpl % (self.watch.name, self.method, self.remote_addr)
    __unicode__ = __str__


class Flare(Timestamped):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    config = models.CharField(max_length=255, blank=True)
    signal = models.CharField(max_length=10, choices=FLARE_SIGNALS, default="email", blank=False)

    def __str__(self):
        return "%s (%s)" % (self.signal, self.config)
    __unicode__ = __str__

    def fire(self, watch):
        launch = Launch(watch=watch, flare=self)
        launch.trigger_state = watch.status()
        classname = self.get_signal_display()
        try:
            mechanism = getattr(flares, classname)()
        except AttributeError as exc:
            # TODO Add logging, inform user that the signal name is bad
            tmpl = "AttributeError: Could not find signal '%s' in flares.py"
            launch.message = tmpl % (classname,)
        else:
            response = mechanism.send(self, watch)
            launch.message = str(response)[:255]
        launch.save()
        return launch


class Launch(Timestamped):
    watch = models.ForeignKey(Watch, on_delete=models.CASCADE)
    flare = models.ForeignKey(Flare, on_delete=models.CASCADE)
    message = models.CharField(max_length=255, blank=True)
    trigger_state = models.CharField(max_length=5, choices=WATCH_STATES)

    def __str__(self):
        tmpl = "%s @ %s, %s => %s"
        return tmpl % ( self.watch.name,
                        self.trigger_state,
                        self.flare.signal,
                        self.message)
    __unicode__ = __str__
