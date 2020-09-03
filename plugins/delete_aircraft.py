from bluesky import stack, traf
import dataRL
import dataDef as data


def init_plugin():

    # Configuration parameters
    config = {
        "plugin_name": "DEL",
        "plugin_type": "sim",
        "update_interval": 150,
        "update": update,
    }

    stackfunctions = {}

    # init_plugin() should always return these two dicts.
    return config, stackfunctions


def update():
    n = len(traf.id)
    if n == 0:
        return None
    for i in range(n):
        if abs(traf.perf.phase[i] - 1) < 0.1:  # if the aircraft is on the ground
            k = data.index_aircraft[traf.id[i]]
            data.merged[k] = False
            stack.stack("DEL {}".format(traf.id[i]))  # it is deleted
