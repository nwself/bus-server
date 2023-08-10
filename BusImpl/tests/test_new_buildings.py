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


class TestNewBuildings:
    def test_new_building(self, state):
        state.newBuilding(bid=0, bType="pub")

        dump = json.loads(state.to_json())
        assert "0" in dump["buildings"].keys()
        assert dump["buildings"]["0"] == "pub"

    def test_two_new_buildings(self, state):
        state.newBuilding(bid=0, bType="pub")
        state.newBuilding(bid=1, bType="pub")

        dump = json.loads(state.to_json())
        assert "0" in dump["buildings"].keys()
        assert "1" in dump["buildings"].keys()
        assert dump["buildings"]["0"] == "pub"
        assert dump["buildings"]["1"] == "pub"

    def test_reuse_address(self, state):
        state.newBuilding(bid=0, bType="pub")
        state.newBuilding(bid=0, bType="home")

        dump = json.loads(state.to_json())
        assert "0" in dump["buildings"].keys()
        assert dump["buildings"]["0"] == "pub"

    def test_build_on_next_set(self, state):
        state.newBuilding(bid=9, bType="pub")

        dump = json.loads(state.to_json())
        assert "9" not in dump["buildings"].keys()

    def test_bad_building_type(self, state):
        state.newBuilding(bid=0, bType="foobar")

        dump = json.loads(state.to_json())
        assert "0" not in dump["buildings"].keys()

    def test_bad_building_id(self, state):
        state.newBuilding(bid=10000, bType="pub")

        dump = json.loads(state.to_json())
        assert "10000" not in dump["buildings"].keys()
