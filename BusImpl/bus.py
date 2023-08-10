import itertools
import json
import random


class Player:
    def __init__(self, name="", color="", workers=0, initial=None, state=None):
        self.state = state
        self.graph = state.graph
        if initial is not None:
            self.from_json(initial)
            return
        self.name = name
        self.color = color
        self.workers = workers
        self.workersUsedThisPhase = 0
        self.passed = False
        self.roads = []
        self.startNode = None
        self.endNode = None
        self.busCount = 1
        self.timeyWimeys = 0
        self.hasFirstPlayerToken = False
        self.victoryPoints = 0

    def to_json(self):
        return {
            "name": self.name,
            "color": self.color,
            "workers": self.workers,
            "canPass": self.canPass(),
            "workersUsedThisPhase": self.workersUsedThisPhase,
            "passed": self.passed,
            "roads": self.roads,
            "canRoad": self.canRoad(),
            "startNode": self.startNode,
            "endNode": self.endNode,
            "busCount": self.busCount,
            "timeyWimeys": self.timeyWimeys,
            "hasFirstPlayerToken": self.hasFirstPlayerToken,
        }

    def from_json(self, initial):
        self.name = initial["name"]
        self.color = initial["color"]
        self.workers = initial["workers"]
        self.workersUsedThisPhase = initial["workersUsedThisPhase"]
        self.passed = initial["passed"]
        self.roads = initial["roads"]
        self.startNode = initial["startNode"]
        self.endNode = initial["endNode"]
        self.busCount = initial["busCount"]
        self.timeyWimeys = initial["timeyWimeys"]
        self.hasFirstPlayerToken = initial["hasFirstPlayerToken"]

    def useWorker(self):
        self.workers -= 1
        self.workersUsedThisPhase += 1

    def canPass(self):
        return self.workersUsedThisPhase >= 2

    def passPhase(self):
        self.passed = True
        self.workersUsedThisPhase = 0

    def addBus(self):
        self.busCount += 1

    def takeTimeyWimey(self):
        self.timeyWimeys += 1

    def takeFirstPlayerToken(self):
        self.hasFirstPlayerToken = True

    def loseFirstPlayerToken(self):
        self.hasFirstPlayerToken = False

    def gainPoint(self):
        self.victoryPoints += 1

    def buildRoad(self, eid):
        edge = [e for e in self.graph["edges"] if e["eid"] == eid][0]

        if eid not in self.canRoad() and len(self.roads) > 0:
            print(f"{self.name} can not build here")
            return False

        if self.startNode is None:
            self.startNode = edge["source"]
            self.endNode = edge["target"]
        else:
            # which end are we building on?
            if self.startNode in (edge["source"], edge["target"]):
                self.startNode = (
                    edge["source"]
                    if edge["source"] != self.startNode
                    else edge["target"]
                )
            else:
                self.endNode = (
                    edge["source"] if edge["source"] != self.endNode else edge["target"]
                )

        self.roads.append(eid)
        return True

    def canRoad(self):
        fromStart = [
            e["eid"]
            for e in self.graph["edges"]
            if e["eid"] not in self.roads
            and self.startNode in (e["source"], e["target"])
        ]
        fromEnd = [
            e["eid"]
            for e in self.graph["edges"]
            if e["eid"] not in self.roads and self.endNode in (e["source"], e["target"])
        ]

        # look through all fromStart
        # for each find the players that have it in their roads
        # add to to_remove unless start in (p.start, p.end)
        to_remove = []
        for eid in fromStart:
            if any(
                [
                    p
                    for p in self.state.players
                    if eid in p.roads and self.startNode not in (p.startNode, p.endNode)
                ]
            ):
                to_remove.append(eid)

        for eid in fromEnd:
            if any(
                [
                    p
                    for p in self.state.players
                    if eid in p.roads and self.endNode not in (p.startNode, p.endNode)
                ]
            ):
                to_remove.append(eid)

        return list((set(fromStart) | set(fromEnd)) - set(to_remove))


