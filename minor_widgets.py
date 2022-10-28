from kivy.uix.label import Label
from kivy.metrics import dp


class HourCellLabel(Label):
    '''Used for displaying hour cell in shifts'''

    def __init__(self, *args, **kwargs):
        text = "-".join(kwargs.get("hour_cell")
        super().__init__(text=text, size_hint_x=None, width=dp(60))
