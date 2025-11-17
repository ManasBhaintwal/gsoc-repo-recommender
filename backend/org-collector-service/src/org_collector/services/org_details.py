import requests

ORG_DETAILS_URL = (
    "https://summerofcode.withgoogle.com/api/archive/programs/{year}/organizations/{slug}/"
)


def fetch_org_details(year: int, slug: str):
    """
    Fetch full details for an organization + list of projects for that specific year.

    Returns:
    {
        "org": {...},
        "projects": [ {...}, {...} ]
    }
    """
    url = ORG_DETAILS_URL.format(year=year, slug=slug)
    print(f"[ORG DETAILS] Fetching: {url}")

    res = requests.get(url)
    if res.status_code != 200:
        print(f"[ORG DETAILS] FAILED: {url}")
        return None

    data = res.json()

    # Extract full org data
    org_info = {
        "slug": data.get("slug"),
        "name": data.get("name"),
        "logo_url": data.get("logo_url"),
        "website_url": data.get("website_url"),
        "tagline": data.get("tagline"),
        "contact_links": data.get("contact_links", []),
        "date_created": data.get("date_created"),
        "tech_tags": data.get("tech_tags", []),
        "topic_tags": data.get("topic_tags", []),
        "categories": data.get("categories", []),
        "description_html": data.get("description_html"),
        "ideas_list_url": data.get("ideas_list_url"),
        "logo_bg_color": data.get("logo_bg_color"),
        "program_slug": data.get("program_slug"),
        "year": year,
    }

    # Extract project list
    project_list = []
    raw_projects = data.get("projects", [])

    for p in raw_projects:
        project_list.append({
            "project_id": p.get("id"),
            "title": p.get("title"),
            "project_code_url": p.get("project_code_url"),
            "date_created": p.get("date_created"),
            "tech_tags": p.get("tech_tags", []),
            "topic_tags": p.get("topic_tags", []),
            "status": p.get("status"),
            "organization_slug": p.get("organization_slug"),
            "organization_name": p.get("organization_name"),
            "mentor_names": p.get("mentor_names", []),
            "contributor_display_name": p.get("contributor_display_name"),
            "abstract_short": p.get("abstract_short"),
            "abstract_html": p.get("abstract_html"),
            "date_archived": p.get("date_archived"),
            "year": year,
        })

    return {
        "org": org_info,
        "projects": project_list
    }