class WorkerArea:
    def __init__(self, name="", size=0, reverse=False, workers=None, initial=None):
        if initial is not None:
            self.from_json(initial)
            return

        self.name = name
        self.size = size
        self.reverse = reverse
        self.workers = list() if workers is None else workers
        self.actions = []

    def to_json(self):
        return {
            "name": self.name,
            "size": self.size,
            "reverse": self.reverse,
            "workers": self.workers,
            "actions": self.actions,
        }

    def from_json(self, initial):
        self.name = initial["name"]
        self.size = initial["size"]
        self.reverse = initial["reverse"]
        self.workers = [n for n in initial["workers"]]
        self.actions = initial["actions"]

    def canReceiveWorker(self):
        return len(self.workers) < self.size

    def receiveWorker(self, player_name):
        self.workers.append(player_name)

    def isDone(self):
        return len(self.workers) == 0

    def startResolveWorkers(self, maxBuses, state):
        print("Time to start resolving workers")
        if self.actions:
            print("We already figured out actions, return early")
            return

        if self.size == 1:
            self.actions = [(self.workers[0], 1)] if self.workers else []
            return

        self.actions = [
            x for x in zip(self.workers, itertools.count(maxBuses, -1)) if x[1] > 0
        ]

        # remove useless workers
        for i in range(0, len(self.workers) - len(self.actions)):
            # if self.reverse:
            state.information.append(
                {"who": self.workers.pop(), "what": "useless-worker"}
            )
            # else:
            #     state.information.append(
            #         {"who": self.workers.pop(0), "what": "useless-worker"}
            #     )

        if self.reverse:
            self.actions.reverse()

        print("actions for {} are {}".format(self.name, self.actions))

    def discardWorker(self):
        # import traceback; traceback.print_stack();
        print("Get rid of this worker")
        print("actions are {}".format(self.actions))
        # if self.reverse:
        # else:
        #     self.workers.pop(0)

        # self.actions[0][1] -= 1
        self.actions[0] = (self.actions[0][0], self.actions[0][1] - 1)
        print("Discarded worker, actions are now {}".format(self.actions))
        if self.actions[0][1] == 0:
            if self.reverse:
                self.workers.pop()
            else:
                self.workers.pop(0)
            self.actions.pop(0)
            print("Current player is out of turns here, new actions are {} new workers are {}".format(self.actions, self.workers))

    def getNextPlayer(self):
        if len(self.workers) == 0:
            return None
        if self.reverse:
            return self.workers[-1]
        return self.workers[0]


