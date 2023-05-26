import label
from secrets import secrets
import gc

X = 2
Y = 24
TIME_URL = "http://worldtimeapi.org/api/ip"

class Power(label.Metric):
    def __init__(self, matrixportal, x, y, description_style, data_style, group):
        super().__init__(x, y, description_style, data_style, "", group, frequency=60)
        self.matrixportal = matrixportal
        #self.get_data()
        self.description.text = "Powerwall"
        gc.collect()
        return

    def get_data(self):
        resp = self.matrixportal.network.fetch(secrets["tesla_gw"])
        data = resp.json()
        if data is None:
            gc.collect()
            return

        power = data.get('battery')
        self.data.text = "{0:.0f}".format(power)
        print("\npower is %s\n" % self.data.text)

        gc.collect()
