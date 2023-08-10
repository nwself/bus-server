import json

from ..bus import State, Player


class TestState:
    def test_initialize(self):
        state = State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])
        assert state

    def test_buildings(self):
        state = State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])

        dump = json.loads(state.to_json())
        assert "buildings" in dump

    def test_remaining_people(self):
        state = State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])

        dump = json.loads(state.to_json())
        assert "remainingPeople" in dump

    def test_time(self):
        state = State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])

        dump = json.loads(state.to_json())
        assert "time" in dump

    def test_timey_wimeys(self):
        state = State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])

        dump = json.loads(state.to_json())
        assert dump["timeyWimeys"] == 5

    def test_take_timey_wimey(self):
        state = State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])
        state.takeTimeyWimey()

        dump = json.loads(state.to_json())
        assert dump["timeyWimeys"] == 4
        assert dump["players"]["tripswithtires"]["timeyWimeys"] == 1

    def test_add_bus(self):
        state = State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])
        state.addBus()

        dump = json.loads(state.to_json())
        assert dump["players"]["tripswithtires"]["busCount"] == 2
        assert dump["maxBuses"] == 2

    def test_take_first_player(self):
        state = State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])
        state.nextTurn()
        state.takeFirstPlayerToken()

        dump = json.loads(state.to_json())
        assert dump["players"]["tripswithtires"]["hasFirstPlayerToken"] == False
        assert dump["players"]["piestastedgood"]["hasFirstPlayerToken"] == True

    def test_max_buses(self):
        state = State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])

        dump = json.loads(state.to_json())
        assert dump["maxBuses"] == 1


class TestJSON:
    def test_active_player(self):
        state = State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])

        dump = state.to_json()
        copy_state = State(initial=dump)

        assert type(copy_state.activePlayer) == Player
        assert len(copy_state.players) == 2
        assert type(copy_state.players[0]) == Player
