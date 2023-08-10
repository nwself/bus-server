import json
import pytest

from ..bus import Bus, State


@pytest.fixture
def bus():
    bus = Bus(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])
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
        "where": "build-road",
    })
    bus.handleEvent({
        "who": "piestastedgood",
        "what": "place-worker",
        "where": "build-road",
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

        assert len(dump["workerAreas"]["build-road"]["actions"]) == 1
        assert dump["workerAreas"]["build-road"]["actions"][0] == ["tripswithtires", 1]

    def test_build_one(self, bus):
        bus.handleEvent({
            "who": "tripswithtires",
            "what": "build-road",
            "where": 0
        })

        dump = json.loads(bus.to_json())
        assert len(dump["workerAreas"]["build-road"]["actions"]) == 0
        assert len(dump["players"]["tripswithtires"]["roads"]) == 1
        assert dump["phase"] != "build-road"
        assert dump["phase"] == "place-workers"
        assert dump["players"]["tripswithtires"]["passed"] == False

    def test_information(self, bus):
        dump = json.loads(bus.to_json())

        assert len(dump["information"]) == 3
        assert dump["information"][0] == {"what": "useless-worker", "who": "piestastedgood"}

    def test_action_order(self, bus):
        dump = json.loads(bus.to_json())

        assert dump["phase"] == "build-road"
        assert dump["activePlayer"] == "tripswithtires"
