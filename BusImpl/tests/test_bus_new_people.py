import json
import pytest

from ..bus import Bus, State


@pytest.fixture
def bus():
    bus = Bus(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])
    bus.handleEvent({
        "who": "tripswithtires",
        "what": "place-worker",
        "where": "new-bus",
    })
    bus.handleEvent({
        "who": "piestastedgood",
        "what": "place-worker",
        "where": "more-people",
    })
    bus.handleEvent({
        "who": "tripswithtires",
        "what": "place-worker",
        "where": "more-people",
    })
    bus.handleEvent({
        "who": "piestastedgood",
        "what": "place-worker",
        "where": "more-people",
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
            "who": "piestastedgood",
            "what": "more-people",
            "where": 31,
            "count": 1,
        })

        dump = json.loads(bus.to_json())
        # assert dump["phase"] == "place-workers"
        print(dump["people"])
        assert "31" in dump["people"]
        assert dump["people"]["31"] == 1

    def test_two_events(self, bus):
        bus.handleEvent({
            "who": "piestastedgood",
            "what": "more-people",
            "where": 31,
            "count": 1,
        })
        bus.handleEvent({
            "who": "piestastedgood",
            "what": "more-people",
            "where": 31,
            "count": 1,
        })

        dump = json.loads(bus.to_json())
        print(dump["people"])
        assert "31" in dump["people"]
        assert dump["people"]["31"] == 2
