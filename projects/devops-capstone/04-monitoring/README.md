# Project 4 - Monitoring and alerting (Prometheus + Grafana)

**Goal:** see what the app is doing (traffic, latency, errors) and get alerts.

```
app :8000 /metrics  <-- scraped every 5s --  Prometheus :9090  <-- queried by --  Grafana :3000
                                                   |
                                             alerts.yml (rules)
```

## What this shows
- The app exposes metrics itself (`/metrics`, the `prometheus_client` library)
- A counter (`http_requests_total`) and a histogram (`http_request_duration_seconds`)
- Prometheus scrape config and **alert rules** (AppDown, HighErrorRate, HighLatency)
- Grafana **provisioned from files**: data source and dashboard come up ready,
  no clicking, and everything is in Git (monitoring as code)

## Run it
```powershell
cd projects\devops-capstone\04-monitoring
docker compose up --build -d
```
| Tool | URL | Login |
|---|---|---|
| App | http://localhost:8000/health | - |
| Prometheus | http://localhost:9090 (Alerts tab shows the rules) | - |
| Grafana | http://localhost:3000, dashboard **Capstone App** | admin / admin |

## Generate traffic and watch the dashboard
```powershell
1..300 | ForEach-Object { curl.exe -s http://localhost:8000/items | Out-Null }
1..50  | ForEach-Object { curl.exe -s http://localhost:8000/does-not-exist | Out-Null }
```

## Trigger an alert
```powershell
docker compose stop app
```
After about 30 seconds the alert **AppDown** turns Pending, then Firing, in Prometheus
(http://localhost:9090/alerts). Start it again with `docker compose start app`.

## Useful PromQL to try in the Prometheus UI
```
sum by (endpoint) (rate(http_requests_total[1m]))
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))
up
```

## Clean up
```powershell
docker compose down
```

## Interview questions this prepares you for
- Metrics vs logs vs traces? Pull (Prometheus) vs push model?
- Counter vs gauge vs histogram? Why `rate()` on a counter?
- The "four golden signals": latency, traffic, errors, saturation
- What is an SLO and how would an alert relate to it?

## Next improvement (try it yourself)
Add Alertmanager and send the alert to email or Slack.
