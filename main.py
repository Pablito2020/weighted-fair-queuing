from argparse import ArgumentParser, RawTextHelpFormatter
from typing import Tuple

from packets import Interface
from streams_configuration import get_configuration_from, StreamConfiguration


def parse_args() -> Tuple[StreamConfiguration, Interface]:
    parser = ArgumentParser(prog="Weighted Fair Queueing",
                            description="Program that implements the packet-based network scheduling algorithm: Weighted Fair Queueing.",
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument('file', type=str,
                        help='File path name containing the list of triplets to be scheduled where each one represents:\n'
                             '   1. Arrival time (float)\n'
                             '   2. Packet length (float)\n'
                             '   3. Stream identifier (int)')
    parser.add_argument('streams', type=str,
                        help='Percentage of bandwidth assigned to each stream, comma separated. Ex: 50,10,40')
    args = parser.parse_args()
    config = get_configuration_from(args.streams)
    return config, Interface(file_name=args.file)


if __name__ == "__main__":
    try:
        configuration, interface = parse_args()
        for packets in interface:
            print(packets)
    except Exception as e:
        print(f"Something went wrong. Please check the error message below:\n{e}")
