import sys
from datetime import datetime, time
from random import randint

import keyboard


class Controller(object):
    def __init__(self, view, model):
        self.view = view
        self.model = model
        pass

    def run(self):
        print("start run")
        keyboard.on_press(self.on_press)
        keyboard.add_hotkey("ctrl+q", self.stop, args=["ctrl+q"])

    def stop(self, key):
        print("stop notify")
        self.model.set_interval(100000000)

    def on_press(self, key):
        if self.model.is_time_to_notify():
            print(f"press {key}")
            self.view.print_msg_to_stdout()
            self.model.set_last_notified_time(datetime.now())
        else:
            pass


class View(object):
    """Dialog."""

    def __init__(self, text, parent=None):
        """Initializer."""
        self.text = text

    def print_msg_to_stdout(self):
        now = datetime.now().strftime("%H:%M:%S")
        print("It's {}, {}".format(now, self.text))


class Model(object):
    def __init__(self, start_time, end_time, interval=10):
        self.start_time = start_time
        self.end_time = end_time
        self.interval = interval
        self.last_notified_time = datetime.now()

    def set_last_notified_time(self, last_notified_time):
        self.last_notified_time = last_notified_time

    def set_interval(self, interval):
        self.interval = interval

    def get_text(self):
        now = datetime.now()
        return f"It's {now}, " + self.text

    def is_sleep_time(self):
        now = datetime.now()
        return self.is_between(now.time(), self.start_time, self.end_time)

    def is_time_to_notify(self):
        return (
            self.is_sleep_time
            and (datetime.now() - self.last_notified_time).seconds > self.interval
        )

    @staticmethod
    def is_between(now, start, end):
        if start <= end:
            return start <= now < end
        else:  # over midnight e.g., 23:30-04:15
            return start <= now or now < end


if __name__ == "__main__":
    view = View("Your mom ask you to go to bed")
    model = Model(time(14), time(0))
    ctrl = Controller(view=view, model=model)
    ctrl.run()
    keyboard.wait()
