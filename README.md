# ShopLite — Flask E-commerce Capstone

A simple, clean e-commerce web app built for an **Azure DevOps CI/CD capstone**.
Stack: **Flask + SQLAlchemy + Bootstrap 5 + Vanilla JS**, SQLite locally / Azure SQL in QA & Prod.

---

## Features

**Customer:** Home, product listing, product details, cart (session-based), login-required checkout, order confirmation, register/login.
**Admin:** Dashboard, product CRUD, view orders + order details.

---

## Project structure

```
capstone/
├── app/
│   ├── __init__.py        # app factory + admin seeding
│   ├── config.py          # env-driven config
│   ├── extensions.py      # db, login, csrf, migrate
│   ├── models.py          # User, Product, Order, OrderItem
│   ├── forms.py           # WTForms
│   ├── routes/            # main, auth, shop, admin blueprints
│   ├── templates/         # Jinja templates (base, partials, shop, auth, admin)
│   └── static/            # CSS, JS
├── scripts/
│   ├── seed_products.py   # sample product seed
│   └── schema.sql         # T-SQL for Azure SQL (reference)
├── requirements.txt
├── run.py                 # local entrypoint
├── startup.txt            # gunicorn command for App Service
├── azure-pipelines.yml    # CI/CD: Build → QA → Prod (with approval)
├── .env.example
└── README.md
```

---

## Local development (Windows / PowerShell)

```powershell
# 1. Activate venv
.\.venv\Scripts\Activate.ps1

# 2. (First time) copy env file
Copy-Item .env.example .env

# 3. Run the app — DB and admin user are auto-created
python run.py

# 4. (Optional) seed sample products
python -m scripts.seed_products
```

Open <http://localhost:5000>.

**Default admin (seeded on first run):**
- Email: `admin@shop.local`
- Password: `changeme`

> Change `ADMIN_EMAIL` / `ADMIN_PASSWORD` in `.env` (or in App Service settings) before deploying.

---

## Environment variables

| Name | Purpose | Example |
|------|---------|---------|
| `SECRET_KEY` | Flask session/CSRF secret | a long random string |
| `DATABASE_URL` | SQLAlchemy URL. Empty → local SQLite | `mssql+pyodbc://user:pwd@server.database.windows.net:1433/db?driver=ODBC+Driver+18+for+SQL+Server` |
| `ADMIN_EMAIL` | Seed admin email | `admin@shop.local` |
| `ADMIN_PASSWORD` | Seed admin password | `StrongPass!` |

---

## Azure deployment

**1. Create resources**
- Azure SQL Database (one for QA, one for Prod — same server is fine)
- Azure App Service (Linux, Python 3.11) — one for QA, one for Prod

**2. App Service > Configuration > Application settings**
- `SECRET_KEY`, `DATABASE_URL`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`
- `SCM_DO_BUILD_DURING_DEPLOYMENT = true`

**3. App Service > Configuration > General settings > Startup Command:**
```
gunicorn --bind=0.0.0.0 --timeout 600 run:app
```

**4. Azure SQL firewall** — allow Azure services + your dev IP.

---

## CI/CD pipeline

`azure-pipelines.yml` includes three stages:

1. **Build** — install deps, run tests, package as zip artifact
2. **Deploy to QA** — deploys to QA App Service automatically
3. **Deploy to Production** — runs only after **manual approval** on the `Production` environment

### Setup steps in Azure DevOps

1. Create a service connection to your Azure subscription; put its name in `azureSubscription`.
2. Set `qaAppName` and `prodAppName` to your App Service names.
3. In **Pipelines → Environments**, create `QA` and `Production`.
4. On `Production` → Approvals & checks → add a manual approver.
5. Push to `main` → pipeline runs Build → QA → wait for approval → Prod.

---

## Tech stack & libraries

- Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF, WTForms, email-validator
- Werkzeug (password hashing), python-dotenv
- pyodbc (Azure SQL), gunicorn (production server)
- Optional: Flask-Migrate, pytest, pytest-flask
- Frontend: Bootstrap 5 + Bootstrap Icons (CDN), vanilla JS
