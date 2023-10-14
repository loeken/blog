---
title: "Kubernetes Create Images in Google Container Registry"
date: 2020-06-12T09:50:23+02:00
draft: false
toc: false
description: 
author: loeken
images:
tags:
  - untagged
---

## create a user and a project 
we ll be using the command line tool 
```
pacaur -S google-cloud-sdk
```

create a GCP service account; format of account is email address
```
SA_EMAIL=$(gcloud iam service-accounts --format='value(email)' create k8s-gcr-auth-ro)
```

create the json key file and associate it with the service account and save it in k8s-gcr-auth-ro.json
```
gcloud iam service-accounts keys create k8s-gcr-auth-ro.json --iam-account=$SA_EMAIL
```
get the project id
```
PROJECT=$(gcloud config list core/project --format='value(core.project)')
```

add the IAM policy binding for the defined project and service account
```
gcloud projects add-iam-policy-binding $PROJECT --member serviceAccount:$SA_EMAIL --role roles/storage.objectViewer
```

and now we ct create a secret which we ll use  to store the user login json info in.
```
SECRETNAME=gcr-json-key

kubectl create secret docker-registry $SECRETNAME \
  --docker-server=https://gcr.io \
  --docker-username=_json_key \
  --docker-email=user@example.com \
  --docker-password="$(cat k8s-gcr-auth-ro.json)"
``` 

now we grab an example project ( for service static files using alpine nginx )
```
cd ~/Projects
git clone https://github.com/loeken/k3s-nginx
cd k3s-nginx 
```

let's get building an image called blog. the Dockerfile in this example repo will copy all other files from the folder ( in this case a index.html exists )
```
docker build -t blog .
docker run -p 80:80 blog
```

tag image and push to registry
```
docker tag blog gcr.io/$PROJECT/blog
docker push gcr.io/$PROJECT/blog
```


and last we can add additional parameters to tell the pod to use these credentials
#### **`example_pod.yaml`**
```
---
apiVersion: v1
kind: Pod
metadata:
  name: <pod_name>
spec:
  containers:
    - name: <container_name>
      image: gcr.io/<registry_name>/<image_name>:<tagname>
  imagePullSecrets:
      - name: your_secret_name
```
