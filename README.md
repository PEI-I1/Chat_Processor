# Chat_Processor

## What is it?

TODO

## Usage

### Development Setup

#### Dependencies

- pip
- python3.6
- redis
- gcc-fortran
- blas
- lapack
- hdf5

#### Worktrough

- `./install.sh`
- `source ./env/bin/activate`
- `redis-server &`
- `python3 chat_processor/app.py`

### Deployment

- Build Docker image: `docker build -t chat_processor .`
- Run Docker container: `docker run -p 5001:5001 -it chat_processor`

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

Example:
```
{
    "idChat":"111",
    "idUser":"111",
    "msg":"Quero ver um filme.",
    "name":"António Maria"
}
```

Returns a message (`string`) to send to user.

------
</details>
