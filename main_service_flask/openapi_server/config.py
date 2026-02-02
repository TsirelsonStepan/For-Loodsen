from openapi_server.database.tables import CandidateDB, candidate_skills, InternshipDB, internship_skills

CORS_ORIGINS = [
    "*"
]

VALID_EMPLOYMENT_TYPES = ['в офисе', 'удалённо', 'гибрид']

SPECIAL_CASE_SKILLS = {
    "sql": "SQL",
    "javascript": "JavaScript",
    "html": "HTML",
    "css": "CSS",
    "http": "HTTP",
    "https": "HTTPS",
    "api": "API",
    "rest": "REST",
    "graphql": "GraphQL",
    "json": "JSON",
    "xml": "XML",
    "jwt": "JWT",
    "jwt auth": "JWT Auth",
    "tcp": "TCP",
    "udp": "UDP",
    "ip": "IP",
    "dns": "DNS",
    "cd": "CD",
    "ci": "CI",
    "ci/cd": "CI/CD",
    "devops": "DevOps",
    "oop": "OOP",
    "mvc": "MVC",
    "sqlalchemy": "SQLAlchemy",
    "ai": "AI",
    "ml": "ML",
    "cv": "CV",
    "nlp": "NLP",
    "gpu": "GPU",
    "cpu": "CPU",
    "ux": "UX",
    "ui": "UI",
    "jwt": "JWT",
    "orm": "ORM",
    "sdk": "SDK",
    "ide": "IDE",
    "vim": "VIM",
    "ssh": "SSH",
    "nginx": "NGINX",
    "aws": "AWS",
    "gcp": "GCP",
    "unix": "Unix",
    "git": "Git",
    "github": "GitHub",
    "gitlab": "GitLab",
    "sql server": "SQL Server",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "nosql": "NoSQL"
}


def normalize_skill_name(name: str) -> str:
    name = name.strip()
    key = name.lower()
    return SPECIAL_CASE_SKILLS.get(key, name.title())

"""Конфигурация для сортировки по моделям."""
MODEL_CONFIG = {
    "CandidateDB": {
        "model": CandidateDB,
        "skills_table": candidate_skills,
        "uuid_column": candidate_skills.c.candidate_uuid,
    },
    "InternshipDB": {
        "model": InternshipDB,
        "skills_table": internship_skills,
        "uuid_column": internship_skills.c.internship_uuid,
    },
}

CAMEL_TO_SNAKE = {
    "hoursPerWeek": "hours_per_week",
    "employmentType": "employment_type",
}