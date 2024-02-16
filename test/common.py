from abc import ABC, abstractmethod
from typing import List

from src.algorithm import WeightedFairQueuing, FairQueuing
from src.packets import TimeInterval
from src.queues import ReceiveQueue
from src.streams_configuration import StreamConfiguration

TEST_FILES_PATH = "./data/"


class CommonFairQueuingT(ABC):
    @abstractmethod
    def file_name(self) -> str:
        pass

    @abstractmethod
    def expected_wfq(self) -> List[int]:
        pass

    @abstractmethod
    def expected_times_wfq(self) -> List[TimeInterval]:
        pass

    @abstractmethod
    def expected_fq(self) -> List[int] | None:
        pass

    @abstractmethod
    def expected_times_fq(self) -> List[TimeInterval] | None:
        pass

    @abstractmethod
    def configuration(self) -> StreamConfiguration:
        pass

    @property
    def recv_queue(self) -> ReceiveQueue:
        full_filename = f"{TEST_FILES_PATH}{self.file_name()}"
        return ReceiveQueue(file_name=full_filename)

    def test_weighted_fair_queuing(self):
        algorithm = WeightedFairQueuing(config=self.configuration())
        send_queue = algorithm.execute(recv_queue=self.recv_queue)
        print(send_queue.package_order)
        print(send_queue.time_order)
        assert send_queue.package_order == self.expected_wfq()
        assert send_queue.time_order == self.expected_times_wfq()

    def test_fair_queueing(self):
        algorithm = FairQueuing()
        send_queue = algorithm.execute(recv_queue=self.recv_queue)
        if fair_queuing_packages := self.expected_fq():
            assert send_queue.package_order == fair_queuing_packages
        if fair_queuing_times := self.expected_times_fq():
            assert send_queue.time_order == fair_queuing_times
