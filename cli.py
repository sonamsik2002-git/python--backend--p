import argparse
from papers.fetcher import fetch_papers, save_as_csv


def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with company affiliation.")
    parser.add_argument("query", help="Query string for PubMed search")
    parser.add_argument("-o", "--file", help="Output CSV filename")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")

    args = parser.parse_args()

    papers = fetch_papers(args.query, debug=args.debug)

    if args.file:
        save_as_csv(papers, args.file)
        print(f"Results saved to {args.file}")
    else:
        for paper in papers:
            print(paper)


if __name__ == "__main__":
    main()
