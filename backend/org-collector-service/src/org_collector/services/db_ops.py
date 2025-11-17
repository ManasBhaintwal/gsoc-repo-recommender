# backend/org-collector-service/src/org_collector/services/db_ops.py
from datetime import datetime
from database.connect import get_conn
import psycopg
from psycopg.rows import dict_row
import json

def upsert_org(org: dict):
    """
    org dict should contain keys:
      org_slug, org_id, name, category, tagline,
      description, description_html, technologies, tech_tags,
      topics, topic_tags, website_url, gsoc_url, ideas_list_url,
      logo_url, logo_bg_color, contact_links (list/dict), year (int),
      years_participated (list of ints) optional
    This function inserts or updates and merges years_participated.
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # ensure contact_links is json string
            contact_json = json.dumps(org.get("contact_links")) if org.get("contact_links") is not None else None

            # build years to add (single year or list)
            years_to_add = org.get("years_participated") or ([org.get("year")] if org.get("year") else [])
            if isinstance(years_to_add, int):
                years_to_add = [years_to_add]

            cur.execute(
                """
                INSERT INTO orgs
                (org_slug, org_id, name, category, tagline, description, description_html,
                 technologies, tech_tags, topics, topic_tags, website_url, gsoc_url, ideas_list_url,
                 logo_url, logo_bg_color, contact_links, years_participated, created_at, updated_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())
                ON CONFLICT (org_slug) DO UPDATE SET
                  org_id = COALESCE(EXCLUDED.org_id, orgs.org_id),
                  name = COALESCE(EXCLUDED.name, orgs.name),
                  category = COALESCE(EXCLUDED.category, orgs.category),
                  tagline = COALESCE(EXCLUDED.tagline, orgs.tagline),
                  description = COALESCE(EXCLUDED.description, orgs.description),
                  description_html = COALESCE(EXCLUDED.description_html, orgs.description_html),
                  technologies = COALESCE(EXCLUDED.technologies, orgs.technologies),
                  tech_tags = COALESCE(EXCLUDED.tech_tags, orgs.tech_tags),
                  topics = COALESCE(EXCLUDED.topics, orgs.topics),
                  topic_tags = COALESCE(EXCLUDED.topic_tags, orgs.topic_tags),
                  website_url = COALESCE(EXCLUDED.website_url, orgs.website_url),
                  gsoc_url = COALESCE(EXCLUDED.gsoc_url, orgs.gsoc_url),
                  ideas_list_url = COALESCE(EXCLUDED.ideas_list_url, orgs.ideas_list_url),
                  logo_url = COALESCE(EXCLUDED.logo_url, orgs.logo_url),
                  logo_bg_color = COALESCE(EXCLUDED.logo_bg_color, orgs.logo_bg_color),
                  contact_links = COALESCE(EXCLUDED.contact_links, orgs.contact_links),
                  years_participated = (
                      SELECT array_agg(DISTINCT y ORDER BY y)
                      FROM unnest(coalesce(orgs.years_participated, ARRAY[]::int[]) || EXCLUDED.years_participated) AS y
                  ),
                  updated_at = NOW();
                """,
                (
                    org.get("org_slug"),
                    org.get("org_id"),
                    org.get("name"),
                    org.get("category"),
                    org.get("tagline"),
                    org.get("description"),
                    org.get("description_html"),
                    org.get("technologies"),
                    org.get("tech_tags"),
                    org.get("topics"),
                    org.get("topic_tags"),
                    org.get("website_url"),
                    org.get("gsoc_url") or org.get("url"),
                    org.get("ideas_list_url"),
                    org.get("logo_url"),
                    org.get("logo_bg_color"),
                    contact_json,
                    years_to_add
                )
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()


def upsert_project(project: dict):
    """
    project dict keys:
     project_id, project_slug, org_slug, organization_name, year,
     title, short_abstract, long_abstract_html, mentor_names,
     contributor_display_name, tech_tags, topic_tags,
     project_code_url, project_url, status, date_created, date_archived
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO org_projects
                (project_id, project_slug, org_slug, organization_name, year, title,
                 short_abstract, long_abstract_html, mentor_names, contributor_display_name,
                 tech_tags, topic_tags, project_code_url, project_url, status, date_created, date_archived, created_at, updated_at)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())
                ON CONFLICT (project_id) DO UPDATE SET
                  project_slug = COALESCE(EXCLUDED.project_slug, org_projects.project_slug),
                  org_slug = COALESCE(EXCLUDED.org_slug, org_projects.org_slug),
                  organization_name = COALESCE(EXCLUDED.organization_name, org_projects.organization_name),
                  year = COALESCE(EXCLUDED.year, org_projects.year),
                  title = COALESCE(EXCLUDED.title, org_projects.title),
                  short_abstract = COALESCE(EXCLUDED.short_abstract, org_projects.short_abstract),
                  long_abstract_html = COALESCE(EXCLUDED.long_abstract_html, org_projects.long_abstract_html),
                  mentor_names = COALESCE(EXCLUDED.mentor_names, org_projects.mentor_names),
                  contributor_display_name = COALESCE(EXCLUDED.contributor_display_name, org_projects.contributor_display_name),
                  tech_tags = COALESCE(EXCLUDED.tech_tags, org_projects.tech_tags),
                  topic_tags = COALESCE(EXCLUDED.topic_tags, org_projects.topic_tags),
                  project_code_url = COALESCE(EXCLUDED.project_code_url, org_projects.project_code_url),
                  project_url = COALESCE(EXCLUDED.project_url, org_projects.project_url),
                  status = COALESCE(EXCLUDED.status, org_projects.status),
                  date_created = COALESCE(EXCLUDED.date_created, org_projects.date_created),
                  date_archived = COALESCE(EXCLUDED.date_archived, org_projects.date_archived),
                  updated_at = NOW();
                """,
                (
                    project.get("project_id"),
                    project.get("project_slug"),
                    project.get("org_slug"),
                    project.get("organization_name"),
                    project.get("year"),
                    project.get("title"),
                    project.get("short_abstract"),
                    project.get("long_abstract_html"),
                    project.get("mentor_names"),
                    project.get("contributor_display_name"),
                    project.get("tech_tags"),
                    project.get("topic_tags"),
                    project.get("project_code_url"),
                    project.get("project_url"),
                    project.get("status"),
                    project.get("date_created"),
                    project.get("date_archived")
                )
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()