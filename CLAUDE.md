# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tech Stack

- **Django 5.2** (Python 3.11) — REST-style JSON API + Django Admin
- **PostgreSQL** (via `dj-database-url` + `psycopg2-binary`)
- **Gunicorn** behind **Nginx** reverse proxy
- **Whitenoise** for static files
- **Ruff** for linting and formatting
- Deployed to Heroku; Docker Compose for local development

## Development Commands

All development runs through Docker Compose. The `web` service mounts the repo at `/opt/apps`.

```bash
# Start services
docker compose up

# Apply migrations
make migrate

# Create new migrations
make makemigrations

# Lint / format
make lint-check       # check only
make lint-fix         # auto-fix lint issues
make format-check     # check only
make format-fix       # auto-fix formatting
make fix              # lint-fix + format-fix in one step

# i18n
make makemessages     # extract strings → apps/embassy/locale/
make compilemessages  # compile .po → .mo
```

Run any Django management command via the `web` service:
```bash
docker compose run --rm -u "$(id -u):$(id -g)" web python manage.py <command>
```

## Environment Variables

Required in `.env`:

| Variable | Purpose |
|---|---|
| `ENVIRONMENT` | `DEV` or `PROD` (required — raises on anything else) |
| `SECRET_KEY` | Django secret key |
| `DATABASE_URL` | PostgreSQL URL (parsed by `dj-database-url`) |
| `POSTGRES_USER/PASSWORD/DB`, `DB_PORT` | Used by docker-compose db service |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | Gmail SMTP credentials |
| `WEB_PORT`, `ADMIN_PORT`, `NGINX_PORT` | Container port mappings |

`ENVIRONMENT=DEV` sets `ALLOWED_HOSTS = ["*"]` and relaxed cookie/CORS settings. The app raises `ValueError` at startup if `ENVIRONMENT` is not exactly `DEV` or `PROD`.

## Project Structure & Architecture

```
apps/
├── settings.py          # Single settings file, env-driven
├── urls.py              # Root URL conf
├── core/
│   └── models/mixins.py # TimestampMixin, SoftDeleteMixin (shared base classes)
├── utils/
│   └── enum.py          # StrEnum base with get_choices() / get_values()
├── auth/                # Session-based auth JSON API
│   ├── auth_views.py    # register, login, logout, me endpoints
│   ├── decorators.py    # @login_required_json (returns 401 JSON instead of redirect)
│   └── urls.py          # /api/auth/…
├── hotel/               # Pet hotel domain
│   ├── models/
│   │   ├── partner.py   # Partner (company that owns hotels)
│   │   └── hotel.py     # Hotel (FK → Partner, city_code, region_code, rating)
│   ├── core/defs/
│   │   ├── city_codes.py    # CityCodes enum (MOSCOW, SAINT_PETERSBURG)
│   │   └── region_codes.py  # RegionCodes enum
│   └── urls.py          # /api/hotels
├── embassy/             # Citizen/university registry domain
│   ├── models/
│   │   ├── citizen.py          # Citizen with soft-delete, CitizenManager
│   │   ├── university.py       # University (city_code, region_code)
│   │   └── citizen_university.py # M2M through-table with enrollment/graduation dates
│   └── locale/es/       # Spanish translations (i18n enabled)
└── mail/                # Email sending via Django Admin
    ├── models/
    │   ├── mail_template.py  # MailTemplate (linked to ContentType + Groups)
    │   └── sent_email.py     # SentEmail audit log (SENT / FAILED)
    ├── admin/
    │   └── mail_template.py  # Custom admin view: /admin/mail/mailtemplate/send-email/
    └── forms/
        └── send_email_form.py  # SendEmailForm — recipients can be Citizens or Users
```

### Key architectural patterns

**Dual-service deployment**: `Dockerfile.web` (public API) and `Dockerfile.admin` (Django Admin) are separate containers behind Nginx. Both run the same Django app; Nginx routes traffic to the appropriate upstream.

**Session-based auth with CSRF**: The frontend must first `GET /api/auth/csrf-token/` to receive the CSRF cookie, then include it on mutating requests. Cross-origin cookie sharing is configured per-environment (Lax in DEV, None+Secure in PROD).

**Soft delete**: `SoftDeleteMixin` adds `is_deleted`; models using it implement `.soft_delete()`, `.hard_delete()`, and corresponding bulk variants. `CitizenManager.not_deleted()` is the canonical queryset for active records.

**`StrEnum` + `get_choices()`**: All choice fields use a custom `StrEnum` subclass (`apps/utils/enum.py`) that exposes `get_choices()` for Django field choices and `get_values()` for validation.

**`MailTemplate` is scoped by `ContentType` and `Group`**: A template targets either `Citizen` or `User` recipients (set via `content_type` FK) and is visible only to users in the matching `Group`. Non-superusers see only templates/recipients belonging to their groups.

**i18n**: The `embassy` app is internationalised (Spanish + English). String fields use `gettext_lazy`. Locale files live in `apps/embassy/locale/`. The `LocaleMiddleware` is active.

## Linting

Ruff is configured in `pyproject.toml`: line length 119, Python 3.11 target, migrations excluded. Rules: E, W, F, I (isort), UP (pyupgrade), DJ (flake8-django). `DJ001` (null on string fields) is suppressed intentionally.

Run via Docker (`make fix`) or locally if Ruff 0.9.10 is installed:
```bash
ruff check --fix . && ruff format .
```
