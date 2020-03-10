import math
class Time:

    def __init__(self, hour, mins):
        self.hour = hour
        self.mins = mins


    def __add__(self,other):
        new_hours = self.hour + other.hour
        new_mins = self.mins + other.mins
        if new_mins >= 60:
            new_hours += 1
            new_mins = new_mins - 60
        return Time(new_hours, new_mins)

    def __sub__(self, other):
        new_hours = self.hour - other.hour
        new_mins = self.mins - other.mins
        if new_mins <= 0:
            new_hours -= 1
            new_mins = new_mins + 60
        
        return Time(new_hours, new_mins)

    def get_mins(self):
        if self.hour < 0:
            return 0
        return self.hour * 60 + self.mins

    def __str__(self):
        str_nums = str(self.mins)
        if self.mins < 10:
            str_nums = "0" + str(math.ceil(self.mins))
        return str("%d:%.2s"%(self.hour, str_nums))