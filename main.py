import calendar
from datetime import datetime
import os
import json
import logging

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.app import App


'''
1. Make calendar

2. Accept operators as new lines

3. Fill daily shif equally and manually

4. randomize equally hourly shift


'''

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handle = logging.FileHandler(os.path.join("data", "log.log"))
handle = logging.StreamHandler()
formatter = logging.Formatter(
    '\n\n=start=\n%(asctime)s - %(funcName)s - %(message)s\n=end=')
logger.addHandler(handle)
handle.setFormatter(formatter)



class GeneralShiftholder(BoxLayout):
    ''' Layout to hold month general shift '''

    def __init__(self, **kwargs):
        self.month = kwargs.get("month", datetime.now().month + 1)
        for_next_year = False

        if self.month > 12:
            self.month = 1
            for_next_year = True

        self.year = kwargs.get("year", False)
        if not self.year:
            if for_next_year:
                self.year = datetime.now().year + 1
            else:
                self.year = datetime.now().year

        self.hours_file = os.path.join("data", "hours.json")

        self.month_days = self.current_month_days()

        self.shift = self.construct_empty_shift()
        logger.debug(f'{self.construct_empty_shift()=}')

    def construct_empty_shift(self):
        ''' return {[day, hour_step]: None}'''
        for day in self.month_days:
            for time_period in self.read_hours():
                self.shift[(day, time_period)] = None

    def current_month_days(self):
        '''return days of current month'''
        return calendar.TextCalendar().monthdayscalendar(self.year, self.month)

    def read_hours(self):
        '''read presaved hours from hours.json'''
        with open(self.hours_file, "r") as f:
            return json.load(f)[0]


class MainApp(App):
    def __init__(self):

        super(MainApp, self).__init__()
        self.file = os.path.join("data", "data.json")
        self.data = dict()
        self.hours = list()
        self.operators = list()

        self.read_data()
        pass

    def read_data(self):
        with open(self.file, "r", encoding="utf8") as f:
            self.data = json.load(f)[0]

        self.hours = self.data["hours"]
        self.operators = self.data["operators"]

    def build(self):
        pass
