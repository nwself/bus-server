import json
import pytest

from ..bus import State

# from empirical study edge 3 has 7 canRoads which are
#  1, 2, 4, 25, 30, 32, 42
#
# 2 4 25 30 via node 1
# 1 32 42 via node 3

@pytest.fixture
def state():
    state = State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])

    for i in range(0, len(state.players)):
        state.players[i].passed = True

    state.workerAreas["build-road"].workers.append("tripswithtires")
    state.nextTurn()
    return state


class TestBuildOver:
    def test_cannot_build_over(self, state):
        # coincidence that nodes and edges are same number here
        state.players[1].roads = [2, 4]
        state.players[1].startNode = 2
        state.players[1].endNode = 4
        state.buildRoad(eid=3)

        dump = json.loads(state.to_json())
        assert 2 not in dump["players"]["tripswithtires"]["canRoad"]
        assert 4 not in dump["players"]["tripswithtires"]["canRoad"]

    def test_can_build_over(self, state):
        # coincidence that nodes and edges are same number here
        state.players[1].roads = [2]
        state.players[1].startNode = 1
        state.players[1].endNode = 2
        state.buildRoad(eid=3)

        dump = json.loads(state.to_json())
        assert 2 in dump["players"]["tripswithtires"]["canRoad"]


class TestCanRoad:
    def test_initial_start_end(self, state):
        state.buildRoad(eid=3)

        dump = json.loads(state.to_json())
        startEnd = sorted([
            dump["players"]["tripswithtires"]["startNode"],
            dump["players"]["tripswithtires"]["endNode"]
        ])
        assert startEnd == [1, 3]

    def test_next_start_end(self, state):
        state.buildRoad(eid=3)
        state.buildRoad(eid=42)

        dump = json.loads(state.to_json())
        startEnd = sorted([
            dump["players"]["tripswithtires"]["startNode"],
            dump["players"]["tripswithtires"]["endNode"]
        ])
        assert startEnd == [1, 22]
        assert 42 in dump["players"]["tripswithtires"]["roads"]

        # these were buildable because node 3 was an end and aren't now
        # (and happen not to be connected to new end 22)
        assert 1 not in dump["players"]["tripswithtires"]["canRoad"]
        assert 32 not in dump["players"]["tripswithtires"]["canRoad"]
        assert 42 not in dump["players"]["tripswithtires"]["canRoad"]

    def test_can_road(self, state):
        state.buildRoad(eid=3)

        dump = json.loads(state.to_json())
        assert len(dump["players"]["tripswithtires"]["canRoad"]) == 7
        assert 1 in dump["players"]["tripswithtires"]["canRoad"]
        assert 2 in dump["players"]["tripswithtires"]["canRoad"]
        assert 4 in dump["players"]["tripswithtires"]["canRoad"]
        assert 25 in dump["players"]["tripswithtires"]["canRoad"]
        assert 30 in dump["players"]["tripswithtires"]["canRoad"]
        assert 32 in dump["players"]["tripswithtires"]["canRoad"]
        assert 42 in dump["players"]["tripswithtires"]["canRoad"]


class TestBuildRoad:
    def test_load_graph(self, state):
        assert state.graph

    def test_build_bad_eid(self, state):
        state.buildRoad(eid=10000)

        dump = json.loads(state.to_json())
        assert 10000 not in dump["players"]["tripswithtires"]["roads"]

    def test_initial_build(self, state):
        # build a valid one
        state.buildRoad(eid=3)

        dump = json.loads(state.to_json())
        assert 3 in dump["players"]["tripswithtires"]["roads"]

    def test_build_not_attached(self, state):
        # try to build one can't build
        state.buildRoad(eid=3)
        state.buildRoad(eid=0)

        dump = json.loads(state.to_json())
        assert 0 not in dump["players"]["tripswithtires"]["roads"]


class TestFromJSON:
    def test_roads(self, state):
        state.buildRoad(eid=3)

        str_dump = state.to_json()
        copy_state = State(initial=str_dump)

        dump = json.loads(str_dump)
        assert 3 in copy_state.players[0].roads
