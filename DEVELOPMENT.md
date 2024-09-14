# Rebuild docker container
For instance, if you change dependencies in `fit_galgo_api` then you have tu run these commands to re-build the container:

```shell
$ docker compose up -d --build fit_galgo_api

$ docker compose stop fit_galgo_api
$ docker compose rm -f fit_galgo_api

$ docker compose up -d fit_galgo_api
```

# Run tests
`docker compose exec fit_galgo_api pytest`

# See logs
`docker compose logs fit_galgo_api --follow`

# Mongosh in mongodb
`docker compose exec -it fit_galgo_mongodb mongosh`

In `mongosh` you can see all databases executing `show databases`.

In `mongosh` you can use a database executing `use <database name>`.

In `mongosh` you can see all files documents, for instance, executing: `db.files.find()`.

In `mongosh` you can delete all files documents, for instance, executing: `db.files.deleteMany({})`.

## Add a new user from mongosh
Once inside mongosh:

1.- `use fitgalgodb` to create the database and active it.
2.- `db` to see what database is activated (it should be *fitgalgodb*)
3.- `db.users.insertOne({username: "<username>", full_name: "<full name>", email: "<email>", password: "<hashed password>", disabled: <true or false>, })` to create a new user.

You can use `get_password_hash` function from `app.auth.auth` to generate a hashed password. From *ipython* o *python REPL*:

```python
from app.auth.auth import get_password_hash


get_password_hash("<the plain password you want to hashed>")
```

# Mongosh in mongodb test
`docker compose exec -it fit_galgo_mongodb_test mongosh`
