from bluesky import (
    stack,
    scr,
    traf,
    sim,
    tools,
)

import dataDef as data
import dataRL
import sys
import time
import createScn, demandExtraction
import numpy as np
import delete_aircraft


def init_plugin():

    config = {
        "plugin_name": "HOLDING",
        "plugin_type": "sim",
        "update_interval": 30,
    }

    stackfunctions = {}

    return config, stackfunctions


def update2():
    """Update called by the RL plugin"""

    n = len(traf.id)
    if n == 0:
        return None

    now = sim.simt

    data.delta_fuel = 0

    l_merged = [k for k in range(data.nbAircraft) if data.merged[k]]

    for i in range(n):
        k = data.index_aircraft[traf.id[i]]
        f = data.aircraftForSearch[traf.id[i]]

        # Computation of fuel consumption
        if not (abs(traf.perf.phase[i] - 1) < 0.25):

            data.fuel_detail[traf.id[i]] += traf.perf.fuelflow[i] * 30
            data.fuel += traf.perf.fuelflow[i] * 30

        if k in data.in_holding_g:
            data.delta_fuel += traf.perf.fuelflow[i] * 30
        if k in data.in_holding_g or data.merged[k]:
            v = traf.gs[i] / 3600
            data.distance_detail[traf.id[i]] += v * 30
            data.time_detail[traf.id[i]] += 30

        if k in data.in_holding_g or data.merged[k]:
            # Dealing with conflicts
            data.states[k].updateLoc(now - data.begHold[k])
            t_m = nearer_merge(traf.id[i], l_merged, data.wtc[traf.id[i]])
            data.states[k].updateTMerged(t_m)
            w = data.wtc[traf.id[i]]

            t_b = 9
            t_a = 9
            t_a_ = 0
            t_b_ = 0
            if n > 1:
                o = data.orders[k]
                n = data.states[k].n
                if o >= 1:
                    k1 = data.order_inv[n][o - 1]

                    if k1 != -1 and k != k1:
                        s = data.states[k1]
                        if s != None:
                            w1 = data.wtc[data.aircraft[k1].callsign]
                            t_sep = sep_aircraft(traf.id[i], data.aircraft[k1].callsign)
                            try:
                                t_b_max = data.wtc_t[(w1, w)]
                            except KeyError:
                                t_b_max = 2

                            if t_sep != None:
                                t_b = t_sep
                                t_b_ = t_b - t_b_max

                elif o == 0:
                    t_b_ = 2
                if o + 1 in data.order_inv[n].keys():
                    k2 = data.order_inv[n][o + 1]
                    w2 = data.wtc[data.aircraft[k2].callsign]
                    t_sep = sep_aircraft(traf.id[i], data.aircraft[k2].callsign)
                    try:
                        t_a_max = data.wtc_t[(w, w2)]

                    except KeyError:
                        t_a_max = 2
                    if k2 != -1 and k != k2:
                        if t_sep != None:
                            t_a = t_sep
                            t_a_ = t_a - t_a_max

                else:
                    t_a_ = 2

            data.states[k].update_t(t_a_, t_b_, k)

        # Updating states after the IAF
        if f.RWY == "02":
            if (
                abs(traf.actwp.lat[i] - 41.0533) <= 0.001
                and abs(traf.actwp.lon[i] - 1.8825) <= 0.001
                and (f.IAF == "TOTKI")
            ):
                startHolding(i, k, 199)

            elif (
                abs(traf.actwp.lat[i] - 41.0089) <= 0.001
                and abs(traf.actwp.lon[i] - 2.0536) <= 0.001
                and (f.IAF == "VIBIM")
            ):
                startHolding(i, k, 199)

        elif f.RWY in ["07L", "07R"]:
            if (
                abs(traf.actwp.lat[i] - 41.2367) <= 0.001
                and abs(traf.actwp.lon[i] - 1.6844) <= 0.001
                and (f.IAF in ["VLA", "SLL"])
            ):
                startHolding(i, k, 245)

            elif (
                abs(traf.actwp.lat[i] - 41.1122) <= 0.001
                and abs(traf.actwp.lon[i] - 1.7594) <= 0.001
                and (f.IAF in ["VIBIM", "RUBOT"])
            ):

                startHolding(i, k, 245)

        elif f.RWY in ["25L", "25R"]:
            if (
                abs(traf.actwp.lat[i] - 41.4756) <= 0.001
                and abs(traf.actwp.lon[i] - 2.385) <= 0.001
                and (f.IAF in ["CLE", "SLL"])
            ):

                startHolding(i, k, 65)

            elif (
                abs(traf.actwp.lat[i] - 41.3508) <= 0.001
                and abs(traf.actwp.lon[i] - 2.4597) <= 0.001
                and (f.IAF in ["LESBA", "RULOS"])
            ):
                startHolding(i, k, 65)


