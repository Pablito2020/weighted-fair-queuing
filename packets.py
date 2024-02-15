from dataclasses import dataclass
from itertools import groupby
from operator import attrgetter
from typing import Generator, Tuple, List


@dataclass(frozen=True, order=True, repr=True, eq=True, unsafe_hash=True)
class StreamIdentifier:
    id_: int

    def __post_init__(self):
        if self.id_ <= 0:
            raise ValueError(f"Stream id must be greater than 0")

    @staticmethod
    def generate(n: int) -> Generator['StreamIdentifier', None, None]:
        for i in range(1, n + 1):
            yield StreamIdentifier(i)


@dataclass(frozen=True)
class Priority:
    priority: int

    def __post_init__(self):
        if self.priority < 0 or self.priority > 100:
            raise ValueError(f"Priority must be in the range [0, 100]")

    @property
    def percentage(self) -> float:
        return self.priority / 100

    def __add__(self, other: 'Priority') -> 'Priority':
        assert isinstance(other, Priority)
        return Priority(self.priority + other.priority)

    @staticmethod
    def maximum() -> 'Priority':
        return Priority(100)

    @staticmethod
    def minimum() -> 'Priority':
        return Priority(0)


@dataclass
class PacketSize:
    size: float

    def __post_init__(self):
        if self.size <= 0:
            raise ValueError(f"Packet size must be greater than 0")


@dataclass(frozen=True, order=True, repr=True, eq=True, unsafe_hash=True)
class Time:
    time: float

    def __post_init__(self):
        if self.time < 0:
            raise ValueError(f"Arrival time must be greater than 0")


@dataclass(frozen=True)
class Packet:
    id_: StreamIdentifier
    size: PacketSize
    time: Time

    @staticmethod
    def from_tuple(t: Tuple[float, float, int]) -> 'Packet':
        time, size, id_ = t
        return Packet(StreamIdentifier(id_), PacketSize(size), Time(time))


class Interface:
    """
    Emulate a network interface that receives packets from a file.
    You can iterate over the packets, if a packet has the same arrival time as another, they will be in the same list.
    """

    def __init__(self, file_name: str):
        sorted_packets = sorted(list(Interface.get_packets_from_file(file_name=file_name)), key=attrgetter('time'))
        self.packets: List[List[Packet]] = [list(group) for _, group in groupby(sorted_packets, key=attrgetter('time'))]

    def __iter__(self):
        for packets in self.packets:
            yield packets

    @staticmethod
    def get_packets_from_file(file_name: str) -> Generator[Packet, None, None]:
        with open(file_name, 'r') as file:
            for index, line in enumerate(file):
                try:
                    values = line.split(" ")
                    values = (float(values[0]), float(values[1]), int(values[2]))
                    yield Packet.from_tuple(values)
                except (ValueError, IndexError) as e:
                    raise ValueError(f"Invalid packet format in file {file_name} line {index}")
