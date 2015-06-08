__author__ = 'dgotbaum'
class PitcherYear:
    def __init__(self, playerID, SO, BB, ERA, IP, H,gameYear, age):
        #Statistics from Data
        self.age = age
        self.name = playerID
        self.strikeouts = SO
        self.walks = BB
        self.era = ERA
        self.hits = H
        self.IP = IP
        self.year = gameYear


        #Set Weights Below
        self.eraWeight = .4
        self.whpWeight = .4
        self.sowWeight = .2

    def __str__(self):
        return "%s: %f" %(self.name, self.pitchScore())

    #walks + hits per innings pitched
    def WHIP(self):
        return (self.strikeouts + self.hits)/self.IP

    #strikeouts divided by walks
    def strikeouts_by_walks(self):
        return self.strikeouts/self.walks

    def weighted_SOW(self):
        return (self.strikeouts_by_walks()/12)*self.sowWeight

    def weighted_ERA(self):
        return (1.5/self.era)*self.eraWeight

    #Weighted walks + hits per innings pitched
    def weighted_WHIP(self):
        return (1.7/self.WHIP())*self.whpWeight

    def pitchScore(self):
        return (self.weighted_ERA() + self.weighted_SOW() + self.weighted_WHIP())*10

    def ERA_category(self):
        if self.era < 2.9:
            return 1
        elif self.era < 3.75:
            return 2
        elif self.era < 4.2:
            return 3
        else:
            return 4

    def WHIP_category(self):
        if self.WHIP() < 1.25:
            return 1
        elif self.WHIP() < 1.4:
            return 2
        elif self.WHIP() < 1.6:
            return 3
        else:
            return 4

    def age_category(self):
        if self.age < 23:
            return 1
        elif self.age < 27:
            return 2
        elif self.age < 30:
            return 3
        else:
            return 4

    def SOW_category(self):
        if self.strikeouts_by_walks() < .86:
            return 1
        elif self.strikeouts_by_walks() < 1.33:
            return 2
        elif self.strikeouts_by_walks() < 2:
            return 3
        else:
            return 4

    def print_categories(self):
        print("age" , self.age_category())
        print("ERA" , self.ERA_category())
        print("WHIP", self.WHIP_category())
        print("SOW" , self.SOW_category())

    def list_categories(self):
        return [self.age_category(), self.ERA_category(), self.WHIP_category(), self.SOW_category()]
