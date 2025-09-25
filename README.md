# OSS-Repositories-as-Stock-Price-Predictor

**Can public GitHub repository activity help predict a software company's stock price?**

This project explores whether repository-level metrics (stars, forks, commit activity, issues, PRs, releases, etc.) can be used as features to predict a company's stock price or short-term returns.

---
## Quick start

1. Clone the repo:

```bash
git clone https://github.com/Pardo6604/OSS-Repositories-as-Stock-Price-Predictor.git
cd OSS-Repositories-as-Stock-Price-Predictor
```

2. Create a virtual environment (recommended) and install deps:

```bash
python -m venv .venv
source .venv/bin/activate   # mac / linux
.\.venv\Scripts\activate  # windows (powershell/cmd)

pip install -r requirements.txt
```
---

## Repository structure

```text
.
├── DataRetriever.py           # Fetches GitHub & stock price data
├── OrganizationFeatures.py    # Extracts repository features per organization
├── ML.py                      # Trains & evaluates predictive models
└── README.md                  # project documentation
```

---

## Contributing

PRs welcome.

---


