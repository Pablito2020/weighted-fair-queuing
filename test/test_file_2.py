from typing import List

from src.packets import TimeInterval, StreamIdentifier, Priority, Time
from src.streams_configuration import StreamConfiguration
from test.common import CommonFairQueuingT


class TestFile2(CommonFairQueuingT):
    def file_name(self) -> str:
        return "file2.txt"

    def configuration(self) -> StreamConfiguration:
        return StreamConfiguration(
            {
                StreamIdentifier(1): Priority(10),
                StreamIdentifier(2): Priority(40),
                StreamIdentifier(3): Priority(40),
                StreamIdentifier(4): Priority(10),
            },
        )

    def expected_wfq(self) -> List[int]:
        return [2, 4, 5, 11, 3, 12, 10, 15, 8, 13, 9, 14, 7, 1, 16, 6]

    def expected_times_wfq(self) -> List[TimeInterval]:
        return [TimeInterval(begin=Time(time=0.0), end=Time(time=60.0)),
                TimeInterval(begin=Time(time=60.0), end=Time(time=110.0)),
                TimeInterval(begin=Time(time=110.0), end=Time(time=185.0)),
                TimeInterval(begin=Time(time=185.0), end=Time(time=210.0)),
                TimeInterval(begin=Time(time=210.0), end=Time(time=305.0)),
                TimeInterval(begin=Time(time=305.0), end=Time(time=365.0)),
                TimeInterval(begin=Time(time=365.0), end=Time(time=430.0)),
                TimeInterval(begin=Time(time=430.0), end=Time(time=500.0)),
                TimeInterval(begin=Time(time=500.0), end=Time(time=545.0)),
                TimeInterval(begin=Time(time=545.0), end=Time(time=585.0)),
                TimeInterval(begin=Time(time=585.0), end=Time(time=640.0)),
                TimeInterval(begin=Time(time=640.0), end=Time(time=690.0)),
                TimeInterval(begin=Time(time=690.0), end=Time(time=770.0)),
                TimeInterval(begin=Time(time=770.0), end=Time(time=870.0)),
                TimeInterval(begin=Time(time=870.0), end=Time(time=945.0)),
                TimeInterval(begin=Time(time=945.0), end=Time(time=1045.0))]

    def expected_fq(self) -> List[int] | None:
        return None

    def expected_times_fq(self) -> List[TimeInterval] | None:
        return None
