from abc import ABC, abstractmethod

from src.packets import Time, Packet, TimeInterval
from src.queues import SendQueue, RouterQueue, ReceiveQueue
from src.streams_configuration import StreamConfiguration


class FairScheduler(ABC):
    """
    Common interface for fair scheduling algorithms
    You must implement the estimated_time_func method, which will be used to calculate the estimated time for each
    packet
    """

    def execute(self, recv_queue: ReceiveQueue, initial_time=Time(0.0)) -> SendQueue:
        router_queue, send_queue = RouterQueue(), SendQueue()
        current_time = initial_time
        while recv_queue or router_queue:
            if not router_queue:
                for packet in recv_queue.pop_first_packets():
                    router_queue.add(
                        self.estimated_time_func(initial_time, packet), packet
                    )
            f_prima, packet = router_queue.get()
            finish_time = current_time + packet.time_to_send()
            time_elapsed = TimeInterval(begin=current_time, end=finish_time)
            send_queue.add(packet, time_elapsed)
            for packet in recv_queue.pop_packets_from(time_elapsed):
                router_queue.add(self.estimated_time_func(f_prima, packet), packet)
            current_time = finish_time
        return send_queue

    @abstractmethod
    def estimated_time_func(self, f_prima: Time, packet: Packet) -> Time:
        pass


class FairQueuing(FairScheduler):
    def estimated_time_func(self, f_prima: Time, packet: Packet) -> Time:
        return Time(max(f_prima.time, packet.time.time) + packet.size.size)


class WeightedFairQueuing(FairScheduler):
    def __init__(self, config: StreamConfiguration):
        self.config = config

    def execute(self, recv_queue: ReceiveQueue, initial_time=Time(0.0)) -> SendQueue:
        self.assert_correct_stream_ids(recv_queue)
        return super().execute(recv_queue, initial_time)

    def assert_correct_stream_ids(self, recv_queue: ReceiveQueue):
        stream_ids = set([p.stream_id for p in recv_queue.get_copy_of_packets()])
        if stream_ids != self.config.ids:
            raise ValueError(
                f"Stream ids in configuration and packets must be the same ({stream_ids} != {self.config.ids})"
            )

    def estimated_time_func(self, f_prima: Time, packet: Packet) -> Time:
        pondered_size = self.config.apply_weight_to(packet).size
        return Time(max(f_prima.time, packet.time.time) + pondered_size)
