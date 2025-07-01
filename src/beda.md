# BEDA EMR

Usage guidance for testing SoA with SDC using [Beda EMR](https://docs.emr.beda.software/Welcome/getting-started/)

## Create a User


```
POST /User
```

**Payload**
```json
{
    "id": "",
    "email": "",
    "password": "",
    "identifier": [],
    "userName": ""
}
```


## Create a Client (OAuth)

```
PUT /Client/api-client
Accept: text/yaml
Content-Type: text/yaml

secret: verysecret
grant_types:
  - client_credentials
```

**Payload**

```json
{
    "id": "basic",
    "secret": "secret",
    "grant_types": ["basic"]
}
```

**Enable the Access**
By linking the Client with a Policy
```
PUT /AccessPolicy/basic
Accept: text/yaml
Content-Type: text/yaml

engine: allow
link:
  - id: basic
    resourceType: Client
```

## Create a Client (basic)

```
POST /Client
Accept: text/yaml
Content-Type: text/yaml

id: basic
secret: secret
grant_types:
  - basic
```


**Enable the Access**

```
PUT /AccessPolicy/api-client
Accept: text/yaml
Content-Type: text/yaml

engine: allow
link:
  - id: api-client
    resourceType: Client
```

**Payload**
```json
{
    "id": "api-clients",
    "engine": "allow", 
    "description": "Root access to specific clients",
    "link":[{"resourceType": "Client", "id": "basic"}]
}
```


# Login

```
POST /auth/token
```

## Payload

```json
{
    "client_id": "password-client",
    "grant_type": "password",
    "username": "user@mail.com",
    "password": "password"
}
```


