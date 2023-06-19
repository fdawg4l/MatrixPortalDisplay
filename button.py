import board
from digitalio import DigitalInOut, Direction, Pull

class Button:
    def __init__(self, address, callBackFn):
        self.button = DigitalInOut(address)

        # I think these are rougly constant.  E.g how can a button be an
        # output?  And pull is how the button is physically wired in the matrix
        # portal board.
        self.button.direction = Direction.INPUT
        self.button.pull = Pull.UP

        # Poor man's atomic/debounce.  We use this to decide if a button was
        # pressed.
        self.prevState = self.button.value

        # When pressed (unfortunately, during Update() because no threads on a
        # microcontroller), run the callback.
        self.callBackFn = callBackFn

    def update(self):
        curr = self.button.value

        if curr != self.prevState:
            if not curr:
                print("BUTTON is down")
                self.callBackFn()

        self.prevState = curr

