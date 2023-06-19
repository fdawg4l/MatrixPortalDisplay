from time import time, monotonic, sleep
from displayio import Group as display_group
from adafruit_display_text.bitmap_label import Label as adaLabel
import gc

import label
import style
from secrets import secrets

X = 2
Y = 30
SECONDS_PER_DAY = 24 * 60 * 60
START_COUNTING = True
STOP_COUNTING = False

class Pots(label.Metric):
    def __init__(self, matrixportal, x, y, description_style, data_style, group):
        super().__init__(x, y, description_style, data_style, "Days", group, description=False, frequency=3)
        self.matrixportal = matrixportal

        self.state = STOP_COUNTING
        self.itemIdx = 0

        self.description = adaLabel(description_style.font)
        self.description.x = x
        self.description.y = y
        self.description.color = description_style.color
        self.description.text = 'En su boca!'

        self.scroll_group = display_group()
        self.scroll_group.append(self.description)
        group.append(self.scroll_group)

        gc.collect()
        return

    def updateText(self):
        if self.state == START_COUNTING:
            count = int((time() - self.startTime) / SECONDS_PER_DAY)
            self.data.text = str(count) 
            s = secrets["items"][self.itemIdx]
            self.description.text = s + " left in sink for:"

            if count >= 2:
                self.data.color = style.ORANGE # orange
            elif count >= 1:
                self.data.color = style.YELLOW # Yellow
            elif count <= 0:
                self.data.color = style.BLUE

            # Might need to move degree symbol over if it's 3 digits
            self.unit.x = self.data.width + 2
        else:
            self.description.text = "Dios Mi!  Nada!"
            self.data.text = str(0)

    def start(self):
        self.state = START_COUNTING
        self.startTime = time()
        print("C'mon, Jen!")
 
    def stop(self):
        self.state = STOP_COUNTING
        self.startTime = time()
        print("All good!  Finally!")

    def toggleStartStop(self):
        if self.state == START_COUNTING:
            self.stop()
        else:
            self.start()

    def incrementItem(self):
        itemIdx = self.itemIdx + 1
        self.itemIdx = itemIdx % len(secrets["items"])

    def update_scroll(self):
        self.scroll_group.x = self.scroll_group.x - 2

        text_width = self.description.bounding_box[2]
        if self.scroll_group.x <= -1 * text_width:
            self.scroll_group.x = 64
        sleep(0.06)

    def update(self):
        self.update_scroll()
        if monotonic() < (self.update_last + self.update_frequency):
            return
        self.update_last = monotonic()
        self.updateText()
