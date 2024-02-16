from dataclasses import dataclass
from typing import Generator, Tuple, List


@dataclass(frozen=True, order=True, repr=True, eq=True, unsafe_hash=True)
class StreamIdentifier:
    id_: int

    def __post_init__(self):
        if self.id_ <= 0:
            raise ValueError(f"Stream id must be greater than 0")

    @staticmethod
    def generate(n: int) -> Generator["StreamIdentifier", None, None]:
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
        return 100 / self.priority

    def __add__(self, other: "Priority") -> "Priority":
        assert isinstance(other, Priority)
        return Priority(self.priority + other.priority)

    @staticmethod
    def maximum() -> "Priority":
        return Priority(100)

    @staticmethod
    def minimum() -> "Priority":
        return Priority(0)


@dataclass(frozen=True, order=True, repr=True, eq=True, unsafe_hash=True)
class Time:
    time: float

    def __post_init__(self):
        if self.time < 0:
            raise ValueError(f"Arrival time must be greater than 0")

    def __add__(self, other: "Time") -> "Time":
        assert isinstance(other, Time)
        return Time(self.time + other.time)

    def __str__(self):
        return f"{self.time} sec."


@dataclass
class PacketSize:
    size: float

    def __post_init__(self):
        if self.size <= 0:
            raise ValueError(f"Packet size must be greater than 0")

    def to_time(self, speed: float) -> Time:
        return Time(self.size / speed)


@dataclass(frozen=True)
class TimeInterval:
    begin: Time
    end: Time

    def __post_init__(self):
        if self.begin.time >= self.end.time:
            raise ValueError(f"Interval begin time must be less than end time")

    def __contains__(self, item: Time) -> bool:
        assert isinstance(item, Time)
        return self.begin.time <= item.time < self.end.time

    def __str__(self):
        return f"[{self.begin} - {self.end}]"


@dataclass(frozen=True)
class Packet:
    id: int
    stream_id: StreamIdentifier
    size: PacketSize
    time: Time

    @staticmethod
    def from_tuple(t: Tuple[float, float, int, int]) -> "Packet":
        time, size, stream_id, packet_id = t
        return Packet(
            packet_id, StreamIdentifier(stream_id), PacketSize(size), Time(time)
        )

    def time_to_send(self, speed: float = 1.0) -> Time:
        return self.size.to_time(speed)

    def __str__(self):
        return str(self.id)


def get_iter_packets_from_file(file_name: str) -> Generator[Packet, None, None]:
    with open(file_name, "r") as file:
        for index, line in enumerate(file):
            try:
                values_str = line.split(" ")
                values = (
                    float(values_str[0]),
                    float(values_str[1]),
                    int(values_str[2]),
                    index + 1,
                )
                yield Packet.from_tuple(values)
            except (ValueError, IndexError):
                raise ValueError(
                    f"Invalid packet format in file {file_name} line {index}"
                )


def get_packets_from_file(file_name: str) -> List[Packet]:
    return list(get_iter_packets_from_file(file_name))