def startHolding(i, k, heading):
    """Function called when an aircraft begins its holding, i is the index in traf object, k in data.aircraft and heading the new heading for the aircraft"""
    traf.ap.selhdgcmd(i, heading)
    if not (k in data.in_holding_g):

        m = traf.perf.mass[i]
        if m > 400000:
            w = "SH"
        elif m > 136000:
            w = "H"
        elif m > 7000:
            w = "M"
        else:
            w = "L"
        data.wtc[traf.id[i]] = w
        data.states[k].make_hold(k, sim.simt, w)


def startMerging(X, printing=True):
    """function used for making merge a plane, 
    X is the callsign of the flight to merge"""

    f = data.aircraftForSearch[X]
    l = data.index_aircraft[X]
    if data.orders[l] == -1:
        return None
    if f.RWY == "02":
        stack.stack("ADDWPT {} SANIS".format(X))
        stack.stack("DIRECT {} SANIS".format(X))
        if f.IAF == "TOTKI":
            stack.stack("DELAY 00:00:00.50, HDG {} 100".format(X))
        elif f.IAF == "VIBIM":
            stack.stack("DELAY 00:00:00.50, HDG {} 270".format(X))
        stack.stack("DELAY 00:00:03.11, HDG {} 19".format(X))
        stack.stack("DELAY 00:00:04.11, DIRECT {} SANIS".format(X))

    elif f.RWY in ["07L", "07R"]:
        stack.stack("ADDWPT {} ASTEK".format(X)) if f.RWY == "07L" else stack.stack(
            "ADDWPT {} PERUK".format(X)
        )
        stack.stack("DIRECT {} ASTEK".format(X)) if f.RWY == "07L" else stack.stack(
            "DIRECT {} PERUK".format(X)
        )
        if f.IAF in ["VLA", "SLL"]:
            stack.stack("DELAY 00:00:00.50, HDG {} 100".format(X))
        elif f.IAF in ["VIBIM", "RUBOT"]:
            stack.stack("DELAY 00:00:00.50, HDG {} 270".format(X))
        stack.stack("DELAY 00:00:03.11, HDG {} 65".format(X))
        stack.stack(
            "DELAY 00:00:04.11, DIRECT {} ASTEK".format(X)
        ) if f.RWY == "07L" else stack.stack(
            "DELAY 00:00:04.11, DIRECT {} PERUK".format(X)
        )

    elif f.RWY in ["25L", "25R"]:
        stack.stack("ADDWPT {} SOTIL".format(X)) if f.RWY == "25L" else stack.stack(
            "ADDWPT {} TEBLA".format(X)
        )
        stack.stack("DIRECT {} SOTIL".format(X)) if f.RWY == "25L" else stack.stack(
            "DIRECT {} TEBLA".format(X)
        )
        if f.IAF in ["CLE", "SLL"]:
            stack.stack("DELAY 00:00:00.50, HDG {} 180".format(X))
        elif f.IAF in ["LESBA", "RULOS"]:
            stack.stack("DELAY 00:00:00.50, HDG {} 300".format(X))
        stack.stack("DELAY 00:00:03.11, HDG {} 245".format(X))
        stack.stack(
            "DELAY 00:00:04.11, DIRECT {} SOTIL".format(X)
        ) if f.RWY == "25L" else stack.stack(
            "DELAY 00:00:04.11, DIRECT {} TEBLA".format(X)
        )

    stack.stack("DELAY 00:00:05.11, DEST {} LEBL".format(X))
    if printing:
        print("{} has been merged at {}".format(X, sim.utc))

    k = data.index_aircraft[X]

    data.states[k].make_merge(k)


def sep_aircraft(X, Y):
    """Computes the separation between 2 aircraft. X and Y are callsigns of the two aircraft"""
    index_x, index_y = -1, -1
    for i in range(len(traf.id)):
        if traf.id[i] == X:
            index_x = i
        if traf.id[i] == Y:
            index_y = i
        if index_x != -1 and index_y != -1:
            break
    if index_x == -1 or index_y == -1:
        return None
    _, d = tools.geo.qdrdist(
        traf.lat[index_x], traf.lon[index_x], traf.lat[index_y], traf.lon[index_y]
    )
    v = traf.gs[index_x]
    t = (d / v) * 60
    return t


def nearer_merge(X, list_merge, wtcX):
    """Calculate the minimum separation to the aircraft which have already merged, X is the callsign"""
    # print('here')
    if list_merge == []:
        return 2
    else:
        t_min = 2
        for k in list_merge:
            t = sep_aircraft(X, data.aircraft[k].callsign)
            w = data.wtc[data.aircraft[k].callsign]
            t_ = t - data.wtc_t[(w, wtcX)]
            if t_ < t_min and t > 0.1:
                t_min = t_
        return t_min
