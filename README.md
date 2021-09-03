# Kim Ir Sen Project
Kim Ir Sen project provides ability to create small encrypted notes.
This project has API.

## Overview

![Kim ir sen project](https://i.imgur.com/pg5GC6v.gif)

## Getting Started
1. Install [docker](https://docs.docker.com/install/) 
    If you use Debian/Ubuntu:
    ```
    sudo apt update && sudo apt install docker
    ```
    If you use Arch(btw I use Arch):
    ```
    sudo pacman -Syy docker
    ```

2. Fill in variables
    1. Open Dockerfile
    2. After SECURITY_KEY write your security key(this key is used to encrypt id of notes in db, after change SECURITY_KEY all old keys will become unusable)
    3. After DATABASE_URL write your database url (example: postgress://user:password@host:port/name_of_db)
    4. Save and exit

3. Build kim image
    In root of download repository execute:
    ```
    docker build -t IMAGE_NAME .
    ```

4. Run kim image
    ```
    docker run -it --rm -p 80:80 IMAGE_NAME
    ```

## How Does It Work?
### Creating note
1. User enters his note
2. Server generates random user_key to encrypt note
3. Server encrypts note with user_key and save ONLY ENCRYPTED note in database
4. Server encrypts user_key and id, of encrypted note in database, and then returns the resulting code to user

### Getting note
1. User enters his resulting code
2. Server decrypts by SECURITY_KEY this code and gets id of note in database and user_key to decrypt note
3. Server decrypts note by user_key and returns note to user
4. After returning note to user server doesn't store note anymore! It deletes note from database after that.

    | WARNING: If SECURITY_KEY changes or user_key is loss there is no chance to decrypt note! |

## Running the tests
It tests only API!
1. Change URL in file api_tests.py to url of server storing your kim-ir-sen-project
2. ```python3 api_tests.py```

## Available database types
1. [Postgresql](https://www.postgresql.org/)
2. [MySQL](https://www.mysql.com/)
3. [SQLite](https://www.sqlite.org/index.html)
4. [CockroachDB](https://www.cockroachlabs.com/)

## REST API
**Create Note**

Returns json with key to get note

* **URL**

  /api/add

* **Method:**

  `POST`
  

* **Data Params**

  text=[string]
  
 
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"key": "12fdjsakjfljald...."}`
 
* **Error Response:**

  * **Code:** 400 Bad Request <br />
    Your json doesn't store field `text`

* **Sample Call:**

  ```python3
      import requests
      requests.post(self.URL + "/api/add", json={"text": "some text you want to store encrypted"})
  ```

**Get Note**

Returns json with decrypted note

* **URL**

  /api/get

* **Method:**

  `POST`
  

* **Data Params**

  key=[string]
  
 
* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"text": "text of your note"}`
 
* **Error Response:**

  * **Code:** 400 Bad Request <br />
    Your json doesn't store field `key` 
  * **Code:** 404 Bad Request <br />
    Note not found in database or Wrong Key(if it is Wrong Key, response is {"error": "Wrong key"})

* **Sample Call:**

  ```python3
      import requests
      requests.post(self.URL + "/api/get", json={"key": "the key you got after creating note"})
  ```

## Deployment
Try something like [docker-compose deployment](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/)

## Built With
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - web framework used
* [Peewee](http://docs.peewee-orm.com/en/latest/peewee/quickstart.html) - ORM for database
* [Cryptography](https://cryptography.io/en/latest/) - library to encrypt/decrypt data

## Authors
* **Vadim Tsindyaykin** - [Vadim-Burns](https://github.com/Vadim-Burns)


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
