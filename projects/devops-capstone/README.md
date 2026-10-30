# DevOps Capstone - one app, four industry-style projects

A small REST API (Flask + PostgreSQL) used as the workload to practice the skills
DevOps job descriptions ask for: containers, CI/CD, Kubernetes and monitoring.
Everything runs on your own laptop; **no cloud account is needed.**

```
          developer
              | git push
              v
   +------------------------+     image      +---------------------+
   | 02 CI/CD (GitHub       | -------------> | GitHub Container    |
   |    Actions)            |                | Registry (ghcr.io)  |
   | lint, test, scan, build|                +---------------------+
   +------------------------+                           |
                                                        v
   +--------------------------+      +--------------------------------+
   | 01 Docker Compose        |      | 03 Kubernetes (kind)           |
   | nginx -> app -> postgres |      | ingress -> app pods -> postgres|
   +--------------------------+      +--------------------------------+
                  |
                  v
   +-----------------------------------------+
   | 04 Monitoring: Prometheus + Grafana     |
   | metrics, dashboard, alert rules         |
   +-----------------------------------------+
```

## Order to follow
| # | Folder | Skill | Needs |
|---|---|---|---|
| 0 | `app/` | The application, tests, Dockerfile | Python (optional) |
| 1 | `01-docker-compose/` | Docker, Compose, Nginx, volumes | Docker Desktop |
| 2 | `02-ci-cd/` | GitHub Actions pipeline | GitHub repo |
| 3 | `03-kubernetes/` | Deployments, probes, HPA, Ingress | Docker Desktop, kind, kubectl |
| 4 | `04-monitoring/` | Prometheus, Grafana, alerting | Docker Desktop |

Read each folder's `README.md`, run it, break something on purpose, and fix it.

## The app
| Endpoint | Purpose |
|---|---|
| `GET /health` | Liveness: the process is alive |
| `GET /ready` | Readiness: the database is reachable |
| `GET /items`, `POST /items` | The business logic |
| `GET /metrics` | Prometheus metrics |

Run the tests without Docker:
```powershell
cd projects\devops-capstone\app
pip install -r requirements.txt -r requirements-dev.txt
python -m pytest -q
```

## Security habits used here
- The container runs as a non-root user
- Passwords come from environment variables / Kubernetes Secrets, never from Git
- `.env` and keys are in `.gitignore`
- Images are scanned in the pipeline
- `/metrics` is not exposed through the public proxy

## Resume bullets you can honestly use after finishing
- Containerized a Flask/PostgreSQL service with Docker and Docker Compose (Nginx reverse proxy, healthchecks, persistent volumes)
- Built a GitHub Actions CI/CD pipeline: lint, unit tests, Trivy image scan and publish to GHCR
- Deployed to Kubernetes with probes, resource limits, HPA and Ingress; managed secrets outside Git
- Added observability with Prometheus and Grafana (provisioned dashboards, alert rules for downtime, errors and latency)
