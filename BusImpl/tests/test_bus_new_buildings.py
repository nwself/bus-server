import json
import pytest

from ..bus import Bus, State


@pytest.fixture
def bus():
    bus = Bus(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])
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
    def test_event(self, bus):
        bus.handleEvent({
            "who": "tripswithtires",
            "what": "new-building",
            "where": 0,
            "type": "pub",
        })

        dump = json.loads(bus.to_json())
        assert dump["phase"] == "place-workers"
        assert "0" in dump["buildings"]
        assert dump["buildings"]["0"] == "pub"


class TestTwoBusActionTurns:
    def test_two_event(self):
        bus = Bus(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])
        bus.handleEvent({
            "who": "tripswithtires",
            "what": "place-worker",
            "where": "new-bus",
        })
        bus.handleEvent({
            "who": "piestastedgood",
            "what": "place-worker",
            "where": "new-buildings",
        })
        bus.handleEvent({
            "who": "tripswithtires",
            "what": "place-worker",
            "where": "first-player",
        })
        bus.handleEvent({
            "who": "piestastedgood",
            "what": "place-worker",
            "where": "new-buildings",
        })

        dump = json.loads(bus.to_json())
        print("buildings before pass workers {}".format(dump["workerAreas"]["new-buildings"]["workers"]))
        print("buildings before pass actions {}".format(dump["workerAreas"]["new-buildings"]["actions"]))
        bus.handleEvent({
            "who": "tripswithtires",
            "what": "pass",
        })
        bus.handleEvent({
            "who": "piestastedgood",
            "what": "pass",
        })

        dump = json.loads(bus.to_json())
        print("buildings workers {}".format(dump["workerAreas"]["new-buildings"]["workers"]))
        print("buildings actions {}".format(dump["workerAreas"]["new-buildings"]["actions"]))

        bus.handleEvent({
            "who": "piestastedgood",
            "what": "new-building",
            "where": 0,
            "type": "pub",
        })

        bus.handleEvent({
            "who": "piestastedgood",
            "what": "new-building",
            "where": 1,
            "type": "pub",
        })

        dump = json.loads(bus.to_json())
        # assert dump["phase"] == "place-workers"
        assert "0" in dump["buildings"]
        assert "1" in dump["buildings"]
        assert dump["buildings"]["0"] == "pub"
        assert dump["buildings"]["1"] == "pub"
