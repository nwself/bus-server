from django.contrib import admin

from .models import Player, Game, GameState


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    raw_id_fields = ('players',)
    search_fields = ('name',)


@admin.register(GameState)
class GameStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'effective', 'state')
    list_filter = ('game', 'effective')
