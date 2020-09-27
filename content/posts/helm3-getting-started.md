---
title: "Helm3 Getting Started"
date: 2020-09-15T11:30:48+02:00
draft: true
---

# helm version 3

installation is quiet easy as it can be found in most repositories for me I used

```bash
sudo pacman -S helm
helm version
```

### initialize the stable repo
to my understanding the helm organization wants to get away from the stable repo being considererd the main source, this is why they ship helm with no default repo enabled.
we can enable a repo like this:
```bash
loeken@0x00E ~ helm repo add stable https://kubernetes-charts.storage.googleapis.com/
"stable" has been added to your repositories
loeken@0x00E ~ helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "stable" chart repository
Update Complete. ⎈Happy Helming!⎈
```

and then we update:
```bash
loeken@0x00E ~ helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "stable" chart repository
Update Complete. ⎈Happy Helming!⎈
```