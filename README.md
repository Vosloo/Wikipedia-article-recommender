<center><h1>Wikipedia article recommender system</h1></center>

<h2>About</h2>

This project is a proof of concept for a recommender system that uses Wikipedia articles as a data source. The articles are scraped from Wikipedia random articles page and stored as a parquet file (As it is only a proof of concept, the amount of articles is limited to a few thousand).

<h2>Overview</h2>

The program consists of mainly four components:
 1. Scraper: Scrapes Wikipedia random articles page and stores the articles in a parquet file (requests are sent with respect to Wikipedia rules so that the requests are not blocked by Wikipedia).
 2. Purifier: General cleaning of the articles - extracting text from paragraphs and removing unnecessary information.
 3. Normalizer: Normalizes the text of the articles including lemmatization and stopword removal.
 4. Recommender: Recommends articles based on the input txt file containing the user's query (can be either titles or links to Wikipedia articles).

<h2>Sample input</h2>

Sample input is a text file containing the user's query. The input file can contain either titles or links to Wikipedia articles. If a title contains spaces, it is changed to underscores. Sample input file can have a form of:

    White House
    Barack Obama
    https://en.wikipedia.org/wiki/Donald_Trump
    USA
    Conference on Innovative Data Systems Research

After creating such file, one need to provide the path to the file in the command line.

<h2>How to run the program</h2>

To run the program one needs to simply call the main script with desired options. Currently available options are:
 1. <b>"-s" / "--scrape" NO_ARTCLES</b>: Number of articles to scrape from Wikipedia (it includes parsing of the articles).
 2. <b>"--refresh"</b>: Force the scraper to scrape the articles from Wikipedia again. (The default option is to load the scraped articles from the parquet file if exists).
 3. <b>"--reparse"</b>: Reparses the scraped articles. (Useful for debugging purposes when Purifier / Normalizer changes its logic).
 4. <b>"-r" / "--recommend" INPUT_FILE</b>: Path to the input file containing the user's query mentioned in section <b>Sample input</b>.
 5. <b>"-nr" / "--no-recommendations" NUMBER</b>: Number of recommendations to be returned.
 6. <b>"--data-dir" DATA_DIR</b>: Path to the data directory that all output files will be stored and loaded from, as well as containing headers.json file necessary for the scraper. (The default option is to use the data directory present in the project root directory).

Example use:
 1. Run scraper for 1000 articles:

        python src/main.py -s 1000
 
 2. Run recommendation for the input file with 10 recommendations:

        python src/main.py -r input.txt -nr 10

All switches can be combined in any order.