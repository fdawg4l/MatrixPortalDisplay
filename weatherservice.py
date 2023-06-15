import label
from time import localtime, monotonic, sleep
from rtc import RTC
from displayio import Group as display_group
from displayio import TileGrid, OnDiskBitmap
from adafruit_display_text.bitmap_label import Label as adaLabel
from secrets import secrets
import gc

X = 2
Y = 4
TIME_URL = "http://worldtimeapi.org/api/ip"
WEATHER_URL = f'https://api.openweathermap.org/data/2.5/weather?zip={secrets["weather_zip"]},us&appid={secrets["weather_app_id"]}&units=imperial'

WEATHER_CLEAR = (['clear', 'fair'], 0)
WEATHER_PART_CLOUDY = (['few clouds', 'broken clouds'], 2)
WEATHER_CLOUDY = (['scattered clouds'], 6)
WEATHER_STORM = (['thunderstorm'], 4)
WEATHER_RAIN = (['rain', 'drizzle', 'showers'], 8)
WEATHER_HAZE = (['overcast', 'dust', 'fog', 'smoke', 'mist', 'haze'], 10)

KNOWN_WEATHER = [
    WEATHER_CLEAR,
    WEATHER_PART_CLOUDY,
    WEATHER_CLOUDY,
    WEATHER_STORM,
    WEATHER_RAIN,
    WEATHER_HAZE,
]

icons = OnDiskBitmap('/icons.bmp')

class Weather(label.Metric):
    def __init__(self, matrixportal, x, y, description_style, data_style, group):
        super().__init__(x, y, description_style, data_style, "F", group, description=False, frequency=1800)
        self.matrixportal = matrixportal
        self.icon_sprite = TileGrid(
            icons,
            pixel_shader=icons.pixel_shader,
            tile_width=10,
            tile_height=10,
            x=53,
            y=y + 4
        )
        self.icon_sprite[0] = 1
        group.append(self.icon_sprite)

        self.description = adaLabel(description_style.font)
        self.description.x = x
        self.description.y = y
        self.description.color = description_style.color
        self.description.text = 'Loading'

        self.scroll_group = display_group()
        self.scroll_group.append(self.description)
        group.append(self.scroll_group)

        #self.get_data()
        gc.collect()
        return

    def get_data(self):
        data = self.update_weather()
        weather_main = data.get('main')

        temp_degrees = int(weather_main.get('temp'))
        self.data.text = str(temp_degrees)

        if temp_degrees < 35:
            self.data.color = BLUE
        elif temp_degrees < 50:
            self.data.color = 0x43E05C # Greenish
        elif temp_degrees < 70:
            self.data.color = 0xACE33B # Greenish
        elif temp_degrees < 80:
            self.data.color = 0xE8E527 # Yellow
        elif temp_degrees < 90:
            self.data.color = 0xFFB325 # orange
        else:
            self.data.color = 0x800000

        # Might need to move degree symbol over if it's 3 digits
        self.unit.x = self.data.width + 2

        weather_condition = data.get('weather')[0]
        description = weather_condition.get('description').lower()

        if description == "broken clouds":
            self.description.text = "broke-ass clouds"
        else:
            self.description.text = description

        # Try and match description to an icon
        weather_icon = WEATHER_CLEAR
        for weather_type in KNOWN_WEATHER:
            if any(item in description for item in weather_type[0]):
                weather_icon = weather_type
                break

        # The second column in the weather sprite sheet is the night
        # versions of the icons
        icon_idx = weather_icon[1]
        if localtime().tm_hour >= 18 or localtime().tm_hour <= 5:
            icon_idx += 1
        self.icon_sprite[0] = icon_idx

    def update_weather(self):
        data = self.matrixportal.network.fetch(WEATHER_URL)
        print("updated weather\n")
        return data.json()

    def update_scroll(self):

        text_width = self.description.bounding_box[2]
        for _ in range(text_width + 1):
            self.scroll_group.x = self.scroll_group.x - 1
            sleep(0.06)

        # Reset position to off the screen and scroll it back into the start
        # position
        self.scroll_group.x = 64
        for _ in range(self.scroll_group.x):
            self.scroll_group.x = self.scroll_group.x - 1
            sleep(0.06)

    def update(self):
        self.update_scroll()
        if monotonic() < (self.update_last + self.update_frequency):
            return
        self.update_last = monotonic()
        self.get_data()
