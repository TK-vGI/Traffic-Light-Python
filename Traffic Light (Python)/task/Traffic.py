class Traffic:
    def __init__(self, roads:int, interval:int) -> None:
        self.road = roads
        self.interval = interval

    @staticmethod
    def add_road() -> None:
        print("Road added")

    @staticmethod
    def delete_road() -> None:
        print("Road deleted")

    @staticmethod
    def open_system() -> None:
        print("System opened")