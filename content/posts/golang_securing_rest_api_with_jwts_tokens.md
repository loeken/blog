---
title: "Golang securing rest api with jwts tokens"
summary: in this tutorial we ll create a server/client the client generates a token and queries the server with that token and the server checks if that token is valid via a middleware function
date: 2020-11-01T10:49:21+01:00
draft: false
---

# go - securing rest api with jwts tokens

JWTs are heaviliy used in single page application as a means to securing an application. there are two main purposes for jwts

- authorization
- information exchange


### How do they work?
These jwts are signed via passwords or keypairs. jwts are tamper proof because they are signed based on the header and payload

In this turoial we are going to create a client and a server. the client will call an endpoint on the server which is protected by jwts middleware.
this middlewear is going to take the token from the header of our request and check if this token is valid based on the request.

creating a simple client
```
mkdir client
cd client
go mod init github.com/loeken/go-jwts-tutorial/client                                                                            0.00   10:53  
go: creating new go.mod: module github.com/loeken/go-jwts-tutorial/client
```


### The Client
#### **`main.go`**
```
package main

import("fmt")

func main() {
    fmt.Println("my simple client")
}
```

##### test if it works
```
go run main.go
my simple client
```

adding jwt to the mix
#### **`main.go`**
```
package main

import(
    "fmt"
    "time"
    jwt "github.com/dgrijalva/jwt-go"
)
//we can alternatively read the signing key from an environment variable which is better as we dont commit any passwords to our repos
//var mySigningKey = os.Get("MY_JWT_TOKEN)
var mySigningKey = []byte("topsecurephrasecomeshere")
func GenerateJWT() (string, error) {
    token := jwt.New(jwt.SigningMethodHS256)

    claims := token.Claims.(jwt.MapClaims)
    claims["authorized"] = true
    claims["user"] = "loeken"
    claims["exp"] = time.Now().Add(time.Minute * 30).Unix()

    tokenString, err := token.SignedString(mySigningKey)

    if err != nil {
        fmt.Errorf("Something went wrong: %s", err.Error())
        return "", err
    }
    return tokenString, nil
}
func main() {
    fmt.Println("my simple client")
    tokenString, err := GenerateJWT()
    if err != nil {
        fmt.Println("error generating token string")
    }
    fmt.Println(tokenString)
}
```


next step is turn it into a server that binds to port 9001
#### **`main.go`**
```
package main

import(
    "fmt"
    "time"
    "log"
    "net/http"
    jwt "github.com/dgrijalva/jwt-go"
)
//we can alternatively read the signing key from an environment variable which is better as we dont commit any passwords to our repos
//var mySigningKey = os.Get("MY_JWT_TOKEN)
var mySigningKey = []byte("topsecurephrasecomeshere")
func GenerateJWT() (string, error) {
    token := jwt.New(jwt.SigningMethodHS256)

    claims := token.Claims.(jwt.MapClaims)
    claims["authorized"] = true
    claims["user"] = "loeken"
    claims["exp"] = time.Now().Add(time.Minute * 30).Unix()

    tokenString, err := token.SignedString(mySigningKey)

    if err != nil {
        fmt.Errorf("Something went wrong: %s", err.Error())
        return "", err
    }
    return tokenString, nil
}

func homePage(w http.ResponseWriter, r *http.Request) {
    validToken, err := GenerateJWT()
    if err != nil {
        fmt.Fprintf(w, err.Error())
    }
    fmt.Fprintf(w, validToken)
}
func handleRequests() {
    http.HandleFunc("/", homePage)
    log.Fatal(http.ListenAndServe(":9001", nil))
}
func main() {
    fmt.Println("my simple client")
    handleRequests()
}
```

now let's verify the application is running:

```
curl localhost:9001
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRob3JpemVkIjp0cnVlLCJleHAiOjE2MDQyMjc2NTAsInVzZXIiOiJsb2VrZW4ifQ.LEp9Qw0RGM7Z2YU1pxVK59hmeW4ZCuSmS6_hUJTvEFs%  
```

we get the token so everything seems to be working fine



### The Server

So we're starting out with a very simple Server that only returns the our Super Secret Information ( which we ll restrict access to later on )
but for now we just want a very simple response. this time we ll bind to port 9000

```
cd ..
mkdir server
cd server
go mod init github.com/loeken/go-jwts-tutorial/server
```

#### **`main.go`**
```
package main


import (
    "fmt"
    "log"
    "net/http"
)

func homePage(w http.ResponseWriter, r *http.Request ) {
    fmt.Fprintf(w, "Super Secret Information")
}

func handleRequests() {
    http.HandleFunc("/", homePage)
    log.Fatal(http.ListenAndServe(":9000", nil))
}

func main() {
    fmt.Println("My Simple Server")
    handleRequests()
}
```


##### test it 
```
go run ./main.go
My Simple Server
```

```
curl localhost:9000 
Super Secret Information
```


### bringing it all together:
#### **`main.go`**
```
package main


import (
    "fmt"
    "log"
    "net/http"
    jwt "github.com/dgrijalva/jwt-go"
)

func homePage(w http.ResponseWriter, r *http.Request ) {
    fmt.Fprintf(w, "Super Secret Information")
}

//middleware function
var mySigningKey = []byte("topsecurephrasecomeshere")

func isAuthorized(endpoint func(http.ResponseWriter, *http.Request)) http.Handler  { 
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // check if token is set
        if r.Header["Token"] != nil {
            // if it is it starts to parse the token
            token, err := jwt.Parse(r.Header["Token"][0], func(token *jwt.Token) (interface{}, error) {
                if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
                    return nil, fmt.Errorf("There was an error")
                }
                return mySigningKey, nil
            })
            // check for errors
            if err != nil {
                fmt.Fprintf(w, err.Error())
            }
            //check if token is valid

            if token.Valid {
                endpoint(w, r)
            }


        } else {
            fmt.Fprintf(w, "Not Authorized")
        }
    })
}
func handleRequests() {
   - http.Handle("/", isAuthorized(homePage))
   +  http.Handle("/", isAuthorized(homePage))
   +  log.Fatal(http.ListenAndServe(":9000", nil))
}
func main() {
    fmt.Println("My Simple Server")
    handleRequests()
}
```


##### test it 
```
//generate a token by quering the client
curl localhost:9001
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRob3JpemVkIjp0cnVlLCJleHAiOjE2MDQyMjkxNzUsInVzZXIiOiJsb2VrZW4ifQ.3XKb5UPsmEBdDHNtKqG8WBjldm6dQ3a2GpeUskg__IU

//use this token to query the server
curl -H "Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRob3JpemVkIjp0cnVlLCJleHAiOjE2MDQyMjkxNzUsInVzZXIiOiJsb2VrZW4ifQ.3XKb5UPsmEBdDHNtKqG8WBjldm6dQ3a2GpeUskg__IU" localhost:9000
Super Secret Information
```
