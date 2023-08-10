import json
import pytest

from ..bus import State


@pytest.fixture
def state():
    return State(slug="abc", players=[{"name": "tripswithtires", "color": "yellow"}, {"name": "piestastedgood", "color": "red"}])


class TestMoveWorker:
    def test_move_worker(self, state):
        assert len(state.workerAreas["build-road"].workers) == 0
        state.moveWorker(to="build-road")

        dump = json.loads(state.to_json())
        assert dump["players"]["tripswithtires"]["workers"] == 20
        assert len(dump["workerAreas"]["build-road"]["workers"]) == 1
        assert dump["workerAreas"]["build-road"]["workers"][0] == "tripswithtires"

    def test_no_room(self, state):
        assert len(state.workerAreas["build-road"].workers) == 0
        state.workerAreas["stop-time"].workers.append("piestastedgood")
        state.moveWorker(to="stop-time")

        dump = json.loads(state.to_json())
        assert dump["players"]["tripswithtires"]["workers"] == 21
        assert len(dump["workerAreas"]["stop-time"]["workers"]) == 1
        assert dump["workerAreas"]["stop-time"]["workers"][0] == "piestastedgood"


class TestNextPlayer:
    def test_next_player(self, state):
        assert len(state.workerAreas["build-road"].workers) == 0
        state.nextTurn()

        dump = json.loads(state.to_json())
        assert dump["activePlayer"] == "piestastedgood"

    def test_next_player_twice(self, state):
        assert len(state.workerAreas["build-road"].workers) == 0
        state.nextTurn()
        state.nextTurn()

        dump = json.loads(state.to_json())
        assert dump["activePlayer"] == "tripswithtires"


class TestJSON:
    def test_from_json(self, state):
        state.moveWorker(to="build-road")

        str_dump = state.to_json()
        copy_state = State(initial=str_dump)

        dump = json.loads(str_dump)
        assert copy_state.players[0].workers == dump["players"]["tripswithtires"]["workers"]
        assert len(copy_state.workerAreas["build-road"].workers[0]) == len(dump["workerAreas"]["build-road"]["workers"][0])
        assert copy_state.workerAreas["build-road"].workers[0] == dump["workerAreas"]["build-road"]["workers"][0]


class TestPassPhase:
    def test_pass_too_soon(self, state):
        state.passPhase()

        dump = json.loads(state.to_json())
        assert dump["players"]["tripswithtires"]["passed"] == False

    def test_cannot_pass_after_1(self, state):
        state.moveWorker(to="build-road")

        dump = json.loads(state.to_json())
        assert dump["players"]["tripswithtires"]["canPass"] == False
        assert dump["players"]["tripswithtires"]["passed"] == False

    def test_can_pass_after_2(self, state):
        state.moveWorker(to="build-road")
        state.moveWorker(to="build-road")

        dump = json.loads(state.to_json())
        assert dump["players"]["tripswithtires"]["canPass"] == True
        assert dump["players"]["tripswithtires"]["passed"] == False

    def test_pass(self, state):
        state.moveWorker(to="build-road")
        state.moveWorker(to="build-road")
        state.passPhase()

        dump = json.loads(state.to_json())
        assert dump["players"]["tripswithtires"]["passed"] == True

    def test_pass_end_phase(self, state):
        # all players pass
        for i in range(0, len(state.players)):
            state.players[i].passed = True

        # add a worker somewhere
        state.workerAreas["build-road"].workers.append("tripswithtires")

        state.nextTurn()

        dump = json.loads(state.to_json())
        assert dump["phase"] != "place-workers"


class TestMoveAndNext:
    def test_move_next_move(self, state):
        assert len(state.workerAreas["build-road"].workers) == 0
        state.moveWorker(to="build-road")
        state.nextTurn()
        state.moveWorker(to="build-road")

        dump = json.loads(state.to_json())
        assert dump["players"]["tripswithtires"]["workers"] == 20
        assert dump["players"]["piestastedgood"]["workers"] == 20
        assert len(dump["workerAreas"]["build-road"]["workers"]) == 2
        assert dump["workerAreas"]["build-road"]["workers"][0] == "tripswithtires"
        assert dump["workerAreas"]["build-road"]["workers"][1] == "piestastedgood"

    def test_pass_next(self, state):
        # next player passes
        state.players[1].passed = True
        state.nextTurn()

        dump = json.loads(state.to_json())
        assert dump["activePlayer"] != "piestastedgood"

