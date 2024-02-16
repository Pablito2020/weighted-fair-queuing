from dataclasses import dataclass
from typing import Set

from src.packets import StreamIdentifier, Priority, Packet, PacketSize


@dataclass
class StreamConfiguration:
    streams: dict[StreamIdentifier, Priority]

    def __post_init__(self):
        if not sum(self.streams.values(), Priority.minimum()) == Priority.maximum():
            raise ValueError(f"Sum of priorities must be 100")

    def apply_weight_to(self, packet: Packet) -> PacketSize:
        if packet.stream_id not in self.streams:
            raise ValueError(f"Stream {packet.stream_id} not found in configuration")
        return PacketSize(self.streams[packet.stream_id].percentage * packet.size.size)

    @property
    def ids(self) -> Set[StreamIdentifier]:
        return set(self.streams.keys())


def get_configuration_from(percentages_str: str) -> StreamConfiguration:
    try:
        percentages_primitives = [int(p) for p in percentages_str.split(",")]
    except ValueError:
        raise ValueError(f"Invalid percentage values: {percentages_str}")
    percentages = [Priority(p) for p in percentages_primitives]
    stream_ids = StreamIdentifier.generate(len(percentages))
    return StreamConfiguration(
        {stream: priority for stream, priority in zip(stream_ids, percentages)}
    )
