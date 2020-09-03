import demandExtraction


### Aircraft data file


# Aircraft in the simulation
aircraft = []
# Number of aircraft in the simulation
nbAircraft = 0
# Different training set for training set disruption
l = []
# Useful to find an flight object from the callsign
aircraftForSearch = {}
index_aircraft = {}

fuel = 0
fuel_detail = {}
time_detail = {}
distance_detail = {}
conflicts = 0
delta_fuel = 0

states = []


begHold = []
nextOrd = []

orders = []
order_inv = {}


wtc = {}
wtc_t = {
    ("SH", "H"): 1.5,
    ("SH", "M"): 3,
    ("SH", "L"): 4,
    ("SH", "SH"): 1.5,
    ("H", "H"): 1.5,
    ("H", "M"): 2,
    ("H", "L"): 3,
    ("H", "SH"): 1.5,
    ("M", "L"): 3,
    ("M", "M"): 1.5,
    ("M", "H"): 1.5,
    ("M", "SH"): 1.5,
    ("L", "L"): 1.5,
    ("L", "M"): 1.5,
    ("L", "H"): 1.5,
    ("L", "SH"): 1.5,
}


# True if the aircraft has merged
merged = []
# Aircraft in holding for each pattern
in_holding = [[], [], [], [], [], []]
# All aircraft in holding
in_holding_g = []
