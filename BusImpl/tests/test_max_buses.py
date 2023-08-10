import json
import pytest

from ..bus import Bus, State


@pytest.fixture
def bus():
    bus = Bus(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])
    bus.state.players[1].busCount = 2
    bus.state.maxBuses = 2
    bus.handleEvent({
        "who": "tripswithtires",
        "what": "place-worker",
        "where": "build-road",
    })
    bus.handleEvent({
        "who": "piestastedgood",
        "what": "place-worker",
        "where": "build-road",
    })
    bus.handleEvent({
        "who": "tripswithtires",
        "what": "place-worker",
        "where": "new-buildings",
    })
    bus.handleEvent({
        "who": "piestastedgood",
        "what": "place-worker",
        "where": "new-buildings",
    })
    bus.handleEvent({
        "who": "tripswithtires",
        "what": "pass",
    })
    bus.handleEvent({
        "who": "piestastedgood",
        "what": "pass",
    })
    return bus


class TestBusActionTurns:
    def test_build_actions(self, bus):
        dump = json.loads(bus.to_json())
        print("actions at start {}".format(dump["workerAreas"]["build-road"]["actions"]))

        bus.handleEvent({
            "who": "piestastedgood",
            "what": "build-road",
            "where": 0
        })

        dump = json.loads(bus.to_json())
        print("actions after one {}".format(dump["workerAreas"]["build-road"]["actions"]))

        bus.handleEvent({
            "who": "tripswithtires",
            "what": "build-road",
            "where": 1
        })

        dump = json.loads(bus.to_json())

        assert len(dump["workerAreas"]["build-road"]["actions"]) == 1
        assert dump["workerAreas"]["build-road"]["actions"][0] == ["tripswithtires", 1]
