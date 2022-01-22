from math import ceil
from pathlib import Path
import argparse
from argparse import ArgumentParser

from controller import Controller

import config as cfg


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="English Wikipedia article recommender.")

    parser.add_argument(
        "-i",
        "--input",
        type=str,
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
        help="Apache parquet containing parsed and normalized articles. Takes precedent over --no-articles (unless in --scrape-only mode)",
    )
    parser.add_argument(
        "-r",
        "--load-responses",
        type=str,
        help="Apache parquet file containing raw article documents. Takes precedent over --load-data and --no-articles (unless in --scrape-only mode)",
    )
    parser.add_argument(
        "-q",
        "--no-recommendations",
        type=int,
        help="Number of articles recommended based on user article history (default 5)",
    )
    parser.add_argument(
        "--skip-recommendation",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Skipping recommendation. Scraping, normalizing and saving specified number of wikipedia articles (required --no-articles).",
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

    input_path = Path(args.input).resolve() if args.load_data else None
    data_path = Path(args.load_data).resolve() if args.load_data else None
    responses_path = (
        Path(args.load_responses).resolve() if args.load_responses else None
    )

    if args.skip_recommendation:
        if args.no_articles is None:
            raise Exception("Argument --no-articles required")
        cfg.NO_ARTICLES = args.no_articles
    else:
        if not input_path or not input_path.exists():
            raise FileNotFoundError("Input path invalid, file not found")

        if args.no_articles:
            cfg.NO_ARTICLES = args.no_articles
        elif data_path:
            if not data_path.exists():
                raise FileNotFoundError("Data path invalid, file not found")
        elif responses_path:
            if not responses_path.exists():
                raise FileNotFoundError("Responses path invalid, file not found")
        else:
            raise Exception(
                "Missing dataset configuration. Either pass --no-articles, --load-data or --load-response."
            )

        # Later check if number of recommendations exceeds number of articles in database
        if args.no_recommendations:
            cfg.NO_RECOMMENDATIONS = args.no_recommendations

    controller = Controller(
        input_path, data_path, responses_path, args.skip_recommendation
    )
    controller.run()
