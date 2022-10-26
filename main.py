import calendar
from datetime import datetime
import os
import json
import logging

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.textinput import TextInput


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


class ShiftCell(TextInput):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.data_holder = kwargs.get("data_holder")
        self.day = kwargs.get("day")
        self.hour_cell = kwargs.get("hour_cell")
        self.role = kwargs.get("role")

    def submit_data(self):
        operator = str(self.text).strip().upper()
        self.data_holder.operators[operator].configure_day(
            day=self.day,
            hours_roles=self.hours_roles)


class Operator:
    def __init__(self, *args, **kwargs):

        self.name = kwargs.get("name")
        self.general_shift = {
            1: "",
            2: "",
            3: "",
            4: "",
            5: "",
            6: "",
            7: "",
            8: "",
            9: "",
            10: "",
            11: "",
            12: "",
            13: "",
            14: "",
            15: "",
            16: "",
            17: "",
            18: "",
            19: "",
            20: "",
            21: "",
            22: "",
            23: "",
            24: "",
            25: "",
            26: "",
            27: "",
            28: "",
            29: "",
            30: "",
            31: ""
        }
        self.quantity_messager_roles = int(kwargs.get("mess_cells"), 0)
        self.quantity_calls_roles = int(kwargs.get("calls_cells"), 0)
        self.quantity_second_line = int(kwargs.get("second_line"), 0)
        #  month shift = dict(1:[(hours, role),])
        self.month_shift = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
            10: [],
            11: [],
            12: [],
            13: [],
            14: [],
            15: [],
            16: [],
            17: [],
            18: [],
            19: [],
            20: [],
            21: [],
            22: [],
            23: [],
            24: [],
            25: [],
            26: [],
            27: [],
            28: [],
            29: [],
            30: [],
            31: []
        }

    def configure_day(self, **kwargs):
        day = kwargs.get("day")
        hours_roles = kwargs.get("hours_role", [])

        self.month_shift[day].append(hours_roles)

    def configure_general_shift(self, **kwargs):
        self.general_shift = kwargs

    def increment_usage(self, *args):
        pass


class GeneralShiftHolder(BoxLayout):
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


class MainLayout(BoxLayout):
    def __init__(self):
        super().__init__()

        self.general_shift_holder = ObjectProperty(None)

        self.file = os.path.join("data", "data.json")
        self.data = dict()
        self.hours = list()
        self.operators = list()
        self.shift = dict()

        self.read_data()
        pass

    def read_data(self):
        with open(self.file, "r", encoding="utf8") as f:
            self.data = json.load(f)[0]

        self.hours = self.data["hours"]
        self.operators = \
            {operator: Operator(name=operator)
             for operator in self.data["operators"]}
        self.shift = self.data["shift"][0]


class MainApp(App):
    def __init__(self):

        super(MainApp, self).__init__()

    def build(self):
        return MainLayout()