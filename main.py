import argparse
from datetime import datetime, time
from time import sleep

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
            self.view.print_msg_to_stdout()
            self.model.set_last_notified_time(datetime.now())
        else:
            pass


class View(object):
    """
    View
    """

    def __init__(self, text, parent=None):
        """Initializer."""
        self.text = text

    def print_msg_to_stdout(self):
        now = datetime.now().strftime("%H:%M:%S")
        print("""{} {} \n {}""".format(bcolors.RED, now, bcolors.ENDC))
        for char in list(self.text):
            sleep(1 / 1000)
            print("""{}{}{}""".format(bcolors.OKCYAN, char, bcolors.ENDC), end="")


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

    def is_sleep_time(self):
        """
        Check if now is in the specific range
        """
        now = datetime.now()
        return self.is_between(now.time(), self.start_time, self.end_time)

    def is_time_to_notify(self):
        """
        Check if it's time to notify
        """
        return (
            self.is_sleep_time()
            and (datetime.now() - self.last_notified_time).seconds > self.interval
        )

    @staticmethod
    def is_between(now, start, end):
        """
        Check if now is between start and end
        """
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
        "-i",
        "--interval",
        dest="interval",
        type=int,
        help="The interval seconds between two notification",
        default=10,
    )
    parser.add_argument(
        "-c",
        "--content",
        dest="content",
        type=str,
        help='The content of notification, for example: "Your mom ask you to go to bed"',
        default="Your mom ask you to go to bed",
    )
    args = parser.parse_args()
    print(args.content)
    view = View(args.content)
    print(f"start_time: {args.go_to_bed_hour}, end_time: {args.wake_up_hour}")
    model = Model(
        time(args.go_to_bed_hour), time(args.wake_up_hour), int(args.interval)
    )
    ctrl = Controller(view=view, model=model)
    ctrl.run()
    keyboard.wait()
