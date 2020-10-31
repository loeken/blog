---
title: "Golang - getting started"
date: 2020-10-31T12:15:57+01:00
draft: false
tags: go, programming
---

# Golang getting started

Go is an open source programming language that makes it easy to build simple, reliable, and efficient software.


## Introduction
From what I can see, over the last couple of years many frontend developers started to use frontend frameworks like vue or react. Javascript itself is definately the leader as the most commonl used language [popular technologies (stackoverflow survey)](https://insights.stackoverflow.com/survey/2020#most-popular-technologies). All these frameworks have one thing in common they pull most of their data from some json endpoints. Python, PHP, Ruby and other languages are often used to provide these data endpoints. 

I personally have used python and PHP to provide most the endpoints over the last couple of years - which worked fine for me as I personally do not have a lot of issues setting up my webservers/stack required to run these - but having worked with friends (mostly frontend developers ) on some small freelance projects - I noticed most people seem to have more issues with setting that up ( and maintaining it ).

At my workplace we started using golang on a project this year - the setup and maintance so far had far less issues compared to php/nodejs etc - and along with a few projects like kubernetes ( written in go ) made me start to dig more into it.

The first thing i looked at is how others felt about it by looking at the stackoverflow developers survey [dreaded languages](https://insights.stackoverflow.com/survey/2020#technology-most-loved-dreaded-and-wanted-languages-dreaded) - and [wanted languages](https://insights.stackoverflow.com/survey/2020#technology-most-loved-dreaded-and-wanted-languages-wanted) - first checklist passed - it is not really hated :) however the like is growing and it's wanted too.


## statically-typed

Go or Golang is a statically-typed language with syntax loosely derived from that of C, with extra features such as garbage collection (like Java), type safety, and some dynamic-typing capabilities. developed at Google in 2007 by a bunch of clever people, Robert Griesemer, Rob Pike, and Ken Thompson.

Unlike a lot of alternatives golang is statically-typed meaning you define a datatype and stick with it - this avoids madness like: https://github.com/denysdovhan/wtfjs


## golang dependencies

Depencency wise all we need to install is the go package, I'm on arch so i ll be using the last stable version via pacman
```
sudo pacman -S go                                                                                                0.07   22:31  
[sudo] password for loeken: 
warning: go-2:1.15.3-1 is up to date -- reinstalling
resolving dependencies...
looking for conflicting packages...

Packages (1) go-2:1.15.3-1

Total Installed Size:  558.97 MiB
Net Upgrade Size:        0.00 MiB

:: Proceed with installation? [Y/n] 
(1/1) checking keys in keyring                                                                [#######################################################] 100%
(1/1) checking package integrity                                                              [#######################################################] 100%
(1/1) loading package files                                                                   [#######################################################] 100%
(1/1) checking for file conflicts                                                             [#######################################################] 100%
(1/1) checking available disk space                                                           [#######################################################] 100%
:: Processing package changes...
(1/1) reinstalling go                                                                         [#######################################################] 100%
:: Running post-transaction hooks...
(1/1) Arming ConditionNeedsUpdate...

```

## hello world

#### **`hello-world.go`**
```
package main

import "fmt"

func main() {
	fmt.Println("Hello World")
}
```

## running your first application

go run hello-world.go

```
go run ./hello-world
Hello World
```