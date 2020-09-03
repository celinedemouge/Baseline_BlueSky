from bluesky import stack, traf, sim
import time
import dataDef as data
import dataRL
import plugin_holding
import random


def init_plugin():
    """Initialization of the plugin."""

    # Configuration parameters
    config = {
        "plugin_name": "RL",
        "plugin_type": "sim",
        "update_interval": 30,
        "update": update,
    }

    stackfunctions = {}
    # init_plugin() should always return these two dicts.
    return config, stackfunctions


def update():
    """Periodic update functions that are called by the simulation."""

    # If this the end of the process
    if sim.simt >= (3600 * 20 - 100):
        print("Fuel consumption: {}".format(data.fuel / data.nbAircraft))
        print("Conflicts : {}".format(data.conflicts))
        sim.quit()
        sim.stop()
        quit()
        return None

    # Update the simulation and the states
    plugin_holding.update2()
    n = len(traf.id)
    if n == 0 or data.delta_fuel == 0:

        return None

    # If an aircraft has been under study at the last step
    if dataRL.orderUnderStudy != -1:

        # Conflict number computation
        t_min = min(
            [
                min(
                    data.states[k].t_before,
                    data.states[k].t_after,
                    data.states[k].t_merge,
                )
                for k in data.in_holding_g
            ]
        )
        l = [data.states[k].t_merge for k in range(data.nbAircraft) if data.merged[k]]
        t_min2 = min(l) if l != [] else 0
        if t_min < 0:
            data.conflicts += 1
            print("conflict")
        if t_min2 < 0:
            if t_min >= 0:
                data.conflicts += 1
            print("conflict in merged aircraft")

    # Find the next aircraft to study
    search_order = 0
    k2 = -1
    while not (k2 in data.in_holding_g) or search_order <= data.nbAircraft:
        dataRL.orderUnderStudy = (dataRL.orderUnderStudy + 1) % (data.nbAircraft)
        if data.aircraft[dataRL.orderUnderStudy].callsign in traf.id:
            k2 = dataRL.orderUnderStudy
        search_order += 1

    # No one found
    if search_order == data.nbAircraft:
        dataRL.orderUnderStudy = -1
        return None

    decision = take_decision(k2, data.states[k2])

    # If the decision is to make the aircraft merge
    if decision == 1:
        plugin_holding.startMerging(data.aircraft[k2].callsign)


def take_decision(k, currentState):
    """Take the decision for the aircraft k in the state currentState."""
    if currentState.t_before >= 0 and currentState.t_merge >= 0:
        return 1
    else:
        return 0
