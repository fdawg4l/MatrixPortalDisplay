import label
from secrets import secrets
import gc

X = 2
Y = 24
TIME_URL = "http://worldtimeapi.org/api/ip"

class Power(label.Metric):
    def __init__(self, matrixportal, x, y, description_style, data_style, group):
        super().__init__(x, y, description_style, data_style, "%         Kw", group, frequency=60)
        self.matrixportal = matrixportal
        #self.get_data()
        self.description.text = "Powerwall"
        gc.collect()
        return

    def _get_data(self):
        gc.collect()
        return self.matrixportal.network.fetch(secrets["tesla_gw"]).json()

    def get_data(self):
        data = self._get_data()
        gc.collect()
        if data is None:
            return

        cap = data.get('battery')
        draw = data.get('inverter')['load_instant_power']
        self.data.text = "{0:.0f} {1:.1f}".format(cap, (draw / 1000))
        self.unit.x = self.data.width + 2
        print("\npower is %s\n" % self.data.text)

        gc.collect()
