### Initialization plugin
import sys
import time
import createScn, demandExtraction
import dataDef as data
import dataRL
import numpy as np
import copy
import random
from bluesky import stack, sim


def init_plugin():
    """Initialization function of your plugin."""

    # Configuration parameters
    config = {
        "plugin_name": "INIT",
        "plugin_type": "sim",
        "update_interval": 3600,
    }

    stackfunctions = {}

    initSim()

    # init_plugin() should always return these two dicts.
    return config, stackfunctions


def initSim():

    stack.stack("HOLD")

    dataRL.nbIter += 1
    data.nextOrd = [0 for _ in range(6)]

    name = "test{}".format(0)
    la = createScn.create(0, 7, name)

    data.l.append(la)

    data.aircraft = copy.deepcopy(la)
    data.nbAircraft = len(data.aircraft)
    for i in range(data.nbAircraft):
        data.wtc[data.aircraft[i].callsign] = "D"
        data.index_aircraft[data.aircraft[i].callsign] = i
    for f in data.aircraft:
        data.aircraftForSearch[f.callsign] = f

    data.orders = [-1 for _ in range(data.nbAircraft)]

    for f in data.aircraft:

        data.fuel_detail[f.callsign] = 0
        data.time_detail[f.callsign] = 0
        data.distance_detail[f.callsign] = 0

    data.states = [dataRL.State(nb_pattern(f)) for f in data.aircraft]
    data.fuel = 0
    data.done_id = []
    data.conflicts = 0
    data.begHold = [-1 for _ in range(data.nbAircraft)]

    dataRL.orderUnderStudy = -1

    stack.stack("ASAS OFF")

    data.order_inv = [{} for _ in range(6)]
    data.merged = [False for _ in range(data.nbAircraft)]
    data.in_holding = [[] for _ in range(6)]

    stack.stack("IC test0.scn")

    stack.stack("DELAY 00:00:00.3, FF")


def nb_pattern(f):
    """Returns the pattern number of the flight f."""
    r = f.RWY
    i = f.IAF
    n = -1
    if r in ["25R", "25L"]:
        if i in ["SLL", "CLE"]:
            n = 0
        else:
            n = 1
    elif r in ["07R", "07L"]:
        if i in ["SLL", "VLA"]:
            n = 2
        else:
            n = 3
    else:
        if i == "TOTKI":
            n = 4
        else:
            n = 5
    return n
