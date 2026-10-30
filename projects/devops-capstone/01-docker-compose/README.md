# Project 1 - Containerize an app (Docker + Docker Compose)

**Goal:** run a 3-tier stack (Nginx -> Flask API -> PostgreSQL) with one command.

```
browser -> nginx :8080 -> app :8000 -> db :5432 (volume pgdata)
```

## What this shows
- A production-style `Dockerfile` (slim base image, non-root user, healthcheck, gunicorn)
- Docker Compose with service dependencies (`depends_on` + healthcheck)
- Persistent data with a named volume
- Reverse proxy with Nginx; `/metrics` is blocked from the outside
- Configuration through environment variables, secrets kept out of Git

## Run it
```powershell
cd projects\devops-capstone\01-docker-compose
Copy-Item .env.example .env        # then edit the password
docker compose up --build -d
docker compose ps
```

## Try it
```powershell
curl.exe http://localhost:8080/health
curl.exe -X POST http://localhost:8080/items -H "Content-Type: application/json" -d "{\"name\":\"laptop\"}"
curl.exe http://localhost:8080/items
curl.exe -i http://localhost:8080/metrics     # 403 - blocked by nginx
```

## Prove the data is persistent
```powershell
docker compose down          # containers removed, volume stays
docker compose up -d
curl.exe http://localhost:8080/items     # your item is still there
```

## Clean up
```powershell
docker compose down -v       # -v also deletes the database volume
```

## Interview questions this prepares you for
- Image vs container? Why a non-root user? Why a slim base image?
- What does `depends_on: condition: service_healthy` solve?
- Where does the data live when a container is deleted?
