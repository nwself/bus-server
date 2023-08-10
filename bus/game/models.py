import json

from django.db import models

from BusImpl.bus import Bus


class Player(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.SlugField(db_index=True)
    players = models.ManyToManyField(Player)

    def get_current_state(self):
        state = self.gamestate_set.all().order_by('-effective').first()
        return state.get_state() if state else None

    def handleEvent(self, event):
        state = self.gamestate_set.all().order_by('-effective').first()
        if not state:
            print("No state?")
            return

        print("Make you a bus")
        bus = Bus(initial=state.state)
        print("Handle this event")
        bus.handleEvent(event)

        print("Save this event")
        self.gamestate_set.create(state=bus.to_json())

    def __str__(self):
        return self.name


class GameState(models.Model):
    class Meta:
        unique_together = (('game', 'effective'),)

    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    effective = models.DateTimeField(auto_now_add=True)

    state = models.TextField()

    def get_state(self):
        return json.loads(self.state)

    def __str__(self):
        return "({}) {}".format(self.game.name, self.effective)
