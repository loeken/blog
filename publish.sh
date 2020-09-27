#!/bin/bash
hugo -D
gcloud container images delete gcr.io/internetzme/blog --quiet

docker build -t blog .
docker tag blog gcr.io/internetzme/blog
docker push gcr.io/internetzme/blog

kubectl rollout restart deployment blog
