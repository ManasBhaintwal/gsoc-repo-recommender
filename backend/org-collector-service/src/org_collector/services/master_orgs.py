import requests

MASTER_ORG_URL = "https://www.gsocorganizations.dev/page-data/index/page-data.json"


def fetch_master_orgs():
    print("Fetching master org list...")

    res = requests.get(MASTER_ORG_URL)
    res.raise_for_status()

    data = res.json()

    edges = data["result"]["data"]["allOrganization"]["edges"]

    master_orgs = []

    for edge in edges:
        node = edge["node"]

        # extract years participated
        years_dict = node.get("years", {})
        years = []
        for key, val in years_dict.items():
            # keys like _2016, _2018
            y = int(key.replace("_", ""))

            # if value is null OR object → means participated
            if val is None or isinstance(val, dict):
                years.append(y)

        master_orgs.append({
            "org_slug": node.get("name").lower().replace(" ", "-"),  # fallback slug
            "name": node.get("name"),
            "category": node.get("category"),
            "description": node.get("description"),
            "technologies": node.get("technologies", []),
            "topics": node.get("topics", []),
            "image_url": node.get("image_url"),
            "image_background_color": node.get("image_background_color"),
            "website_url": node.get("url"),
            "years_participated": years
        })

    return master_orgs
