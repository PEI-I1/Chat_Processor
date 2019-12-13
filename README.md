# Chat_Processor

## What is it?

TODO

## Usage

### Development Setup

#### Dependencies

- pip
- python3.6
- redis
- gfortran
- libblas-dev
- liblapack-dev
- libhdf5-dev

#### Worktrough

- `./install.sh`
- `source ./env/bin/activate`
- `redis-server &`
- `python3.6 chat_processor/app.py`

### Deployment

- Build Docker image: `docker build -t chat_processor .`
- Create Docker volume for data persistence across containers: `docker volume create chat_processor`
- Run Docker container: `docker run -p 5001:5001 -it chat_proc -v chat_processor:/root/`

**NOTE:** You need to run redis-server apart (`redis-server &`).

## API

<details>
<summary>Get response for a user message</summary>

```http
POST /getResponse
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `idChat` | `string` | **Required**. Chat id. |
| `idUser` | `string` | **Required**. User id. |
| `msg` | `string` | **Required**. User message. |
| `name` | `string` | **Required**. User name. |
| `location` | `None` or `{"lat": float, "lon": float}` | **Required**. User location. |

Example:
```
{
    "idChat":"111",
    "idUser":"111",
    "msg":"Quero ver um filme.",
    "name":"António Maria",
    "location": None
}
```

Example sending location:
```
{
    "idChat":"111",
    "idUser":"111",
    "msg":"Quero ver um filme.",
    "name":"António Maria",
    "location": {
        "lat": 32.543042,
        "lon": -10.424717
    }
}
```

Returns a message (`string`) to send to user.

------
</details>
