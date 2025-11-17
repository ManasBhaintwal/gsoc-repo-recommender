import requests

GOOGLE_ORG_LIST = "https://summerofcode.withgoogle.com/api/archive/programs/{year}/organizations/"


def fetch_yearly_orgs(year: int):
    url = GOOGLE_ORG_LIST.format(year=year)
    print(f"Fetching org list for year {year}: {url}")

    res = requests.get(url)
    if res.status_code != 200:
        print(f"FAILED: {url}")
        return []

    data = res.json()

    result = []

    for org in data:
        result.append({
            "slug": org.get("slug"),
            "name": org.get("name"),
            "tagline": org.get("tagline"),
            "logo_url": org.get("logo_url"),
            "website_url": org.get("website_url"),
            "tech_tags": org.get("tech_tags", []),
            "topic_tags": org.get("topic_tags", []),
            "categories": org.get("categories", []),
            "description_html": org.get("description_html"),
            "ideas_list_url": org.get("ideas_list_url"),
            "contact_links": org.get("contact_links", []),
            "program_slug": org.get("program_slug"),  # year stored as string
            "year": year,
        })

    return result
