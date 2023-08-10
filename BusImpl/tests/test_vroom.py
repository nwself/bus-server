import json
import pytest

from ..bus import State


@pytest.fixture
def state():
    state = state = State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])

    for i in range(0, len(state.players)):
        state.players[i].passed = True

    state.players[0].roads = [0, 1]
    state.people["2"] = 1
    state.buildings["3"] = "work"

    state.workerAreas["vroom"].workers.append("tripswithtires")
    state.nextTurn()
    return state


class TestVroom:
    def test_vroom(self, state):
        assert state.can_ride(state.activePlayer, 2, 3) == True
