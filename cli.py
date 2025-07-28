# cli.py

import argparse
from papers.fetcher import fetch_pubmed_ids, fetch_pubmed_details, parse_and_filter, save_to_csv


def main():
    parser = argparse.ArgumentParser(description="PubMed Paper Fetcher")
    parser.add_argument("query", help="PubMed query string")
    parser.add_argument("-o", "--output", default="results.csv", help="Output CSV filename")
    parser.add_argument("-m", "--max", type=int, default=10, help="Max number of results")
    args = parser.parse_args()

    ids = fetch_pubmed_ids(args.query, max_results=args.max)
    xml_data = fetch_pubmed_details(ids)
    results = parse_and_filter(xml_data)

    if results:
        save_to_csv(results, filename=args.output)
        print(f"Saved {len(results)} papers to {args.output}")
    else:
        print("No papers found with non-academic pharma/biotech authors.")


if __name__ == "__main__":
    main()
