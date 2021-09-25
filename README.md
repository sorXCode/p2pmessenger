# P2PMESSENGER

P2PMessenger is an asycnchronous and real-time messaging system. It also has an inbuilt support for user registeration and authentication.

## TECHNOLOGY STACK

- Python/Django
- DjangoRestFramework
- Channels
- PostgreSQL
- Redis

## RUNNING PROJECT (Docker compose)

- Run `docker compose build` to build the images for the project
- Run `docker compose up` to start the project; the api endpoint can be accessed at `http://127.0.0.1:8080` .

- To shutdown the project, run `docker compose down`

## DEPLOYING (K8S)

All deployment script (yaml) are in the `k8s/` folder. You can either apply them manually `kubectl apply -f ...`
or use the `deploy.sh` helper script.

### To use the helper script

```bash
chmod +x ./deploy.sh
./deploy.sh
```

### Notes

The deployment will create 3 `(cache, db, web)` pods on the k8s cluster.

- The `web` cluster will have 3 replicasets of the backend service and 1 service with LoadBalancing capability. The service will expose port 8080 of the backend service over port 80.
- Both cache and db pods will have one replicaset and a clusterIP service of respective container.

## ENDPOINT DOCUMENTATION

Endpoints are documented in [POSTMAN and can be viewed here](https://documenter.getpostman.com/view/11647149/UUxxg8Tr)
