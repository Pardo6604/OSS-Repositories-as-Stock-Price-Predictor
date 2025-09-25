import requests
from collections import Counter
from datetime import datetime, timezone
import pandas as pd

# =====================
# CONFIG
# =====================
GITHUB_TOKEN = ""
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}
BASE_URL = "https://api.github.com"


def get_json(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()


def collect_lightweight_org_stats(orgs):
    results = []

    for org in orgs:

        print(f"\nAnalyzing {org} ...")

        # --- Organization metadata ---
        org_data = get_json(f"{BASE_URL}/orgs/{org}")
        public_repos = org_data.get("public_repos", 0)
        followers = org_data.get("followers", 0)
        following = org_data.get("following", 0)

        # --- First page of repos (max 100) ---
        repos = get_json(f"{BASE_URL}/orgs/{org}/repos", params={"per_page": 100})
        repo_count = len(repos)

        total_stars = sum(r.get("stargazers_count", 0) for r in repos)
        total_forks = sum(r.get("forks_count", 0) for r in repos)
        total_issues = sum(r.get("open_issues_count", 0) for r in repos)

        avg_stars = total_stars / repo_count if repo_count else 0
        avg_forks = total_forks / repo_count if repo_count else 0
        avg_issues = total_issues / repo_count if repo_count else 0

        # top repos
        top_repo_stars = max(repos, key=lambda r: r.get("stargazers_count", 0), default=None)
        top_repo_forks = max(repos, key=lambda r: r.get("forks_count", 0), default=None)

        # language distribution
        lang_counter = Counter(r.get("language") for r in repos if r.get("language"))
        top_language, top_lang_count = lang_counter.most_common(1)[0] if lang_counter else (None, 0)

        # repo ages
        repo_ages = []
        for r in repos:
            created = datetime.fromisoformat(r["created_at"].replace("Z", "+00:00"))
            age_days = (datetime.now(timezone.utc) - created).days
            repo_ages.append(age_days)
        avg_age_days = sum(repo_ages) / len(repo_ages) if repo_ages else 0

        org_stats = {
            "organization": org,
            "public_repos_total": public_repos,
            "sampled_repos_count": repo_count,
            "followers": followers,
            "following": following,
            "total_stars": total_stars,
            "total_forks": total_forks,
            "total_open_issues": total_issues,
            "avg_stars_per_repo": round(avg_stars, 2),
            "avg_forks_per_repo": round(avg_forks, 2),
            "avg_issues_per_repo": round(avg_issues, 2),
            "top_repo_by_stars": top_repo_stars["name"] if top_repo_stars else None,
            "top_repo_stars": top_repo_stars["stargazers_count"] if top_repo_stars else None,
            "top_repo_by_forks": top_repo_forks["name"] if top_repo_forks else None,
            "top_repo_forks": top_repo_forks["forks_count"] if top_repo_forks else None,
            "top_language": top_language,
            "top_language_repo_count": top_lang_count,
            "avg_repo_age_days": round(avg_age_days, 1),
        }

        results.append(org_stats)

    return results


# =====================
# Example usage
# =====================
if __name__ == "__main__":

    org_list = [
    "microsoft",
    "google",
    "aws",
    "apple",
    "facebook",
    "netflix",
    "spotify",
    "adobe",
    "salesforce",
    "oracle",
    "intel",
    "NVIDIA",
    "amd",
    "cisco",
    "qualcomm",
    "paypal",
    "shopify",
    "atlassian",
    "twilio",
    "okta",
    "datadog",
    "crowdstrike",
    "palantir",
    "cloudflare",
    "akamai",
    "fastly",
    "mongodb",
    "elastic",
    "confluentinc",
    "gitlab",
    "jfrog",
    "couchbase",
    "box",
    "dropbox",
    "uber",
    "lyft",
    "airbnb",
    "intuit",
    "workday",
    "broadcom",
    "unity-technologies",
    "roblox",
    "electronicarts",
    "robinhoodmarkets",
    "zillow",
    "ServiceNow",
    "Snowflake-Labs",
    "ringcentral",
    ]
    
    ticker_list = [
    "MSFT",
    "GOOGL",
    "AMZN",
    "AAPL",
    "META",
    "NFLX",
    "SPOT",
    "ADBE",
    "CRM",
    "ORCL",
    "INTC",
    "NVDA",
    "AMD",
    "CSCO",
    "QCOM",
    "PYPL",
    "SHOP",
    "TEAM",
    "TWLO",
    "OKTA",
    "DDOG",
    "CRWD",
    "PLTR",
    "NET",
    "AKAM",
    "FSLY",
    "MDB",
    "ESTC",
    "CFLT",
    "GTLB",
    "FROG",
    "BASE",
    "BOX",
    "DBX",
    "UBER",
    "LYFT",
    "ABNB",
    "INTU",
    "WDAY",
    "AVGO",
    "U",
    "RBLX",
    "EA",
    "HOOD",
    "Z",
    "NOW",
    "SNOW",
    "RNG",
    ]

    
    stats = collect_lightweight_org_stats(org_list)
    stats = pd.DataFrame(stats)

    stats.insert(0, "ticker", ticker_list)

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(stats)
    df.to_csv("github_org_stats.csv", index=False)

    print("Stats exported to github_org_stats.csv")

