import argparse
import sys
from datetime import datetime, time
from random import randint

import keyboard


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RED = "\033[1;31m"


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
        print(
            "{} Warning: It's {}, {}{}".format(
                bcolors.RED, now, self.text, bcolors.ENDC
            )
        )


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
    # Instantiate the parser
    parser = argparse.ArgumentParser(description="GTB App description")
    parser.add_argument(
        "-g",
        "--go_to_bed_hour",
        dest="go_to_bed_hour",
        type=int,
        help="The start time of notification in hour format, for example: 0",
        default=0,
    )
    parser.add_argument(
        "-w",
        "--wake_up_hour",
        dest="wake_up_hour",
        type=int,
        help="The start time of notification in hour format, for exampe: 7. If you press any key in 0:00:00-7:00:00, you will get a notification",
        default=7,
    )
    parser.add_argument(
        "-c",
        "--content",
        dest="content",
        type=ascii,
        help="The content of notification",
        default="Your mom ask you to go to bed",
    )
    args = parser.parse_args()
    view = View(args.content)
    model = Model(time(args.go_to_bed_hour), time(args.wake_up_hour))
    ctrl = Controller(view=view, model=model)
    ctrl.run()
    keyboard.wait()
