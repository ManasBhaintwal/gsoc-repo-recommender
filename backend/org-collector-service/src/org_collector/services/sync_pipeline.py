# backend/org-collector-service/src/org_collector/services/sync_pipeline.py
import time
import traceback
from org_collector.services.master_orgs import fetch_master_orgs
from org_collector.services.yearly_orgs import fetch_yearly_orgs
from org_collector.services.org_details import fetch_org_details
from org_collector.services.db_ops import upsert_org, upsert_project
from org_collector.services.sync_status import update_sync_status

# parameters you can tweak
YEARS = list(range(2016, 2024 + 1))
SLEEP_BETWEEN_REQUESTS = 0.2  # seconds -- be polite
SLEEP_BETWEEN_ORGS = 0.1

def sync_master_then_yearly_then_projects(
    do_master=True,
    do_yearly=True,
    do_projects=True
):
    """
    Enhanced sync pipeline with toggleable stages:
      do_master  -> fetch and upsert master orgs (gsocorganizations.dev)
      do_yearly  -> fetch yearly Google org list (slug, tagline, tech, etc.)
      do_projects -> fetch detailed projects for each org-year
    """

    print("STEP 4: Starting sync pipeline")
    print(f"Modes => master: {do_master}, yearly: {do_yearly}, projects: {do_projects}")

    # ------------------------------
    # 1) MASTER ORGS
    # ------------------------------
    if do_master:
        print("\n=== MASTER ORGS SYNC ===")
        try:
            master = fetch_master_orgs()
            print(f"Master orgs loaded: {len(master)}")
        except Exception:
            print("Failed loading master org list.")
            traceback.print_exc()
            master = []

        for m in master:
            try:
                upsert_org({
                    "org_slug": m.get("org_slug"),
                    "name": m.get("name"),
                    "category": m.get("category"),
                    "description": m.get("description"),
                    "technologies": m.get("technologies"),
                    "topics": m.get("topics"),
                    "website_url": m.get("website_url"),
                    "logo_url": m.get("image_url"),
                    "logo_bg_color": m.get("image_background_color"),
                    "years_participated": m.get("years_participated", [])
                })
            except Exception:
                print(f"Failed upsert master org: {m.get('name')}")
                traceback.print_exc()

            time.sleep(SLEEP_BETWEEN_REQUESTS)

    # ------------------------------
    # 2) YEARLY ORGS
    # ------------------------------
    if do_yearly:
        print("\n=== YEARLY ORG SYNC ===")

        for year in YEARS:
            print(f"\n--- Processing year {year} ---")

            try:
                yearly = fetch_yearly_orgs(year)
            except Exception:
                print(f"Failed fetching yearly list for {year}")
                traceback.print_exc()
                yearly = []

            # ------------------------------
            # For each org in that year
            # ------------------------------
            for g in yearly:
                slug = g.get("slug")

                # YEARLY UPSERT
                try:
                    upsert_org({
                        "org_slug": slug,
                        "org_id": None,
                        "name": g.get("name"),
                        "tagline": g.get("tagline"),
                        "description_html": g.get("description_html"),
                        "tech_tags": g.get("tech_tags"),
                        "topic_tags": g.get("topic_tags"),
                        "website_url": g.get("website_url"),
                        "ideas_list_url": g.get("ideas_list_url"),
                        "logo_url": g.get("logo_url"),
                        "years_participated": [year]
                    })
                except Exception:
                    print(f"Failed upsert yearly org: {slug}")
                    traceback.print_exc()

                time.sleep(SLEEP_BETWEEN_REQUESTS)

                # ------------------------------
                # 3) PROJECT DETAILS
                # ------------------------------
                if do_projects:
                    try:
                        details = fetch_org_details(year, slug)
                        if not details:
                            continue

                        org_info = details.get("org", {})
                        projects = details.get("projects", [])

                        # Upsert enriched org details
                        try:
                            upsert_org({
                                "org_slug": org_info.get("slug") or slug,
                                "org_id": None,
                                "name": org_info.get("name"),
                                "tagline": org_info.get("tagline"),
                                "description_html": org_info.get("description_html"),
                                "tech_tags": org_info.get("tech_tags"),
                                "topic_tags": org_info.get("topic_tags"),
                                "website_url": org_info.get("website_url"),
                                "ideas_list_url": org_info.get("ideas_list_url"),
                                "logo_url": org_info.get("logo_url"),
                                "contact_links": org_info.get("contact_links"),
                                "years_participated": [year]
                            })
                        except Exception:
                            print(f"Failed upsert org(details): {slug}")
                            traceback.print_exc()

                        # Insert all projects
                        for p in projects:
                            try:
                                upsert_project({
                                    "project_id": p.get("project_id"),
                                    "project_slug": p.get("project_id"),
                                    "org_slug": p.get("organization_slug") or slug,
                                    "organization_name": p.get("organization_name"),
                                    "year": p.get("year") or year,
                                    "title": p.get("title"),
                                    "short_abstract": p.get("abstract_short"),
                                    "long_abstract_html": p.get("abstract_html"),
                                    "mentor_names": p.get("mentor_names"),
                                    "contributor_display_name": p.get("contributor_display_name"),
                                    "tech_tags": p.get("tech_tags"),
                                    "topic_tags": p.get("topic_tags"),
                                    "project_code_url": p.get("project_code_url"),
                                    "project_url": None,
                                    "status": p.get("status"),
                                    "date_created": p.get("date_created"),
                                    "date_archived": p.get("date_archived")
                                })
                            except Exception:
                                print(f"Failed upsert project: {p.get('project_id')}")
                                traceback.print_exc()

                            time.sleep(SLEEP_BETWEEN_REQUESTS)

                    except Exception:
                        print(f"Failed fetch details for {slug} year {year}")
                        traceback.print_exc()

                time.sleep(SLEEP_BETWEEN_ORGS)

    print("\nSTEP 4: Sync pipeline finished")
    update_sync_status("org_sync")