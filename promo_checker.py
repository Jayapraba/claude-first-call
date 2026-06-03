import json
import os
import csv
import argparse
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent / "claude-first-call" / ".env"

def get_client():
    load_dotenv(ENV_PATH)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("Missing ANTHROPIC_API_KEY. Add it to .env or export it first.")

    return Anthropic(api_key=api_key)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to config.json")
    parser.add_argument("--records", required=True, help="Path to records.csv")
    parser.add_argument(
        "--model",
        default=os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5"),
        help="Claude model to use",
    )
    args = parser.parse_args()

    # Load rules from config.json
    with open(args.config, "r") as f:
        config = json.load(f)
        rules = config.get("rules", [])

    # System prompt - JSON output only
    system_prompt = """You are a promo eligibility checker. Analyze the customer record against the provided rules.
Return ONLY valid JSON with the following structure:
{
    "eligible": true/false,
    "reason": "brief explanation"
}"""

    client = get_client()

    with open(args.records, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Build user prompt with rules + row
            user_prompt = f"""Rules:
{json.dumps(rules, indent=2)}

Customer Record:
{json.dumps(row, indent=2)}

Is this customer eligible based on the rules?"""

            # Call Claude
            message = client.messages.create(
                model=args.model,
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            # Parse response — strip markdown code fences if present
            raw = message.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()
            try:
                result = json.loads(raw)
                print(f"Account ID: {row.get('account_id', 'N/A')} | Eligible: {result['eligible']} | Reason: {result['reason']}")
            except json.JSONDecodeError:
                print(f"Account ID: {row.get('account_id', 'N/A')} | Raw response: {raw!r}")


if __name__ == "__main__":
    main()
