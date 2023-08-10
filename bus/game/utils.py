from .models import Game, Player

from BusImpl.bus import Bus


colors = ["yellow", "red", "blue", "green"]

def initialize_game(slug, player_names):
    # look for players in db
    players = Player.objects.filter(name__in=player_names)

    if players.count() != len(player_names):
        print("Couldn't find all these players {} -- found {}".format(player_names, players))
        return

    # create new game with players
    new_game = Game.objects.create(name=slug)
    new_game.players.add(*players)
    new_game.save()

    #  create initial state
    players = [{
        "name": p.name,
        "color": colors[i]
    } for i, p in enumerate(new_game.players.all())]

    initial_state = Bus(
        slug=new_game.name,
        players=players
    )

    # save initial state and return this game
    new_game.gamestate_set.create(state=initial_state.to_json())
    return new_game
