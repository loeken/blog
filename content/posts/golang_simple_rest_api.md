---
title: "Golang simple rest api"
summary: a very simple rest api that reacts onto different methods (GET/POST) we ll be using gorilla/mux as a router
date: 2020-11-01T10:45:20+01:00
draft: false
tags: go, programming
---

# simple golang rest api with gorilla/mux router


```
package main

//import the needed packages
import (
    "fmt"
    "log"
    "net/http"
    "encoding/json"
    "github.com/gorilla/mux"
)
// define the structure of our articles
type Article struct {
    Title string `json:"Title"`
    Desc string `json:"desc"`
    Content string `json:"content"`
}
type Articles []Article

// a function to return all articles
func allArticles(w http.ResponseWriter, r *http.Request){
    Articles := []Article{
        Article{Title: "Hello", Desc: "Article Description", Content: "Article Content"},
        Article{Title: "Hello 22", Desc: "Article Description", Content: "Article Content"},
    }
    fmt.Println("Endpoint Hit: All Articles Endpoint")
    json.NewEncoder(w).Encode(Articles)
}

// a function to return the default homepage
func homePage(w http.ResponseWriter, r *http.Request ) {
    fmt.Fprintf(w, "Homepage Endpoint Hit")
}

//testing function for a post to /articles
func testPostArticle(w http.ResponseWriter, r *http.Request ) {
    fmt.Fprintf(w, "test post endpoint worked")
}
//the handling of the application request with mux router
func handleRequest() {
    myRouter :=mux.NewRouter().StrictSlash(true)
    myRouter.HandleFunc("/", homePage);
    myRouter.HandleFunc("/articles", allArticles).Methods("GET")
    myRouter.HandleFunc("/articles", testPostArticle).Methods("POST")
    log.Fatal(http.ListenAndServe(":8081", myRouter))
}
// the default entry point into our go app
func main() {
    handleRequest()
}
```