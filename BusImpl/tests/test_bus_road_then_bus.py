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
        "where": "new-bus",
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
    def test_phase_change(self, bus):
        bus.handleEvent({
            "who": "tripswithtires",
            "what": "build-road",
            "where": 0
        })

        dump = json.loads(bus.to_json())
        assert dump["phase"] == "new-buildings"
        assert len(dump["information"]) == 1
        assert dump["information"][0] == {
            "who": "piestastedgood",
            "what": "new-bus"
        }

class TestNewBusFirstPlayer:
    def test_information(self):
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
            "where": "new-bus",
        })
        bus.handleEvent({
            "who": "piestastedgood",
            "what": "place-worker",
            "where": "first-player",
        })
        bus.handleEvent({
            "who": "tripswithtires",
            "what": "pass",
        })
        bus.handleEvent({
            "who": "piestastedgood",
            "what": "pass",
        })
        bus.handleEvent({
            "who": "tripswithtires",
            "what": "build-road",
            "where": 0
        })

        dump = json.loads(bus.to_json())
        assert dump["phase"] == "place-workers"
        assert len(dump["information"]) == 2
        print(dump["information"])
        assert dump["information"][0] == {
            "who": "tripswithtires",
            "what": "new-bus"
        }
        assert dump["information"][1] == {
            "who": "piestastedgood",
            "what": "first-player"
        }
