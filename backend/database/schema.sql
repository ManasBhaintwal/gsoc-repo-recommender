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



-- user-profile-service 

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    github_username TEXT,
    languages TEXT[],             -- e.g. ['python','js']
    experience_level TEXT,        -- e.g. 'junior'|'mid'|'senior'
    interests TEXT[],             -- e.g. ['ml','backend']
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- optional index for quick lookup by github_username
CREATE INDEX IF NOT EXISTS idx_users_github_username ON users (github_username);
