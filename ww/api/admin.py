from django.contrib import admin

from ww.api.models import Watch, Ping, Flare, Launch

@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'word', 'state', 'status', 'last_ping',)

@admin.register(Ping)
class PingAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'watch_name', 'method', 'user_agent', 'remote_addr',)

    def watch_name(self, ping):
        return ping.watch.name

@admin.register(Flare)
class FlareAdmin(admin.ModelAdmin):
    list_display = ('id', 'signal', 'config',)

@admin.register(Launch)
class LaunchAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'flare', 'watch', 'trigger_state', 'message',)
