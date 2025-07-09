from dataclasses import dataclass


@dataclass
class DriverScore:
    driverId: int
    position: int
    points: int

    def __hash__(self):
        return hash((self.driverId, self.position, self.points))

    def __eq__(self, other):
        return (self.driverId == other.driverId
                and self.position == other.position
                and self.points == other.points)