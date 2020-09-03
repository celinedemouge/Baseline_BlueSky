from enum import Enum
import dataDef as data


orderUnderStudy = -1
nbIter = 0
maxIter = 1
nbAction = 0


class Location(Enum):
    """Location in the pattern"""

    BEGINNING = 1
    MIDDLE = 2
    END = 3


class WTC(Enum):
    L = 1  # Light
    M = 2  # Medium
    H = 3  # Heavy
    SH = 4  # Super Heavy
    D = 5  # Default


class State:
    """States objects"""

    def __init__(self, num_pattern):
        self.t_before = 2
        self.t_after = 2
        self.location = Location.BEGINNING
        self.before_merged = False
        self.order_in_holding = -1
        self.t_merge = 2
        self.n = num_pattern
        self.wtc = WTC.D
        self.wtc_b = WTC.D
        self.wtc_a = WTC.D

    def updateTMerged(self, t):
        """Updates the attribute t_merge"""
        if t >= 0:
            k_b = int(t / 0.25)
            self.t_merge = k_b * 0.25 if t < 2 else 2
        else:
            k_b = int(t / 0.25)
            self.t_merge = (k_b - 1) * 0.25 if t > -2 else -2

    def updateLoc(self, t):
        """update the localisation of the aircraft in the pattern"""
        if t <= 20 * 10:
            self.location = Location.BEGINNING
        elif t <= 40 * 10:
            self.location = Location.MIDDLE
        else:

            self.location = Location.END

    def toNumber(self):
        """From a state to a number."""
        i_ = int((self.t_before) / 0.25)
        j_ = int((self.t_after) / 0.25)
        i = i_ + 8
        j = j_ + 8
        k = 0
        wa = self.wtc_a.value - 1
        wb = self.wtc_b.value - 1
        w = self.wtc.value - 1
        mm = int((self.t_merge) / 0.25) + 8
        if self.location == Location.MIDDLE:
            k = 1
        elif self.location == Location.END:
            k = 2
        m = 0 if self.before_merged else 1
        o = self.order_in_holding

        return (
            w * 2010000
            + wb * 402000
            + wa * 80400
            + self.n * 13400
            + m * 6700
            + (o + 1) * 670
            + m * 330
            + k * 290
            + (17 * i + j)
        )

    def make_hold(self, i, t, w):
        """When an aircraft starts the holding"""
        w_ok = WTC.D
        if w == "L":
            w_ok = WTC.L
        elif w == "M":
            w_ok = WTC.M
        elif w == "H":
            w_ok = WTC.H
        elif w == "SH":
            w_ok = WTC.SH

        self.wtc = w_ok

        data.orders[i] = data.nextOrd[self.n]
        try:
            data.order_inv[self.n][data.nextOrd[self.n]] = i
            i_before = data.order_inv[self.n][data.nextOrd[self.n] - 1]
            if data.merged[i_before]:
                self.before_merged = True
            data.states[i_before].wtc_a = w_ok
            self.wtc_b = data.states[i_before].wtc
        except KeyError:
            pass
        data.begHold[i] = t
        data.nextOrd[self.n] += 1
        self.order_in_holding = len(data.in_holding[self.n])
        data.in_holding[self.n].append(i)
        data.in_holding_g.append(i)

    def make_merge(self, i):
        """When an aircraft starts to merge"""
        data.merged[i] = True

        data.in_holding[self.n].remove(i)
        data.in_holding_g.remove(i)
        data.merged.append(i)
        o = data.orders[i]
        o1 = self.order_in_holding
        self.order_in_holding = -1
        for k in data.in_holding[self.n]:
            ok = data.orders[k]
            nk = data.states[k].n
            if ok > o:
                data.states[k].order_in_holding -= 1
        try:
            i1 = data.order_inv[self.n][o + 1]
            data.states[i1].before_merged = True
        except KeyError:
            pass

    def update_t(self, t_a, t_b, k):
        """update separation attributes"""
        if t_b >= 0:
            k_b = int(t_b / 0.25)
            self.t_before = k_b * 0.25 if t_b < 2 else 2
        else:
            k_b = int(t_b / 0.25)
            self.t_before = (k_b - 1) * 0.25 if t_b > -2 else -2
        if t_a >= 0:
            k_a = int(t_a / 0.5)
            self.t_after = k_a * 0.25 if t_a < 2 else 2
        else:
            k_a = int(t_a / 0.5)
            self.t_after = (k_a - 1) * 0.25 if t_a > -2 else -2
