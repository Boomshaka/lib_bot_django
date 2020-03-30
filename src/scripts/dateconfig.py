import configure as cfg
import datetime
from datetime import date

class Dates:
    start_date = datetime.datetime(2020, 2, 13, 0, 0)

    def __init__(self, start_id, target_time):
        self.current_date = datetime.datetime.now()
        self.start_id = start_id
        self.target_time = target_time
        self.date_to_reserve = None
        self.diff_day = None

    def configure(self):
        self.target_time = datetime.datetime(self.current_date.year, self.current_date.month, 
                                            self.current_date.day, self.target_time, 0)
        self.date_to_reserve = self.target_time + datetime.timedelta(days = 11)
        self.diff_day = (self.date_to_reserve - self.start_date).days
        
    




