import logging
from argparse import ArgumentParser, RawTextHelpFormatter
from typing import Tuple

from src.algorithm import FairScheduler, WeightedFairQueuing, FairQueuing
from src.logging import configure_logging
from src.queues import ReceiveQueue
from src.streams_configuration import get_configuration_from


def parse_algorithm(args) -> FairScheduler:
    match args.algorithm:
        case "wfq":
            if args.streams is None:
                raise ValueError(
                    "You must provide the streams configuration for the Weighted Fair Queueing algorithm"
                )
            config = get_configuration_from(args.streams)
            return WeightedFairQueuing(config)
        case "fq":
            return FairQueuing()
        case _:
            raise ValueError(f"Invalid algorithm: {args.algorithm}")


def parse_args() -> Tuple[FairScheduler, str]:
    parser = ArgumentParser(
        prog="Weighted Fair Queueing",
        description="Program that implements the packet-based network scheduling algorithm: Weighted Fair Queueing.",
        formatter_class=RawTextHelpFormatter,
    )
    parser.add_argument(
        "file",
        type=str,
        help="File path name containing the list of triplets to be scheduled where each one represents:\n"
        "   1. Arrival time (float)\n"
        "   2. Packet length (float)\n"
        "   3. Stream identifier (int)",
    )
    parser.add_argument(
        "streams",
        type=str,
        nargs="?",
        default=None,
        help="Percentage of bandwidth assigned to each stream, comma separated. Ex: 50,10,40",
    )
    parser.add_argument(
        "-log",
        "--loglevel",
        default="info",
        help="Provide logging level. Example --loglevel debug",
    )
    parser.add_argument(
        "-a",
        "--algorithm",
        default="wfq",
        help="Provide the algorithm to be used. Example --algorithm wfq or --algorithm fq",
    )
    args = parser.parse_args()
    configure_logging(args.loglevel.upper())
    alg = parse_algorithm(args)
    return alg, args.file


if __name__ == "__main__":
    try:
        algorithm, file_name = parse_args()
        receive_queue = ReceiveQueue(file_name)
        send_queue = algorithm.execute(receive_queue)
        logging.info(send_queue.package_order)
    except Exception as e:
        logging.error(
            f"Something went wrong. Please check the error message below:\n{e}"
        )
