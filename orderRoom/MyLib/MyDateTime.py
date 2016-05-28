# -*- coding: utf-8 -*-
import time
import datetime

class MyDateTime:
    def __init__(self, yyyy_mm_dd):
        year, month, day = yyyy_mm_dd.split('-')
        self.main_datetime = datetime.datetime(int(year), int(month), int(day))  

    def date(self):
        return self.main_datetime.date()
        
    def date_time(self):
        return self.main_datetime
        
    def time(self):
        return self.main_datetime.time()
    
    def add_day(self, day_num):
        return self.main_datetime + datetime.timedelta(days=day_num)

    def comprise_between(self, bound_my_datetime):
        return abs((bound_my_datetime.main_datetime - self.main_datetime).days)+1
        
    def comprise_everyday(self, bound_my_datetime):
        everyday_list=[]
        for day in range(self.comprise_between(bound_my_datetime)):
            curr_datetime = self.add_day(day)
            everyday_list.append(curr_datetime)
        return everyday_list

    def __str__(self):
        return self.main_datetime
