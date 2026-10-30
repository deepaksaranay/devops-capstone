# Project 3 - Run it on Kubernetes

**Goal:** deploy the same app on a local Kubernetes cluster with self-healing,
health checks and autoscaling.

```
Ingress (capstone.local) -> Service app -> 2+ app Pods -> Service postgres -> Postgres Pod + PVC
                                  ^
                        HorizontalPodAutoscaler (2..5 pods at 70% CPU)
```

## Files
| File | What it creates |
|---|---|
| `namespace.yaml` | Namespace `capstone` |
| `postgres.yaml` | PersistentVolumeClaim, Deployment and Service for the database |
| `app.yaml` | Deployment (2 replicas, probes, resources) and Service |
| `hpa.yaml` | Autoscaler |
| `ingress.yaml` | HTTP route for `capstone.local` |
| `kustomization.yaml` | Applies everything together |

The database password is **not** stored in these files. You create the Secret yourself.

## Prerequisites
Docker Desktop, [kind](https://kind.sigs.k8s.io/) and `kubectl`:
```powershell
winget install Kubernetes.kind
winget install Kubernetes.kubectl
```

## Run it
```powershell
cd projects\devops-capstone\03-kubernetes

# 1. cluster + image
kind create cluster --name capstone
docker build -t devops-capstone:local ..\app
kind load docker-image devops-capstone:local --name capstone

# 2. namespace and secret (the password never goes into Git)
kubectl apply -f namespace.yaml
kubectl create secret generic postgres-credentials -n capstone `
  --from-literal=POSTGRES_USER=app `
  --from-literal=POSTGRES_PASSWORD=change-me

# 3. everything else
kubectl apply -k .
kubectl get pods -n capstone -w
```

## Try it
```powershell
kubectl port-forward -n capstone svc/app 8080:80
# in another window:
curl.exe http://localhost:8080/health
curl.exe -X POST http://localhost:8080/items -H "Content-Type: application/json" -d "{\"name\":\"laptop\"}"
```

## Experiments (this is where the learning happens)
```powershell
# Self-healing: delete a pod, watch Kubernetes replace it
kubectl get pods -n capstone
kubectl delete pod -n capstone <one-app-pod-name>
kubectl get pods -n capstone     # a new pod is already starting

# Scale by hand
kubectl scale deployment app -n capstone --replicas=4

# Rolling update: change something in app.yaml, then
kubectl apply -k .
kubectl rollout status deployment/app -n capstone
kubectl rollout undo deployment/app -n capstone      # rollback

# Debug
kubectl describe pod -n capstone <pod-name>
kubectl logs -n capstone deploy/app
```

The HPA needs the metrics-server add-on to read CPU. Without it `kubectl get hpa -n capstone`
shows `<unknown>`; that is expected on a fresh kind cluster.

## Clean up
```powershell
kind delete cluster --name capstone
```

## Interview questions this prepares you for
- Pod vs Deployment vs Service? Liveness vs readiness probe?
- Requests vs limits? What happens when a pod exceeds its memory limit?
- Why is the Secret created outside Git? Why `strategy: Recreate` for a single-replica database?
