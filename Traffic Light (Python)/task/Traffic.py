import os
import time
import threading
from enum import Enum


ANSI_RESET = "\u001B[0m"
ANSI_GREEN = "\u001B[32m"
ANSI_RED = "\u001B[31m"


class Prompt(Enum):
    WELCOME = 'welcome to the traffic management system!'
    ROADS = 'input the number of roads'
    INTERVAL = 'input the interval'
    ROAD_NAME = 'input road name'
    MENU = ''
    ERROR = 'Incorrect option'


class Menu(Enum):
    QUIT = 'quit'
    ADD = 'add road'
    DELETE = 'delete road'
    OPEN = 'open system'


class Entry:
    @staticmethod
    def cap(msg):
        return ' '.join(word.capitalize() for word in msg.strip().split())

    def take_positive(self, prompt):
        print(Entry.cap(prompt.value), end=': ')
        while True:
            try:
                val = int(input())
                if val > 0:
                    return val
            except ValueError:
                pass
            print('Error! Incorrect Input. Try again: ', end='')

    def take_menu(self):
        print('\nMenu:')
        for i, item in enumerate(Menu):
            print(f'{i}.{Entry.cap(item.value)}')
        try:
            val = int(input('> '))
            if val in range(len(Menu)):
                return list(Menu)[val]
        except ValueError:
            pass
        print(Entry.cap(Prompt.ERROR.value))
        input()
        return None


class Road:
    def __init__(self, name):
        self.name = name


class TrafficController:
    def __init__(self, entry: Entry):
        print(Entry.cap(Prompt.WELCOME.value))
        self.entry = entry
        self.roads = entry.take_positive(Prompt.ROADS)
        self.interval = entry.take_positive(Prompt.INTERVAL)
        self.queue_roads = []
        self.status_list = []  # Each element: [seconds_remaining, is_open]
        self.lock = threading.Lock()
        self.system_mode = threading.Event()
        self.quit = False

    def add_road(self):
        name = input(f'{Entry.cap(Prompt.ROAD_NAME.value)}: ').strip()
        with self.lock:
            if len(self.queue_roads) >= self.roads:
                print("queue is full")
            else:
                self.queue_roads.append(Road(name))
                if len(self.status_list) == 0:
                    self.status_list.append([self.interval, True])
                else:
                    max_time = max(t[0] for t in self.status_list)
                    self.status_list.append([max_time + self.interval, False])
                    if len(self.queue_roads) == 2:
                        self.status_list[1][0] -= self.interval
                print(f"{name} Added!")
        input()

    def delete_road(self):
        with self.lock:
            if not self.queue_roads:
                print("queue is empty")
            else:
                removed = self.queue_roads.pop(0)
                self.status_list.pop(0)
                print(f"{removed.name} deleted!")
        input()

    def open_system(self):
        print("System opened")
        self.system_mode.set()
        input()
        self.system_mode.clear()

    def main_loop(self):
        while not self.quit:
            os.system('cls' if os.name == 'nt' else 'clear')
            choice = self.entry.take_menu()
            if choice == Menu.ADD:
                self.add_road()
            elif choice == Menu.DELETE:
                self.delete_road()
            elif choice == Menu.OPEN:
                self.open_system()
            elif choice == Menu.QUIT:
                print("Bye!")
                self.quit = True


class QueueThread(threading.Thread):
    def __init__(self, controller: TrafficController):
        super().__init__(daemon=True)
        self.controller = controller
        self.start_time = time.time()

    def run(self):
        while not self.controller.quit:
            time.sleep(1)
            self.tick()
            if self.controller.system_mode.is_set():
                os.system('cls' if os.name == 'nt' else 'clear')
                elapsed = int(time.time() - self.start_time)
                print(f"! {elapsed}s. have passed since system startup !")
                print(f"! Number of roads: {self.controller.roads} !")
                print(f"! Interval: {self.controller.interval} !")

                with self.controller.lock:
                    if self.controller.queue_roads:
                        print()
                        for road, (secs, is_open) in zip(
                                self.controller.queue_roads,
                                self.controller.status_list):
                            color = ANSI_GREEN if is_open else ANSI_RED
                            state = "open" if is_open else "closed"
                            print(f"{color}Road \"{road.name}\" will be {state} for {secs}s.{ANSI_RESET}")
                        print()
                print('! Press "Enter" to open menu !')

    def tick(self):
        with self.controller.lock:
            status = self.controller.status_list
            if any(s[1] for s in status):
                for i, (secs, is_open) in enumerate(status):
                    if secs <= 1 and is_open:
                        if len(status) == 1:
                            status[i] = [self.controller.interval, True]
                        else:
                            status[i] = [len(status) * self.controller.interval - self.controller.interval, False]
                    elif secs <= 1 and not is_open:
                        status[i] = [self.controller.interval, True]
                    else:
                        status[i][0] -= 1
            elif status:
                status[0] = [self.controller.interval, True]
                for i in range(1, len(status)):
                    status[i][0] = i * self.controller.interval


if __name__ == '__main__':
    entry = Entry()
    controller = TrafficController(entry)
    thread = QueueThread(controller)
    thread.start()
    controller.main_loop()
    thread.join()