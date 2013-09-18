import re


class Result(object):
    def __init__(self, scores, odds):
        super(Result, self).__init__()
        self._scores = scores
        self.odds_ = odds

    def detect_odds(self):
        if self.odds_:
            o310 = self.odds_.split(" ");
            o310 = [float(f) for f in o310]
            if len(o310) == 3:
                r = dict()
                r[o310[0]] = "3"
                r[o310[1]] = "1"
                r[o310[2]] = "0"
                return r[min(o310)]
                pass
            pass
        return ""

    def detect(self, last4):
        r = list()
        com_odds_result = self.detect_odds()
        #r.add(com_odds_result)
        num_3 = self._scores.count(3)
        num_1 = self._scores.count(1)
        num_0 = self._scores.count(0)

        total_3 = num_3 + num_1
        total_0 = num_0 + num_1
        total_3_0 = num_3 + num_0

        if total_3 > total_0:
            r.append("3")
        elif total_3 < total_0:
            r.append("0")
        if num_1 > total_3_0:
            r.clear()
            r.append("1")

        program_result = "".join(r)
        return program_result


class Formula(object):
    TYPE_TOTAL = "total"
    TYPE_LAST10 = "last10"
    TYPE_LAST6 = "last6"
    TYPE_LAST4 = "last4"
    TYPE_LAST_MID = "last_mid"

    def __init__(self, type_=TYPE_TOTAL):
        super(Formula, self).__init__()
        self._type = type_
        self._results = []
        self.main_force = 0.0 #攻击
        self.main_defence = 0.0 #防御
        self.client_force = 0.0
        self.client_defence = 0.0
        self.avg_balls = 0.0
        self.full_io_balls = 0.0

    def type_(self):
        return self._type

    def to_results(self):
        self.count_force(self.main_force, self.client_force)
        #self.count_defence(self.main_defence,self.client_defence)
        return self._results

    def count_force(self, main, client, fact=0.75):
        self.full_io_balls = main + client
        diff = main - client
        self.avg_balls = diff
        if diff >= fact and main > 1:
            self._results.append(3)
        elif diff <= -1 * fact and client > 1:
            self._results.append(0)
        else:
            self._results.append(1)

    def count_defence(self, main, client, fact=0.5):
        if main > 1 and client > 1:
            self._results.append(1)
            return
        diff = main - client
        if diff >= fact:
            self._results.append(3)
        elif diff <= -1 * fact:
            self._results.append(0)
        else:
            self._results.append(1)


def get_float_numbers_(text):
    p = re.compile("\\d+\\.\\d+", re.M)
    return p.findall(text)


def get_int_numbers_(text):
    p = re.compile("\\d+", re.M)
    strs = p.findall(text)
    return [int(i) for i in strs]