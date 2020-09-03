import demandExtraction as e
import sys
import utils


def wpInter(rwy, iaf):
    """Returns the WP just after the IAF, None for RWY 02 because there is no such a point"""
    if rwy == "02":
        return None
    elif rwy in ["07R", "07L"]:
        if iaf in ["VLA", "SLL"]:
            return 41.340278, 1.719167, "BL545"
        elif iaf in ["VIBIM", "RUBOT"]:
            return 41.06389, 1.88528, "BL546"
    elif rwy in ["25R", "25L"]:
        if iaf in ["CLE", "SLL"]:
            return 41.52389, 2.2583, "BL443"
        elif iaf in ["LESBA", "RULOS"]:
            return 41.2475, 2.4247, "BL444"


def wpAfterIAF(rwy, iaf):
    """Returns the two first WP after the IAF"""
    if rwy == "02":
        if iaf == "TOTKI":
            return 41.11639, 1.9111, "BL640", 41.0533, 1.8825, "BL636"
        elif iaf == "VIBIM":
            return 41.07194, 2.08222, "BL639", 41.0089, 2.0536, "BL635"
    elif rwy in ["07R", "07L"]:
        if iaf in ["VLA", "SLL"]:
            return 41.264167, 1.76472, "BL541", 41.2367, 1.6844, "BL537"
        elif iaf in ["VIBIM", "RUBOT"]:
            return 41.13972, 1.8397, "BL542", 41.1122, 1.7594, "BL538"
    elif rwy in ["25R", "25L"]:
        if iaf in ["CLE", "SLL"]:
            return 41.4481, 2.304167, "BL439", 41.4756, 2.385, "BL435"
        elif iaf in ["LESBA", "RULOS"]:
            return 41.3236, 2.379167, "BL440", 41.3508, 2.4597, "BL436"


def createScn(liste, scnName, ii, jj):
    """Create a Scenario for BlueSky from a flight list, a name for the file and two index for slicing the list."""
    list_sorted = sorted(liste, key=lambda flight: flight.timeOver)
    data_keeped = []
    with open(scnName, "w") as file:
        for i in range(ii, jj):
            flight = list_sorted[i]
            time = flight.timeOver[-8:]

            wp = flight.entryWP
            cs = flight.callsign

            ac_type = flight.aircraftType

            rwy = flight.RWY
            iaf = flight.IAF

            if (
                utils.WP[wp][0] != 0 and iaf != "" and wpAfterIAF(rwy, iaf) != None
            ):  # Only usable data are keeped

                data_keeped.append(flight)

                # Writing the scenario
                file.write(
                    "{}.00>CRE {} {} {} {} 90 25000 250".format(
                        time, cs, ac_type, utils.WP[wp][0], utils.WP[wp][1]
                    )
                )
                file.write("\n")
                file.write("{}.00>ADDWPT {} {}".format(time, cs, wp))
                file.write("\n")
                if iaf != "TOTKI":
                    file.write("{}.00>ADDWPT {} {} 7000 220".format(time, cs, iaf))
                else:
                    file.write("{}.00>DEFWPT TOTKI 41.1336 1.7311".format(time))
                    file.write("\n")
                    file.write("{}.00>ADDWPT {} TOTKI 7000 220".format(time, cs))
                file.write("\n")
                if wpInter(rwy, iaf) != None:
                    lat, lon, name = wpInter(rwy, iaf)
                    file.write("{}.00>DEFWPT {} {} {}".format(time, name, lat, lon))
                    file.write("\n")
                    file.write("{}.00>ADDWPT,{},{},,220".format(time, cs, name))
                    file.write("\n")
                lat1, lon1, name1, lat2, lon2, name2 = wpAfterIAF(rwy, iaf)
                file.write("{}.00>DEFWPT {} {} {}".format(time, name1, lat1, lon1))
                file.write("\n")
                file.write("{}.00>ADDWPT {} {}".format(time, cs, name1))
                file.write("\n")
                file.write("{}.00>DEFWPT {} {} {}".format(time, name2, lat2, lon2))
                file.write("\n")
                file.write("{}.00>ADDWPT {} {}".format(time, cs, name2))
                file.write("\n")
                file.write("{}.00>LNAV {} ON".format(time, cs))
                file.write("\n")
                file.write("{}.00>VNAV {} ON".format(time, cs))
                file.write("\n")
                file.write("\n")
    return data_keeped


def create(ii, jj, n):
    """Create a scenario with two index to slice the file and a number for the scenario file name, used for number of aircraft training set disruption"""
    flight_list = e.extractData("plugins/wtc.csv")  # flights from the file
    keeped_data = createScn(
        flight_list, "scenario/{}.scn".format(n), ii, jj
    )  # keeped data
    return keeped_data
