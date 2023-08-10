import json
import pytest

from ..bus import State


@pytest.fixture
def state():
    state = state = State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])

    for i in range(0, len(state.players)):
        state.players[i].passed = True

    state.workerAreas["new-buildings"].workers.append("tripswithtires")
    state.nextTurn()
    return state


class TestPeople:
    def test_add_people(self, state):
        state.addPeople(nid=9, count=3)
        state.addPeople(nid=31, count=1)

        dump = json.loads(state.to_json())
        assert dump["people"]["9"] == 3
        assert dump["people"]["31"] == 1
        assert dump["remainingPeople"] == 15 - 3 - 1

    def test_two_adds(self, state):
        state.addPeople(nid=9, count=1)
        state.addPeople(nid=9, count=1)

        dump = json.loads(state.to_json())
        assert dump["people"]["9"] == 2
        assert dump["remainingPeople"] == 15 - 2
