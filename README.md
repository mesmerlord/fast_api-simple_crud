## Installation

1. First install pipenv

```bash
pip install pipenv
```

2. Install dependencies from Pipfile

```bash
pipenv install
```

3. Once all dependencies are installed, activate environment and enter shell

```bash
pipenv shell
```

4. Create a ".env" file with the necessary details

```text
SECRET_KEY=LONG_RANDOM_STRING_FEEL_FREE_TO_REPLACE
POSTGRES_DB_NAME=
POSTGRES_DB_USER_NAME=
POSTGRES_DB_USER_PASSWORD=
POSTGRES_DB_PORT=5432
```

5. Start the app

```bash
uvicorn main:app --reload
```

## Usage

1. Open [local api docs](http://127.0.0.1:8000/api/v1/docs)
2. Create a user using the [signup endpoint](http://127.0.0.1:8000/signup) - POST endpoint
3. Login using created user using the [login endpoint](http://127.0.0.1:8000/login) - POST endpoint
4. You can now create, update, list and delete cars for a specific user. For Authorization use Bearer type

`Authorization: Bearer xxx`

## License

[MIT](https://choosealicense.com/licenses/mit/)