class State:
    building_spaces = {"A": 12, "B": 10, "C": 8, "D": 15}

    def __init__(self, slug="", players=[], initial=None):
        self.graph = self.load_graph()

        if initial is not None:
            self.from_json(initial)
        else:
            self.initialize(slug, players)

    def load_graph(self):
        with open("/Users/nwself/nathan/bus/django/BusImpl/graph.json") as f:
            return json.load(f)

    def to_json(self):
        return json.dumps(
            {
                "slug": self.slug,
                "phase": self.phase,
                "activePlayer": self.activePlayer.name,
                "players": {p.name: p.to_json() for p in self.players},
                "workerAreas": {a.name: a.to_json() for a in self.workerAreas.values()},
                "timeyWimeys": self.timeyWimeys,
                "time": self.time,
                "buildings": self.buildings,
                "people": self.people,
                "maxBuses": self.maxBuses,
                "information": self.information,
                "remainingPeople": self.remainingPeople,
            }
        )

    def from_json(self, initial):
        data = json.loads(initial)
        self.slug = data["slug"]
        self.phase = data["phase"]
        self.players = [Player(initial=p, state=self) for p in data["players"].values()]
        self.activePlayer = [p for p in self.players if p.name == data["activePlayer"]][
            0
        ]
        self.workerAreas = {
            a["name"]: WorkerArea(initial=a) for a in data["workerAreas"].values()
        }
        self.timeyWimeys = data["timeyWimeys"]
        self.time = data["time"]
        self.buildings = data["buildings"]
        self.people = data["people"]
        self.maxBuses = data["maxBuses"]
        self.information = data["information"]
        self.remainingPeople = data["remainingPeople"]

    def initialize(self, slug, players):
        self.slug = slug
        self.phase = "place-workers"
        self.players = [
            Player(name=p["name"], color=p["color"], workers=21, state=self)
            for p in players
        ]
        self.workerAreas = {
            "build-road": WorkerArea(name="build-road", reverse=True, size=6),
            "new-bus": WorkerArea(name="new-bus", size=1),
            "more-people": WorkerArea(name="more-people", size=6),
            "new-buildings": WorkerArea(name="new-buildings", reverse=True, size=6),
            "stop-time": WorkerArea(name="stop-time", size=1),
            "vroom": WorkerArea(name="vroom", size=6),
            "first-player": WorkerArea(name="first-player", size=1),
        }
        self.activePlayer = self.players[0]
        self.activePlayer.takeFirstPlayerToken()
        self.timeyWimeys = 5
        self.time = "work"
        self.buildings = {}
        self.people = {}
        self.maxBuses = 1
        self.information = []
        self.remainingPeople = 15

    def moveWorker(self, to):
        if not self.workerAreas[to].canReceiveWorker():
            print("no can do")
            return

        self.activePlayer.useWorker()
        self.workerAreas[to].receiveWorker(self.activePlayer.name)

    def can_ride(self, player, from_nid, to_nid):
        pass

    def vroom(self, from_nid, to_nid, to_bid):
        if 0 > from_nid < 35 or 0 > to_nid < 35:
            print("Bad nid")
            return False

        if self.people[from_nid] == 0:
            print("No people at this nid")
            return False

        if 0 > to_bid < 44:
            print("Bad bid")
            return False

        if self.buildings[to_bid]["occupied"]:
            print("Building already occupied")
            return False

        if self.buildings[to_bid]["type"] != self.time:
            print("Not the right time of day to go to this building")
            return False

        if not self.can_ride(self.activePlayer, from_nid, to_nid):
            print("No path from {} to {} for {}".format(from_nid, to_nid, self.activePlayer))
            return False

        self.people[from_nid] -= 1
        self.buildings[to_bid]["occupied"] = True
        self.activePlayer.gainPoint()
        return True

    def prepare_vroom(self):
        for nid in self.people.keys():
            # node = [n for n in self.graph["nodes"] if n["nid"] == nid][0]
            if nid in self.buildings:
                for building in self.buildings[nid]:
                    if building["occupied"] and building["type"] != self.time:
                        building["occupied"] = False
                        self.people[nid] += 1

                for building in self.buildings[nid]:
                    if (
                        not building["occupied"]
                        and building["type"] == self.type
                        and self.people[nid] > 0
                    ):
                        building["occupied"] = True
                        self.people[nid] -= 1

    def buildRoad(self, eid):
        if eid not in [e["eid"] for e in self.graph["edges"]]:
            print("No such edge")
            return False

        return self.activePlayer.buildRoad(eid)

    def addPeople(self, nid, count):
        # TODO check not more people than allowed

        if count > self.remainingPeople:
            print("Not enough people left")
            return

        if nid not in [9, 31]:
            print("This is not a tube")
            return

        if str(nid) not in self.people:
            print("Resetting people at {}".format(nid))
            self.people[str(nid)] = 0

        print("Adding count to people at {}".format(nid))
        self.people[str(nid)] += count
        self.remainingPeople -= count

    def newBuilding(self, bid, bType):
        if bType not in ["home", "work", "pub"]:
            print("Bad bType")
            return

        if bid < 0 or bid > 45:
            print("Bad bid")
            return

        if bid in self.buildings:
            print("Already built here")
            return

        # check letter on building
        # node = self.graph["nodes"][nid]
        building = [b for b in itertools.chain.from_iterable([
            n["buildings"] for n in self.graph["nodes"] if "buildings" in n
        ]) if b["bid"] == bid][0]

        # if address < 0 or address > len(node["buildings"]):
        #     print("Bad building address")
        #     return

        # letter = node["buildings"][address]["stop"]
        letter = building["stop"]

        currentBuildingCount = len(self.buildings)
        print(f"currentBuildingCount {currentBuildingCount} {letter}")

        correctLetter = False
        match letter:
            case "A":
                correctLetter = currentBuildingCount < 12
            case "B":
                correctLetter = 12 <= currentBuildingCount < 22
            case "C":
                correctLetter = 22 <= currentBuildingCount < 30
            case "D":
                correctLetter = 30 <= currentBuildingCount

        if not correctLetter:
            print("It's not time to play that letter")
            return

        # currentLen = len(self.buildings[nid]) if nid in self.buildings else 0
        # if address != currentLen:
        #     print("Wrong address")
        #     return

        # if nid not in self.buildings:
        #     self.buildings[nid] = []

        # self.buildings[nid].append(bType)
        self.buildings[bid] = bType

    def addBus(self):
        self.activePlayer.addBus()
        self.maxBuses = max([p.busCount for p in self.players])
        self.information.append({"who": self.activePlayer.name, "what": "new-bus"})

    def clearInformation(self):
        self.information = []

    def takeTimeyWimey(self):
        self.activePlayer.takeTimeyWimey()
        self.timeyWimeys -= 1

    def takeFirstPlayerToken(self):
        for p in self.players:
            p.loseFirstPlayerToken()
        self.activePlayer.takeFirstPlayerToken()
        self.information.append({"who": self.activePlayer.name, "what": "first-player"})

    def passPhase(self):
        if not self.activePlayer.canPass():
            print("Need to play two workers to pass")
            return

        self.activePlayer.passPhase()

    def nextTurn(self):
        if self.phase == "place-workers":
            if all([p.passed for p in self.players]):
                self.nextPhase()
            else:
                num_players = len(self.players)
                index = (self.players.index(self.activePlayer) + 1) % num_players
                while self.players[index].passed:
                    index = (index + 1) % num_players
                self.activePlayer = self.players[index]
        else:
            self.nextResolvePhase()

    def nextPhase(self):
        match self.phase:
            case "place-workers":
                self.startResolveWorkers()
            case _:
                # do any cleanup here?
                self.phase = "place-workers"
                for p in self.players:
                    p.passed = False
                self.activePlayer = [p for p in self.players if p.hasFirstPlayerToken][0]

    def startResolveWorkers(self):
        # for area in self.workerAreas.values():
        #     area.startResolveWorkers(self.maxBuses, self)

        self.nextResolvePhase()

    def nextResolvePhase(self):
        notYetDone = [a for a in self.workerAreas.values() if not a.isDone()]
        if any(notYetDone):
            nextWorkerArea = notYetDone[0]
            self.phase = nextWorkerArea.name
            nextWorkerArea.startResolveWorkers(self.maxBuses, self)

            # print("Time for a {}".format(self.phase))
            # print(nextWorkerArea.workers)
            pname = nextWorkerArea.getNextPlayer()
            # print("Next player is {}".format(pname))
            # print("{}".format(self.information))
            self.activePlayer = [p for p in self.players if p.name == pname][0]
            return

        print("Should be phase is place-workers again unless game end")
        self.phase = "place-workers"
        for p in self.players:
            p.passed = False
        self.activePlayer = [p for p in self.players if p.hasFirstPlayerToken][0]


