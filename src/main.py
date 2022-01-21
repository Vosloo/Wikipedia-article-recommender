from math import ceil
from pathlib import Path
from argparse import ArgumentParser

from controller import Controller

import config as cfg


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="English Wikipedia article recommender.")

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="Text file containing titles and url's of prevously read wiki articles. (one entry per line)",
    )
    parser.add_argument(
        "-n",
        "--no-articles",
        type=int,
        help="Number of articles to scrape from english wikipedia. (default 1000)",
    )
    parser.add_argument(
        "-d",
        "--load-data",
        type=str,
        help="Apache parquet containing parsed and normalized articles",
    )
    parser.add_argument(
        "-r",
        "--load-responses",
        type=str,
        help="Apache parquet file containing raw article documents",
    )
    parser.add_argument(
        "-q",
        "--no-recommendations",
        type=int,
        help="Number of articles recommended based on user article history (default 5)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        choices=["silent", "info", "debug"],
        help="Prints debug information.",
        default="info",
    )

    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        raise FileNotFoundError("Input path invalid, file not found")

    data_path = Path(args.load_data).resolve() if args.load_data else None
    responses_path = (
        Path(args.load_responses).resolve() if args.load_responses else None
    )

    if args.no_articles:
        cfg.NO_BATCHES = ceil(args.no_articles / cfg.BATCH_SIZE)
    elif not (data_path or responses_path):
        raise Exception(
            "Missing dataset configuration. Either pass --no-articles, --load-data or --load-response."
        )

    if args.no_recommendations:
        cfg.NO_RECOMMENDATIONS = args.no_recommendations

    controller = Controller(input_path, data_path, responses_path)
    controller.run()
