from kivy.uix.label import Label


class HourCellLabel(Label):
    '''Used for displaying hour cell in shifts'''

    def __init__(self, *args, **kwargs):
        text = str(kwargs.get("hour_cell"))
        super().__init__(text=text)
