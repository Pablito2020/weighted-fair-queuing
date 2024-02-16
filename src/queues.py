import logging
from dataclasses import dataclass, field
from itertools import groupby
from queue import PriorityQueue
from typing import Tuple, List

from src.packets import Packet, Time, get_packets_from_file, TimeInterval

"""
This file includes the three "queues" that a router should have:
    - ReceiveQueue: Receive packages from different interfaces
    - RouterQueue: Schedules when to send packages
    - SendQueue: The package that has exited the router queue enters this queue. We're sending it to the final receiver.
"""


class ReceiveQueue:
    """
    Gets packages from an interface (in this case it's virtual, we emulate it from a file).
    The packages are sorted from the time they arrived.
    If two packets arrive at the same time they are returned as a list:
    [Package1, Package2, ..., PackageN]
    """

    def __init__(self, file_name: str):
        sorted_packets = sorted(
            get_packets_from_file(file_name=file_name), key=lambda p: p.time
        )
        self.packets: List[List[Packet]] = [
            list(group) for _, group in groupby(sorted_packets, key=lambda p: p.time)
        ]

    def __bool__(self):
        return len(self.packets) > 0

    def pop_first_packets(self) -> List[Packet]:
        if not self.packets:
            raise ValueError("No packets to retrieve from file")
        return self.packets.pop(0)

    def pop_packets_from(self, interval: TimeInterval) -> List[Packet]:
        filtered_packets = []
        for packets in list(self.packets):
            if packets[0].time in interval:
                filtered_packets.extend(packets)
                self.packets.remove(packets)
        logging.debug(f"[ReceiveQueue] received packets: {filtered_packets}")
        return filtered_packets

    def get_copy_of_packets(self) -> List[Packet]:
        return list([item for sublist in self.packets for item in sublist])


@dataclass(order=True)
class PrioritizedItem:
    estimated_time: Time
    packet: Packet = field(compare=False)


class RouterQueue:
    def __init__(self):
        self.queue = PriorityQueue[PrioritizedItem]()

    def add(self, estimated_finish_time: Time, item: Packet):
        logging.debug(
            f"[RouterQueue] add packet: {item.id} with estimated finish time: {estimated_finish_time.time}"
        )
        self.queue.put(PrioritizedItem(estimated_finish_time, item))

    def get(self) -> Tuple[Time, Packet]:
        item = self.queue.get()
        return item.estimated_time, item.packet

    def __bool__(self) -> bool:
        return not self.queue.empty()


class SendQueue:
    def __init__(self):
        self.queue = list[Tuple[TimeInterval, Packet]]()

    def add(self, packet: Packet, interval: TimeInterval):
        logging.debug(f"[SendQueue]: packet {packet} sent from {interval}")
        self.queue.append((interval, packet))

    @property
    def package_order(self) -> List[int]:
        return [p.id for _, p in self.queue]

    @property
    def time_order(self) -> List[TimeInterval]:
        return [t for t, _ in self.queue]

    @property
    def packages(self) -> List[Tuple[TimeInterval, Packet]]:
        return list(self.queue)

    def __len__(self):
        return len(self.queue)
