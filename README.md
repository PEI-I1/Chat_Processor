# Chat_Processor

## Table of Contents
* [What is it?](#what-is-it)
* [Usage](#usage)
  - [Development setup](#development-setup)
    - [Dependencies](#dependencies)
    - [Worktrough](#worktrough)
  - [Deployment](#deployment)
* [API](#api)

## What is it?

Chat Processor is a natural language interpreter that tries to tag messages in order to determine the best answer is for it.
It works as the main controller of the NOS Bot, making requests to other components based on the user's queries/questions.
It supports two execution modes, a default one and a rules based mode. In the default mode the users messages are understood using a dictionary where each element is a category, which represents a feature made available by the bot, as well as a group of words against which each message is compared to in order to tag it in one of the categories.
Each message is spell checked (symspellpy with frequency words generated from a OpenSubtitles corpus) to fix misspellings/typos.
Entity recognition is achieved by using a modified multilingual version of BERT model developed by deeppavlov although, because some entities are not detected by the model, regex is also used.
The response to each user is "prettified" using the text formatting capabilities of Telegram.

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

- `python3.6 -m venv env`
- `source ./env/bin/activate`
- `pip install -r requirements.txt`
- `python3.6 -m deeppavlov install ner_ontonotes_bert_mult`
- `redis-server &`
- `python3.6 chat_processor/app.py`

### Deployment

- Build Docker image: `docker build -t chat_processor .`
- Create Docker volume for data persistence across containers: `docker volume create chat_processor`
- Run Docker container: `docker run -p 5001:5001 -v chat_processor:/root/ -it chat_processor`

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
