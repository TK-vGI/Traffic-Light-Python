class Traffic:
    def __init__(self, roads:int, interval:int) -> None:
        self.roads = roads
        self.interval = interval

    def add_road(self) -> None:
        self.roads += 1
        print("Road added")

    def delete_road(self) -> None:
        if self.roads > 1:
            self.roads -= 1
            print("Road deleted")
        else:
            print("Cannot delete: At least one road is required")

    def open_system(self) -> None:
        print("System opened")