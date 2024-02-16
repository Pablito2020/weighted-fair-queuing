from typing import List

from src.packets import TimeInterval, Priority, StreamIdentifier, Time
from src.streams_configuration import StreamConfiguration
from test.common import CommonFairQueuingT


class TestFile1(CommonFairQueuingT):
    def file_name(self) -> str:
        return "file.txt"

    def expected_wfq(self) -> List[int]:
        return [2, 3, 4, 1, 5, 6, 8, 9, 7]

    def expected_times_wfq(self) -> List[TimeInterval]:
        return [
            TimeInterval(begin=Time(0.0), end=Time(1.0)),
            TimeInterval(begin=Time(1.0), end=Time(2.0)),
            TimeInterval(begin=Time(2.0), end=Time(3.0)),
            TimeInterval(begin=Time(3.0), end=Time(7.0)),
            TimeInterval(begin=Time(7.0), end=Time(9.0)),
            TimeInterval(begin=Time(9.0), end=Time(11.0)),
            TimeInterval(begin=Time(11.0), end=Time(12.0)),
            TimeInterval(begin=Time(12.0), end=Time(14.0)),
            TimeInterval(begin=Time(14.0), end=Time(18.0)),
        ]

    def expected_fq(self) -> List[int]:
        return self.expected_wfq()

    def expected_times_fq(self) -> List[TimeInterval]:
        return self.expected_times_wfq()

    def configuration(self) -> StreamConfiguration:
        return StreamConfiguration({StreamIdentifier(1): Priority(100)})
