# Python-ReST-API

A python ReST API using flask and dynamodb.

Based on Jake Wright's excellent video and home automation project
https://youtu.be/4T5Gnrmzjak


## Usage
All responses will have the form

```json
{
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

Subsequent response definitions will only detail the expected value of the `data field`

### List all items

**Definition**

`GET /items`

**Response**

- `200 OK` on success

```json
[
    {
        "identifier": "first",
        "name": "First Item"
    },
    {
        "identifier": "second",
        "name": "Second Item"
    }
]
```

### Adding a new item

**Definition**

`POST /items`

**Arguments**

- `"identifier":string` a globally unique identifier for this item
- `"name":string` a friendly name for this item


If an item with the given identifier already exists, the existing device will be overwritten.

**Response**

- `201 Created` on success

```json
{
    "identifier": "third",
    "name": "Third Item"
}
```

## Lookup item details

`GET /item/<identifier>`

**Response**

- `404 Not Found` if the device does not exist
- `200 OK` on success

```json
{
    "identifier": "third",
    "name": "Third Item"
}
```

## Delete an item

**Definition**

`DELETE /item/<identifier>`

**Response**

- `204 No Content`


## Docker-Compose
```
docker-compose build
docker-compose up
```

The project will be running on localhost:5000

Run integration tests with 
```
python -m pytest -v
```