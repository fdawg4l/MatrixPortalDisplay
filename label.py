from adafruit_display_text.bitmap_label import Label as adaLabel
from time import monotonic
import gc

class Style:
    def __init__(self, color, font):
        self.color = color
        self.font = font


class Unit(adaLabel):
    """
    A unit is a units label for the metric
    """
    def __init__(self, x, y, unit_letter, style):
        super().__init__(style.font)
        self.color = style.color
        self.x = x
        self.y = y
        self.text = unit_letter


class Metric():
    """
    A metric is 2 Labels;  a description, and then the data under it.

    """
    def __init__(self, x, y, description_style, data_style, unit_letter, group, description=True, frequency=10):
        # We start the metric with the description.  But, you can disable the

        if description == True:
            self.description = adaLabel(description_style.font)
            self.description.color = description_style.color
            self.description.x = x
            self.description.y = y
            self.description.text = " "
            group.append(self.description)

        self.data = adaLabel(data_style.font)
        self.data.color = data_style.color
        # Left justified
        self.data.x = x
        # height of the description + description y
        self.data.y =  y + 7
        group.append(self.data)

        # XXX todo(x)
        self.unit = Unit(self.data.x + 22, self.data.y, unit_letter, description_style)
        group.append(self.unit)

        self.update_frequency = frequency
        self.update_last = monotonic() - frequency
        gc.collect()

    def update_data(self):
        """
        Override this method to update the data and description text
        """
        raise Exception("get_data unset")

    def update(self):
        if monotonic() < (self.update_last + self.update_frequency):
            return
        self.update_last = monotonic()
        gc.collect()
        self.get_data()
        gc.collect()

class URLMetric(Metric):
    """
    A metric based on a URL which gets updated on a frquency
    """
    def __init__(self, x, y, description_style, data_style, unit_letter, url, data_key, description_text, description_key=None, frequency=10):
        super().__init__(x, y, description_style, data_style, unit_letter, frequency=10)


