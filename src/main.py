import argparse

from src.orchestrator import Orchestrator


def main() -> None:
    parser = argparse.ArgumentParser(description="Turn a CSV into a chart")
    parser.add_argument("csv_path", help="Path to the input CSV")
    parser.add_argument("-o", "--output", default="chart.png", help="Path to write the chart PNG")
    args = parser.parse_args()

    print(Orchestrator().run(args.csv_path, args.output))


if __name__ == "__main__":
    main()
