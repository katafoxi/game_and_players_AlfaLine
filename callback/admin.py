from django.contrib import admin
from callback.models import *


class PlayerAdmin(admin.ModelAdmin):
    # list_display = ['id', 'name', 'email', 'date_create', 'date_change']
    list_display = ['name', 'email', 'date_create', 'date_change']
    search_fields = ('name', 'email',)


class PlayerInline(admin.TabularInline):
    model = Game.players.through


class GameAdmin(admin.ModelAdmin):
    # list_display = ['id', 'name', 'get_players', 'date_create', 'date_change']
    list_display = ['name', 'get_players', 'date_create', 'date_change']
    inlines = [PlayerInline, ]

    @admin.display(description='Игроки')
    def get_players(self, obj):
        return ", ".join([p.name for p in obj.players.all()])


admin.site.register(Player, PlayerAdmin)
admin.site.register(Game, GameAdmin)
