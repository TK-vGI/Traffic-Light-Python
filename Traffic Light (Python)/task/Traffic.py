class Traffic:
    def __init__(self, max_roads:int, interval:int) -> None:
        self.max_roads = max_roads
        self.interval = interval
        self.queue = []
        self.front = 0
        self.rear = -1
        self.size = 0

    def add_road(self,road_name:str) -> None:
        if self.size >= self.max_roads:
            print("Queue is full")
            return
        self.rear = (self.rear + 1) % self.max_roads
        if len(self.queue) <= self.rear:
            self.queue.append(road_name)
        else:
            self.queue[self.rear] = road_name
        self.size += 1
        print(f"{road_name} Added")

    def delete_road(self) -> None:
        if self.size == 0:
            print("Queue is empty")
            return
        road_name = self.queue[self.front]
        self.front = (self.front + 1) % self.max_roads
        self.size -= 1
        print(f"{road_name} deleted")

    def get_queue_size(self) -> int:
        return self.size

    def get_roads(self) -> list:
        if self.size == 0:
            return []
        roads = []
        for i in range(self.size):
            index = (self.front + i) % self.max_roads
            roads.append(self.queue[index])
        return roads

    def open_system(self) -> None:
        print("System opened")