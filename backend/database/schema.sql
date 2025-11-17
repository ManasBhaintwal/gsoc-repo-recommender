CREATE TABLE orgs (
    org_slug TEXT PRIMARY KEY,       -- unique slug from website
    org_id TEXT,                     -- GSoC numeric ID
    name TEXT,
    category TEXT,
    tagline TEXT,
    image_url TEXT,
    bg_color TEXT,
    topics JSONB,
    tech_tags JSONB,
    years_participated JSONB,
    description TEXT
);

CREATE TABLE org_projects (
    project_id TEXT PRIMARY KEY,     -- GSoC project slug
    org_slug TEXT REFERENCES orgs(org_slug),

    year INT,
    title TEXT,
    tech_tags JSONB,
    topic_tags JSONB,
    status TEXT,
    contributor TEXT,
    mentors JSONB,
    abstract TEXT,
    project_url TEXT
);
