---
title: "Llama"
date: 2023-04-15T10:55:19+02:00
draft: false
---

## Table of contents
- [1. Introduction](#1-introduction)
  - [1.1. performance 4/8/16 bit](#11-performance-4816-bit)
  - [1.2. 4-bit Model Requirements for LLaMA](#12-4-bit-model-requirements-for-llama)
  - [1.3. 8-bit Model Requirements for LLaMA](#13-8-bit-model-requirements-for-llama)
  - [1.4 downloading the correct models](#14-downloading-the-correct-models)
- [2 text-generation-webui](#2-text-generation-webui)
  - [2.1 Ubuntu 22.04](#21-ubuntu-2204)
    - [2.1.0. youtube video](#210-youtube-video)
    - [2.1.1. update the drivers](#211-update-the-drivers)
    - [2.1.2. reboot](#212-reboot)
    - [2.1.3. install docker](#213-install-docker)
    - [2.1.4. docker \& container toolkit](#214-docker--container-toolkit)
    - [2.1.5. clone the repo](#215-clone-the-repo)
    - [2.1.6. prepare models](#216-prepare-models)
    - [2.1.7. prepare .env file](#217-prepare-env-file)
    - [2.1.8. startup docker container](#218-startup-docker-container)
  - [2.2. Manjaro](#22-manjaro)
    - [2.2.1 update the drivers](#221-update-the-drivers)
    - [2.2.2 reboot](#222-reboot)
    - [2.2.3 docker \& container toolkit](#223-docker--container-toolkit)
    - [2.2.4 continue with ubuntu task](#224-continue-with-ubuntu-task)
  - [2.3. Windows](#23-windows)
    - [2.3.0. youtube video](#230-youtube-video)
    - [2.3.1. choco package manager](#231-choco-package-manager)
    - [2.3.2. install drivers/dependencies](#232-install-driversdependencies)
    - [2.3.3. install wsl](#233-install-wsl)
    - [2.3.4. reboot](#234-reboot)
    - [2.3.5. git clone \&\& startup](#235-git-clone--startup)
    - [2.3.6. prepare models](#236-prepare-models)
    - [2.3.7. startup](#237-startup)


# 1. Introduction

## 1.1. performance 4/8/16 bit
![compared](/media/img/bitrate-compared.png)


## 1.2. 4-bit Model Requirements for LLaMA
Model | Model Size | Minimum Total VRAM | Card examples | RAM/Swap to Load
:------: | :------: | :------: | :------: | :------:
LLaMA-7B | 3.5GB | 6GB | RTX 1660, 2060, AMD 5700xt, RTX 3050, 3060 | 16 GB
LLaMA-13B | 6.5GB | 10GB | AMD 6900xt, RTX 2060 12GB, 3060 12GB, 3080, A2000 | 32 GB
LLaMA-30B | 15.8GB | 20GB | RTX 3080 20GB, A4500, A5000, 3090, 4090, 6000, Tesla V100| 64 GB
LLaMA-65B | 31.2GB | 40GB | A100 40GB, 2x3090, 2x4090, A40, RTX A6000, 8000, Titan Ada | 128 GB


## 1.3. 8-bit Model Requirements for LLaMA
Model | VRAM Used | Minimum Total VRAM | Card examples | RAM/Swap to Load
:------: | :------: | :------: | :------: | :------: 
LLaMA-7B | 9.2GB | 10GB | 3060 12GB, RTX 3080 10GB, RTX 3090 | 24 GB
LLaMA-13B | 16.3GB | 20GB | RTX 3090 Ti, RTX 4090 | 32GB
LLaMA-30B | 36GB | 40GB | A6000 48GB, A100 40GB | 64GB
LLaMA-65B | 74GB | 80GB | A100 80GB | 128GB

## 1.4 downloading the correct models
The original leaked weights won't work. You need the "HFv2" (HuggingFace version 2) converted model weights. 
You can get them by using this [torrent](https://files.catbox.moe/wbzpkx.torrent) or this [magnet link](magnet:?xt=urn:btih:dc73d45db45f540aeb6711bdc0eb3b35d939dcb4&dn=LLaMA-HFv2&tr=http%3a%2f%2fbt2.archive.org%3a6969%2fannounce&tr=http%3a%2f%2fbt1.archive.org%3a6969%2fannounce)

The **WRONG** original leaked weights have filenames that look like:

```
consolidated.00.pth
consolidated.01.pth
```

The **CORRECT** "HF Converted" weights have filenames that look like:
```
pytorch_model-00001-of-00033.bin
pytorch_model-00002-of-00033.bin
pytorch_model-00003-of-00033.bin
pytorch_model-00004-of-00033.bin
```

now place the folders into the subfolder
```
loeken@the-machine:~/Projects/text-generation-webui$ tree models/llama-7b-hf/
models/llama-7b-hf/
├── config.json
├── generation_config.json
├── model-00001-of-00002.safetensors
├── model-00002-of-00002.safetensors
├── model.safetensors.index.json
├── special_tokens_map.json
├── tokenizer_config.json
└── tokenizer.model
```

alternatively you can use huggingface ones:
https://huggingface.co/decapoda-research


# 2 text-generation-webui

https://github.com/oobabooga/text-generation-webui is a nice dashboard that allows you to load various models and make them output(genearte) and you can also use it to train models.


## 2.1 Ubuntu 22.04

### 2.1.0. youtube video
A video walking you through the setup can be found here:

[![oobabooga text-generation-webui setup in docker on ubuntu 22.04](https://img.youtube.com/vi/ELkKWYh8qOk/0.jpg)](https://www.youtube.com/watch?v=ELkKWYh8qOk)


### 2.1.1. update the drivers
in the the “software updater” update drivers to the last version of the prop driver.

### 2.1.2. reboot
to switch using to new driver

### 2.1.3. install docker
```bash
sudo apt update
sudo apt-get install curl
sudo mkdir -m 0755 -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-compose -y
sudo usermod -aG docker $USER
newgrp docker
```

### 2.1.4. docker & container toolkit
```bash
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://nvidia.github.io/libnvidia-container/stable/ubuntu22.04/amd64 /" | \
sudo tee /etc/apt/sources.list.d/nvidia.list > /dev/null 
sudo apt update
sudo apt install nvidia-docker2 nvidia-container-runtime -y
sudo systemctl restart docker
```

### 2.1.5. clone the repo
```
git clone https://github.com/oobabooga/text-generation-webui
cd text-generation-webui
```

### 2.1.6. prepare models
download and place the models inside the models folder. tested with:

4bit
https://github.com/oobabooga/text-generation-webui/pull/530#issuecomment-1483891617
https://github.com/oobabooga/text-generation-webui/pull/530#issuecomment-1483941105

8bit:
https://github.com/oobabooga/text-generation-webui/pull/530#issuecomment-1484235789

### 2.1.7. prepare .env file
edit .env values to your needs.
```bash
cp .env.example .env
nano .env
```

### 2.1.8. startup docker container
```bash
docker-compose up --build
```

## 2.2. Manjaro
manjaro/arch is similar to ubuntu just the dependency installation is more convenient

### 2.2.1 update the drivers
```bash
sudo mhwd -a pci nonfree 0300
```
### 2.2.2 reboot
```bash
reboot
```
### 2.2.3 docker & container toolkit
```bash
yay -S docker docker-compose buildkit gcc nvidia-docker
sudo usermod -aG docker $USER
newgrp docker
sudo systemctl restart docker # required by nvidia-container-runtime
```

### 2.2.4 continue with ubuntu task
continue at [5. clone the repo](#215-clone-the-repo)

## 2.3. Windows
### 2.3.0. youtube video
A video walking you through the setup can be found here:
[![oobabooga text-generation-webui setup in docker on windows 11](https://img.youtube.com/vi/ejH4w5b5kFQ/0.jpg)](https://www.youtube.com/watch?v=ejH4w5b5kFQ)

### 2.3.1. choco package manager
install package manager  (https://chocolatey.org/ )
```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

### 2.3.2. install drivers/dependencies
```
choco install nvidia-display-driver cuda git docker-desktop
```

### 2.3.3. install wsl
wsl --install

### 2.3.4. reboot
after reboot enter username/password in wsl

### 2.3.5. git clone && startup
clone the repo and edit .env values to your needs.
```
cd Desktop
git clone https://github.com/oobabooga/text-generation-webui
cd text-generation-webui
COPY .env.example .env
notepad .env
```

### 2.3.6. prepare models
download and place the models inside the models folder. tested with:

4bit https://github.com/oobabooga/text-generation-webui/pull/530#issuecomment-1483891617 https://github.com/oobabooga/text-generation-webui/pull/530#issuecomment-1483941105

8bit: https://github.com/oobabooga/text-generation-webui/pull/530#issuecomment-1484235789

### 2.3.7. startup
```
docker-compose up
```
