from dataclasses import dataclass

from packets import StreamIdentifier, Priority, Packet, PacketSize


@dataclass
class StreamConfiguration:
    streams: dict[StreamIdentifier, Priority]

    def __post_init__(self):
        if not sum(self.streams.values(), Priority.minimum()) == Priority.maximum():
            raise ValueError(f"Sum of priorities must be 100")

    def apply_weight_to(self, packet: Packet) -> PacketSize:
        if packet.id_ not in self.streams:
            raise ValueError(f"Stream {packet.id_} not found in configuration")
        return PacketSize(self.streams[packet.id_].percentage * packet.size.size)


def get_configuration_from(percentages_str: str) -> StreamConfiguration:
    try:
        percentages = [int(p) for p in percentages_str.split(",")]
    except ValueError:
        raise ValueError(f"Invalid percentage values: {percentages_str}")
    percentages = [Priority(p) for p in percentages]
    stream_ids = StreamIdentifier.generate(len(percentages))
    return StreamConfiguration({stream: priority for stream, priority in zip(stream_ids, percentages)})
