# 🐘 Odoo + PostgreSQL Docker Development Environment

A minimal, secure, and extensible Docker setup for developing custom Odoo modules.

---

## 🧱 Project Structure

```text
project_repo/
├── docker-compose.yml
├── .env.example
├── README.md
├── LICENSE
├── init-db.sh           # PostgreSQL bootstrap script
├── extra-addons/        # Your custom Odoo apps go here
│   └── .gitkeep
````

---

## 🚀 Quick Start

1. **Clone the repo**

```bash
git clone https://github.com/abdi-bb/project_repo
cd project_repo
```

2. **Set up your environment**

```bash
cp .env.example .env
# Edit .env if needed
```

3. **Start the stack**

```bash
docker compose up --build
```

First run will initialize:

* A PostgreSQL user `test_usr`
* A database `project_db`
* An empty `extra-addons/` directory

---

## 🔧 Working with Addons

* Create a new addon:

```bash
docker compose run --rm odoo_app odoo scaffold my_module /mnt/extra-addons
```

* Fix local permissions:

```bash
sudo chown -R $USER:$USER extra-addons/
```

---

## 🧹 Clean Everything

```bash
docker compose down -v
```

---

## 💡 Tips

* Odoo Web: [http://localhost:8069](http://localhost:8069)
* PostgreSQL: `localhost:5444`
* View logs: `docker compose logs -f`
* Check DB health: `docker compose ps`