class Bus:
    def __init__(self, initial=None, slug="", players=[]):
        if initial is not None:
            self.state = State(initial=initial)
        else:
            self.state = State(slug=slug, players=players)

    def to_json(self):
        return self.state.to_json()

    def handleEvent(self, event):
        if event["who"] != self.state.activePlayer.name:
            print(f"It is not {event['who']}'s turn")
            return

        self.state.clearInformation()

        match self.state.phase:
            case "place-workers":
                self.handlePlaceWorkers(event)
            case "build-road":
                self.handleBuildRoads(event)
            case "new-buildings":
                self.handleNewBuilding(event)
            case "more-people":
                self.handleNewPeople(event)
            case _:
                print("No such state")

        # if auto-event
        if self.state.phase == "new-bus":
            self.state.addBus()
            self.state.workerAreas["new-bus"].discardWorker()
            self.state.nextTurn()

        if self.state.phase == "first-player":
            self.state.takeFirstPlayerToken()
            self.state.workerAreas["first-player"].discardWorker()
            self.state.nextTurn()

        # if self.state.phase == "stop-time":
        #     self.state.takeFirstPlayerToken()
        #     self.state.workerAreas["first-player"].discardWorker()
        #     self.state.nextTurn()

    def handlePlaceWorkers(self, event):
        match event:
            case {"what": "place-worker", "where": where}:
                self.state.moveWorker(to=where)
                self.state.nextTurn()
            case {"what": "pass"}:
                self.state.passPhase()
                self.state.nextTurn()
            case _:
                print(f"Can't {event['what']} in place-workers phase")

    def handleBuildRoads(self, event):
        match event:
            case {"what": "build-road", "where": eid}:
                if self.state.buildRoad(eid=eid):
                    self.state.workerAreas["build-road"].discardWorker()
                    self.state.nextTurn()
            case _:
                print("Can't do that now")

    def handleNewBuilding(self, event):
        match event:
            case {
                "what": "new-building",
                "where": bid,
                "type": bType,
            }:
                self.state.newBuilding(bid=bid, bType=bType)
                self.state.workerAreas["new-buildings"].discardWorker()
                self.state.nextTurn()
            case _:
                print("Can't do that now")

    def handleNewPeople(self, event):
        match event:
            case {
                "what": "more-people",
                "where": nid,
                # "count": 1,
            }:
                self.state.addPeople(nid=nid, count=1)
                self.state.workerAreas["more-people"].discardWorker()
                self.state.nextTurn()
            case _:
                print("Can't do that now")
