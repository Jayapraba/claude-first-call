"""Simple per-row Claude data-quality checker.

Run from this folder:
  python3 data_quality.py --csv ../data.csv
"""

import argparse
import csv
import os
import sys
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent / ".env"


def get_client():
    load_dotenv(ENV_PATH)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("Missing ANTHROPIC_API_KEY. Add it to .env or export it first.")

    return Anthropic(api_key=api_key)


def read_rows(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def format_row(row):
    return "\n".join(f"{column}: {value}" for column, value in row.items())


def check_row(client, row, model):
    prompt = f"""
Check this CSV row for data quality issues.

Row:
{format_row(row)}

Reply with:
- OK, if the row looks good
- A short list of issues, if there are problems
""".strip()

    response = client.messages.create(
        model=model,
        max_tokens=200,
        system="You are a data quality expert. Always respond in valid JSON format only. Format: {has_anomaly: true/false, issues: [], severity: high/medium/low/none}",
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    return raw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to the CSV file")
    parser.add_argument(
        "--model",
        default=os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5"),
        help="Claude model to use",
    )
    args = parser.parse_args()

    client = get_client()
    rows = read_rows(args.csv)

    for row_number, row in enumerate(rows, start=1):
        try:
            result = check_row(client, row, args.model)
        except Exception as error:
            result = f"API error: {error}"

        print(f"Row {row_number}: {result}")


if __name__ == "__main__":
    main()
