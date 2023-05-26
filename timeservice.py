import label
from time import localtime
from rtc import RTC
import gc

X = 2
Y = 48
TIME_URL = "http://worldtimeapi.org/api/ip"

class Time(label.Metric):
    def __init__(self, matrixportal, x, y, description_style, data_style, group):
        super().__init__(x, y, description_style, data_style, "", group, frequency=3)
        self.matrixportal = matrixportal
        self.update_time()
        #self.get_data()
        gc.collect()
        return

    def get_data(self):
        current = localtime()
        actual_hour = current.tm_hour

        if actual_hour > 12:
            self.data.text = "{:d}:{:02d}".format(actual_hour - 12, current.tm_min)
        else:
            self.data.text = "{:d}:{:02d}".format(actual_hour, current.tm_min)

        self.unit.x = self.data.width + 4
        self.unit.text = 'PM' if actual_hour > 12 else 'AM'

    def update_time(self):
        data = self.matrixportal.network.fetch(TIME_URL)
        the_time = data.json().get('unixtime') + data.json().get('raw_offset')
        if data.json().get('dst') == True:
            the_time += 60 * 60

        RTC().datetime = localtime(the_time)
        print("updated time\n")
        gc.collect()
