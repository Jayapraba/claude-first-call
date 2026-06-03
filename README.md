AI Promo Eligibility Checker
A configuration-driven AI tool that uses Claude to analyze customer promo records against business rules and determine eligibility.
What It Does

Reads promo rules from a config file — no code changes needed when rules change
Reads customer records from a CSV file
Sends each record to Claude API with the current rules
Returns structured JSON output with eligibility decision and reason

Why I Built This
At Comcast I built PromoShield — a rule-based reconciliation platform that prevented $2M in annual revenue leakage across 10 million subscribers. This project reimagines that work using AI. Instead of writing and maintaining complex rule logic in code, Claude reasons against configuration-driven rules and explains its decisions in plain English.
Sample Output
Account ID: ACC001 | Eligible: True  | Reason: Amount is positive, status active, PROMO10 within limit
Account ID: ACC002 | Eligible: False | Reason: Amount must be positive (currently -50)
Account ID: ACC003 | Eligible: True  | Reason: Expired status allowed, amount within PROMO10 limit
Account ID: ACC004 | Eligible: False | Reason: PROMO30 not recognized in current rules
Account ID: ACC005 | Eligible: False | Reason: PROMO20 is for new customers only
How To Run
1. Clone the repo
bashgit clone https://github.com/yourusername/ai-journey
cd claude-first-call
2. Install dependencies
bashpip3 install anthropic python-dotenv
3. Add your API key
bash# Create .env file
echo "ANTHROPIC_API_KEY=your-key-here" > .env
4. Run
bashpython3 promo_checker.py \
  --config config.json \
  --records records.csv
Configuration
Edit config.json to change business rules — no code changes needed:
json{
    "rules": [
        "Amount must be positive",
        "Status must be active or expired only",
        "PROMO10 maximum discount is $100",
        "PROMO20 is for new customers only"
    ]
}
Key Design Decisions
Configuration driven — business rules live in config.json. When rules change, only the config changes. No engineer needed.
System prompt enforces JSON — Claude always returns structured output. No prose. No parsing errors.
Defensive JSON parsing — strips markdown code fences from Claude responses before parsing.
Safe config loading — uses .get() with defaults so missing keys don't crash the program.
Tech Stack

Python 3
Anthropic Claude API (claude-haiku-4-5)
python-dotenv for secrets management

What I Learned

How to inject dynamic business rules into Claude prompts at runtime
How system prompts enforce consistent output format
How to handle Claude API responses defensively
Configuration driven design applied to AI workflows

Author
Jaya — Senior Data Engineer transitioning to AI Enablement
15 years building data platforms at enterprise scale
