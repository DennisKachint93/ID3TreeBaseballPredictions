__author__ = 'dgotbaum'
class Year:
    def __init__(self, year):
        self.year = year
        self.pitchers = []

    def enterPitcher(self, pitcher):
        self.pitchers.append(pitcher)


