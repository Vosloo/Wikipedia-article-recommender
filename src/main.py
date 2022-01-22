from math import ceil
from pathlib import Path
import argparse
from argparse import ArgumentParser

from controller import Controller

import config as cfg


def check_dir(value):
    path = Path(value).resolve()
    if not path.is_dir():
        raise argparse.ArgumentTypeError(f"{path} is not a valid directory")
    return path


def check_file(value):
    path = Path(value).resolve()
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"{path} is not a valid file")
    return path


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    return ivalue


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="English Wikipedia article recommender.")

    parser.add_argument(
        "-s",
        "--scrape",
        metavar="NO_ARTICLES",
        required=False,
        type=check_positive,
        help=(
            "Scrapes desired number of wiki articles to create initial DB"
            + " (loads from file if exists unless --refresh is specified)"
        ),
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        required=False,
        default=False,
        help="Refreshes DB and scrapes new articles (only applicable if --scrape is specified)",
    )
    parser.add_argument(
        "--reparse",
        action="store_true",
        required=False,
        default=False,
        help="Reparses scraped articles",
    )
    parser.add_argument(
        "-r",
        "--recommend",
        metavar="INPUT_FILE",
        required=False,
        type=check_file,
        help="Runs recommendation on given file containing wiki articles urls or titles",
    )
    parser.add_argument(
        "-nr",
        "--no-recommendations",
        required=False,
        type=check_positive,
        help="Number of recommended articles (default 5)",
    )
    parser.add_argument(
        "--data-dir",
        required=False,
        type=check_dir,
        help=f"Path to data directory containing headers and all outputs (default: {cfg.DATA_PATH})",
    )

    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    if args.no_recommendations is not None:
        cfg.NO_RECOMMENDATIONS = args.no_recommendations

    if args.data_dir is not None:
        cfg.DATA_PATH = args.data_dir

        # Update all paths relative to data directory
        cfg.HEADERS_PATH = cfg.DATA_PATH / cfg.HEADERS_PATH.name
        cfg.WIKI_PARSED_PARQUET_PATH = cfg.DATA_PATH / cfg.WIKI_PARSED_PARQUET_PATH.name
        cfg.WIKI_RESPONSES_PARQUET_PATH = (
            cfg.DATA_PATH / cfg.WIKI_RESPONSES_PARQUET_PATH.name
        )
        cfg.WIKI_RECOMMENDATIONS_CSV_PATH = (
            cfg.DATA_PATH / cfg.WIKI_RECOMMENDATIONS_CSV_PATH.name
        )

    controller = Controller(args.scrape, args.refresh, args.reparse, args.recommend)
    controller.run()
