import json
import pytest

from ..bus import Bus, State


@pytest.fixture
def bus():
    return Bus(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])

@pytest.fixture
def place_worker_event():
    return {
        "who": "tripswithtires",
        "what": "place-worker",
        "where": "build-road",
    }

@pytest.fixture
def pass_place_worker_event():
    return {
        "who": "tripswithtires",
        "what": "pass",
    }

class TestBus:
    def test_bus(self):
        state = State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])
        # state = '{"slug": "abcdef", "phase": "place-workers", "activePlayer": "tripswithtires", "players": {"tripswithtires": {"name": "tripswithtires", "workers": 21, "canPass": false, "workersUsedThisPhase": 0, "passed": false, "roads": [], "canRoad": [], "startNode": null, "endNode": null, "busCount": 1, "timeyWimeys": 0, "hasFirstPlayerToken": true}, "piestastedgood": {"name": "piestastedgood", "workers": 21, "canPass": false, "workersUsedThisPhase": 0, "passed": false, "roads": [], "canRoad": [], "startNode": null, "endNode": null, "busCount": 1, "timeyWimeys": 0, "hasFirstPlayerToken": false}}, "workerAreas": {"build-road": {"name": "build-road", "size": 6, "workers": [], "done": false}, "new-bus": {"name": "new-bus", "size": 1, "workers": [], "done": false}, "more-people": {"name": "more-people", "size": 6, "workers": [], "done": false}, "new-buildings": {"name": "new-buildings", "size": 6, "workers": [], "done": false}, "stop-time": {"name": "stop-time", "size": 1, "workers": [], "done": false}, "vroom": {"name": "vroom", "size": 6, "workers": [], "done": false}, "first-player": {"name": "first-player", "size": 1, "workers": [], "done": false}}, "timeyWimeys": 5, "time": "work", "buildings": {}, "people": {}}'
        bus = Bus(initial=state.to_json())
        assert bus
        assert len(bus.state.players) == 2

    def test_bus_handle(self):
        state = State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])
        # state = '{"slug": "abcdef", "phase": "place-workers", "activePlayer": "tripswithtires", "players": {"tripswithtires": {"name": "tripswithtires", "workers": 21, "canPass": false, "workersUsedThisPhase": 0, "passed": false, "roads": [], "canRoad": [], "startNode": null, "endNode": null, "busCount": 1, "timeyWimeys": 0, "hasFirstPlayerToken": true}, "piestastedgood": {"name": "piestastedgood", "workers": 21, "canPass": false, "workersUsedThisPhase": 0, "passed": false, "roads": [], "canRoad": [], "startNode": null, "endNode": null, "busCount": 1, "timeyWimeys": 0, "hasFirstPlayerToken": false}}, "workerAreas": {"build-road": {"name": "build-road", "size": 6, "workers": [], "done": false}, "new-bus": {"name": "new-bus", "size": 1, "workers": [], "done": false}, "more-people": {"name": "more-people", "size": 6, "workers": [], "done": false}, "new-buildings": {"name": "new-buildings", "size": 6, "workers": [], "done": false}, "stop-time": {"name": "stop-time", "size": 1, "workers": [], "done": false}, "vroom": {"name": "vroom", "size": 6, "workers": [], "done": false}, "first-player": {"name": "first-player", "size": 1, "workers": [], "done": false}}, "timeyWimeys": 5, "time": "work", "buildings": {}, "people": {}}'
        bus = Bus(initial=state.to_json())
        bus.handleEvent({
            "who": "tripswithtires",
            "what": "place-worker",
            "where": "build-road",
        })

        dump = json.loads(bus.to_json())

        assert bus
        assert dump["players"]["tripswithtires"]["workers"] == 20
        assert len(dump["workerAreas"]["build-road"]["workers"]) == 1
        assert dump["workerAreas"]["build-road"]["workers"][0] == "tripswithtires"


class TestMoveWorkerEvent:
    def test_move_worker(self, bus, place_worker_event):
        bus.handleEvent(place_worker_event)

        dump = json.loads(bus.state.to_json())
        assert dump["players"]["tripswithtires"]["workers"] == 20
        assert len(dump["workerAreas"]["build-road"]["workers"]) == 1
        assert dump["workerAreas"]["build-road"]["workers"][0] == "tripswithtires"
