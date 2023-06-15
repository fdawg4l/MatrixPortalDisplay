from displayio import Group as display_group
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.matrixportal import MatrixPortal
import gc
import timeservice
import weatherservice
import powerwallservice
from label import Style
import style

gc.collect()

matrixportal = MatrixPortal(height=64, width=64)

# Fonts
glyphs = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ% "
nums = b"0123456789:"

med_font = bitmap_font.load_font('/Tamzen8x16b.bdf')
med_font.load_glyphs(nums)

tiny_font = bitmap_font.load_font('/pixel-3x5.bdf')
tiny_font.load_glyphs(glyphs)

gc.collect()

class Group(display_group):
    def __init__(self, matrixportal, description_style, data_style):
        super().__init__()
        w = weatherservice.Weather(matrixportal, weatherservice.X, weatherservice.Y, description_style, data_style, self)
        t = timeservice.Time(matrixportal, timeservice.X, timeservice.Y, description_style, data_style, self)
        p = powerwallservice.Power(matrixportal, powerwallservice.X, powerwallservice.Y, description_style, data_style, self)
        self.members = [w, t, p]

    def update(self):
        for i in self.members:
            i.update()


description_style = Style(style.OFF_WHITE, tiny_font)
data_style = Style(style.BLUE, med_font)
services = Group(matrixportal, description_style, data_style)

root_group = display_group()
root_group.append(services)
matrixportal.display.show(root_group)

while True:
    try:
        services.update()
        gc.collect()
    except Exception as e:
        print(f"exception {e=}, {type(e)=}")
